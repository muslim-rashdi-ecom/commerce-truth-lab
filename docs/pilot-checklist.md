# First real-store pilot

The next milestone is a **verified pilot**, not another impressive-looking simulated metric.

## 1. Agree scope and access

- Obtain written authorization from the merchant for the specific exports and analysis.
- Start with one store, one currency and a defined, mature order cohort.
- Choose supported prepaid or COD orders. Document excluded subscriptions, split tenders, returns, terms and other unsupported cases.
- Use read-only exports; do not request owner passwords or payment-write scopes.
- Agree retention, secure storage, permitted viewers and deletion procedure. Never commit the exports.

## 2. Prepare evidence

- Final order snapshots at the same cutoff.
- Successful captures/refunds linked to orders, not merely payment-status labels.
- Order-level completed-delivery records.
- For COD: courier collections and supported bank/fee/adjustment allocations with due-date conventions.
- Per-destination purchase observations with the observation point and identity semantics documented.
- Explicit policy eligibility and destination value definition for each selected order.
- Count reconciliation, pagination confirmation and lifecycle completeness for every declared stream.
- Consistent pseudonyms across sources; no raw PII or credentials.

## 3. Validate mappings before findings

- Manually reconcile several known-good and known-problem orders first.
- Check integer minor units, currency basis and timezone conversion.
- Ensure authorizations/pending transactions are not captures.
- Ensure a mirrored Shopify/gateway transaction is not counted twice.
- Confirm signal values use the correct item/tax/shipping conventions.
- Mark incomplete streams incomplete; do not turn unknowns into zero.

## 4. Review with the owner

For every finding, record its source-system confirmation, alternative explanations, investigator, action approval and result. Track false positives and supported issues missed by the rules. Keep unverified findings labeled unverified.

Treat any due-date thresholds as operational assumptions, not universal contract terms. Never issue a refund, collect a payment, resend signals or change spend based solely on this report.

## 5. Measure a defensible outcome

Useful claims after verification might include the number of reconciled orders, confirmed mapping defects, investigated unsettled balances or elapsed investigation time. Only claim money recovered after a verified transaction, with overlap and fees reconciled. Do not attribute all before/after performance changes to one fix.

Get written permission for the exact public case-study content. Anonymize client details even when the code is public.
