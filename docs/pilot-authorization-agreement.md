# Shopify Measurement & Funnel Truth Sprint
## Data Processing & Audit Authorization Agreement

This Data Processing & Audit Authorization Agreement ("Agreement") is executed between:

1. **Merchant / Client:**  
   Company Name: `________________________________________________`  
   Store Domain(s): `________________________________________________`  
   Authorized Representative: `________________________________________________`  
   Title: `________________________________________________`  
   Contact Email: `________________________________________________`  

2. **Lead Auditor & Service Provider:**  
   Syed Muslim Shah  
   Commerce Truth Lab v1  
   Portfolio: [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)  
   Repository: [https://github.com/muslim-rashdi-ecom/commerce-truth-lab](https://github.com/muslim-rashdi-ecom/commerce-truth-lab)  

---

### 1. Purpose of the Audit Sprint
The Merchant authorizes Commerce Truth Lab to perform an offline, evidence-first data reconciliation sprint ("Shopify Measurement & Funnel Truth Sprint") to evaluate consistency across:
- Store orders registered in Shopify
- Payment gateway captures (e.g. Stripe, Shopify Payments, PayPal)
- Courier Cash on Delivery (COD) settlement records (if applicable)
- Customer refunds and returns
- Marketing tracking signals (Meta Pixel, Meta Conversions API, GA4)

---

### 2. Audit Scope & Target Windows
- **Audit Date Range:** From `[ YYYY-MM-DD ]` to `[ YYYY-MM-DD ]`
- **Authorized Stores / Channels:** `________________________________________`
- **Authorized Currencies:** `[ e.g. USD, AED, EUR, GBP ]`
- **Courier Remittance Grace Period:** `[ 7 / 14 ]` calendar days from delivery

---

### 3. Customer Privacy & Zero-Plaintext-PII Policy
1. **No Plaintext PII Storage:** Commerce Truth Lab strictly enforces a zero-plaintext-PII architecture. The Merchant agrees that files uploaded will NOT contain unmasked customer credit card numbers, national IDs, or passwords.
2. **Deterministic Pseudonymization:** During file ingestion, all customer identifiers (emails, phone numbers, customer IDs) are immediately hashed using a cryptographically salted SHA-256 algorithm (`CUST_<hash>`).
3. **No Third-Party Sharing:** Merchant data is never shared with, sold to, or processed by third-party AI/LLM models or external brokers.

---

### 4. Multi-Tenant Isolation & Workspace Security
1. **Tenant Separation:** All Merchant data resides within an isolated workspace container keyed by a unique `workspace_id`. Cross-tenant querying is forbidden by composite database constraints.
2. **Access Control:** Workspace access is restricted strictly to authenticated Merchant users and the assigned Lead Auditor via JWT session tokens.
3. **Formula Injection Defense:** Uploaded files undergo automated CWE-1236 sanitization to prevent command execution when reports are opened in spreadsheet software.

---

### 5. Anti-Hype & Non-Claim Principles
Both parties agree to the fundamental operating principles of Commerce Truth Lab:
- **No Speculative Fraud Claims:** Identified discrepancies indicate record non-alignment, not legal proof of fraud or theft.
- **No Recovered Revenue Guarantees:** Discrepancy totals indicate unverified capital flows, not guaranteed recoverable cash.
- **No Causal ROAS Claims:** Pixel and CAPI gaps demonstrate event delivery and deduplication defects, not marketing performance causality.
- **Strict Evidence Boundaries:** Every finding explicitly notes what is observed, what assumptions were applied, what is NOT proven, and recommended next steps.

---

### 6. Deliverables
Upon sprint completion, the Merchant will receive:
1. **Interactive HTML Audit Report:** Standalone executive briefing detailing all findings, healthy controls, and methodology.
2. **Structured JSON Export:** Complete, machine-readable dataset of findings with integer minor-unit amounts and evidence pointers.
3. **Markdown Engineering Briefing:** Actionable markdown file formatted for GitHub issues, Jira, or engineering wikis with three prioritized fixes (P0, P1, P2).

---

### 7. Data Retention & Deletion Schedule
- **Default Retention:** All ingested data, staged tables, and audit logs will be permanently deleted **30 calendar days** following sprint report delivery.
- **Early Deletion:** The Merchant may request immediate workspace purging at any time via written notice.
- **Purge Confirmation:** Lead Auditor will furnish written confirmation upon database row purging.

---

### 8. Case Study & Portfolio Publication Consent
Please select one option regarding sprint findings and outcomes:

- [ ] **Option A (Full Attribution):** Commerce Truth Lab may publish an evidence-linked case study mentioning the brand name and verified findings.
- [ ] **Option B (Pseudonymized / Anonymized):** Commerce Truth Lab may publish a case study using an industry pseudonym (e.g. "DTC Lifestyle Brand") with all identifying brand markers removed.
- [ ] **Option C (Strictly Confidential):** All findings and data are confidential. No case study or public mention will be produced.

---

### Authorized Signatures

**For the Merchant:**  
Signature: `______________________________________`  
Printed Name: `______________________________________`  
Title: `______________________________________`  
Date: `____________________`  

**For Commerce Truth Lab:**  
Signature: `______________________________________`  
Printed Name: Syed Muslim Shah  
Title: Lead Product Architect & Auditor  
Date: `____________________`  
