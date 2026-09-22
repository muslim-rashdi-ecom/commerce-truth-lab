# Statement of Work & Engagement Proposal
## Service: Shopify Measurement & Funnel Truth Sprint

**Proposal Date:** `[DATE]`  
**Proposal Reference:** `SOW-CTL-[YYYY]-[BRAND_ID]`  
**Client:** `[CLIENT_LEGAL_NAME]` ("Client")  
**Brand / URL:** `[STORE_NAME]` (`[STORE_URL]`)  
**Lead Auditor / Service Provider:** Syed Muslim Shah, Lead Product Architect, Commerce Truth Lab ("Provider")  
**Contact:** `[AUDITOR_EMAIL]` | [Portfolio](https://syed-muslim-shah-portfolio.vercel.app/)  

---

## 1. Engagement Overview

The **Shopify Measurement & Funnel Truth Sprint** is a rapid, 48-hour forensic reconciliation audit. It determines whether four critical commercial facts agree across Client's e-commerce operations:

1. **What your store recorded:** Shopify Plus / Shopify store checkout orders.
2. **What your gateways captured:** Stripe, PayPal, Tabby, or bank transfer deposits.
3. **What your couriers remitted:** Cash on Delivery (COD) physical cash collections vs bank settlement disbursements.
4. **What your ad platforms counted:** Meta Pixel, Conversions API (CAPI), and Google Analytics 4 purchase signals.

---

## 2. Scope of Services & Ingested Streams

Provider will ingest and analyze a bounded 30-day cohort of operational data:

- **Audit Date Cohort:** From `[START_DATE]` (00:00 UTC) to `[END_DATE]` (23:59 UTC).
- **Core Streams Ingested:**
  - `shopify_orders`: Order ID, timestamp, currency, total amount, status, customer token.
  - `payments`: Transaction capture ID, order ID, currency, amount, gateway, capture timestamp.
  - `courier_settlements`: Airway bill number, order ID, delivery timestamp, collected amount, settled amount.
  - `refunds`: Refund ID, order ID, currency, refunded amount, timestamp.
  - `purchase_signals`: Event ID, order ID, signal type (pixel/CAPI), reported value, timestamp.

---

## 3. Deliverables & Turnaround SLA

Provider agrees to deliver the following items within **48 hours** of receiving sanitized CSV files:

| Milestone | Deliverable Description | Delivery Format | SLA Timeline |
|---|---|---|---|
| **Phase 1** | Ingestion confirmation, schema review, and salted pseudonymization | Email / Portal | T + 6 Hours |
| **Phase 2** | Comprehensive Forensic Implementation Report: <ul><li>Empirical findings with exact evidence pointers</li><li>Verified healthy control transactions</li><li>**Three Prioritized Remediations (P0, P1, P2)**</li></ul> | Standalone HTML, Markdown, and JSON | **T + 48 Hours** |
| **Phase 3** | 45-Minute Executive Walkthrough with technical and operational leads | Video Conference | Scheduled at Client convenience |
| **Phase 4** | Follow-Up Verification Audit on 7-day post-fix cohort to measure reconciliation deltas | Updated Verification Report | 14 Days post-walkthrough |

---

## 4. Client Privacy & Data Governance

1. **Zero Plaintext Customer PII:** Client agrees to export data without plaintext customer names, phone numbers, or physical street addresses. Any identifiers ingested are salted with cryptographic SHA-256 hashes prior to database persistence.
2. **Tenant Isolation:** Client data resides in an isolated private workspace accessible solely by Client and Provider.
3. **30-Day Mandatory Deletion Schedule:** All uploaded CSV files, intermediate hashes, and workspace records are permanently purged 30 calendar days following report delivery.

---

## 5. Commercial Terms & Investment

- **Selected Sprint Package:** `[Tier 1: Core ($1,250) | Tier 2: Multi-Stream ($2,450) | Tier 3: Enterprise ($3,850)]`
- **Total Fixed Investment:** `$ [AMOUNT] USD`
- **Payment Structure:** 50% upon execution of this Statement of Work; 50% upon delivery of the Phase 2 Forensic Implementation Report.
- **Contingency Disclaimer:** Provider charges zero percentage-of-recovery fees. Deliverables represent objective forensic reconciliation findings and engineering remediation plans.

---

## 6. Execution & Acceptance

By signing below, the parties agree to the terms, scopes, and data governance standards outlined in this Statement of Work and the attached [`docs/pilot-authorization-agreement.md`](../pilot-authorization-agreement.md).

**For Client (`[CLIENT_LEGAL_NAME]`):**

Name: ___________________________  
Title: ____________________________  
Signature: ________________________  
Date: ____________________________  

**For Provider (Commerce Truth Lab):**

Name: Syed Muslim Shah  
Title: Lead Product Architect  
Signature: ________________________  
Date: ____________________________  
