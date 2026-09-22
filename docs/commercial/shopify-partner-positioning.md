# Shopify Partner Profile & Positioning Specification
## Partner Ecosystem Positioning: Commerce Truth Lab

**Product:** Commerce Truth Lab v1  
**Lead Practitioner:** Syed Muslim Shah ([Portfolio](https://syed-muslim-shah-portfolio.vercel.app/))  
> [!IMPORTANT] GOVERNANCE STATUS: PENDING PARTNER APPLICATION
> - **Compliance Rule:** Do NOT claim "Official Shopify Partner", "Shopify Plus Certified Partner", or official Shopify endorsement until the partner application is formally submitted, reviewed, and approved.
> - **Current Representation:** Independent Technical Consultant and E-Commerce Engineer specializing in Shopify measurement, reconciliation, and data infrastructure.

---

### 1. Partner Profile Description

```text
Commerce Truth Lab provides independent measurement verification and financial reconciliation services for Shopify and Shopify Plus merchants.

We resolve the common "dashboard discrepancy" problem: when Shopify orders, payment gateway settlements, courier cash-on-delivery manifests, refunds, and Meta CAPI / GA4 purchase signals do not agree.

Rather than relying on probabilistic attribution modeling or black-box algorithms, we use a 100% deterministic Python audit engine (Rules CTL-001 to CTL-012) operating on sanitized CSV exports. Within 48 hours, merchants receive an objective evidence-linked report identifying exact operational discrepancies and three prioritized fixes (P0, P1, P2) for their engineering, media, or logistics teams.
```

---

### 2. Service Categories (Shopify Partner Directory Alignment)

1. **Analytics and Tracking:**
   - Server-side tracking setup verification (Conversions API / CAPI)
   - Google Analytics 4 (GA4) e-commerce purchase signal audit
   - Event deduplication and pixel identity alignment
2. **Store Management & Operations:**
   - Multi-currency payment gateway reconciliation (Stripe, Checkout.com, Tap, PayPal)
   - Courier Cash on Delivery (COD) settlement and remittance tracking
   - Return and refund balance verification
3. **Custom Solutions & Data Architecture:**
   - Data hygiene and CSV export validation
   - Independent measurement baseline before agency onboarding or replatforming

---

### 3. Short Partner Bio (100–150 Words)

> Syed Muslim Shah is an e-commerce technical architect and the creator of Commerce Truth Lab, an open, evidence-first audit platform for Shopify and DTC brands. With deep expertise across full-stack systems, multi-currency data pipelines, and conversion tracking mechanics, Syed helps founders and growth leaders independently verify whether their reported sales match real cash deposits and ad platform purchase tokens. All audits operate under strict zero-PII security standards with isolated tenant workspaces and 48-hour turnarounds.

---

### 4. Merchant-Facing Offer Description: "Shopify Measurement & Funnel Truth Sprint"

```text
The Shopify Measurement & Funnel Truth Sprint is a 48-hour rapid diagnostic designed to give Shopify operators mathematical confidence in their numbers.

What We Verify:
1. Deduplication Integrity: Do Meta CAPI and web pixel events share matching event_id tokens, or are you overcounting purchases?
2. Minor-Unit Multipliers: Are zero-decimal (JPY) or multi-decimal (KWD) transactions distorted by 100x in marketing reports?
3. Cash Settlement Lag: Are courier COD collections actually remitted within contractual grace periods?
4. Refund Ceilings: Have customer service adjustments inadvertently exceeded initial order capture amounts?

Deliverables:
- Standalone Forensic Report (HTML, Markdown, and JSON)
- Evidence Reference Ledger linking every anomaly to transaction IDs
- 3 Prioritized Fixes (P0 Critical, P1 High, P2 Operational)
- 45-Minute Executive Walkthrough
- 14-Day Post-Fix Re-Verification Audit

Requirements: Sanitized CSV exports covering a 30-day cohort. No live admin logins. Zero customer PII.
```

---

### 5. Agency-Partner Version of the Offer

```text
For Shopify Design, Development, and Performance Agencies:

When onboarding a new Shopify client or preparing to scale paid acquisition, unverified measurement baselines create friction. If a client's tracking is double-counting or courier remittances are lagging, your agency risks taking the blame for poor ROAS or cash shortfalls.

Our Agency Partner Sprint provides:
• Objective Baseline Audit: Delivered within 48 hours of client onboarding.
• White-Label or Co-Branded Delivery: Present objective forensic reports under your brand or as an independent verification partner.
• Clear Engineering Handoff: We isolate the exact code or pixel misconfigurations so your developers can implement the fixes immediately.
• Zero Threat to Agency Scope: We do not manage ad spend, design themes, or build custom apps—we solely verify data integrity.
```

---

### 6. Recommended Portfolio & Evidence Links

- **Interactive Synthetic Casebook:** `https://commerce-truth-lab.vercel.app/demo` (Demonstrates 12 multi-currency test orders with 8 anomalies and 4 healthy controls across AED, USD, EUR, GBP, JPY, KWD, PKR).
- **Public Audit Engine Source Code:** `https://github.com/muslim-rashdi-ecom/commerce-truth-lab` (Demonstrates production engineering standards, 63 passing tests, salted SHA-256 pseudonymization, and tenant isolation).
- **Founder Engineering Portfolio:** `https://syed-muslim-shah-portfolio.vercel.app/`

---

### 7. Shopify Partner Application Preparation Checklist

Before submitting the formal Shopify Partner Directory listing:
- [ ] Active Shopify Partner account created and verified with business email.
- [ ] Two-factor authentication (2FA) enforced on all partner logins.
- [ ] Public development store created to demonstrate theme and app sandbox integrations.
- [ ] Service offering page drafted according to Shopify Partner Guidelines (no prohibited marketing claims, no guaranteed revenue recovery claims).
- [ ] Standard commercial contract and mutual non-disclosure agreement (NDA) in place.
- [ ] Privacy policy and data-retention policy published and publicly linked.
- [ ] First real merchant engagement successfully completed and documented in the evidence ledger.
