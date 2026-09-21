# Public Demo Deployment Guide — Commerce Truth Lab v1

This document outlines the step-by-step procedure for deploying **Commerce Truth Lab v1** to public hosting platforms (such as **Vercel** for the React frontend and **Render / Railway / Koyeb** for the FastAPI backend) with zero cost and zero paid API dependencies.

- **Public Production URL:** [https://commerce-truth-lab.vercel.app/demo](https://commerce-truth-lab.vercel.app/demo)
- **GitHub Repository:** [https://github.com/muslim-rashdi-ecom/commerce-truth-lab](https://github.com/muslim-rashdi-ecom/commerce-truth-lab)
- **Founder Portfolio:** [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)

---

## Architecture Overview for Deployment

Commerce Truth Lab v1 uses a decoupled client-server architecture:
- **Frontend (`apps/web`)**: Single-Page Application (SPA) built with React, TypeScript, and Vite. Static output in `dist/`.
- **Backend API (`apps/api`)**: Python 3.12+ ASGI application using FastAPI, SQLAlchemy 2.0, and SQLite (`data/demo.db`) seeded with reproducible synthetic test vectors.

```
       [ Client Browser ]
               │
        ┌──────┴──────┐
        ▼             ▼
   [ Vercel CDN ]  [ Backend Host: Render / Railway ]
    apps/web/dist    apps/api (FastAPI + SQLite)
        │                     ▲
        └────── /api ─────────┘
```

---

## 1. Required Environment Variables

### Frontend (`apps/web`)

| Variable | Environment | Example Value | Description |
|---|---|---|---|
| `VITE_API_URL` | Production / Preview | `https://commerce-truth-lab-api.onrender.com` | Base URL of the deployed FastAPI backend. Omit in local development to use the default `http://localhost:8000` or the Vite dev proxy. |

### Backend (`apps/api`)

| Variable | Environment | Default Value | Description |
|---|---|---|---|
| `PORT` | Production | `8000` | Port assigned by hosting provider (Render/Railway sets this automatically). |
| `DATABASE_URL` | Production | `sqlite+aiosqlite:///data/demo.db` | Path to SQLite database file. Automatically populated on startup by `seed.py`. |
| `DEMO_MODE` | Production | `true` | Enforces synthetic data constraints and disables destructive mutations. |
| `CORS_ORIGINS` | Production | `https://*.vercel.app,http://localhost:5173` | Allowed CORS origins for the frontend. |

---

## 2. Public vs. Authenticated Route Matrix

| Route Path | Type | Access Level | Description |
|---|---|---|---|
| `/` | Frontend | **Public (No Login)** | Marketing landing page with mission, target users, anti-hype guarantee, limitations, and founder links. |
| `/demo` | Frontend | **Public (No Login)** | Direct entry to the public synthetic demonstration. |
| `/demo/overview` | Frontend | **Public (No Login)** | Summary dashboard calculating metrics from the 12 synthetic orders. |
| `/demo/findings` | Frontend | **Public (No Login)** | Complete list of flagged exceptions and healthy controls with rule filters. |
| `/demo/reconciliation` | Frontend | **Public (No Login)** | Order-level cross-system comparison (order, payment, courier COD, refund, signals). |
| `/demo/tracking-health`| Frontend | **Public (No Login)** | Ad platform signal verification table with duplicate identity and mismatch flags. |
| `/demo/reports` | Frontend | **Public (No Login)** | Export interface for HTML, JSON, and Markdown audit reports. |
| `/workspace/*` | Frontend | **Protected** | Displays merchant authorization and security requirements screen. |
| `/app/*` | Frontend | **Protected** | Enforces pilot authorization prerequisites before accessing real data. |
| `/api/health` | Backend API | **Public** | System status, version info, and demo mode indicator. |
| `/api/demo/*` | Backend API | **Public** | All read-only synthetic demonstration endpoints. |
| `/api/upload` | Backend API | **Public** | CSV header detection and column mapping simulation. |

---

## 3. Frontend Deployment (Vercel)

### Option A: Via Vercel Web Dashboard (Recommended)

1. Push the code to GitHub:
   ```bash
   git remote add origin https://github.com/muslim-rashdi-ecom/commerce-truth-lab.git
   git push -u origin main
   ```
2. In the [Vercel Dashboard](https://vercel.com/new), select **Import Git Repository**.
3. Configure project settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `apps/web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
4. Add Environment Variable:
   - `VITE_API_URL`: Your deployed backend URL (e.g., `https://commerce-truth-lab-api.onrender.com`).
5. Click **Deploy**.

### Option B: Via Vercel CLI

```bash
cd apps/web
npm install -g vercel
vercel --prod
```

### SPA Routing Configuration (`vercel.json`)
To ensure direct links to `/demo/reconciliation` or `/demo/findings` work without 404s, `apps/web/vercel.json` is provided:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 4. Backend Deployment (Render / Railway / Koyeb Free Tier)

### Deploying to Render.com (Web Service)

1. In the [Render Dashboard](https://dashboard.render.com), click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Name**: `commerce-truth-lab-api`
   - **Environment**: `Python 3`
   - **Region**: Closest to your users (e.g., Frankfurt or Oregon)
   - **Branch**: `main`
   - **Root Directory**: `commerce-truth-lab-v1`
   - **Build Command**:
     ```bash
     pip install -r apps/api/requirements.txt && pip install -r packages/ctl_engine/requirements.txt && PYTHONPATH=packages:apps/api python apps/api/seed.py
     ```
   - **Start Command**:
     ```bash
     PYTHONPATH=packages:apps/api uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT
     ```
4. Environment Variables:
   - `DEMO_MODE` = `true`
5. Click **Create Web Service**.

### Alternative: Docker Deployment

The repository includes a production `Dockerfile` in `apps/api/Dockerfile`. To build and run with Docker:
```bash
docker build -t commerce-truth-lab-api -f apps/api/Dockerfile .
docker run -p 8000:8000 -e DEMO_MODE=true commerce-truth-lab-api
```

---

## 5. Post-Deployment Verification Checklist

Once deployed, run through these verification steps to confirm everything operates as expected:

- [ ] **1. Public Access**: Open `https://<your-app>.vercel.app/demo` in an Incognito window. The demo must render immediately without prompting for login.
- [ ] **2. Synthetic Label**: Verify the banner `“SYNTHETIC DEMO — NOT REAL BUSINESS DATA”` appears prominently across all `/demo/*` pages.
- [ ] **3. Metric Verification**: On `/demo/overview`, check that the cards calculate:
  - Orders Reviewed: `12`
  - Findings: `8`
  - Affected Orders: `8`
  - Data Completeness: `100.0%`
- [ ] **4. Responsive Layout**: Resize the browser to mobile viewport (375px width). Verify the collapsible hamburger navigation menu works and tables scroll smoothly.
- [ ] **5. Order Reconciliation Detail**: Navigate to `/demo/reconciliation`, click `ORD-001`, and switch between Order, Courier COD, Payment, and Signals tabs. Verify the timeline loads without errors.
- [ ] **6. Report Downloads**: On `/demo/reports`, click **Download JSON** and **Download Markdown**. Confirm both files download with synthetic disclaimers intact.
- [ ] **7. Protected Route Enforcement**: Visit `https://<your-app>.vercel.app/workspace`. Confirm the private workspace notice renders and explains authorization requirements.
- [ ] **8. Founder Portfolio & GitHub Links**: Check the footer and landing page links to Syed Muslim Shah's portfolio (`https://syed-muslim-shah-portfolio.vercel.app/`) and the GitHub repository.
