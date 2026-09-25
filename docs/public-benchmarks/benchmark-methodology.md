# Public Benchmark Audit Methodology

**Commerce Truth Lab — Public Benchmark Validation Track**  
*Document Version: 1.0.0 &middot; Date: September 25, 2026*  
*Author: Syed Muslim Shah &middot; Portfolio: [syed-muslim-shah-portfolio.vercel.app](https://syed-muslim-shah-portfolio.vercel.app/)*

---

## 1. Methodological Philosophy: Deterministic Arithmetic vs. Machine Guesswork

Traditional analytics tools frequently rely on statistical estimation, algorithmic attribution modeling, and probabilistic matching. Commerce Truth Lab adopts an **evidence-first, deterministic arithmetic methodology**:

1. **Integer Minor-Unit Representation:** All financial quantities are stored as integers in their respective lowest minor currency denomination (e.g. cents, centavos, pence, fils, yen) to avoid IEEE-754 floating-point rounding errors.
2. **Explicit Variance Boundaries:** Exceptions are triggered only when discrete mathematical criteria fail.
3. **Healthy Controls Verification:** An audit is incomplete without demonstrating clean transactions that pass all criteria with zero discrepancy.
4. **Transparent Data Lineage:** Every finding cites the exact source dataset, record identifiers, evaluated fields, and observed values.

---

## 2. Evaluation Rules Applied Across Public Benchmarks

### 2.1 CTL-006-PUB: Payment Value Less Than Order Checkout Total (Undercollection)
- **Applicable Datasets:** Olist Brazilian E-Commerce (`bench-01-olist-reconciliation`).
- **Input Records:** `orders` (sum of item prices and freight) vs. `order_payments` (sum of payment sequential installments, vouchers, and credit cards).
- **Trigger Logic:**
  $$\sum \text{PaymentValue}_{\text{centavos}} < \text{GrossOrderTotal}_{\text{centavos}}$$
- **Handling of Marketplace Complexities:**
  - Marketplace vouchers and promotions often cause intentional net customer reductions. The engine reports the variance as an exception requiring cross-referencing against promotional voucher subsidies, avoiding premature accusations of lost funds.

### 2.2 CTL-007-PUB: Payment Value Exceeds Order Checkout Total (Overcollection)
- **Applicable Datasets:** Olist Brazilian E-Commerce (`bench-01-olist-reconciliation`).
- **Input Records:** `orders` gross total vs. `order_payments` aggregate capture value.
- **Trigger Logic:**
  $$\sum \text{PaymentValue}_{\text{centavos}} > \text{GrossOrderTotal}_{\text{centavos}}$$
- **Observation:** Flags records where customer payments exceed invoice lines, identifying potential shipping adjustments or double voucher application.

### 2.3 CTL-LOG-001: Customer Delivery Elapsed Past Estimated Delivery Date
- **Applicable Datasets:** Olist Logistics Telemetry (`bench-02-olist-logistics`).
- **Input Records:** `order_delivered_customer_date` vs. `order_estimated_delivery_date`.
- **Trigger Logic:**
  $$\text{Timestamp}(\text{actual\_delivery}) > \text{Timestamp}(\text{estimated\_delivery})$$
- **Distinction from Breach of Contract:**
  - Finding explicitly highlights that operational shipping delays do not automatically prove carrier contractual SLA breaches without examining courier agreements and postal ZIP zone exclusions.

### 2.4 CTL-008-PUB: Cancelled Quantity Greater Than Original Invoiced Quantity
- **Applicable Datasets:** UCI Online Retail (`bench-03-uci-cancellations`).
- **Input Records:** Standard sales invoices vs. cancellation invoices (`InvoiceNo` prefix `'C'`).
- **Trigger Logic:**
  $$|\text{Quantity}_{\text{cancelled}}| > \text{Quantity}_{\text{invoiced}} \quad (\text{for identical CustomerID and StockCode})$$
- **Classification Discipline:**
  - Described strictly as invoice cancellations, not payment gateway refunds. Negative quantities represent accounting credit adjustments.

### 2.5 CTL-CAPI-PUB-01: Ad Conversion Recorded Beyond Standard Attribution Window
- **Applicable Datasets:** Criteo Sponsored Search Log (`bench-04-criteo-ad-conversions`).
- **Input Records:** `click_timestamp` vs. `conversion_timestamp`.
- **Trigger Logic:**
  $$\Delta t = \text{Timestamp}(\text{conversion}) - \text{Timestamp}(\text{click}) > 7 \text{ days}$$
- **Non-Causal Boundary:**
  - Finding notes that time lag beyond 7 days causes attribution drop-off in standard ad networks, but does not prove whether the ad contributed causally to purchase intent.

### 2.6 CTL-001 & CTL-005: Multi-Stream Stress Testing (`bench-05-composite-cod-signals`)
- **Duplicate Identity (CTL-001):** Triggers when concurrent browser pixel and server CAPI purchase events bear mismatched `event_id` tokens, preventing ad network deduplication.
- **COD Collection Overdue (CTL-005):** Triggers when an order marked delivered has elapsed past the 7-day contractual grace window with zero courier remittance.

---

## 3. Healthy Controls Methodology

For each exception category, the benchmark pipeline explicitly verifies a corresponding **Healthy Control**:
- **Olist Payment Balance:** Orders where multi-part customer payments exactly equal the item and freight total down to 0 centavos variance.
- **Logistics Delivery Compliant:** Orders delivered safely prior to estimated delivery date.
- **UCI Cancellation Balanced:** Invoices where negative cancellation quantities perfectly match the original purchased quantity.
- **Criteo Timely Conversion:** Ad conversions occurring within 24 hours of click with valid session tokens.
- **Composite Signal Deduplication Clean:** Orders where browser and server signals report identical `event_id` tokens.

This ensures the audit engine produces zero false positives on compliant records.
