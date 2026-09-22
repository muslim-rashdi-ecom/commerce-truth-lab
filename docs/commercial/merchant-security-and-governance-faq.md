# Merchant Security, Data Governance & Operational FAQ
## Enterprise Data Handling Guide for Shopify & DTC Operators

**Product:** Commerce Truth Lab v1  
**Lead Architect & Auditor:** Syed Muslim Shah ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))  
**Governance Standard:** Zero Plaintext PII, Isolated Workspaces, Deterministic Audit Rules, 30-Day Mandatory Purge.

---

### 1. Merchant Security FAQ

#### Q1: Why do you not use a live Shopify App or ask for API keys?
**Answer:** Requesting live API keys or installing unvetted apps introduces supply chain risk and creates persistent third-party access to your production store. Commerce Truth Lab is an investigative audit tool, not a continuous integration or background worker. We run on bounded historical CSV exports (e.g., a 30-day cohort) so your live store infrastructure remains completely untouched and isolated.

#### Q2: What exact customer personal information (PII) do you see?
**Answer:** **None.** You delete all name, phone, email, and address columns before uploading. If an internal customer ID (e.g., Shopify customer number `CUST_1001`) is included in the export, our ingestion pipeline immediately applies a cryptographically salted SHA-256 hash before writing to the database. The original identifier cannot be reconstructed.

#### Q3: Where is our audit data hosted and who can see it?
**Answer:** Audit data is ingested into an isolated PostgreSQL tenant schema with composite primary keys (`workspace_id`, `id`) and strict JWT-based tenant authentication. No other merchant, guest, or public user can access your workspace. Only the lead auditor (Syed Muslim Shah) accesses the isolated environment during the active audit window.

#### Q4: How long is our data retained?
**Answer:** All uploaded CSV files, temporary tables, and tenant database records are permanently deleted **30 calendar days** after the final report delivery. A formal Certificate of Destruction is available upon request.

#### Q5: Is case-study permission required to get the audit?
**Answer:** **No.** Case-study consent is 100% optional, separate, and handled via an independent form. Declining case-study publication has zero effect on your audit deliverables, turnaround, or support.

---

### 2. Pre-Upload PII Minimization Checklist

Before transmitting any CSV export, verify each item on this checklist:

| Check | Export Column Category | Required Action Before Upload | Verification |
|:---:|---|---|:---:|
| 1 | **Customer Names** | Delete all columns titled `First Name`, `Last Name`, `Customer Name`, `Recipient Name`. | [ ] Confirmed |
| 2 | **Customer Contact Info** | Delete all columns titled `Email`, `Phone`, `Mobile Number`, `Customer Phone`. | [ ] Confirmed |
| 3 | **Customer Addresses** | Delete all columns titled `Shipping Address`, `Billing Address`, `Street Address`, `Postal Code`, `City`. | [ ] Confirmed |
| 4 | **Payment Card Data** | Verify that no credit card numbers, CVVs, expiration dates, or bank account numbers are present. | [ ] Confirmed |
| 5 | **Credentials & Secrets** | Ensure no passwords, API tokens, webhook secrets, or private keys are pasted into any notes or metadata columns. | [ ] Confirmed |
| 6 | **Monetary Precision** | Verify that currency columns specify standard ISO codes (e.g., `AED`, `USD`, `EUR`, `GBP`, `JPY`, `KWD`, `PKR`). | [ ] Confirmed |

---

### 3. Secure Data-Upload Instructions

Once files have passed the PII Minimization Checklist:

1. **Step 1: File Preparation:** Ensure your exports are saved in standard UTF-8 `.csv` format:
   - `shopify_orders_sanitized.csv`
   - `payment_gateway_captures.csv`
   - `courier_cod_settlements.csv` (if applicable)
   - `refunds_adjustments.csv` (if applicable)
   - `ad_platform_signals.csv` (Meta CAPI / GA4 logs, if available)
2. **Step 2: Secure Delivery:**
   - **Method A (Direct Isolated Upload):** Use the authenticated single-tenant upload page at `https://commerce-truth-lab.vercel.app/login` with your assigned private pilot credentials.
   - **Method B (Encrypted Transfer):** Transmit via password-protected ZIP or end-to-end encrypted link (e.g., Tresorit, ProtonDrive, or WeTransfer Encrypted) directly to the lead auditor.
3. **Step 3: Receipt Validation:** The auditor validates file headers and schema within 4 business hours and sends an email receipt confirming that zero PII was detected.

---

### 4. Report-Delivery Checklist

Before the completed forensic report is presented to the merchant, the auditor verifies:

- [ ] All 12 audit rules (`CTL-001` through `CTL-012`) have executed without unhandled errors.
- [ ] Every investigative finding links to an exact record identifier in the evidence reference ledger.
- [ ] All monetary discrepancies are calculated using integer minor-unit arithmetic without floating-point rounding errors.
- [ ] At least three prioritized fixes are formulated (`P0` Critical, `P1` High, `P2` Operational) with clear role assignments (Engineering, Media Buying, Operations).
- [ ] The report explicitly details healthy controls (checks where zero discrepancies were found).
- [ ] The report explicitly states operational limitations and what is **NOT** proven (no unsupported claims of fraud or recovered revenue).
- [ ] Report formats are generated in HTML, Markdown, and JSON.

---

### 5. Invoice & Payment Workflow

*For paid engagements, follow-up sprints, and monitoring retainers:*

1. **Invoicing Standard:** Invoices are issued electronically through Stripe Invoicing or bank wire transfer in USD or AED.
2. **Payment Schedule:**
   - **Fixed-Price Sprints:** 50% upon SOW execution; 50% upon final report delivery.
   - **Validation Pilots:** $0 setup fee; billed only for agreed optional custom engineering scope.
   - **Quarterly Monitoring Retainers:** Billed monthly in advance on the 1st calendar day.
3. **Payment Gateways Supported:** Major credit cards (Visa, Mastercard, Amex), ACH transfer, SEPA, and UAE local bank wire.

---

### 6. Discovery-Call Booking Instructions

To schedule an initial 15–20 minute diagnostic session:

1. **Calendar Link:** Connect directly via Syed Muslim Shah’s booking link or email request at:
   - **Founder Portfolio & Contact:** [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)
   - **Direct Email:** `syedmuslimshah@gmail.com` (or LinkedIn Direct Message)
2. **Call Preparation:** No technical preparation is needed from the merchant. Come prepared to share:
   - Store platform (Shopify or Shopify Plus)
   - Estimated monthly order volume
   - Current advertising channels (Meta, Google, TikTok)
   - Primary operational questions (e.g., courier COD remittance lag, CAPI deduplication, or currency drift)
