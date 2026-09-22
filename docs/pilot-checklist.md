# Merchant Pilot Authorization & Readiness Checklist

## Shopify Measurement & Funnel Truth Sprint

This checklist governs the secure onboarding and execution of an evidence-first audit sprint for Shopify brands using Commerce Truth Lab v1.

---

### Phase 1: Authorization & Legal Governance
- [ ] **1.1 Data-Sharing Authorization Signed**  
  Mutual data processing agreement executed confirming audit purpose, non-disclosure terms, and authorized recipients.
- [ ] **1.2 Anti-Hype & Non-Claim Alignment**  
  Merchant acknowledges that Commerce Truth Lab outputs deterministic record discrepancies and does NOT claim automated fraud detection, causal ROAS increases, or recovered revenue.
- [ ] **1.3 Data Retention & Deletion Schedule**  
  Merchant specifies data retention policy (default: 30 days post-sprint with complete workspace purge).
- [ ] **1.4 Point of Contact Designation**  
  Designated merchant owners identified for Paid Media, Operations/Fulfillment, and Finance/Reconciliation.

---

### Phase 2: Technical Preparation & Data Sanitization
- [ ] **2.1 Plaintext PII Zero-Storage Policy**  
  Ensure customer names, physical addresses, phone numbers, and raw email addresses are salted and hashed (`CUST_<hash>`) prior to or during CSV upload staging.
- [ ] **2.2 Currency Configuration Confirmation**  
  Identify store base checkout currencies and presentment currencies (e.g. USD, AED, JPY, KWD, PKR, GBP, EUR) to configure minor-unit integer precision.
- [ ] **2.3 Courier COD Grace Period Confirmation**  
  Define merchant's contractual courier remittance settlement grace period in days (e.g. 7 days or 14 days) for CTL-005 evaluation.
- [ ] **2.4 CSV Export Verification Against Sample Templates**  
  Confirm uploaded files align with schemas in [`docs/sample-csv-templates/`](sample-csv-templates/):
  - `shopify_orders_sample.csv` (Order IDs, timestamps, amounts, payment methods, fulfillment status)
  - `payments_sample.csv` (Payment gateway transaction captures, fees, payout statuses)
  - `cod_settlements_sample.csv` (Airway bill delivery dates, courier collections, settled remittances)
  - `refunds_sample.csv` (Refund transactions, timestamps, reasons, amounts)
  - `purchase_signals_sample.csv` (Meta Pixel / CAPI / Google Ads conversion events with `event_id`)

---

### Phase 3: Tenant Isolation & Workspace Execution
- [ ] **3.1 Dedicated Workspace Provisioning**  
  Create an isolated merchant workspace (`workspace_id`) in PostgreSQL with composite primary keys preventing cross-tenant access.
- [ ] **3.2 CSV Formula Injection Neutralization**  
  Verify file upload passes CWE-1236 sanitization (`=`, `+`, `-`, `@` characters prefixed with single quotes in CSV rows).
- [ ] **3.3 Column Mapping Review**  
  Merchant or lead auditor confirms detected headers and column mappings prior to committing staged records.
- [ ] **3.4 Audit Engine Run (CTL-001 through CTL-012)**  
  Execute deterministic audit engine run asynchronously or on backend API. Ensure zero execution errors.

---

### Phase 4: Truth Briefing Delivery & Verification
- [ ] **4.1 Evidence Integrity Audit**  
  Confirm every flagged exception links directly to source transaction IDs with explicit "What Is Observed" and "What Is NOT Proven" notes.
- [ ] **4.2 Healthy Control Verification**  
  Confirm that clean orders (zero-discrepancy refunds, within-grace COD, synchronized event IDs) are logged as verified controls.
- [ ] **4.3 Export Deliverables Generated**  
  Generate deliverables following [`docs/implementation-report-template.md`](implementation-report-template.md):
  - Standalone HTML executive report for stakeholder briefing
  - Machine-readable JSON export for analytics ingestion
  - Markdown briefing for internal engineering wikis and issue tracking
- [ ] **4.4 Action Item Hand-off**  
  Deliver prioritized recommendations to Media, Ops, and Finance teams.
- [ ] **4.5 Workspace Archival or Scheduled Purge**  
  Confirm workspace retention expiration or execute purge per agreed terms.
