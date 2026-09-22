# Merchant Onboarding & Data Export Guide
## Preparing Your Data for Commerce Truth Lab

This practical guide assists merchant operations, finance, and technical teams in extracting the five operational data streams required for the **Shopify Measurement & Funnel Truth Sprint**.

---

## 🔒 Golden Privacy Rule: No Plaintext Customer PII

**Do NOT export or upload customer personal information:**
- Exclude: Customer Full Name, Physical Street Address, Mobile/Phone Number, Credit Card Number.
- Include: Numeric Order ID, Timestamp, Currency, Item Total, Salted Customer ID (or email handle to be hashed upon upload).

All values are processed using cryptographic SHA-256 salting (`PSEUDONYMIZATION_SALT`). Raw identifiers never touch production database tables.

---

## 1. Shopify Orders Export

### How to Export from Shopify Admin:
1. Navigate to **Shopify Admin** $\rightarrow$ **Orders**.
2. Click **Export** in the top right corner.
3. Select **Orders by date** and enter the agreed 30-day audit range (e.g. `2026-08-01` to `2026-08-31`).
4. Select **Export as CSV (for Excel, Numbers, or other spreadsheet programs)**.
5. Click **Export orders**.

### Required Columns in Final File:
- `Name` or `Order ID` (e.g. `#10492` or `ORD-10492`)
- `Created at` (ISO timestamp)
- `Financial Status` (`paid`, `pending`, `partially_refunded`, `refunded`)
- `Fulfillment Status` (`fulfilled`, `unfulfilled`, `delivered`)
- `Total` (Gross order amount)
- `Currency` (3-letter ISO code, e.g. `USD`, `AED`, `EUR`)

---

## 2. Payment Gateway Captures (Stripe, PayPal, Tabby, Tamara)

### How to Export from Stripe Dashboard:
1. Navigate to **Stripe Dashboard** $\rightarrow$ **Payments**.
2. Filter by status: **Succeeded**.
3. Set the date range to match your Shopify order cohort.
4. Click **Export** $\rightarrow$ select **All columns** $\rightarrow$ Download CSV.

### Required Columns:
- `Payment ID` or `Charge ID` (`ch_xxx` or `pi_xxx`)
- `Description` or `Metadata: order_id` (Crucial for 1:1 order reconciliation)
- `Amount`
- `Currency`
- `Created (UTC)`

---

## 3. Courier COD Settlement Remittances (Aramex, Fetchr, DHL, etc.)

### How to Export from Courier Portal:
1. Log into your courier corporate portal (e.g. Aramex Click, DHL Corporate, Shipa).
2. Navigate to **COD Statements** or **Remittance Reports**.
3. Download the settlement statement CSV covering the audit date range.

### Required Columns:
- `Airway Bill (AWB)` / Tracking Number
- `Reference Number` / Merchant Order ID
- `Delivery Date` / Delivered Timestamp
- `Collected COD Amount`
- `Settled / Remitted Amount`
- `Settlement Status` (`settled`, `pending`, `transferred`)

---

## 4. Shopify Refunds Export

### How to Export:
1. Navigate to **Shopify Admin** $\rightarrow$ **Analytics** $\rightarrow$ **Reports** $\rightarrow$ **Finances: Returns / Refunds**.
2. Set the date range to match the audit window + 14 days (to capture post-order returns).
3. Export CSV.

### Required Columns:
- `Refund ID` or Order Reference
- `Order ID`
- `Date`
- `Refund Amount`
- `Currency`

---

## 5. Marketing Purchase Signals (Meta Events Manager & GA4)

### How to Export from Meta Events Manager:
1. Go to **Meta Events Manager** $\rightarrow$ Select your **Pixel / Dataset**.
2. Click **Purchase** event $\rightarrow$ **View Details**.
3. Under the **Recent Activity** / **Diagnostics** tab, download event sample CSV or export diagnostic log.
4. If using an automated webhook logger, export the payload stream including `event_name`, `event_id`, and `value`.

### Required Columns:
- `Event ID` (The deduplication token)
- `Order ID` / Order Reference
- `Signal Type` (`browser` or `server`)
- `Event Time` (Unix timestamp or ISO-8601)
- `Value`
- `Currency`

---

## 6. Uploading to Commerce Truth Lab

1. Log into your private workspace at `https://commerce-truth-lab.vercel.app/workspace/login`.
2. Select your provisioned workspace.
3. Click **Stage CSV Upload** for each stream.
4. Review the auto-detected column mappings and data quality warnings.
5. Click **Commit Upload** to finalize ingestion.
