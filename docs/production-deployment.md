# Production Deployment & Architecture Guide
**Commerce Truth Lab v1 &middot; Production Milestone 1 Hardening**

---

## 1. System Architecture

```
                                  +-------------------------------------------------------+
                                  |                 Frontend (Vercel)                     |
                                  |  https://commerce-truth-lab.vercel.app                |
                                  +---------------------------+---------------------------+
                                                              |
                                           HTTPS Requests     | (Bearer JWT Auth)
                                                              v
+-----------------------------+   CORS: Exact Origin Match    +---------------------------+
|      Public Synthetic       | <---------------------------- |      FastAPI Backend      |
|   Demo Route (`/demo`)      |                               |   Python 3.14 / Uvicorn   |
| (No Login / Zero Real Data) |                               +-------------+-------------+
+-----------------------------+                                             |
                                                                            | SQLAlchemy 2.0 (asyncpg)
                                                                            v
                                                              +---------------------------+
                                                              |  PostgreSQL Database      |
                                                              |  (Managed via Alembic)    |
                                                              +---------------------------+
```

---

## 2. Production Environment Variables

In production (`ENVIRONMENT=production`), the application enforces **fail-fast startup validation** in `apps/api/config.py`. If any required secret is missing, weak, or uses default placeholders, the backend terminates immediately with a descriptive `RuntimeError`.

| Variable | Type | Required in Prod | Description & Validation Rules |
|---|---|---|---|
| `ENVIRONMENT` | `string` | **Yes** | Must be set to `production`. Activates strict configuration, disables automatic schema creation, enforces CORS restrictions, and forbids SQLite. |
| `DATABASE_URL` | `string` | **Yes** | Must be a valid PostgreSQL connection string starting with `postgresql://`, `postgres://`, or `postgresql+asyncpg://`. SQLite is strictly forbidden and rejected at startup. |
| `JWT_SECRET_KEY` | `string` | **Yes** | Minimum 32 characters. Must be cryptographically random. Known defaults and dictionary values are blacklisted. |
| `PSEUDONYMIZATION_SALT` | `string` | **Yes** | Minimum 16 characters. Used for deterministic HMAC-SHA256 customer PII hashing. Known defaults are blacklisted. |
| `FRONTEND_ORIGIN` | `string` | **Yes** | Set to the exact deployed frontend origin (e.g., `https://commerce-truth-lab.vercel.app`). Wildcard `*` is strictly forbidden in production. |
| `PORT` | `integer` | No | Default `8000`. Port for Uvicorn ASGI server. |

---

## 3. Database Schema Management & Migrations

Automatic schema creation (`create_all`) is **disabled** in production lifespan to preserve data integrity and migration governance. Database schemas are managed exclusively via Alembic migrations.

### Running Migrations
From `apps/api`:
```bash
# Execute all pending migrations up to head
python -m alembic upgrade head

# Verify database schema matches models with zero discrepancies
python -m alembic check
```

### Initial Migration Reference
- Version ID: `87dcf646c5e0` (`87dcf646c5e0_initial_production_schema.py`)
- Tables Managed (13 tables):
  1. `users`: Merchant user accounts with PBKDF2-HMAC-SHA256 password hashing.
  2. `workspaces`: Multi-tenant organization boundaries.
  3. `workspace_members`: Role-based access control (`admin`, `auditor`, `viewer`).
  4. `orders`: Composite primary key `(workspace_id, id)` with pseudonymized customer IDs.
  5. `payments`: Composite primary key `(workspace_id, id)` with indexed `order_id`.
  6. `courier_settlements`: Composite primary key `(workspace_id, id)` with indexed `order_id`.
  7. `refunds`: Composite primary key `(workspace_id, id)` with indexed `order_id`.
  8. `purchase_signals`: Composite primary key `(workspace_id, id)` with indexed `order_id`.
  9. `data_sources`: Composite primary key `(workspace_id, id)` tracking ingestion status.
  10. `findings`: Audit engine exceptions with source records, assumptions, and next steps.
  11. `upload_metadata`: Staged/committed CSV upload sessions and column mappings.
  12. `audit_runs`: Audit run summary statistics and execution metadata.
  13. `audit_logs`: Immutable audit trail of merchant actions.

---

## 4. Multi-Tenant Isolation Security

Every merchant entity belongs to a workspace identified by a unique `workspace_id`.
Tenant isolation is enforced cryptographically and at the query level:

1. **Composite Primary Keys**: Every transactional table (`orders`, `payments`, `courier_settlements`, `refunds`, `purchase_signals`, `data_sources`) enforces `(workspace_id, id)` as composite primary keys. Cross-tenant row collisions or queries are physically isolated by primary key design.
2. **Access Control Middleware**: `verify_workspace_access(workspace_id, user, db)` validates that the requesting user owns or has an authorized role in the target workspace. Any unauthorized request produces `HTTP 403 Forbidden` (`"Tenant Isolation: You do not have permission to access this merchant workspace."`).
3. **Automated Cross-Tenant Isolation Tests**: Covered by automated test cases in `tests/api/test_auth_and_isolation.py`.

---

## 5. Privacy & PII Non-Persistence Architecture

Commerce Truth Lab operates on an **evidence-first, zero-PII persistence** model:
1. **Never Stored in Plaintext**: Customer names, email addresses, phone numbers, and street addresses are never written to disk or database tables.
2. **Deterministic Pseudonymization**:
   ```python
   def pseudonymize_identifier(raw_value: str, salt: Optional[str] = None) -> str:
       effective_salt = salt or get_pseudonymization_salt()
       digest = hashlib.sha256((raw_value.strip().lower() + effective_salt).encode('utf-8')).hexdigest()
       return f"CUST_{digest[:16]}"
   ```
3. **Preview Masking**: Staged CSV previews mask detected PII columns with `[PSEUDONYMIZED: CUST_xxxx]`.
4. **Verified by Test Suite**: `tests/api/test_production_hardening.py::test_pii_non_persistence_in_database` validates that raw customer emails never exist in the database.

---

## 6. CSV Formula Injection Defense (CWE-1236)

All uploaded CSV text fields and preview representations are processed through formula sanitization:
```python
def sanitize_csv_value(val: Any) -> str:
    # If cell starts with '=', '+', '-', '@', '\t', '\r', prepend single quote
    # Preserves purely numeric signed numbers (e.g. -49.99)
```
This neutralizes command execution or DDE injection when exported reports or data tables are opened in Microsoft Excel or Google Sheets.

---

## 7. Public Demo vs. Private Workspace Routing

| Path | Access Level | Data Source | Security |
|---|---|---|---|
| `/` | Public | Marketing landing page | No auth required |
| `/demo` | Public | Deterministic synthetic dataset only | No auth required; clearly labeled |
| `/login` | Public | Authentication endpoint | Secure token issuance |
| `/workspace/*` | **Protected** | Real merchant PostgreSQL database | Strict JWT Bearer auth + Tenant isolation |

---

## 8. Verification Runbook

To verify deployment end-to-end:
1. Run backend test suite:
   ```bash
   python -m pytest tests/ -v
   # Output: 39 passed in ~8s
   ```
2. Run frontend production build:
   ```bash
   cd apps/web && npm run build
   # Output: built in ~9s with 0 errors
   ```
3. Verify Alembic schema synchronicity:
   ```bash
   cd apps/api && python -m alembic check
   # Output: No new upgrade operations detected.
   ```
