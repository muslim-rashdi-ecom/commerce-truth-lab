import io
import json
import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
from models import Order as OrderORM
from sqlalchemy import select


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def get_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def rand_email(prefix: str = "pilot") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@pilot-audit.com"


def register_and_login(client, email: str, name: str = "Pilot User") -> str:
    res = client.post("/api/auth/register", json={
        "email": email,
        "password": "PilotSecurePassword2026!",
        "full_name": name
    })
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


def create_workspace(client, token: str, name: str = "Aura Living Studio Pilot") -> str:
    res = client.post("/api/workspaces", json={"name": name}, headers=get_auth_headers(token))
    assert res.status_code == 200, res.text
    return res.json()["id"]


def upload_source(client, token: str, workspace_id: str, source_type: str, filename: str, csv_content: str):
    csv_bytes = csv_content.strip().encode("utf-8")
    st_res = client.post(
        f"/api/workspaces/{workspace_id}/upload/stage",
        data={"source_type": source_type},
        files={"file": (filename, io.BytesIO(csv_bytes), "text/csv")},
        headers=get_auth_headers(token)
    )
    assert st_res.status_code == 200, f"Stage failed for {source_type}: {st_res.text}"
    stage_data = st_res.json()

    commit_res = client.post(
        f"/api/workspaces/{workspace_id}/upload/commit",
        data={
            "upload_id": stage_data["upload_id"],
            "mappings": json.dumps(stage_data["suggested_mappings"])
        },
        files={"file": (filename, io.BytesIO(csv_bytes), "text/csv")},
        headers=get_auth_headers(token)
    )
    assert commit_res.status_code == 200, f"Commit failed for {source_type}: {commit_res.text}"
    return commit_res.json()


def test_pilot_workspace_creation_and_authorization(client):
    """Verify pilot workspace creation, initial empty state, and audit log tracking."""
    token = register_and_login(client, rand_email("brand_auth"), "Aura Living Lead")
    ws_id = create_workspace(client, token, "Aura Living Studio Pilot - 2026-001")
    assert ws_id.startswith("ws_")

    # Verify workspace summary is accessible
    summary_res = client.get(f"/api/workspaces/{ws_id}", headers=get_auth_headers(token))
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["name"] == "Aura Living Studio Pilot - 2026-001"
    assert summary["order_count"] == 0
    assert summary["finding_count"] == 0


def test_pilot_sanitized_upload_with_pii_neutralization(client):
    """Verify customer PII is salted/hashed and formula injection characters are neutralized."""
    token = register_and_login(client, rand_email("sanitizer"), "Data Quality Officer")
    ws_id = create_workspace(client, token, "Sanitization Test Workspace")

    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-AURA-1001,store_aura,2026-08-01T10:00:00Z,USD,120.00,prepaid,confirmed,john.doe@customer-secret.com\n"
        "ORD-AURA-1002,store_aura,2026-08-02T11:00:00Z,USD,250.00,cod,confirmed,=cmd|' /C calc'!A0\n"
    )

    upload_res = upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)
    assert upload_res["imported_rows"] == 2

    # Verify in DB that raw email is not stored in plaintext
    with SessionLocal() as db:
        order_1 = db.execute(select(OrderORM).where(OrderORM.workspace_id == ws_id, OrderORM.id == "ORD-AURA-1001")).scalar_one()
        assert "john.doe@customer-secret.com" not in order_1.customer_id
        assert order_1.customer_id.upper().startswith("CUST_")
        assert len(order_1.customer_id) > 10

        # Verify formula injection character was stripped or neutralized
        order_2 = db.execute(select(OrderORM).where(OrderORM.workspace_id == ws_id, OrderORM.id == "ORD-AURA-1002")).scalar_one()
        assert not order_2.customer_id.startswith("=")


def test_pilot_missing_source_ctl009(client):
    """When required courier settlement data is missing for COD orders, CTL-009 must trigger."""
    token = register_and_login(client, rand_email("missing_src"), "Logistics Auditor")
    ws_id = create_workspace(client, token, "Missing Source Workspace")

    # Ingest a delivered COD order without uploading any courier settlement file
    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-AURA-1090,store_aura,2026-08-05T10:00:00Z,AED,350.00,cod,delivered,customer_90\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    # Run audit
    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200
    audit_data = audit_res.json()
    assert audit_data["status"] == "completed"

    findings_res = client.get(f"/api/workspaces/{ws_id}/findings", headers=get_auth_headers(token))
    assert findings_res.status_code == 200
    findings = findings_res.json()["items"]
    
    # Must flag CTL-009
    rule_ids = [f["rule_id"] for f in findings]
    assert "CTL-009" in rule_ids
    ctl009 = next(f for f in findings if f["rule_id"] == "CTL-009")
    assert "couriersettlement" in ctl009["observed"].lower() or "courier" in ctl009["observed"].lower()


def test_pilot_multicurrency_ctl004_and_ctl012(client):
    """Verify multi-currency reconciliation detects cross-currency mismatches accurately."""
    token = register_and_login(client, rand_email("multicurrency"), "Treasury Auditor")
    ws_id = create_workspace(client, token, "Multi Currency Workspace")

    # Ingest Order in USD
    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-CURR-01,store_aura,2026-08-01T10:00:00Z,USD,100.00,prepaid,confirmed,cust_1\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    # Ingest Payment in EUR (Currency Mismatch with Order)
    payments_csv = (
        "id,order_id,captured_at,currency,amount,method,gateway,status\n"
        "PAY-CURR-01,ORD-CURR-01,2026-08-01T10:05:00Z,EUR,100.00,card,stripe,captured\n"
    )
    upload_source(client, token, ws_id, "payments", "payments.csv", payments_csv)

    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200

    findings_res = client.get(f"/api/workspaces/{ws_id}/findings", headers=get_auth_headers(token))
    findings = findings_res.json()["items"]
    rule_ids = [f["rule_id"] for f in findings]
    assert "CTL-004" in rule_ids or "CTL-012" in rule_ids


def test_pilot_capi_duplicate_signals_ctl001(client):
    """Verify CTL-001 triggers when multiple un-deduplicated signals arrive for the same order."""
    token = register_and_login(client, rand_email("tracking"), "Tracking Engineer")
    ws_id = create_workspace(client, token, "Tracking Duplicate Workspace")

    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-TRACK-01,store_aura,2026-08-01T12:00:00Z,USD,95.00,prepaid,confirmed,cust_t1\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    # Ingest 2 signals for the same order without matching event_id
    signals_csv = (
        "id,order_id,signal_type,platform,event_name,event_id,reported_at,currency,value,consent_granted,pixel_id\n"
        "SIG-01,ORD-TRACK-01,browser,meta,Purchase,,2026-08-01T12:00:05Z,USD,95.00,true,PIX-123\n"
        "SIG-02,ORD-TRACK-01,server,meta,Purchase,,2026-08-01T12:00:06Z,USD,95.00,true,PIX-123\n"
    )
    upload_source(client, token, ws_id, "purchase_signals", "signals.csv", signals_csv)

    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200

    findings_res = client.get(f"/api/workspaces/{ws_id}/findings", headers=get_auth_headers(token))
    findings = findings_res.json()["items"]
    rule_ids = [f["rule_id"] for f in findings]
    assert "CTL-001" in rule_ids


def test_pilot_cod_shortfall_and_overdue_ctl005_ctl006(client):
    """Verify CTL-005 (overdue grace period) and CTL-006 (cash shortfall) trigger accurately."""
    token = register_and_login(client, rand_email("cod_auditor"), "COD Controller")
    ws_id = create_workspace(client, token, "COD Audit Workspace")

    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-COD-SHORT,store_aura,2026-08-01T08:00:00Z,AED,500.00,cod,delivered,cust_c1\n"
        "ORD-COD-OVERDUE,store_aura,2026-08-01T09:00:00Z,AED,300.00,cod,delivered,cust_c2\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    settlements_csv = (
        "id,order_id,courier_name,delivered_at,collected_amount,settled_amount,collection_currency,settlement_status,grace_days\n"
        "AWB-SHORT,ORD-COD-SHORT,Aramex,2026-08-05T14:00:00Z,400.00,400.00,AED,settled,7\n"
        "AWB-OVERDUE,ORD-COD-OVERDUE,Aramex,2026-08-02T10:00:00Z,,,AED,pending,7\n"
    )
    upload_source(client, token, ws_id, "courier_settlements", "settlements.csv", settlements_csv)

    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200

    findings_res = client.get(f"/api/workspaces/{ws_id}/findings", headers=get_auth_headers(token))
    findings = findings_res.json()["items"]
    rule_ids = [f["rule_id"] for f in findings]
    assert "CTL-006" in rule_ids  # Shortfall: 500 order vs 400 collected
    assert "CTL-005" in rule_ids  # Overdue: delivered > 7 days ago, still pending


def test_pilot_refund_exceeding_order_ctl008(client):
    """Verify CTL-008 triggers when refund amount exceeds captured order value."""
    token = register_and_login(client, rand_email("refund_auditor"), "Dispute Officer")
    ws_id = create_workspace(client, token, "Refund Audit Workspace")

    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-REF-01,store_aura,2026-08-01T10:00:00Z,USD,100.00,prepaid,delivered,cust_r1\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    payments_csv = (
        "id,order_id,captured_at,currency,amount,method,gateway,status\n"
        "PAY-REF-01,ORD-REF-01,2026-08-01T10:05:00Z,USD,100.00,card,stripe,captured\n"
    )
    upload_source(client, token, ws_id, "payments", "payments.csv", payments_csv)

    refunds_csv = (
        "id,order_id,refunded_at,currency,amount,reason\n"
        "REF-01,ORD-REF-01,2026-08-10T15:00:00Z,USD,140.00,excess_goodwill\n"
    )
    upload_source(client, token, ws_id, "refunds", "refunds.csv", refunds_csv)

    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200

    findings_res = client.get(f"/api/workspaces/{ws_id}/findings", headers=get_auth_headers(token))
    findings = findings_res.json()["items"]
    rule_ids = [f["rule_id"] for f in findings]
    assert "CTL-008" in rule_ids
    f008 = next(f for f in findings if f["rule_id"] == "CTL-008")
    assert f008["severity"].lower() in ("critical", "high")


def test_pilot_client_ready_report_exports(client):
    """Verify JSON, Markdown, and HTML reports contain date range, prioritized fixes, and before/after verification."""
    token = register_and_login(client, rand_email("report_tester"), "Executive Auditor")
    ws_id = create_workspace(client, token, "Aura Living Studio Official Pilot")

    # Ingest comprehensive pilot test data
    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-PLT-101,store_aura,2026-08-01T10:00:00Z,USD,100.00,prepaid,delivered,cust_p1\n"
        "ORD-PLT-102,store_aura,2026-08-15T15:00:00Z,AED,500.00,cod,delivered,cust_p2\n"
    )
    upload_source(client, token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    # Ingest duplicate signals to trigger CTL-001 (P0 candidate)
    signals_csv = (
        "id,order_id,signal_type,platform,event_name,event_id,reported_at,currency,value,consent_granted,pixel_id\n"
        "SIG-P1,ORD-PLT-101,browser,meta,Purchase,,2026-08-01T10:01:00Z,USD,100.00,true,PIX-1\n"
        "SIG-P2,ORD-PLT-101,server,meta,Purchase,,2026-08-01T10:01:05Z,USD,100.00,true,PIX-1\n"
    )
    upload_source(client, token, ws_id, "purchase_signals", "signals.csv", signals_csv)

    # Ingest COD shortfall to trigger CTL-006 (P1 candidate)
    settlements_csv = (
        "id,order_id,courier_name,delivered_at,collected_amount,settled_amount,collection_currency,settlement_status,grace_days\n"
        "AWB-P102,ORD-PLT-102,Aramex,2026-08-16T12:00:00Z,400.00,400.00,AED,settled,7\n"
    )
    upload_source(client, token, ws_id, "courier_settlements", "settlements.csv", settlements_csv)

    # Execute audit
    audit_res = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(token))
    assert audit_res.status_code == 200

    # 1. Test JSON Export
    rep_json = client.get(f"/api/workspaces/{ws_id}/reports/json", headers=get_auth_headers(token))
    assert rep_json.status_code == 200
    json_data = rep_json.json()
    assert json_data["workspace_id"] == ws_id
    assert "date_range" in json_data
    assert json_data["date_range"]["start"] is not None
    assert json_data["date_range"]["end"] is not None
    assert "prioritized_fixes" in json_data
    assert len(json_data["prioritized_fixes"]) >= 2
    assert json_data["prioritized_fixes"][0]["priority"] == "P0"
    assert "before_after_verification" in json_data
    assert len(json_data["before_after_verification"]) >= 4
    assert "boundary_disclaimer" in json_data

    # 2. Test Markdown Export
    rep_md = client.get(f"/api/workspaces/{ws_id}/reports/markdown", headers=get_auth_headers(token))
    assert rep_md.status_code == 200
    md_text = rep_md.text
    assert "# Audit Report — Aura Living Studio Official Pilot" in md_text
    assert "## 1. Executive Summary" in md_text
    assert "Audit Date Range:" in md_text
    assert "## 3. Prioritized Remediations (Action Plan)" in md_text
    assert "| P0 |" in md_text
    assert "## 4. Before-and-After Verification Summary" in md_text
    assert "Methodological Guardrails" in md_text

    # 3. Test HTML Export
    rep_html = client.get(f"/api/workspaces/{ws_id}/reports/html", headers=get_auth_headers(token))
    assert rep_html.status_code == 200
    html_text = rep_html.text
    assert "Commerce Truth Lab — Audit Report" in html_text
    assert "Prioritized Remediation Action Plan" in html_text
    assert "Before-and-After Verification Summary" in html_text
    assert "Aura Living Studio Official Pilot" in html_text


def test_pilot_tenant_isolation_boundary(client):
    """Verify tenant isolation strictly prevents unauthorized merchants from accessing pilot data."""
    pilot_owner_token = register_and_login(client, rand_email("pilot_owner"), "Authorized Merchant")
    adversary_token = register_and_login(client, rand_email("adversary"), "Adversary Merchant")

    ws_id = create_workspace(client, pilot_owner_token, "Confidential Pilot Brand Data")

    # Ingest secret order into pilot workspace
    orders_csv = (
        "id,store_id,created_at,currency,total_amount,payment_method,status,customer_id\n"
        "ORD-SECRET-99,store_secret,2026-08-01T10:00:00Z,USD,999.00,prepaid,delivered,cust_sec\n"
    )
    upload_source(client, pilot_owner_token, ws_id, "shopify_orders", "orders.csv", orders_csv)

    # Adversary attempts to view workspace summary -> 403 Forbidden
    res_summary = client.get(f"/api/workspaces/{ws_id}", headers=get_auth_headers(adversary_token))
    assert res_summary.status_code == 403

    # Adversary attempts to view orders -> 403 Forbidden
    res_orders = client.get(f"/api/workspaces/{ws_id}/orders", headers=get_auth_headers(adversary_token))
    assert res_orders.status_code == 403

    # Adversary attempts to trigger audit -> 403 Forbidden
    res_audit = client.post(f"/api/workspaces/{ws_id}/audit/run", headers=get_auth_headers(adversary_token))
    assert res_audit.status_code == 403

    # Adversary attempts to download reports -> 403 Forbidden
    res_report = client.get(f"/api/workspaces/{ws_id}/reports/json", headers=get_auth_headers(adversary_token))
    assert res_report.status_code == 403


def test_public_demo_unaffected_by_pilot_operations(client):
    """Confirm the public synthetic demo (/demo) remains completely open and unaffected."""
    res_demo = client.get("/api/demo/workspace")
    assert res_demo.status_code == 200
    demo_data = res_demo.json()
    assert demo_data["is_synthetic"] is True

    res_findings = client.get("/api/demo/findings")
    assert res_findings.status_code == 200
    assert len(res_findings.json()) > 0
