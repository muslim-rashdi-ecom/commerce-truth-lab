# Freelance Platform Positioning: Upwork & Contra
## Profile & Proposal Templates: Syed Muslim Shah

**Product:** Commerce Truth Lab v1  
**Practitioner:** Syed Muslim Shah, Lead E-Commerce Architect ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))  
**Governance Standard:** Strictly honest representations. No fabricated project history, no unearned badge claims ("Top Rated", "Contra Pro") unless officially awarded, and no simulated client testimonials.

---

### 1. Master Profile Overview (Upwork / Contra Specialized Profiles)

**Profile Title:** Shopify Technical Architect & Measurement Audit Specialist | Meta CAPI, GA4, Payment & COD Reconciliation

**Overview Text:**
```text
I help Shopify and DTC brands independently verify whether their store checkouts, payment gateway captures, courier COD settlements, refunds, and ad tracking signals agree.

When scaling paid acquisition, brands frequently suffer from silent measurement leaks:
• Meta CAPI and web pixels firing non-matching event IDs, causing double-reported purchases.
• Zero-decimal (JPY) or multi-decimal (KWD) orders miscalculating conversion values by 100x.
• Regional courier Cash-on-Delivery (COD) collections lagging past contractual remittance terms.
• Customer service refund adjustments exceeding original order authorized totals.

Rather than guessing with probabilistic attribution tools, I conduct a 48-Hour "Shopify Measurement & Funnel Truth Sprint" using Commerce Truth Lab—an independent deterministic audit engine.

How the Engagement Works:
1. Scope & Zero-PII Export: You provide sanitized CSV exports for a 30-day cohort (no customer names, phones, or addresses required).
2. Deterministic Audit (48h Turnaround): I ingest the files into an isolated workspace and run 12 programmatic verification checks (Rules CTL-001 to CTL-012).
3. Deliverables: You receive an evidence-linked forensic report (HTML/Markdown/JSON), 3 prioritized fixes (P0, P1, P2) for your developers or media team, a 45-minute walkthrough, and a 14-day post-fix re-verification audit.

Try the interactive demo (zero login required):
https://commerce-truth-lab.vercel.app/demo
```

---

### 2. Specialized Proposal 1: Shopify Tracking & Deduplication Audit (Meta CAPI & GA4)

**Applicable Job Postings:** "Fix Meta CAPI duplication", "Shopify GA4 purchase event mismatch", "Pixel firing twice on Shopify checkout".

**Proposal Template:**
```text
Hi [Client Name],

I noticed your job regarding tracking discrepancies between Shopify and your ad reporting.

When both web pixels and server Conversions API (CAPI) are enabled on Shopify, many stores experience duplicate purchase reporting because the browser and server payloads emit differing event_id tokens or fire at slightly different checkout lifecycle steps.

I conduct an independent, evidence-first tracking audit using Commerce Truth Lab:
• We compare your Shopify order exports directly against Meta CAPI/pixel and GA4 event logs for a recent cohort.
• We verify event deduplication, missing server events, and currency minor-unit precision.
• You receive a complete forensic report and 3 prioritized code/pixel fixes within 48 hours.

Privacy standard: We require zero customer personal data (no names, phones, or addresses).
You can review the methodology on our live synthetic demo: https://commerce-truth-lab.vercel.app/demo

Are you available for a 15-minute diagnostic chat to review your current tracking architecture?

Best regards,
Syed Muslim Shah
Lead E-Commerce Architect | https://syed-muslim-shah-portfolio.vercel.app/
```

---

### 3. Specialized Proposal 2: Payment & Refund Reconciliation Audit

**Applicable Job Postings:** "Shopify Stripe reconciliation", "Audit refund discrepancies", "Reconcile Shopify multi-currency payouts".

**Proposal Template:**
```text
Hi [Client Name],

I saw your requirement to reconcile Shopify orders against payment gateway captures and refunds.

In multi-currency or multi-gateway Shopify stores, accounting drift often occurs when gateway fees are deducted before gross matching, currency conversion rounding drifts from store rates, or manual customer service credits bypass original order ceilings.

I offer a fixed-scope Payment & Refund Reconciliation Sprint:
• Integer minor-unit verification across all transaction records (cents, fils, etc.) to eliminate rounding errors.
• Exact matching between Shopify orders, gateway capture statements (Stripe/PayPal/Checkout.com), and refund ledgers.
• Identification of over-refunded orders, uncaptured checkouts, and unallocated gateway deductions.
• Turnaround in 48 business hours with zero customer PII needed.

Interactive demo: https://commerce-truth-lab.vercel.app/demo

Would you like me to send over our 1-page sanitized CSV export checklist to see how quickly we can run this for your store?

Best regards,
Syed Muslim Shah
Lead E-Commerce Architect | https://syed-muslim-shah-portfolio.vercel.app/
```

---

### 4. Specialized Proposal 3: Courier Cash on Delivery (COD) Settlement Audit

**Applicable Job Postings:** "COD reconciliation", "Courier settlement audit", "Track uncollected COD payments".

**Proposal Template:**
```text
Hi [Client Name],

I read your job post regarding courier Cash on Delivery (COD) tracking and settlement.

For brands operating in COD-heavy regions (such as the GCC or South Asia), one of the biggest cash flow leaks is delayed courier remittance: parcels marked "Delivered" in the courier portal that sit unremitted past contractual grace periods, or unrecorded cash shortfalls upon bank deposit.

I provide an automated, evidence-first COD Reconciliation Audit:
• Cross-referencing your Shopify order manifests against your courier remittance statements.
• Deterministic detection of overdue remittances, short-collected parcels, and courier fee deductions beyond contract.
• Full evidence reference ledger showing exact tracking numbers, order IDs, and overdue days.
• Delivery within 48 hours of receiving sanitized CSV files.

Demo: https://commerce-truth-lab.vercel.app/demo

Let me know if you would like to review our sample COD audit report format.

Best regards,
Syed Muslim Shah
Lead E-Commerce Architect | https://syed-muslim-shah-portfolio.vercel.app/
```

---

### 5. Specialized Proposal 4: E-Commerce Data-Quality & Pre-Scale Baseline Audit

**Applicable Job Postings:** "E-commerce data audit", "Audit Shopify tracking before Black Friday / scaling spend", "Verify store analytics accuracy".

**Proposal Template:**
```text
Hi [Client Name],

Scaling paid acquisition or onboarding a new growth agency without verifying your baseline numbers is a major operational risk.

If your dashboard metrics, gateway receipts, and ad signals don't agree, media buyers end up optimizing against distorted purchase values.

I conduct the "Shopify Measurement & Funnel Truth Sprint":
• 12 deterministic integrity checks evaluating orders, gateway payouts, refunds, and ad platform tokens.
• Identifies exact data quality breaks: missing transaction timestamps, broken pixel tokens, uncaptured payments, or misaligned currencies.
• Provides 3 prioritized engineering fixes (P0, P1, P2) and a 14-day post-fix re-verification audit.
• 100% sanitized data process—zero customer personal info required.

Interactive synthetic casebook: https://commerce-truth-lab.vercel.app/demo

I'd be glad to discuss your current data stack on a quick 15-minute diagnostic call.

Best regards,
Syed Muslim Shah
Lead E-Commerce Architect | https://syed-muslim-shah-portfolio.vercel.app/
```
