# Discovery Call Playbook: Shopify Measurement & Funnel Truth Sprint

**Role:** Lead Product Architect & Auditor (Syed Muslim Shah)  
**Duration:** 15–20 Minutes  
**Target Stakeholder:** Founder, Head of E-Commerce, VP Operations, or Finance Controller  
**Goal:** Qualify operational complexity, uncover discrepancy pain, address privacy guardrails, and secure agreement to review the Proposal & Data Contract.

---

## 1. Call Structure (20-Minute Agenda)

1. **Introduction & Anti-Hype Positioning (2 mins):** Establish that Commerce Truth Lab is an evidence-first audit engine—not an ad agency claiming magic ROAS improvements, nor a collection agency claiming guaranteed fraud recoveries.
2. **Operational Architecture Diagnosis (8 mins):** Walk through the 5 core transactional facts (Orders, Payments, Couriers, Refunds, Tracking Signals).
3. **Privacy & Security Walkthrough (3 mins):** Explain cryptographic salting, zero plaintext PII, and 30-day purge schedule.
4. **48-Hour Sprint Overview & Value Exchange (5 mins):** Outline the pilot deliverable, 3 prioritized fixes, and post-fix verification.
5. **Next Steps & Action Item (2 mins):** Send Proposal & Statement of Work + Data Contract within 2 hours.

---

## 2. Ten Targeted Diagnostic Questions

Use these questions to identify technical vulnerabilities and operational friction points:

### Track A: Paid Media & Tracking Signals
1. *"Are you currently running Meta Ads with both the Shopify Web Pixel and Conversions API (CAPI) active simultaneously?"*
   - *Vulnerability:* If both run without matching `event_id` tokens, Meta double-counts purchases, artificially inflating reported conversions (`CTL-001`).
2. *"When you compare your Shopify gross sales to Meta Ads Manager purchase conversion value for the same 30-day period, how wide is the gap?"*
   - *Vulnerability:* Gaps $> 10\%$ usually indicate missing server events or un-deduplicated browser signals (`CTL-002`, `CTL-010`).

### Track B: Courier COD & Cash Settlement (If Applicable)
3. *"If you offer Cash on Delivery (COD), how do you reconcile parcels marked 'Delivered' by the courier against actual bank deposits?"*
   - *Vulnerability:* Most brands rely on manual spreadsheets; delayed remittances past the 7-day grace window go unnoticed (`CTL-005`).
4. *"Have you ever caught courier shortfalls where the courier remitted less cash than the invoice total stated?"*
   - *Vulnerability:* Couriers frequently deduct unauthorized handling fees or round down collections (`CTL-006`, `CTL-007`).

### Track C: Gateway Deposits, Multi-Currency, and Refunds
5. *"Do you sell internationally across multiple currencies on a single Shopify store?"*
   - *Vulnerability:* 0-decimal currencies (JPY) or 3-decimal currencies (KWD) frequently suffer floating-point truncation in reporting (`CTL-003`, `CTL-004`).
6. *"How are refunds handled in customer service—can an agent issue an arbitrary refund amount, or does Shopify enforce a ceiling?"*
   - *Vulnerability:* Goodwill credits issued without parent payment caps create silent margin leakage (`CTL-008`).
7. *"Do payment gateway payout delays or currency conversions ever make it difficult to balance monthly cash against Shopify reported sales?"*
   - *Vulnerability:* Gateway reserve holds and currency exchange rate drift mask reconciliation variances (`CTL-012`).

---

## 3. Handling Merchant Privacy & Security Objections

| Common Merchant Question / Objection | Recommended Direct Response |
|---|---|
| *"Can we sign an NDA before sending our sales data?"* | *"Absolutely. Our formal Pilot Authorization Agreement (`docs/pilot-authorization-agreement.md`) includes standard confidentiality terms, strict tenant isolation, and a mandatory 30-day database purge schedule."* |
| *"Our legal team won't let us share customer email addresses or phone numbers."* | *"You shouldn't share them. Our Data Contract specifically asks you to export orders without customer names, phone numbers, or addresses. Any customer ID ingested is salted with a cryptographic SHA-256 hash upon upload."* |
| *"Do you need access to our live Shopify Admin or ad account?"* | *"No. We do not require admin access, API tokens, or OAuth apps. You provide raw CSV exports. We run the deterministic engine in your isolated workspace."* |

---

## 4. Closing & Commitment

At the conclusion of the call, confirm the next concrete milestone:

> *"Based on what you shared about your [CAPI setup / COD courier reconciliation / multi-currency operations], running our 48-hour Truth Sprint on your last 30 days will immediately clarify if your orders, deposits, and signals agree.*
> 
> *I will email you two documents within the hour:*
> 1. *Our Statement of Work & Proposal with our zero-PII commitment.*
> 2. *Our 1-page Data Export Guide showing exactly which CSV columns to pull.*
> 
> *If you can review and sign by [DAY], we can provision your private workspace and deliver your Forensic Implementation Report within 48 hours of file upload. Does that timeline work for your team?"*
