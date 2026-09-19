# Commerce Truth Lab

## Evidence before action

Data: **SYNTHETIC** · As of 2026-09-19T12:00:00Z · Engine 0.1.0

This is an offline prototype audit. Findings are exceptions under supplied assumptions, not verified causes or recovered revenue.

12 orders · 7 findings · 7 affected orders · 0 checks not evaluated.

Finding amounts have different meanings and may overlap. Never sum them as revenue lost, recovered or at risk.

## Investigation queue

### DEMO-009 — Purchase signal conflicts with supplied policy

Priority: critical · Rule: `signal_policy_conflict` · Destination: meta

A purchase signal is present although this order/destination is marked not permitted. This is a policy-contract exception, not a legal determination.

Amount: Not quantified. No monetary impact inferred.

Next verification: Inspect the consent/policy mapping and emission path before further collection. Do not infer legal compliance from this tool.

Evidence: order-6adf64f4931e25cc, event-b19e3dcb43d22b16

### DEMO-004 — Delivered order has a recorded collection shortfall

Priority: high · Rule: `delivered_cash_shortfall` · Destination: operations

Delivery is recorded and the configured grace period elapsed, but gross customer collections do not cover the final order total.

Amount: AED 80.00. unmatched delivered order balance; not proven bad debt

Next verification: Verify cash receipt, payment terms and final order amount with the gateway or courier. Do not charge the customer automatically.

Evidence: order-72f81392f8855dff, event-1f0e2e11484c6e43

### DEMO-011 — Recorded collection exceeds the order total

Priority: high · Rule: `overcollection` · Destination: operations

Distinct successful collection transactions exceed the supplied final order total; a mapping error is also possible.

Amount: AED 99.00. gross collection above final order total; not lost revenue

Next verification: Verify transaction identities, order edits and legitimate adjustments with payments operations before considering any refund.

Evidence: order-00f7f10955bbdaf9, event-65f22d65252daefd, event-dde42bccdf9acfbd

### DEMO-002 — Multiple purchase identities for one order

Priority: medium · Rule: `duplicate_purchase_keys` · Destination: meta

Distinct normalized deduplication keys were observed for one order/destination. Actual downstream double counting is not established.

Amount: Not quantified. No monetary impact inferred.

Next verification: Inspect browser/server identity alignment and the destination's own deduplication results. Never infer Meta, TikTok and GA4 share one dedup rule.

Evidence: order-a06c59fc52540ed9, event-5b6b1aca14929b8b, event-85db4fb447bfdf70

### DEMO-006 — Purchase value differs from its configured basis

Priority: medium · Rule: `signal_value_mismatch` · Destination: meta

Expected 5000 minor units for this destination; at least one observation differs. Tax/shipping conventions are configured, not guessed.

Amount: Not quantified. No monetary impact inferred.

Next verification: Verify each destination's value definition, discounts, tax and shipping treatment against the source order.

Evidence: order-22c9a9b70b513049, event-19a4dd0b5def837f

### DEMO-010 — Expected purchase signal is absent

Priority: medium · Rule: `missing_purchase_signal` · Destination: meta

No purchase signal exists in the declared complete destination export after the configured grace period.

Amount: Not quantified. No monetary impact inferred.

Next verification: Verify identity mapping, consent snapshot, integration delivery logs and downstream receipt before resending anything.

Evidence: order-7aab1560d35978e0

### DEMO-012 — Purchase currency differs from the expected basis

Priority: medium · Rule: `signal_currency_mismatch` · Destination: meta

Observed purchase currency differs from the canonical order currency. Cross-currency amounts are not subtracted.

Amount: Not quantified. No monetary impact inferred.

Next verification: Check whether the destination intentionally uses shop currency versus presentment currency and correct the mapping contract first.

Evidence: order-921d68ea0498dbc4, event-0ec6ff2a084740fb

## Order-level cash evidence

Observed collections are not bank payouts or accounting revenue. COD collection means courier-held cash. No total is combined across currencies.

| Order | Method | Order total | Observed net customer cash | Cash coverage |
|---|---|---:|---:|---|
| DEMO-001 | prepaid | AED 100.00 | AED 100.00 | declared complete |
| DEMO-002 | prepaid | AED 140.00 | AED 140.00 | declared complete |
| DEMO-003 | cod | AED 250.00 | AED 250.00 | declared complete |
| DEMO-004 | prepaid | AED 80.00 | AED 0.00 | declared complete |
| DEMO-005 | prepaid | USD 120.00 | USD 0.00 | declared complete |
| DEMO-006 | prepaid | JPY 5,000 | JPY 5,000 | declared complete |
| DEMO-007 | prepaid | KWD 15.900 | KWD 15.900 | declared complete |
| DEMO-008 | cod | PKR 2,000.00 | PKR 2,000.00 | declared complete |
| DEMO-009 | prepaid | AED 110.00 | AED 110.00 | declared complete |
| DEMO-010 | prepaid | AED 75.00 | AED 75.00 | declared complete |
| DEMO-011 | prepaid | AED 99.00 | AED 198.00 | declared complete |
| DEMO-012 | prepaid | USD 30.00 | USD 30.00 | declared complete |

## Reproducibility

Canonical input SHA-256: `9976f8a1c2ebcef1d914a08f2805cdc8b0c190e889e1efec55dd2637e0b57b38`

See report.json for every rule decision, coverage interval, timeline and source record. Compare the original source systems before taking action.
