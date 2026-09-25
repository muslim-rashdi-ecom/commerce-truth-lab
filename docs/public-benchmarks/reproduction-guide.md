# Public Benchmark Reproduction Guide

**Commerce Truth Lab — Public Benchmark Validation Track**  
*Document Version: 1.0.0 &middot; Date: September 25, 2026*  
*Author: Syed Muslim Shah &middot; Portfolio: [syed-muslim-shah-portfolio.vercel.app](https://syed-muslim-shah-portfolio.vercel.app/)*

---

## 1. Prerequisites

To execute and independently reproduce all public benchmark validations:
- **Python:** 3.12+ (tested on Python 3.14.5)
- **Node.js:** 20+
- **Operating System:** Windows, macOS, or Linux
- **Dependencies:** All backend dependencies installed via `apps/api/requirements.txt`.

---

## 2. Running Automated Benchmark Tests via Pytest

Commerce Truth Lab ships with a complete test suite under `tests/api/test_benchmarks.py` covering all 5 public benchmark casebooks.

### 2.1 Run the Full Public Benchmark Test Suite
From the repository root (`commerce-truth-lab-v1`):

```bash
python -m pytest tests/api/test_benchmarks.py -v
```

Expected output: **17 passed** benchmark assertions verifying provenance, classification tags, composite warning banners, non-claims, and multi-format report exports.

### 2.2 Run Specific Benchmark Casebooks

#### Case 1: Olist Payment & Order Gross Reconciliation
```bash
python -m pytest tests/api/test_benchmarks.py -k test_bench_01_olist -v
```

#### Case 2: Olist Logistics Delay Analysis
```bash
python -m pytest tests/api/test_benchmarks.py -k test_bench_02_logistics -v
```

#### Case 3: UCI Online Retail Cancellations Benchmark
```bash
python -m pytest tests/api/test_benchmarks.py -k test_bench_03_uci -v
```

#### Case 4: Criteo Sponsored Search & Attribution Timing
```bash
python -m pytest tests/api/test_benchmarks.py -k test_bench_04_criteo -v
```

#### Case 5: Public-Plus-Synthetic Composite (COD & CAPI)
```bash
python -m pytest tests/api/test_benchmarks.py -k test_bench_05_composite -v
```

### 2.3 Run the Entire System Test Suite
To verify that benchmark additions did not affect core engine rules, private workspace endpoints, or synthetic demo routes:

```bash
python -m pytest tests/ -v
```

Expected result: **70 passed, 0 failed**.

---

## 3. Interacting via FastAPI REST Endpoints

Start the API server locally:
```bash
uvicorn apps.api.main:app --reload --port 8000
```

Verify endpoints via `curl` or browser:

### 3.1 List All Benchmarks
```bash
curl -s http://localhost:8000/api/benchmarks | jq .
```

### 3.2 Fetch Benchmark Detail (e.g. Olist Reconciliation)
```bash
curl -s http://localhost:8000/api/benchmarks/bench-01-olist-reconciliation | jq .
```

### 3.3 Download Exported Reports
- **HTML Report:**
  ```bash
  curl -s http://localhost:8000/api/benchmarks/bench-01-olist-reconciliation/reports/html > olist_report.html
  ```
- **Markdown Report:**
  ```bash
  curl -s http://localhost:8000/api/benchmarks/bench-01-olist-reconciliation/reports/markdown > olist_report.md
  ```
- **JSON Structured Data:**
  ```bash
  curl -s http://localhost:8000/api/benchmarks/bench-01-olist-reconciliation/reports/json > olist_report.json
  ```

---

## 4. Viewing via Web Interface

Start the frontend development server:
```bash
cd apps/web
npm run dev
```

Navigate to:
- **Benchmark Casebook Explorer:** `http://localhost:5173/benchmarks`
- **Direct Casebook Deep Link:** `http://localhost:5173/benchmarks/bench-05-composite-cod-signals`
