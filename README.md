# Commerce Truth Lab v1

> **Evidence-first e-commerce audit application for Shopify and DTC brands.**  
> Answers: *"Do our orders, payments, COD settlements, refunds, and advertising purchase signals agree—and what evidence supports each exception?"*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Tests](https://img.shields.io/badge/Tests-63%20Passed-emerald.svg)](#tests)

---

### ⚠️ SYNTHETIC DEMO — NOT REAL BUSINESS DATA
**All records, financial metrics, customer identifiers, and tracking events shown in this demonstration are strictly synthetic test vectors.**  
Commerce Truth Lab **never** makes unsubstantiated claims of recovered revenue, lost revenue, automated fraud detection, or causal ROAS improvements.

- **Public Demo URL:** [https://commerce-truth-lab.vercel.app/demo](https://commerce-truth-lab.vercel.app/demo)
- **Founder Portfolio:** [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)
- **GitHub Repository:** [https://github.com/muslim-rashdi-ecom/commerce-truth-lab](https://github.com/muslim-rashdi-ecom/commerce-truth-lab)

---

## 🎯 What Problem It Solves

A purchase event reported by Meta, an order registered in Shopify, a cash receipt collected by a courier, and a bank deposit are four completely different operational facts:
1. **COD Settlement Delay:** Courier collects Cash on Delivery but does not remit it within agreed grace periods.
2. **Signal Deduplication Failures:** Web pixel and server CAPI fire differing `event_id` keys, causing ad platforms to over-report conversions.
3. **Currency Minor-Unit Anomalies:** Multi-currency stores (e.g. JPY with 0 decimals or KWD with 3 decimals) suffer 100x value misreporting due to floating-point truncation.
4. **Refund Leakage:** Refunds issued exceed original transaction captures.

Every exception identified by Commerce Truth Lab provides:
- **What was observed**
- **Which source records support it**
- **Which assumptions were applied**
- **What is NOT proven (anti-hype boundary)**
- **The recommended next verification step**
- **The responsible team owner**

---

## 🚀 Public Demo Routes (No Login Required)

| Route | Description |
|---|---|
| `/` | Landing page explaining mission, anti-hype principles, and limitations |
| `/demo` or `/demo/overview` | Executive audit dashboard calculating metrics from synthetic dataset |
| `/demo/findings` | Categorized exceptions and healthy controls with severity filters |
| `/demo/reconciliation` | Order lifecycle explorer (Order, Payment, Courier COD, Refund, Signals) |
| `/demo/tracking-health` | Ad platform purchase signal comparison & duplicate identity review |
| `/demo/reports` | Export audit results to standalone HTML, JSON, or Markdown (.md) |
| `/workspace/login` | Merchant authentication portal (registration and JWT login) |
| `/workspace/*` | Protected multi-tenant merchant portal (CSV upload, audit runner, and reconciliation) |

---

## 🛠️ Local Setup & Quickstart

No API keys, external databases, or paid SaaS tools are needed to run the entire suite locally.

### Prerequisites
- Python 3.12+
- Node.js 18+ (or Node 20+)
- npm

### 1. Start the FastAPI Backend
```bash
# From workspace root:
cd apps/api
python -m pip install -r requirements.txt
python seed.py          # Seeds SQLite with the 12 synthetic orders
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
API runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 2. Start the React Frontend
```bash
# In a separate terminal:
cd apps/web
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## 🧪 Test Commands
 
```bash
# Run 63 automated tests covering engine rules, auth, tenant isolation, pilot workflow, demo reliability, and production hardening:
python -m pytest tests/ -v

# Run production frontend build
cd apps/web
npm run build
```

---

## 🏗️ Monorepo Architecture

```
commerce-truth-lab-v1/
├── apps/
│   ├── web/               # React 18, TypeScript, Vite, Tailwind CSS
│   └── api/               # Python 3.12+, FastAPI, SQLAlchemy 2.0 (PostgreSQL asyncpg / SQLite aiosqlite)
├── packages/
│   ├── ctl_engine/        # Pure Python deterministic audit rules (CTL-001 to CTL-012)
│   └── shared/            # Shared Pydantic v2 domain schemas and currency metadata
├── data/
│   └── synthetic/         # Reproducible 12-order test dataset across 7 currencies
├── docs/                  # Product specs, architecture, security, templates, deployment guides
│   ├── pilot-authorization-agreement.md  # Pilot authorization agreement, scopes, zero-PII and 30-day retention terms
│   ├── pilot-data-contract.md            # Minimum required input streams, column synonyms, integer minor units
│   ├── pilot-evidence-ledger.md          # Traceable evidence pointers and controls for pilot brand 01
│   ├── pilot-implementation-report-brand-01.md # Client-ready audit report with 3 prioritized fixes & verification
│   ├── pilot-case-study-template.md      # Strictly formatted case study template with anti-fabrication standards
│   └── sample-csv-templates/             # Safe CSV templates for merchant pilot onboarding
├── scripts/               # PowerShell convenience startup scripts
├── docker-compose.yml     # Containerized deployment spec
└── pytest.ini             # Pytest discovery configuration
```

---

## 📋 Synthetic Casebook Overview

The seed workspace includes **12 synthetic orders across 7 currencies (AED, USD, JPY, KWD, PKR, GBP, EUR)**:
- **4 Healthy Controls:** Valid deduplication, zero-discrepancy refunds, within-grace COD delivery, and accurate KWD 3-decimal precision.
- **8 Intentional Audit Exceptions:** Duplicate signal event IDs, missing pixel events, 100x JPY decimal error, currency mismatch, overdue COD remittance, delivery shortfall, overcollection, and refund exceeding capture.

---

## 🔒 Security & Merchant Pilot Readiness

Real-world pilot sprints for Shopify brands operate on authorized, pseudonymized data exports:
1. **Zero Plaintext PII:** No customer names, phone numbers, credit card numbers, or plaintext emails are stored.
2. **Tenant Isolation:** Independent merchant workspaces enforced at database query and session levels.
3. **Formal Pilot Governance:** Governed by [`docs/pilot-authorization-agreement.md`](docs/pilot-authorization-agreement.md) and [`docs/pilot-data-contract.md`](docs/pilot-data-contract.md).
4. **Traceable Evidence:** Every exception points to immutable source rows documented in [`docs/pilot-evidence-ledger.md`](docs/pilot-evidence-ledger.md).
5. **Actionable Remediation:** Verified implementation report with 3 prioritized fixes in [`docs/pilot-implementation-report-brand-01.md`](docs/pilot-implementation-report-brand-01.md).
6. **Case Study Integrity:** Anti-fabrication template with strict placeholders in [`docs/pilot-case-study-template.md`](docs/pilot-case-study-template.md).
7. **Production Deployment Guide:** See [`docs/public-demo-deployment.md`](docs/public-demo-deployment.md).

---

## 👨‍💻 Founder & Portfolio

Built by **Syed Muslim Shah** as an evidence-first e-commerce measurement and verification portfolio project.  
- Portfolio: [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)  
- GitHub: [https://github.com/muslim-rashdi-ecom/commerce-truth-lab](https://github.com/muslim-rashdi-ecom/commerce-truth-lab)
