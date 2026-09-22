# Mutual Non-Disclosure & Data Confidentiality Agreement (NDA)
## Data Processing, Privacy & Retention Governance

**Document ID:** CTL-LEGAL-NDA-v1  
**Auditor / Service Provider:** Syed Muslim Shah, Operating as Commerce Truth Lab ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))  
**Client / Merchant:** ___________________________ ("Merchant")  
**Effective Date:** ___________________________  

---

### 1. Purpose of Agreement

This Mutual Non-Disclosure and Data Processing Agreement ("Agreement") governs the handling of business records, operational exports, and technical telemetry disclosed by Merchant to Commerce Truth Lab solely for executing the **"Shopify Measurement & Funnel Truth Sprint"** (the "Audit").

---

### 2. Strict Definition of Permitted Data & Zero-PII Standard

Both parties explicitly agree to adhere to a **Zero Personally Identifiable Information (Zero-PII)** disclosure policy:

> [!CAUTION] PROHIBITED DATA ELEMENTS — STRICT EXCLUSION
> The Merchant shall **NOT** provide, transmit, or disclose to Commerce Truth Lab any of the following data elements:
> 1. Customer full names, first names, or last names.
> 2. Customer personal email addresses or direct phone numbers.
> 3. Customer billing or shipping street addresses.
> 4. Credit card numbers, debit card numbers, CVVs, or bank account credentials.
> 5. Store admin passwords, staff account logins, or live platform API access tokens.
>
> Any files containing prohibited data elements will be immediately rejected and deleted without processing.

#### Permitted Data Elements:
Merchant shall only provide bounded, sanitized CSV exports consisting of:
- Order identifiers (e.g., `ORD_1001`), line item counts, order timestamps, and integer monetary totals.
- Gateway payment transaction tokens, capture timestamps, and captured amounts.
- Courier tracking airway bill (AWB) numbers, delivery timestamps, and courier remittance settlement amounts.
- Refund transaction tokens, refund timestamps, and refunded minor-unit totals.
- Ad platform purchase event IDs, server/browser signal timestamps, and reported conversion values.

---

### 3. Cryptographic Pseudonymization & Tenant Isolation

1. **Immediate Pseudonymization:** Any internal merchant customer IDs (e.g., `1001`) are processed through a cryptographic one-way salted hash (SHA-256) upon file ingestion, producing irreversible tokens (e.g., `CUST_7a8f...`).
2. **Multi-Tenant Isolation:** All ingested records and audit logs are assigned a unique, randomly generated `workspace_id`. PostgreSQL row-level security and schema isolation guarantee zero cross-merchant data leakage.

---

### 4. Data Retention & Mandatory Deletion Policy

1. **Active Audit Window:** Data is retained in the isolated workspace only for the duration of the audit sprint and post-fix re-verification period (maximum 30 calendar days).
2. **Mandatory 30-Day Purge:** Within **30 calendar days** following delivery of the final audit report, all uploaded CSV files, database records, and intermediate staging tables associated with the Merchant's `workspace_id` are permanently and irreversibly purged from all production servers and backups.
3. **Written Purge Confirmation:** Upon request, Commerce Truth Lab will issue a formal written Certificate of Data Destruction.

---

### 5. Confidentiality & Non-Disclosure Obligations

1. **Confidential Information:** All transactional records, sales volumes, average order values, courier contracts, and audit findings disclosed under this Agreement constitute proprietary Confidential Information of the Merchant.
2. **Standard of Care:** Commerce Truth Lab shall hold Merchant’s Confidential Information in strict confidence, applying industry-standard physical, technical, and administrative controls (TLS 1.3 in transit, AES-256 at rest, strict tenant separation).
3. **No Secondary Use:** Information disclosed shall never be used for commercial training of external generative AI models, marketing intelligence, or secondary commercial sale.

---

### 6. Separation of Pilot Execution and Case Study Consent

> [!IMPORTANT] CASE STUDY CONSENT IS STRICTLY OPTIONAL
> Merchant participation in the audit sprint does **NOT** obligate Merchant to consent to case studies, marketing testimonials, or public references. 
> 
> Any public attribution, anonymized benchmarking, or logo usage requires a separate, explicitly signed **Case Study Consent Release** (Option A or Option B). If Merchant declines or ignores the release, all audit records and merchant identity remain 100% confidential in perpetuity.

---

### 7. Signatures

By signing below, the parties agree to all terms and conditions set forth in this Agreement:

**For Merchant:**  
Authorized Signature: ________________________________  
Name: ________________________________  
Title: ________________________________  
Date: ________________________________  

**For Commerce Truth Lab:**  
Authorized Signature: ________________________________  
Name: Syed Muslim Shah  
Title: Lead Product Architect & Auditor  
Date: ________________________________  
