# Data Sources, Legal Provenance, and Licensing

**Commerce Truth Lab — Public Benchmark Validation Track**  
*Document Version: 1.0.0 &middot; Date: September 25, 2026*  
*Author: Syed Muslim Shah &middot; Portfolio: [syed-muslim-shah-portfolio.vercel.app](https://syed-muslim-shah-portfolio.vercel.app/)*

---

## Executive Summary & Non-Client Evidence Notice

> ⚠️ **STRICT NON-CLIENT EVIDENCE DECLARATION**  
> Public datasets utilized in this benchmark track are strictly for technical validation of the audit engine's arithmetic precision, rule logic, and data ingestion pipeline.  
> - **Not Client Proof:** None of these datasets represent private merchant pilot results or case studies.
> - **Zero Recovered Cash:** No recovered merchant revenue, cash dividends, or proven fraud is claimed.
> - **Unchanged Funnel:** The commercial pilot funnel for Commerce Truth Lab remains strictly at **0 contacted, 0 pilots, and 0 paid engagements** until real merchants authorize engagements.

---

## 1. Overview of Public Datasets

Commerce Truth Lab evaluates 4 primary public/composite data sources across 5 structured benchmark casebooks:

| Benchmark Case ID | Dataset Name | Primary Purpose | Original License | Classification |
|---|---|---|---|---|
| `bench-01-olist-reconciliation` | Brazilian E-Commerce Public Dataset by Olist | Order total vs. multi-part payment sequence reconciliation | CC BY-NC-SA 4.0 | `PUBLIC_BENCHMARK` |
| `bench-02-olist-logistics` | Brazilian E-Commerce Public Dataset by Olist | Handoff latency and delivery timestamp vs. estimated delivery SLA | CC BY-NC-SA 4.0 | `PUBLIC_BENCHMARK` |
| `bench-03-uci-cancellations` | UCI Online Retail Dataset | Negative invoice quantity cancellation matching | CC BY 4.0 | `PUBLIC_BENCHMARK` |
| `bench-04-criteo-ad-conversions` | Criteo Sponsored Search & Attribution Dataset | Ad click to conversion time lag & token verification | CC BY-NC-SA 3.0 | `PUBLIC_BENCHMARK` |
| `bench-05-composite-cod-signals` | Olist Base + Synthetic Companion Tables | Multi-table correlation across courier COD & Meta CAPI | Base: CC BY-NC-SA 4.0; Companion: MIT | `PUBLIC_PLUS_SYNTHETIC_COMPOSITE` |

---

## 2. Dataset-by-Dataset Provenance & Attribution

### 2.1 Brazilian E-Commerce Public Dataset by Olist
- **Publisher / Maintainer:** Olist & Kaggle community
- **Repository URL:** [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
- **Citation:** *Olist and Andre Sionek (2018). Brazilian E-Commerce Public Dataset by Olist. Kaggle.*
- **Scope & Fields Ingested:**
  - `orders`: `order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`.
  - `order_payments`: `order_id`, `payment_sequential`, `payment_type`, `payment_installments`, `payment_value`.
  - `order_items`: `order_id`, `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price`, `freight_value`.
- **Unavailable Telemetry in Public Data:**
  - Gateway interchange fee schedules and net settlement remittance slips.
  - Carrier contractual SLA penalty schedules.
  - Customer chargeback dispute documentation.
- **Transformations Applied:**
  - Conversion of Brazilian Real (BRL) floating-point currency to integer minor units (centavos: 1 BRL = 100 centavos) to eliminate floating-point arithmetic errors.
  - Multi-installment payment grouping per `order_id`.

---

### 2.2 UCI Online Retail Dataset (Cancellations Benchmark)
- **Publisher / Maintainer:** UCI Machine Learning Repository (Chen, D., Sain, S.L., & Guo, K.)
- **Repository URL:** [https://archive.ics.uci.edu/dataset/352/online+retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Citation:** *Chen, D., Sain, S. L., & Guo, K. (2012). Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining. Database Marketing & Customer Strategy Management, 19(3), 197-208.*
- **Scope & Fields Ingested:**
  - `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`.
- **Terminology & Categorization Guard:**
  - **Cancellations Only:** Invoices with a `'C'` prefix (e.g., `C536379`) with negative `Quantity` values are strictly classified as **invoice cancellations** or transaction reversals.
  - **Not Gateway Refunds:** Because the UCI dataset does not include merchant payment gateway capture/refund APIs or bank statements, these rows are never represented as verified gateway cash refunds.
- **Transformations Applied:**
  - Monetary values converted to minor units (GBP pence: 1 GBP = 100 pence) by multiplying integer quantity and unit price in pence.
  - Pairing cancellation lines against positive purchase invoices for the same `CustomerID` and `StockCode`.

---

### 2.3 Criteo Sponsored Search & Attribution Dataset
- **Publisher / Maintainer:** Criteo AI Lab
- **Repository URL:** [https://ailab.criteo.com/criteo-attribution-modeling-for-bidding-dataset/](https://ailab.criteo.com/criteo-attribution-modeling-for-bidding-dataset/)
- **License:** Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
- **Citation:** *Criteo AI Lab (2020). Attribution Modeling for Bidding Dataset.*
- **Scope & Fields Ingested:**
  - `sale_id`, `click_timestamp`, `conversion_timestamp`, `attribution_flag`, `conversion_value_minor`, `currency`.
- **Strict Isolation Guarantee:**
  - Ad click and conversion logs from Criteo are kept strictly in an independent advertising telemetry table.
  - **Never Merged:** Criteo ad logs are never merged or blended into Olist or UCI order tables as if they belonged to the same store. Cross-dataset attribution joins are explicitly forbidden.
- **Unavailable Telemetry:**
  - Merchant store cart items, customer contact records, and courier delivery scans.

---

### 2.4 Google Analytics Merchandise Store Demo Account
- **Governance & Policy:** Used strictly for manual exploratory research, schema documentation, and analytical understanding of GA4 event formatting (e.g. `purchase`, `view_item`, `add_to_cart`).
- **No Automated Scraping / No API Pulls:** No automated ingestion pipelines or credentials against the Google Analytics demo account are deployed.
- **No Implied Partnership:** Commerce Truth Lab explicitly asserts no commercial partnership, endorsement, or certification with Google LLC.

---

### 2.5 Public-Plus-Synthetic Composite Dataset (`bench-05-composite-cod-signals`)
- **Base Layer:** Real public Olist order identifiers, timestamps, and order values (CC BY-NC-SA 4.0).
- **Synthetic Companion Layer:** Companion courier Cash-on-Delivery (COD) remittance logs and Meta CAPI server-side event signals generated for testing.
- **Prominent Warning Requirement:**
  > *"Some source tables in this benchmark were generated for testing because the public dataset does not contain payment, refund, COD, or tracking-signal records."*
- **License of Synthetic Companion:** MIT License.

---

## 3. Data Integrity & PII Safeguards

All benchmark records committed or processed in Commerce Truth Lab comply with strict pseudonymization:
1. No raw customer names, phone numbers, or credit card PANs exist in public datasets.
2. Order IDs are retained or prefixed for traceable reproduction.
3. Raw database exports are tracked in `.gitignore` if containing multi-gigabyte files; sample verification subsets are housed deterministically in test fixtures.
