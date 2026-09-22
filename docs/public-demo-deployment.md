# Public Demo & Production Deployment Guide — Commerce Truth Lab v1

This guide documents the architecture and deployment workflow for **Commerce Truth Lab v1** on **Vercel** with zero-login public demonstration, offline synthetic fallback, and secure multi-tenant PostgreSQL workspace connectivity.

- **Public Production URL:** [https://commerce-truth-lab.vercel.app](https://commerce-truth-lab.vercel.app)
- **Public Demo Route:** [https://commerce-truth-lab.vercel.app/demo](https://commerce-truth-lab.vercel.app/demo)
- **GitHub Repository:** [https://github.com/muslim-rashdi-ecom/commerce-truth-lab](https://github.com/muslim-rashdi-ecom/commerce-truth-lab)
- **Founder Portfolio:** [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)

---

## Architecture Overview

Commerce Truth Lab v1 uses a monorepo structure deploying frontend static assets and serverless Python API endpoints via Vercel:

```
                      [ Client Browser ]
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
       [ Vercel CDN ]              [ Vercel Serverless ]
      Static React SPA           FastAPI (/api/index.py)
   (Overview, Reconciliation,                │
     Findings, Tracking,                     ▼
     Client-Side Fallbacks)       [ PostgreSQL (Neon / Supabase) ]
                                  (Auth, Tenant Isolation, Alembic)
```

### Dual Operating Modes
1. **Public Demonstration Mode (`/demo/*`):**
   - 100% public, zero login required.
   - Built-in client-side synthetic fallback adapter (`apps/web/src/api/client.ts`).
   - If the backend API is unreachable or returns an empty dataset, the UI automatically and reliably serves the complete 12-order, 7-currency synthetic casebook with 8 findings and 4 healthy controls.
   - HTML, JSON, and Markdown reports are generated deterministically directly in the browser via Blob URLs.
2. **Private Merchant Workspace Mode (`/workspace/*`):**
   - Protected behind JWT Bearer authentication (`/workspace/login`).
   - Requires real PostgreSQL connection managed via Alembic migrations.
   - Enforces cryptographic tenant isolation via composite primary keys `(workspace_id, id)`.
   - Salted SHA-256 PII pseudonymization and CWE-1236 CSV formula injection defense.

---

## 1. Environment Variables Configuration

### Production Settings (Vercel Project Settings -> Environment Variables)

| Variable | Target | Required in Prod? | Description / Example Value |
|---|---|---|---|
| `ENVIRONMENT` | API | **Yes** | Set to `production` (enforces PostgreSQL, rejects SQLite). |
| `DATABASE_URL` | API | **Yes** | `postgresql+asyncpg://user:pass@host:5432/dbname` (PostgreSQL connection string). |
| `JWT_SECRET_KEY` | API | **Yes** | Cryptographically random string (min 32 chars) for signing session tokens. |
| `PSEUDONYMIZATION_SALT` | API | **Yes** | Cryptographically random salt (min 16 chars) for SHA-256 PII hashing. |
| `FRONTEND_ORIGIN` | API | **Yes** | `https://commerce-truth-lab.vercel.app` (Strict CORS origin; no wildcard). |
| `VITE_API_URL` | Web | Optional | Optional custom API base URL. If empty, the frontend uses relative `/api` paths routed to `/api/index.py`. |

---

## 2. Public vs. Authenticated Route Matrix

| Route Path | Access Level | Description |
|---|---|---|
| `/` | **Public** | Marketing & positioning landing page (9 anti-hype sections, pilot CTAs). |
| `/demo` | **Public** | Direct entry redirecting to synthetic demo overview. |
| `/demo/overview` | **Public** | KPI metrics, registered data sources table, and recent findings. |
| `/demo/findings` | **Public** | Filterable list of 8 investigative exceptions and 4 healthy controls. |
| `/demo/reconciliation` | **Public** | Order lifecycle explorer (Order, Gateway, Courier COD, Refund, Signals). |
| `/demo/tracking-health` | **Public** | Meta Pixel vs CAPI tracking signals comparison with duplicate identity review. |
| `/demo/reports` | **Public** | Export interface for standalone HTML, machine-readable JSON, and Markdown. |
| `/workspace/login` | **Public** | Merchant sign-in and registration portal. |
| `/workspace/*` | **Protected (JWT)** | Authenticated multi-tenant merchant portal (CSV upload, audit run, audit logs). |
| `/api/health` | **Public** | Health status check returning version and operational mode. |
| `/api/demo/*` | **Public** | Backend synthetic endpoints (with client-side fallback guarantee). |

---

## 3. Vercel Monorepo Deployment Setup

The repository contains `apps/web/vercel.json` configured for a unified monorepo deployment:

```json
{
  "buildCommand": "python prepare_api.py && npm run build && python ../api/production_migrate.py",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Build Pipeline Steps:
1. `python prepare_api.py`: Copies backend source files (`apps/api/`, `packages/ctl_engine/`, `packages/shared/`) into `apps/web/api_src` and configures the entry point `apps/web/api/index.py`.
2. `npm run build`: Executes TypeScript compilation (`tsc`) and Vite static asset bundling into `apps/web/dist`.
3. `python ../api/production_migrate.py`: Runs Alembic migrations (`alembic upgrade head`) against the production PostgreSQL database.

### Deployment Instructions:
1. In the [Vercel Dashboard](https://vercel.com/new), import the GitHub repository:  
   `https://github.com/muslim-rashdi-ecom/commerce-truth-lab.git`
2. Configure settings:
   - **Root Directory:** `apps/web`
   - **Framework Preset:** `Vite`
   - **Build Command:** (Leave default, detected from `vercel.json`)
   - **Output Directory:** `dist`
3. Add the production environment variables (`DATABASE_URL`, `JWT_SECRET_KEY`, `PSEUDONYMIZATION_SALT`, `FRONTEND_ORIGIN`, `ENVIRONMENT`).
4. Click **Deploy**.

---

## 4. Post-Deployment Verification Checklist

After deployment finishes, run through these checks:

- [ ] **1. Public Access Without Login:** Navigate to `https://<your-app>.vercel.app/demo`. The audit dashboard renders immediately without login.
- [ ] **2. Prominent Synthetic Notice:** Verify the yellow banner `“SYNTHETIC DEMO — NOT REAL BUSINESS DATA”` appears across `/demo/*`.
- [ ] **3. Metric Totals:** Verify `/demo/overview` displays:
  - Orders Reviewed: `12`
  - Findings: `8`
  - Affected Orders: `8`
  - Data Completeness: `100.0%`
  - Currencies evaluated: `7` (AED, USD, JPY, KWD, PKR, GBP, EUR)
- [ ] **4. Responsive Layout:** Check desktop (1440px), tablet (768px), and mobile (375px) viewports. Verify sidebar navigation collapses into a hamburger menu.
- [ ] **5. Order Reconciliation Explorer:** Navigate to `/demo/reconciliation`, select `ORD-001`, and click through Order, Payment, Courier COD, and Signals tabs. Verify the timeline loads without errors.
- [ ] **6. Report Generation:** On `/demo/reports`, click **Open in New Tab** (HTML), **Download JSON**, and **Download Markdown**. Confirm all three work without network failure.
- [ ] **7. Protected Workspace Gate:** Visit `/workspace` without a token. Verify you are prompted to sign in at `/workspace/login`.
- [ ] **8. Portfolio & GitHub Links:** Verify footer and landing page links direct to Syed Muslim Shah's portfolio (`https://syed-muslim-shah-portfolio.vercel.app/`) and the GitHub repository.
