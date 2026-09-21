import io
import json
import uuid
import asyncio
import pytest
from fastapi.testclient import TestClient
from main import app
from database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    async def _init():
        await init_db()
    asyncio.run(_init())


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def get_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

def rand_email(prefix: str = "user") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@teststore.com"

def test_public_demo_remains_unauthenticated(client):
    """Verify that public synthetic demo routes require no login and remain fully accessible."""
    res_summary = client.get("/api/demo/workspace")

    assert res_summary.status_code == 200
    data = res_summary.json()
    assert data["is_synthetic"] is True
    assert "tracking_confidence_pct" in data

    res_orders = client.get("/api/demo/orders")
    assert res_orders.status_code == 200
    orders = res_orders.json()
    assert len(orders) > 0


def test_auth_registration_and_login(client):
    """Verify registration, login, and rejection of invalid credentials."""
    email_a = rand_email("merchant_a")
    pwd_a = "SecurePass123!"


    # 1. Register Merchant A
    reg_res = client.post("/api/auth/register", json={
        "email": email_a,
        "password": pwd_a,
        "full_name": "Merchant Alpha"
    })
    assert reg_res.status_code == 200, reg_res.text
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == email_a

    # 2. Duplicate registration should be rejected
    dup_res = client.post("/api/auth/register", json={
        "email": email_a,
        "password": pwd_a,
        "full_name": "Duplicate Alpha"
    })
    assert dup_res.status_code == 400

    # 3. Login with correct password
    login_res = client.post("/api/auth/login", json={
        "email": email_a,
        "password": pwd_a
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data

    # 4. Login with wrong password
    bad_pwd_res = client.post("/api/auth/login", json={
        "email": email_a,
        "password": "WrongPassword!"
    })
    assert bad_pwd_res.status_code == 401

    # 5. Login with non-existent email
    bad_user_res = client.post("/api/auth/login", json={
        "email": rand_email("nobody"),
        "password": "WrongPassword!"
    })
    assert bad_user_res.status_code == 401

    # 6. Check /api/auth/me
    token = login_data["access_token"]
    me_res = client.get("/api/auth/me", headers=get_auth_headers(token))
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email_a


def test_tenant_workspace_isolation(client):
    """Verify strict tenant isolation: Merchant B cannot access Merchant A's workspace or data."""
    # Register Merchant 1

    m1_res = client.post("/api/auth/register", json={
        "email": rand_email("tenant1"),
        "password": "Password123!",
        "full_name": "Tenant One"
    })
    assert m1_res.status_code == 200
    m1_token = m1_res.json()["access_token"]

    # Register Merchant 2
    m2_res = client.post("/api/auth/register", json={
        "email": rand_email("tenant2"),
        "password": "Password123!",
        "full_name": "Tenant Two"
    })
    assert m2_res.status_code == 200
    m2_token = m2_res.json()["access_token"]

    # Merchant 1 creates Workspace Alpha
    ws1_res = client.post("/api/workspaces", json={
        "name": "Alpha Isolated Store",
        "currency": "USD"
    }, headers=get_auth_headers(m1_token))
    assert ws1_res.status_code == 200
    ws1_id = ws1_res.json()["id"]

    # Merchant 2 creates Workspace Beta
    ws2_res = client.post("/api/workspaces", json={
        "name": "Beta Isolated Store",
        "currency": "AED"
    }, headers=get_auth_headers(m2_token))
    assert ws2_res.status_code == 200
    ws2_id = ws2_res.json()["id"]

    # Merchant 1 can view Workspace Alpha
    get_ws1 = client.get(f"/api/workspaces/{ws1_id}", headers=get_auth_headers(m1_token))
    assert get_ws1.status_code == 200
    assert get_ws1.json()["name"] == "Alpha Isolated Store"

    # CRITICAL ISOLATION CHECK: Merchant 2 attempts to view Workspace Alpha -> 403 Forbidden
    cross_access_res = client.get(f"/api/workspaces/{ws1_id}", headers=get_auth_headers(m2_token))
    assert cross_access_res.status_code == 403

    # CRITICAL ISOLATION CHECK: Merchant 1 attempts to view Workspace Beta -> 403 Forbidden
    cross_access_res2 = client.get(f"/api/workspaces/{ws2_id}", headers=get_auth_headers(m1_token))
    assert cross_access_res2.status_code == 403

    # CRITICAL ISOLATION CHECK: Merchant 2 attempts to list orders from Workspace Alpha -> 403 Forbidden
    cross_orders = client.get(f"/api/workspaces/{ws1_id}/orders", headers=get_auth_headers(m2_token))
    assert cross_orders.status_code == 403


def test_secure_upload_staging_mapping_and_pii_pseudonymization(client):
    """Verify CSV upload, column mapping preview, PII pseudonymization, and commit."""
    # Register Merchant

    m_res = client.post("/api/auth/register", json={
        "email": rand_email("privacy_merchant"),
        "password": "Password123!",
        "full_name": "Privacy Conscious Merchant"
    })
    token = m_res.json()["access_token"]

    ws_res = client.post("/api/workspaces", json={
        "name": "Privacy Pilot Store",
        "currency": "USD"
    }, headers=get_auth_headers(token))
    ws_id = ws_res.json()["id"]

    # CSV with customer plaintext PII (email, name, phone)
    raw_csv = (
        "order_id,created_at,total_amount,currency,payment_method,financial_status,customer_email,customer_name,phone\n"
        "ORD-PRIV-001,2026-03-01T10:00:00Z,129.50,USD,card,paid,real.alice@secretmail.com,Alice Wonderland,+1-555-0199\n"
        "ORD-PRIV-002,2026-03-02T11:00:00Z,250.00,USD,cod,pending,bob.builder@secretmail.com,Bob Builder,+1-555-0288\n"
    ).encode("utf-8")

    # Stage CSV
    stage_res = client.post(
        f"/api/workspaces/{ws_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("orders.csv", io.BytesIO(raw_csv), "text/csv")},
        headers=get_auth_headers(token)
    )
    assert stage_res.status_code == 200, stage_res.text
    stage_data = stage_res.json()
    upload_id = stage_data["upload_id"]
    assert stage_data["row_count"] == 2
    assert "suggested_mappings" in stage_data
    assert len(stage_data["pseudonymized_fields"]) > 0

    # Ensure preview does NOT show raw email
    for row in stage_data["preview_rows"]:
        for val in row.values():
            assert "real.alice@secretmail.com" not in str(val)
            assert "bob.builder@secretmail.com" not in str(val)

    # Commit CSV
    mappings = stage_data["suggested_mappings"]
    commit_res = client.post(
        f"/api/workspaces/{ws_id}/upload/commit",
        data={
            "upload_id": upload_id,
            "mappings": json.dumps(mappings)
        },
        files={"file": ("orders.csv", io.BytesIO(raw_csv), "text/csv")},
        headers=get_auth_headers(token)
    )
    assert commit_res.status_code == 200, commit_res.text
    assert commit_res.json()["imported_rows"] == 2

    # Query orders and verify strict pseudonymization in the database
    orders_res = client.get(f"/api/workspaces/{ws_id}/orders", headers=get_auth_headers(token))
    assert orders_res.status_code == 200
    orders = orders_res.json()
    assert len(orders) == 2

    for o in orders:
        # Customer ID must be a pseudonymized hash token, never plaintext
        assert o["customer_id"].startswith("CUST_")
        assert "real.alice@secretmail.com" not in o["customer_id"]
        assert "bob.builder@secretmail.com" not in o["customer_id"]
        assert "Alice" not in o["customer_id"]
        # Total minor amount parsed correctly
        if o["id"] == "ORD-PRIV-001":
            assert o["total_amount_minor"] == 12950
        elif o["id"] == "ORD-PRIV-002":
            assert o["total_amount_minor"] == 25000


def test_full_acceptance_pilot_workflow(client):
    """End-to-end acceptance test:

    1. Test merchant registers and creates a private workspace.
    2. Uploads orders, payments, signals CSV.
    3. Runs the deterministic audit engine.
    4. Inspects findings with evidence and anti-hype boundaries.
    5. Exports reports (HTML, JSON, Markdown).
    6. Verifies second merchant cannot access the first merchant's workspace, data, or reports.
    """
    # Merchant Alpha
    m_alpha = client.post("/api/auth/register", json={
        "email": rand_email("pilot_alpha"),
        "password": "Password123!",
        "full_name": "Pilot Lead Alpha"
    }).json()
    token_a = m_alpha["access_token"]

    ws_a = client.post("/api/workspaces", json={
        "name": "Alpha Brand Direct",
        "currency": "USD"
    }, headers=get_auth_headers(token_a)).json()
    ws_a_id = ws_a["id"]

    # Merchant Beta (Competitor / isolated)
    m_beta = client.post("/api/auth/register", json={
        "email": rand_email("pilot_beta"),
        "password": "Password123!",
        "full_name": "Pilot Lead Beta"
    }).json()
    token_b = m_beta["access_token"]

    ws_b = client.post("/api/workspaces", json={
        "name": "Beta Brand Direct",
        "currency": "USD"
    }, headers=get_auth_headers(token_b)).json()
    ws_b_id = ws_b["id"]

    # Ingest Orders into Workspace Alpha
    orders_csv = (
        "order_id,created_at,total_amount,currency,payment_method,financial_status,customer_email\n"
        "ORD-PILOT-001,2026-03-01T10:00:00Z,100.00,USD,card,paid,cust1@mail.com\n"
        "ORD-PILOT-002,2026-03-02T10:00:00Z,200.00,USD,cod,delivered,cust2@mail.com\n"
    ).encode("utf-8")

    st_orders = client.post(
        f"/api/workspaces/{ws_a_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("orders.csv", io.BytesIO(orders_csv), "text/csv")},
        headers=get_auth_headers(token_a)
    ).json()

    client.post(
        f"/api/workspaces/{ws_a_id}/upload/commit",
        data={"upload_id": st_orders["upload_id"], "mappings": json.dumps(st_orders["suggested_mappings"])},
        files={"file": ("orders.csv", io.BytesIO(orders_csv), "text/csv")},
        headers=get_auth_headers(token_a)
    )

    # Ingest Payments into Workspace Alpha
    payments_csv = (
        "id,order_id,captured_at,currency,amount,method,gateway,status\n"
        "PAY-001,ORD-PILOT-001,2026-03-01T10:05:00Z,USD,100.00,card,stripe,captured\n"
    ).encode("utf-8")

    st_payments = client.post(
        f"/api/workspaces/{ws_a_id}/upload/stage",
        data={"source_type": "payments"},
        files={"file": ("payments.csv", io.BytesIO(payments_csv), "text/csv")},
        headers=get_auth_headers(token_a)
    ).json()

    client.post(
        f"/api/workspaces/{ws_a_id}/upload/commit",
        data={"upload_id": st_payments["upload_id"], "mappings": json.dumps(st_payments["suggested_mappings"])},
        files={"file": ("payments.csv", io.BytesIO(payments_csv), "text/csv")},
        headers=get_auth_headers(token_a)
    )

    # Run Backend Audit on Workspace Alpha
    audit_res = client.post(
        f"/api/workspaces/{ws_a_id}/audit/run",
        headers=get_auth_headers(token_a)
    )
    assert audit_res.status_code == 200, audit_res.text
    audit_data = audit_res.json()
    assert audit_data["status"] == "completed"
    assert audit_data["evaluated_orders"] == 2
    assert audit_data["total_findings"] > 0

    # Query Findings for Workspace Alpha
    findings_res = client.get(f"/api/workspaces/{ws_a_id}/findings", headers=get_auth_headers(token_a))
    assert findings_res.status_code == 200
    findings_data = findings_res.json()
    findings = findings_data["items"]
    assert len(findings) > 0

    # Check finding content and anti-hype boundaries
    first_finding = findings[0]
    assert "rule_id" in first_finding
    assert "observed" in first_finding
    assert "not_proven" in first_finding
    assert "recommended_action" in first_finding

    # Reports Export
    rep_html = client.get(f"/api/workspaces/{ws_a_id}/reports/html", headers=get_auth_headers(token_a))
    assert rep_html.status_code == 200
    assert "Commerce Truth Lab — Audit Report" in rep_html.text

    rep_json = client.get(f"/api/workspaces/{ws_a_id}/reports/json", headers=get_auth_headers(token_a))
    assert rep_json.status_code == 200
    assert rep_json.json()["workspace_id"] == ws_a_id

    rep_md = client.get(f"/api/workspaces/{ws_a_id}/reports/markdown", headers=get_auth_headers(token_a))
    assert rep_md.status_code == 200
    assert "# Audit Report" in rep_md.text

    # Audit Logs
    logs_res = client.get(f"/api/workspaces/{ws_a_id}/logs", headers=get_auth_headers(token_a))
    assert logs_res.status_code == 200
    logs = logs_res.json()
    assert len(logs) >= 3  # csv_uploaded, audit_executed, report_exported

    # --- CROSS-TENANT ISOLATION ASSERTIONS ---
    # Merchant Beta tries to run audit on Workspace Alpha -> 403
    bad_audit = client.post(f"/api/workspaces/{ws_a_id}/audit/run", headers=get_auth_headers(token_b))
    assert bad_audit.status_code == 403

    # Merchant Beta tries to view Workspace Alpha findings -> 403
    bad_findings = client.get(f"/api/workspaces/{ws_a_id}/findings", headers=get_auth_headers(token_b))
    assert bad_findings.status_code == 403

    # Merchant Beta tries to export Workspace Alpha reports -> 403
    bad_report = client.get(f"/api/workspaces/{ws_a_id}/reports/html", headers=get_auth_headers(token_b))
    assert bad_report.status_code == 403

    # Merchant Beta views their own findings in Workspace Beta -> 0 findings (isolated)
    beta_findings = client.get(f"/api/workspaces/{ws_b_id}/findings", headers=get_auth_headers(token_b))
    assert beta_findings.status_code == 200
    assert len(beta_findings.json()["items"]) == 0

