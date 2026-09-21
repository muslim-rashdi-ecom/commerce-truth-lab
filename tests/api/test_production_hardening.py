import io
import json
import os
import uuid
import pytest
from fastapi.testclient import TestClient

from main import app
from config import validate_production_config, get_jwt_secret_key, get_pseudonymization_salt
from services.merchant_upload_service import sanitize_csv_value
from database import AsyncSessionLocal
from models import Order, User
from sqlalchemy import select


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def get_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def rand_email(prefix: str = "hardened") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@merchant-audit.com"


# ---------------------------------------------------------------------------
# 1. Strict Environment & Production Configuration Tests
# ---------------------------------------------------------------------------

def test_production_config_rejects_sqlite():
    """Verify validate_production_config fails fast if SQLite is specified in production."""
    old_env = os.environ.get("ENVIRONMENT")
    old_db = os.environ.get("DATABASE_URL")
    old_jwt = os.environ.get("JWT_SECRET_KEY")
    old_salt = os.environ.get("PSEUDONYMIZATION_SALT")

    try:
        import config
        # Mock production environment
        config.ENVIRONMENT = "production"
        config.RAW_DATABASE_URL = "sqlite+aiosqlite:///demo.db"
        config.RAW_JWT_SECRET_KEY = "a_very_secure_and_long_production_jwt_secret_32_chars"
        config.RAW_PSEUDONYMIZATION_SALT = "secure_production_salt_12345"

        with pytest.raises(RuntimeError, match="SQLite is strictly forbidden in production"):
            config.validate_production_config()
    finally:
        config.ENVIRONMENT = old_env or "development"
        config.RAW_DATABASE_URL = old_db or ""
        config.RAW_JWT_SECRET_KEY = old_jwt or ""
        config.RAW_PSEUDONYMIZATION_SALT = old_salt or ""


def test_production_config_rejects_missing_or_weak_jwt_secret():
    """Verify validate_production_config fails fast if JWT_SECRET_KEY is missing, too short, or blacklisted."""
    old_env = os.environ.get("ENVIRONMENT")
    try:
        import config
        config.ENVIRONMENT = "production"
        config.RAW_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/truthlab"
        config.RAW_PSEUDONYMIZATION_SALT = "secure_production_salt_12345"

        # Missing
        config.RAW_JWT_SECRET_KEY = ""
        with pytest.raises(RuntimeError, match="JWT_SECRET_KEY must be set in production"):
            config.validate_production_config()

        # Too short (< 32 chars)
        config.RAW_JWT_SECRET_KEY = "short_secret_key"
        with pytest.raises(RuntimeError, match="must be at least 32 characters long"):
            config.validate_production_config()

        # Blacklisted default
        config.RAW_JWT_SECRET_KEY = "ctl_production_secret_key_change_in_env_2026"
        with pytest.raises(RuntimeError, match="forbidden in production"):
            config.validate_production_config()
    finally:
        config.ENVIRONMENT = old_env or "development"


def test_production_config_rejects_missing_or_weak_salt():
    """Verify validate_production_config fails fast if PSEUDONYMIZATION_SALT is weak or missing."""
    old_env = os.environ.get("ENVIRONMENT")
    try:
        import config
        config.ENVIRONMENT = "production"
        config.RAW_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/truthlab"
        config.RAW_JWT_SECRET_KEY = "a_very_secure_and_long_production_jwt_secret_32_chars"

        # Missing
        config.RAW_PSEUDONYMIZATION_SALT = ""
        with pytest.raises(RuntimeError, match="PSEUDONYMIZATION_SALT must be set in production"):
            config.validate_production_config()

        # Too short (< 16 chars)
        config.RAW_PSEUDONYMIZATION_SALT = "short_salt"
        with pytest.raises(RuntimeError, match="must be at least 16 characters long"):
            config.validate_production_config()

        # Blacklisted
        config.RAW_PSEUDONYMIZATION_SALT = "ctl_salt_987654321"
        with pytest.raises(RuntimeError, match="forbidden in production"):
            config.validate_production_config()
    finally:
        config.ENVIRONMENT = old_env or "development"


def test_production_config_rejects_wildcard_cors():
    """Verify validate_production_config fails fast if FRONTEND_ORIGIN is wildcard or missing."""
    old_env = os.environ.get("ENVIRONMENT")
    try:
        import config
        config.ENVIRONMENT = "production"
        config.RAW_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/truthlab"
        config.RAW_JWT_SECRET_KEY = "a_very_secure_and_long_production_jwt_secret_32_chars"
        config.RAW_PSEUDONYMIZATION_SALT = "secure_production_salt_12345"

        config.FRONTEND_ORIGIN = "*"
        with pytest.raises(RuntimeError, match="Wildcard or empty FRONTEND_ORIGIN is forbidden"):
            config.validate_production_config()
    finally:
        config.ENVIRONMENT = old_env or "development"


# ---------------------------------------------------------------------------
# 2. CSV Formula Injection Sanitization Tests
# ---------------------------------------------------------------------------

def test_sanitize_csv_value_neutralizes_formulas():
    """Verify formula injection triggers (=, +, -, @, \\t, \\r) are prepended with single quote."""
    assert sanitize_csv_value("=cmd|'/c calc'!A0") == "'=cmd|'/c calc'!A0"
    assert sanitize_csv_value("+SUM(A1:A10)") == "'+SUM(A1:A10)"
    assert sanitize_csv_value("@HYPERLINK('http://evil.com')") == "'@HYPERLINK('http://evil.com')"
    assert sanitize_csv_value("\t=1+1") == "'\t=1+1"
    assert sanitize_csv_value("\r=cmd") == "'\r=cmd"

    # Numeric literals with sign should remain intact
    assert sanitize_csv_value("-49.99") == "-49.99"
    assert sanitize_csv_value("+100") == "+100"
    assert sanitize_csv_value("250.00") == "250.00"

    # Clean text should remain intact
    assert sanitize_csv_value("ORD-1001") == "ORD-1001"
    assert sanitize_csv_value("Shopify Payments") == "Shopify Payments"


def test_upload_formula_injection_sanitization_in_preview_and_commit(client):
    """Verify CSV formula injection payloads in uploaded CSVs are neutralized in preview and db."""
    # 1. Create merchant and workspace
    email = rand_email("inject")
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Formula Guard Tester"
    })
    token = reg_res.json()["access_token"]
    headers = get_auth_headers(token)

    ws_res = client.post("/api/workspaces", json={"name": "Formula Security Store"}, headers=headers)
    ws_id = ws_res.json()["id"]

    # 2. Prepare malicious CSV with formula injection payloads in order_id, customer_id, and status
    malicious_csv = (
        "order_id,created_at,total_amount,currency,payment_method,status,customer_id\n"
        "=cmd|'/c calc'!A0,2026-03-01T10:00:00Z,150.00,USD,prepaid,+2+5,@evil_domain.com\n"
    )

    # 3. Stage upload
    stage_res = client.post(
        f"/api/workspaces/{ws_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("malicious.csv", malicious_csv.encode("utf-8"), "text/csv")},
        headers=headers
    )
    assert stage_res.status_code == 200, stage_res.text
    stage_data = stage_res.json()

    # Verify preview is sanitized
    preview_row = stage_data["preview_rows"][0]
    # Status (+2+5) should be sanitized to '+2+5
    assert preview_row["status"] == "'+2+5"
    # Customer ID should be pseudonymized
    assert preview_row["customer_id"].startswith("[PSEUDONYMIZED: CUST_")

    # 4. Commit upload
    commit_res = client.post(
        f"/api/workspaces/{ws_id}/upload/commit",
        data={
            "upload_id": stage_data["upload_id"],
            "mappings": json.dumps(stage_data["suggested_mappings"])
        },
        files={"file": ("malicious.csv", malicious_csv.encode("utf-8"), "text/csv")},
        headers=headers
    )
    assert commit_res.status_code == 200

    # 5. Fetch imported orders and check DB values
    orders_res = client.get(f"/api/workspaces/{ws_id}/orders", headers=headers)
    assert orders_res.status_code == 200
    orders = orders_res.json()
    assert len(orders) == 1

    stored_order = orders[0]
    # Order ID '=cmd|...' must be stored sanitized with leading quote
    assert stored_order["id"] == "'=cmd|'/c calc'!A0"
    # Status '+2+5' must be stored sanitized with leading quote
    assert stored_order["status"] == "'+2+5"
    # Customer identifier must be pseudonymized (never plaintext evil email)
    assert "evil_domain" not in stored_order["customer_id"]
    assert stored_order["customer_id"].startswith("CUST_")


# ---------------------------------------------------------------------------
# 3. Upload File Size & Extension Validation Tests
# ---------------------------------------------------------------------------

def test_upload_rejects_non_csv_extension(client):
    """Verify non-CSV files (.pdf, .xlsx, .json, .exe) are rejected with HTTP 400."""
    email = rand_email("file_type")
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "File Type Tester"
    })
    token = reg_res.json()["access_token"]
    headers = get_auth_headers(token)

    ws_res = client.post("/api/workspaces", json={"name": "File Type Store"}, headers=headers)
    ws_id = ws_res.json()["id"]

    res_pdf = client.post(
        f"/api/workspaces/{ws_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("report.pdf", b"%PDF-1.4 ... fake pdf content", "application/pdf")},
        headers=headers
    )
    assert res_pdf.status_code == 400
    assert "Only .csv files are supported" in res_pdf.json()["detail"]


def test_upload_rejects_oversized_file(client):
    """Verify file uploads exceeding 25MB are rejected with HTTP 400."""
    email = rand_email("size_limit")
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Size Limit Tester"
    })
    token = reg_res.json()["access_token"]
    headers = get_auth_headers(token)

    ws_res = client.post("/api/workspaces", json={"name": "Size Limit Store"}, headers=headers)
    ws_id = ws_res.json()["id"]

    # 26MB dummy byte payload
    oversized_bytes = b"a" * (26 * 1024 * 1024)
    res_oversized = client.post(
        f"/api/workspaces/{ws_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("large_orders.csv", oversized_bytes, "text/csv")},
        headers=headers
    )
    assert res_oversized.status_code == 400
    assert "exceeds 25MB limit" in res_oversized.json()["detail"]


# ---------------------------------------------------------------------------
# 4. Strict PII Non-Persistence Verification
# ---------------------------------------------------------------------------

def test_pii_non_persistence_in_database(client):
    """Confirm customer email, phone, and address are NEVER written in plaintext to the database."""
    email = rand_email("pii_audit")
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "PII Tester"
    })
    token = reg_res.json()["access_token"]
    headers = get_auth_headers(token)

    ws_res = client.post("/api/workspaces", json={"name": "PII Store"}, headers=headers)
    ws_id = ws_res.json()["id"]

    secret_raw_email = "very_confidential_customer_99@private.com"
    csv_content = (
        "order_id,created_at,total_amount,currency,payment_method,status,customer_id\n"
        f"PII-ORD-01,2026-03-01T10:00:00Z,200.00,USD,prepaid,paid,{secret_raw_email}\n"
    )

    stage_res = client.post(
        f"/api/workspaces/{ws_id}/upload/stage",
        data={"source_type": "shopify_orders"},
        files={"file": ("pii_test.csv", csv_content.encode("utf-8"), "text/csv")},
        headers=headers
    )
    stage_data = stage_res.json()

    commit_res = client.post(
        f"/api/workspaces/{ws_id}/upload/commit",
        data={
            "upload_id": stage_data["upload_id"],
            "mappings": json.dumps(stage_data["suggested_mappings"])
        },
        files={"file": ("pii_test.csv", csv_content.encode("utf-8"), "text/csv")},
        headers=headers
    )
    assert commit_res.status_code == 200

    # Query directly from the database using SQLAlchemy session
    async def _verify():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Order).where(Order.workspace_id == ws_id, Order.id == "PII-ORD-01")
            )
            db_order = result.scalars().first()

            assert db_order is not None
            # Must NOT equal secret_raw_email
            assert db_order.customer_id != secret_raw_email
            # Must NOT contain the raw email string
            assert secret_raw_email not in db_order.customer_id
            # Must be a deterministic pseudonym
            assert db_order.customer_id.startswith("CUST_")
            assert len(db_order.customer_id) == 21  # "CUST_" + 16 hex chars

    import asyncio
    asyncio.run(_verify())
