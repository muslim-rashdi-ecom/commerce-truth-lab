# Research and positioning

Research checked: 19 September 2026. Sources below are primary vendor documentation or product pages. Vendor capability descriptions are not independent performance validation.

## What already exists

| Existing product or specification | Verified scope relevant to this idea | Design implication |
|---|---|---|
| [Triple Whale](https://www.triplewhale.com/) | Describes attribution, data integration, analytics, AI analysis and governed actions | “AI ecommerce dashboard” is not a defensible novelty claim |
| [A2X](https://www.a2xaccounting.com/) | Describes payout reconciliation, order-to-cash subledger capabilities and profitability analytics | Order-to-cash auditing is an established category |
| [Shopify OrderTransaction](https://shopify.dev/docs/api/admin-graphql/latest/objects/OrderTransaction) | Distinguishes transaction kinds and statuses; exposes monetary/currency fields | An authorization must not be mapped as a successful capture |
| [Shopify MoneyBag](https://shopify.dev/docs/api/admin-graphql/latest/objects/MoneyBag) | Separates shop currency from customer presentment currency | Currency basis must be deliberate before comparing amounts |
| [Shopify manual payments](https://help.shopify.com/en/manual/payments/manual-payments) | Explains that manual-payment orders are unpaid until payment is received and recorded | Order creation is not proof of cash collection |
| [Stripe webhooks](https://docs.stripe.com/webhooks) | Documents unordered delivery and duplicate event deliveries, including duplicate underlying objects | Audit identities must not depend on delivery order or blindly count webhook deliveries |
| [GA4 ecommerce measurement](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce) | Documents purchase/refund measurement and separate value, tax, shipping and currency fields | Configure destination value semantics; do not equate all platform values with order totals |

These observations informed the prototype; they do not mean this repository implements or is endorsed by these vendors.

## The selected angle

An **open, local, evidence-first investigation workbench** for technical performance marketers:

1. Import a narrowly specified, merchant-authorized order/cash/signal export.
2. Show exactly what can and cannot be evaluated.
3. Trace each exception to individual source observations and a mapping assumption.
4. Reproduce failure modes safely on synthetic copies before touching real systems.
5. Hand the founder an investigation queue rather than an unsupported recovery estimate.

This combination is a proposed portfolio differentiation, not proof that no competitor or repository has it. This research was targeted, not an exhaustive patent, trademark, product or open-source search. The project name is a working title; trademark availability is unverified.

## Why not lead with “AI”

The difficult first problem is evidence semantics: retries, currency basis, settlement timing, incomplete exports and legitimate refunds. A language model does not make those mappings correct. The v0.1 findings therefore use deterministic rules with explicit assumptions. An optional explanation layer could be added later without letting it invent amounts or execute actions.

## Practical global scope

The core uses integer minor units, explicit currency exponents, timezone-aware dates, store-scoped identifiers and Unicode labels. Those choices make the schema portable. They do not create universal integrations, translations, legal compliance or coverage of every commerce business model.

Prioritize one verified merchant workflow first: prepaid purchases plus a clearly specified COD courier settlement flow. Extend only after adding fixtures and regression tests for the new semantics.

## Validation needed before stronger claims

- A merchant-authorized pilot with all required records and explicit scope.
- A reviewer checking each exception against the originating system.
- Measured false positives, unknown checks and missed supported exceptions.
- Verified remediation and a follow-up export, with attribution limits documented.
- Written permission before publishing any merchant name, result or screenshot.

No founder response, conversion rate, business benefit, uniqueness or commercial success is guaranteed.
