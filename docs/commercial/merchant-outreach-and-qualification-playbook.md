# Merchant Outreach & Qualification Playbook
## Securing the Next Real Merchant Pilot Engagement

**Objective:** Onboard one qualified, active Shopify DTC merchant for a rapid 48-hour "Shopify Measurement & Funnel Truth Sprint".

---

## 1. Ideal Customer Profile (ICP)

A high-probability candidate merchant exhibits at least **two** of the following operational traits:

| ICP Filter | Operational Characteristic | Audit Resonance |
|---|---|---|
| **Platform** | Shopify or Shopify Plus | Native order schema compatibility (`shopify_orders`) |
| **Order Volume** | 1,500 to 15,000 orders per month | Sufficient volume for statistical discrepancy emergence |
| **Paid Media** | Running Meta Ads / Google Ads with Web Pixel + CAPI | High likelihood of signal duplicate identity mismatch (`CTL-001`) |
| **Fulfillment Mode** | Cash on Delivery (COD) in GCC / South Asia / MENA | Severe operational exposure to courier remittance lag (`CTL-005`, `CTL-006`) |
| **Currency** | Multi-currency checkout (USD, AED, EUR, GBP) | Vulnerability to integer minor-unit truncation (`CTL-003`, `CTL-004`) |

---

## 2. Direct Outreach Messaging (Anti-Hype, High Precision)

### Channel: LinkedIn Direct Message or Founder Email
**Subject:** Quick question on your Shopify CAPI deduplication & COD reconciliation

> Hi [FIRST_NAME],
> 
> I built **Commerce Truth Lab** ([https://commerce-truth-lab.vercel.app/demo](https://commerce-truth-lab.vercel.app/demo)), an evidence-first audit engine that reconciles Shopify orders against Stripe captures, courier COD remittances, refunds, and Meta CAPI purchase signals.
> 
> Most DTC brands running Meta ads and courier fulfillment assume their dashboards agree, but in practice:
> 1. Browser pixels and server CAPI often fire unmatched `event_id` keys, silently double-counting purchases.
> 2. Courier COD remittances frequently sit pending past the agreed 7-day grace window without operations noticing.
> 
> I'm currently offering a 48-hour **Shopify Measurement & Funnel Truth Sprint** for one selected Shopify brand:
> - You provide sanitized CSV exports (zero customer names, phones, or addresses needed).
> - Within 48 hours, I run our deterministic engine and deliver a forensic report highlighting your exact data exceptions, verified controls, and 3 prioritized technical fixes.
> - We execute a follow-up verification audit 14 days later to measure the reconciliation delta.
> 
> Would you be open to running an audit on your last 30 days of transactions?
> 
> Best regards,  
> **Syed Muslim Shah**  
> Lead Product Architect | [Portfolio](https://syed-muslim-shah-portfolio.vercel.app/)

---

## 3. Qualification Checklist (Pre-Sprint Screen)

Before executing the agreement, confirm the candidate merchant meets these minimum technical criteria:
- [ ] Has administrative or export access to Shopify Orders CSV.
- [ ] Has export access to their payment processor (Stripe, PayPal, etc.).
- [ ] If running COD, has weekly courier remittance statements (Aramex, Fetchr, DHL, etc.).
- [ ] Confirms willing to sign [`docs/pilot-authorization-agreement.md`](../pilot-authorization-agreement.md).
- [ ] Understands and agrees to the 48-hour delivery timeline and 14-day post-fix re-audit window.
