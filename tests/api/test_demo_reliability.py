import asyncio
import pytest
from fastapi.testclient import TestClient
from main import app
from database import init_db
from seed import seed_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    async def _init():
        await init_db()
    asyncio.run(_init())
    seed_db()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_demo_workspace_endpoint(client):
    """Verify demo workspace returns complete synthetic metadata."""
    res = client.get("/api/demo/workspace")
    assert res.status_code == 200
    data = res.json()
    assert data["is_synthetic"] is True
    assert data["order_count"] == 12
    assert data["finding_count"] == 8
    assert data["data_completeness_pct"] == 100.0

def test_demo_orders_endpoint(client):
    """Verify demo orders endpoint returns all 12 orders across 7 currencies."""
    res = client.get("/api/demo/orders")
    assert res.status_code == 200
    orders = res.json()
    assert len(orders) == 12
    currencies = {o["currency"] for o in orders}
    # Dataset includes AED, USD, JPY, KWD, PKR, GBP, EUR
    assert "AED" in currencies
    assert "USD" in currencies
    assert "JPY" in currencies
    assert "KWD" in currencies
    assert "PKR" in currencies
    assert "GBP" in currencies
    assert "EUR" in currencies

def test_demo_order_detail(client):
    """Verify order detail retrieval for specific synthetic orders."""
    res = client.get("/api/demo/orders/ORD-001")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "ORD-001"
    assert data["currency"] == "AED"
    assert data["payment_method"] == "COD"

def test_demo_findings_and_healthy_controls(client):
    """Verify findings (8 exceptions) and healthy controls (4 clean cases)."""
    res_f = client.get("/api/demo/findings")
    assert res_f.status_code == 200
    findings_data = res_f.json()
    items = findings_data.get("items", [])
    assert len(items) == 8
    for item in items:
        assert item["is_healthy_control"] is False
        assert "observed" in item
        assert "not_proven" in item
        assert "next_step" in item

    res_hc = client.get("/api/demo/healthy-controls")
    assert res_hc.status_code == 200
    controls = res_hc.json()
    assert len(controls) == 4
    for ctrl in controls:
        assert ctrl["is_healthy_control"] is True

def test_demo_reconciliation(client):
    """Verify lifecycle reconciliation view returns linked records."""
    res = client.get("/api/demo/reconciliation/ORD-001")
    assert res.status_code == 200
    data = res.json()
    assert data["order"]["id"] == "ORD-001"
    assert len(data.get("settlements", [])) >= 1
    assert len(data.get("timeline", [])) >= 1

    # ORD-005 is JPY with tracking signal
    res_jpy = client.get("/api/demo/reconciliation/ORD-005")
    assert res_jpy.status_code == 200
    data_jpy = res_jpy.json()
    assert data_jpy["order"]["currency"] == "JPY"
    assert len(data_jpy.get("purchase_signals", [])) >= 1

def test_demo_tracking_health(client):
    """Verify tracking signal health summary and comparisons."""
    res = client.get("/api/demo/tracking-health")
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_orders"] == 12
    assert len(data["order_signals"]) == 12

def test_demo_report_exports(client):
    """Verify standalone HTML, Markdown, and JSON report generation."""
    res_html = client.get("/api/demo/reports/html")
    assert res_html.status_code == 200
    assert "text/html" in res_html.headers.get("content-type", "")
    assert "SYNTHETIC" in res_html.text

    res_md = client.get("/api/demo/reports/markdown")
    assert res_md.status_code == 200
    assert "Commerce Truth Lab" in res_md.text

    res_json = client.get("/api/demo/reports/json")
    assert res_json.status_code == 200
    data = res_json.json()
    assert "workspace" in data
    assert "findings" in data
    assert "healthy_controls" in data

def test_demo_routes_404_on_missing_id(client):
    """Verify 404 handling for nonexistent order requests."""
    res1 = client.get("/api/demo/orders/ORD-NONEXISTENT")
    assert res1.status_code == 404

    res2 = client.get("/api/demo/reconciliation/ORD-NONEXISTENT")
    assert res2.status_code == 404

def test_api_health_endpoint(client):
    """Verify public health endpoint."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "version" in data
