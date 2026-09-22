# Pilot Ingestion Data Contract & Input Specifications

**Commerce Truth Lab v1 — Audit Engine Ingestion Standard**  
**Version:** 1.0 (Deterministic Rules CTL-001 through CTL-012)  

---

## 1. Overview of Required Data Streams

To conduct a comprehensive "Shopify Measurement & Funnel Truth Sprint", merchants provide up to **five standardized CSV exports**. Each stream represents an independent factual observation in the commerce lifecycle:

```
[ Shopify Store Orders ] ──┬── [ Payment Gateway Captures ]
                           ├── [ Courier COD Settlements ]
                           ├── [ Customer Refunds ]
                           └── [ Meta / GA4 Tracking Signals ]
```

---

## 2. Stream Specifications & Accepted Column Mappings

### Stream 1: Shopify Store Orders (`shopify_orders`)
The baseline commercial record of customer checkout commitments.

| Canonical Field | Required? | Accepted CSV Column Synonyms | Expected Data Type | Example Value |
|---|---|---|---|---|
| `order_id` | **Yes** | `Order ID`, `Name`, `order_name`, `id` | String | `ORD-10492` or `#10492` |
| `created_at` | **Yes** | `Created at`, `created_date`, `order_date` | ISO 8601 or UTC Date | `2026-08-15T14:30:00Z` |
| `currency` | **Yes** | `Currency`, `order_currency`, `currency_code` | ISO 4217 (3-letter) | `USD`, `AED`, `EUR` |
| `total_amount` | **Yes** | `Total`, `total_price`, `order_total` | Decimal or Integer | `129.50` or `12950` |
| `payment_method`| **Yes** | `Payment Method`, `gateway`, `payment_type` | String (`prepaid` / `cod`) | `prepaid`, `cod`, `credit_card` |
| `fulfillment_status`| No | `Fulfillment Status`, `status`, `delivery_status` | String | `fulfilled`, `delivered`, `pending` |
| `customer_identifier`| No | `Customer ID`, `Email`, `phone`, `customer_id` | String (Masked on upload) | `CUST_7f8a9b1c2d3e4f50` |

---

### Stream 2: Payment Gateway Captures (`payments`)
Independent proof of funds collected from card processors or wallets (e.g. Stripe, Shopify Payments, Checkout.com, PayPal).

| Canonical Field | Required? | Accepted CSV Column Synonyms | Expected Data Type | Example Value |
|---|---|---|---|---|
| `payment_id` | **Yes** | `Payment ID`, `Transaction ID`, `charge_id`, `id` | String | `ch_3M4k92e` or `TXN-8829` |
| `order_id` | **Yes** | `Order ID`, `Description`, `metadata.order_id` | String | `ORD-10492` or `#10492` |
| `captured_at` | **Yes** | `Created (UTC)`, `captured_at`, `timestamp` | ISO 8601 or UTC Date | `2026-08-15T14:31:12Z` |
| `amount` | **Yes** | `Amount`, `captured_amount`, `gross_amount` | Decimal or Integer | `129.50` |
| `currency` | **Yes** | `Currency`, `currency_code` | ISO 4217 (3-letter) | `USD` |
| `gateway` | No | `Gateway`, `processor`, `source` | String | `stripe`, `shopify_payments` |
| `status` | No | `Status`, `charge_status` | String | `captured`, `succeeded` |

---

### Stream 3: Courier COD Settlements (`courier_settlements`)
Courier delivery records and remittance files for Cash on Delivery orders (e.g. Aramex, DHL, FedEx, TCS).

| Canonical Field | Required? | Accepted CSV Column Synonyms | Expected Data Type | Example Value |
|---|---|---|---|---|
| `settlement_id` | **Yes** | `Settlement ID`, `Remittance ID`, `Airway Bill`, `AWB` | String | `AWB-98127391` |
| `order_id` | **Yes** | `Reference ID`, `Order Number`, `order_id` | String | `ORD-10492` |
| `courier_name` | No | `Courier`, `Carrier`, `vendor` | String | `Aramex`, `DHL Express` |
| `delivered_at` | **Yes** | `Delivery Date`, `delivered_time`, `pod_date` | ISO 8601 or UTC Date | `2026-08-18T10:15:00Z` |
| `collected_amount`| **Yes** | `Collected Amount`, `cash_collected`, `cod_value` | Decimal or Integer | `250.00` |
| `settled_amount` | No | `Settled Amount`, `net_remittance`, `remitted_value`| Decimal or Integer | `250.00` (Empty if pending) |
| `collection_currency`| **Yes** | `Currency`, `cod_currency` | ISO 4217 (3-letter) | `AED` |
| `settlement_status`| No | `Status`, `settlement_state` | String (`settled`/`pending`) | `settled`, `pending` |
| `grace_days` | No | `Grace Days`, `payment_terms_days` | Integer (Default: 7) | `7` or `14` |

---

### Stream 4: Customer Refunds & Returns (`refunds`)
Records of refunds issued through Shopify, gateways, or customer service adjustments.

| Canonical Field | Required? | Accepted CSV Column Synonyms | Expected Data Type | Example Value |
|---|---|---|---|---|
| `refund_id` | **Yes** | `Refund ID`, `return_id`, `id` | String | `REF-38910` |
| `order_id` | **Yes** | `Order ID`, `order_name`, `reference` | String | `ORD-10492` |
| `refunded_at` | **Yes** | `Refunded at`, `created_at`, `timestamp` | ISO 8601 or UTC Date | `2026-08-20T16:00:00Z` |
| `amount` | **Yes** | `Amount`, `refund_amount`, `subtotal` | Decimal or Integer | `129.50` |
| `currency` | **Yes** | `Currency`, `currency_code` | ISO 4217 (3-letter) | `USD` |
| `reason` | No | `Reason`, `note`, `adjustment_reason` | String | `defective`, `customer_return` |

---

### Stream 5: Marketing Tracking Signals (`purchase_signals`)
Ad platform event logs from Meta Pixel, Meta Conversions API (CAPI), Google Analytics 4 (GA4), or Google Ads.

| Canonical Field | Required? | Accepted CSV Column Synonyms | Expected Data Type | Example Value |
|---|---|---|---|---|
| `signal_id` | **Yes** | `Event ID`, `signal_id`, `transaction_id` | String | `SIG-9921` |
| `order_id` | **Yes** | `Order ID`, `external_id`, `content_name` | String | `ORD-10492` |
| `platform` | **Yes** | `Platform`, `source`, `channel` | String | `meta_browser`, `meta_capi`, `ga4` |
| `event_name` | No | `Event Name`, `event_type` | String (Default: `Purchase`) | `Purchase`, `purchase` |
| `event_id` | **Yes** | `Deduplication ID`, `event_id`, `match_key` | String | `EVT-ORD-10492` |
| `reported_at` | **Yes** | `Event Time`, `timestamp`, `date` | ISO 8601 or UTC Date | `2026-08-15T14:30:18Z` |
| `currency` | **Yes** | `Currency`, `currency_code` | ISO 4217 (3-letter) | `USD` |
| `value` | **Yes** | `Value`, `event_value`, `revenue` | Decimal or Integer | `129.50` |
| `consent_granted`| No | `Consent`, `gdpr_consent`, `opt_in` | Boolean (`true`/`false`) | `true` |

---

## 3. Unsupported Formats & Data Exclusions

The following formats and structures are **explicitly unsupported** and will be rejected at ingestion:
1. **Nested JSON / NDJSON:** Data must be normalized into flat tabular CSV.
2. **Proprietary Binary Formats:** Excel `.xlsx`, `.xls`, `.parquet`, or `.feather` files must be exported to standard UTF-8 `.csv`.
3. **Password-Protected / Encrypted CSVs:** Encryption must be removed prior to upload.
4. **Files Exceeding 25 MB:** Large multi-year files should be split into monthly or quarterly batches.
5. **PDF Invoices / Courier Scans:** Only machine-readable tabular CSV exports are supported.

---

## 4. Missing-Data & Missing-Stream Behavior

Commerce Truth Lab operates with explicit evidentiary completeness checks:

1. **Missing Courier Settlement File (COD Store):**  
   If an order is marked with `payment_method = 'COD'` and `status = 'delivered'`, but no corresponding courier settlement file is provided, rule **CTL-009 (Incomplete Evidence Coverage)** triggers. It is flagged as an *unverified cash state*, NOT assumed to be lost or stolen.
2. **Missing Marketing Tracking Stream:**  
   If no pixel or CAPI export is provided, rules CTL-001 through CTL-004 are gracefully skipped, and the audit briefing explicitly notes: *"Tracking signal verification not executed due to unprovided ad platform logs."*
3. **Courier Remittance Pending Within Grace Period:**  
   If a courier delivery occurred 4 days prior and the agreed grace period is 7 days, rule **CTL-005** flags the order as a **Verified Healthy Control** (`is_healthy_control = true`), noting that settlement is active and within terms.

---

## 5. Currency Handling & Minor-Unit Math

All currency computations are conducted in **integer minor units** (e.g. cents, fils) according to ISO 4217 precision rules:

| Currency Code | Minor Unit Decimals | Multiplier to Minor Units | Sample Order Total | Stored Minor Unit Integer |
|---|---|---|---|---|
| **USD** | 2 | $100$ | $120.50 | `12050` |
| **AED** | 2 | $100$ | AED 250.00 | `25000` |
| **JPY** | 0 | $1$ | ¥12,000 | `12000` |
| **KWD** | 3 | $1000$ | KWD 15.900 | `15900` |
| **PKR** | 2 | $100$ | PKR 5,000.00 | `500000` |
| **GBP** | 2 | $100$ | £150.00 | `15000` |
| **EUR** | 2 | $100$ | €90.00 | `9000` |

### Cross-Currency Guard (Rule CTL-012)
- Commerce Truth Lab **never performs arithmetic across differing currencies** without explicit daily exchange rate matrices.
- If an order's checkout currency is `USD` and a tracking signal is emitted in `EUR`, rule **CTL-004 (Currency Mismatch)** triggers, and cross-system arithmetic is guarded by **CTL-012**.
