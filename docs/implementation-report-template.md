# Shopify Measurement & Funnel Truth Sprint — Audit Report Template

**Merchant Name:** [Merchant Store / Brand Name]  
**Store URL:** [e.g. brand.myshopify.com]  
**Audit Sprint Window:** [YYYY-MM-DD to YYYY-MM-DD]  
**Lead Auditor:** Syed Muslim Shah ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))  
**Engine Version:** Commerce Truth Lab v1 (Rules CTL-001 through CTL-012)  
**Report Classification:** CONFIDENTIAL — MERCHANT PILOT WORKSPACE  

---

## 1. Executive Summary

| Audit Metric | Result | Operational Meaning |
|---|---|---|
| **Orders Evaluated** | `[COUNT]` | Total store orders analyzed across date window |
| **Currencies Audited** | `[CURRENCIES]` | Base checkout and presentment currencies (e.g. USD, AED, EUR) |
| **Exceptions Flagged** | `[COUNT]` | Transaction records requiring operational review |
| **Healthy Controls** | `[COUNT]` | Clean records validating baseline rule specificity |
| **Data Completeness** | `[PERCENT]%` | Proportion of required sources mapped and verified |
| **Signal Alignment Score** | `[PERCENT]%` | Ad platform conversion identity consistency |

### Core Finding Summary
> [Executive 2-3 paragraph summary of primary discrepancy patterns: e.g. COD courier collection lag, CAPI deduplication failure rate, or refund reconciliation balance.]

---

## 2. Anti-Hype & Non-Claim Boundaries

Commerce Truth Lab operates strictly under empirical evidence boundaries:
- **No Claim of Recovered Revenue:** Identified shortfalls reflect unverified records, not funds automatically recovered.
- **No Accusation of Fraud:** Missing courier settlements or payment gaps indicate record discrepancies, not confirmed theft or bad faith.
- **No Causal ROAS Assertion:** Signal tracking issues demonstrate event delivery defects, not marketing performance causality.
- **Independent Currency Partitioning:** No amounts are summed across differing currencies.

---

## 3. Data Sources Ingested & Pseudonymization Verification

| Data Source | Type | File Reference | Ingested Records | PII Status |
|---|---|---|---|---|
| Shopify Orders | Store Orders | `orders_export.csv` | `[COUNT]` | Pseudonymized (`CUST_xxxx`) |
| Payment Gateway | Captured Payments | `gateway_payouts.csv` | `[COUNT]` | Tokenized / No Card Data |
| Courier Remittances | COD Settlements | `courier_settlement.csv` | `[COUNT]` | Airway bill reference |
| Customer Refunds | Returns & Credits | `refunds_export.csv` | `[COUNT]` | Order-linked |
| Meta CAPI / Pixel | Tracking Signals | `events_log.csv` | `[COUNT]` | Event ID & Timestamp |

---

## 4. Reconciled Audit Findings (CTL Rules)

### CTL-001: Signal Deduplication Failures
- **Impacted Orders:** `[LIST]`
- **Observation:** Differing browser vs. server `event_id` strings reported for identical order.
- **Source Evidence:** `[Browser Event ID]` vs `[Server Event ID]`
- **Assumptions Applied:** Ad platforms count unmatched IDs as distinct conversions.
- **What Is NOT Proven:** Does not prove ad network double-billed the merchant.
- **Next Step:** Unify event ID generation in theme checkout script and backend webhook.

### CTL-005 / CTL-006: COD Remittance Shortfalls & Delays
- **Impacted Orders:** `[LIST]`
- **Observation:** Courier marked orders delivered `[X]` days ago; remittance is `[shortfall amount / missing]`.
- **Source Evidence:** `[Courier Tracking ID]`, `[Airway Bill POD]`
- **Assumptions Applied:** Agreed courier remittance grace period is `[7]` days post-delivery.
- **What Is NOT Proven:** Does not prove courier default; could be pending weekly batch adjustment.
- **Next Step:** Open courier settlement inquiry ticket with batch reference.

### CTL-008: Excessive Refund Discrepancies
- **Impacted Orders:** `[LIST]`
- **Observation:** Total refunds processed exceed initial captured transaction amount.
- **Source Evidence:** `[Refund IDs]` vs `[Payment Capture ID]`
- **Assumptions Applied:** Full refund policy without separate goodwill credit authorizations.
- **What Is NOT Proven:** Does not prove unauthorized agent refunding.
- **Next Step:** Review support ticket logs for compensatory shipping vouchers.

---

## 5. Verified Healthy Controls

| Order ID | Verified Rule | Result | Verification Standard |
|---|---|---|---|
| `[ORD-xxx]` | CTL-001 (Deduplication) | Pass | Shared `event_id` verified across browser and server payloads |
| `[ORD-xxx]` | CTL-008 (Refund Balance) | Pass | Refund amount exactly matches original capture |
| `[ORD-xxx]` | CTL-005 (COD Grace Window) | Pass | Delivery age within merchant 7-day settlement window |
| `[ORD-xxx]` | CTL-003 (Currency Precision) | Pass | Integer minor units match across store and signal payloads |

---

## 6. Actionable Implementation Plan

| Priority | Responsible Owner | Recommended Action | Verification Target |
|---|---|---|---|
| **P0** | Paid Media / Dev | Sync `event_id` between client pixel and Conversions API | Next ad sprint |
| **P1** | Logistics / Ops | Submit courier claim for overdue COD batch `[BATCH-ID]` | Within 3 business days |
| **P2** | Finance / Support | Establish compensatory credit logging standard for refunds | End of week |
| **P3** | Analytics | Adjust zero-decimal currency pixel handling for JPY/KRW | Next sprint release |

---

## 7. Sign-Off & Verification

- **Lead Auditor:** Syed Muslim Shah
- **Merchant Sponsor:** `[Name / Title]`
- **Date Delivered:** `[YYYY-MM-DD]`
- **Workspace Data Deletion Date:** `[Scheduled Date per Agreement]`
