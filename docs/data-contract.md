# Canonical data contract v1

The canonical format is deliberately **not** a raw Shopify, Stripe or ad-platform payload. No importer is included. Validate a mapping on a small sample before relying on a report.

The complete runnable fixture is `examples/demo/input.json`; validation lives in `src/commerce_truth/schema.py`. Unknown keys are rejected throughout.

## Top-level fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | integer, exactly 1 | Contract version |
| `data_kind` | `synthetic` or `merchant_export` | Explicit provenance category |
| `as_of` | ISO-8601 with timezone | Audit cutoff; no implicit current time |
| `currency_exponents` | currency → integer 0–4 | Verified decimal conventions; three-letter uppercase labels, not an ISO-code certification |
| `policy` | object | `signal_grace_hours`, `collection_grace_hours`, `cod_settlement_grace_hours`; integer elapsed hours |
| `coverage` | array | Completeness declarations by store/stream |
| `orders` | array | Pseudonymized final order snapshots valid at cutoff |
| `events` | array | Normalized, successful observations; not every webhook event |

## Orders

Required fields: `store_id`, `order_id`, `created_at`, `currency`, `total_minor`, `payment_method`, `market`, `locale`, `signals`.

- IDs must be stable, nonempty, pseudonymized strings, unique within their documented scope.
- `total_minor` is the final collectible order total at cutoff, after edits and discounts, with the chosen tax/shipping scope explicitly mapped. This prototype assumes a fixed final total throughout the evaluated collection lifecycle.
- `payment_method` is `prepaid` or `cod`; mixed tenders, terms, subscriptions, cancelled/unfulfilled refund obligations, COD returns and gift-card liabilities are out of scope.
- `market` and `locale` are labels, not geolocation inference or translation. The rules do not depend on the language of these labels.
- `signals` maps a destination label, such as `meta` or `ga4`, to `{"permitted": true, "expected_value_minor": 10000}`. Both fields are mandatory.
- The expectation is an **order-placement purchase signal**. A fully refunded order can still legitimately have an earlier purchase signal. Refund analytics emission is not checked in v0.1.
- `permitted` is an operator-supplied snapshot for the relevant emission policy; it must be a JSON boolean, not `"true"`, `"false"` or `"denied"`. This does not establish legal consent or model later policy changes.

## Event mapping

All events require `id`, `store_id`, `order_id`, `stream`, `kind`, `at`.

| Kind | Stream | Additional fields | Meaning |
|---|---|---|---|
| `capture` | `payments` | `currency`, `amount_minor` | Successful prepaid collection; not authorization, pending or failed payment |
| `refund` | `payments` | `currency`, `amount_minor` | Successful prepaid customer refund; not a requested refund |
| `delivered` | `fulfillment` | none | Order-level delivery completed; not a partial package shipment |
| `cod_collected` | `cod` | `currency`, `amount_minor` | Courier has collected from customer |
| `cod_settled` | `cod` | `currency`, `amount_minor` | Gross order collection liability discharged with supported bank/fee/adjustment allocation |
| `purchase_signal` | `signals:<destination>` | `currency`, `amount_minor`, `dedup_key` | Purchase observation from a documented point in the signal pipeline |

Do not combine emitted events, delivery attempts and downstream accepted events into one undocumented stream. Name the observation point in the mapping notes. An emitted signal is not proof it was received, counted or attributed by the platform.

Each financial record ID must identify the underlying business transaction. Deduplicate webhook notifications representing the same successful transaction **before** mapping. Supply only one authoritative collection source per canonical transaction; never import a Shopify payment and its matching gateway capture as two payments.

The signal dedup key is normalized according to the destination's documented identity rules. This engine deliberately makes no claim to implement any vendor's server-side deduplication behavior.

## Coverage

Each entry requires `store_id`, `stream`, `from`, `through`, `complete`. Only one interval per store/stream is accepted.

To evaluate an absence or financial discrepancy, the relevant interval must start at or before order creation, extend through the audit cutoff, and be explicitly complete. A recent export that omits older captures is not complete for an old order, even if recent rows downloaded successfully.

“Complete” must mean all supported lifecycle records, including pagination, retries, refunds and updates relevant to the snapshot. The engine trusts this declaration; verifying it is the operator's responsibility.

## Unsupported input must be handled explicitly

Exclude unsupported business cases in a documented scope manifest; do not mislabel them to pass validation. Reconcile order counts before and after exclusions so that a small successful sample is not presented as an all-store audit.

Use merchant-authorized exports only. Replace real order identifiers with consistent pseudonyms across all streams. Do not include names, email addresses, telephone numbers, postal addresses, access tokens or raw provider payloads. Unknown-field rejection is useful but is not a comprehensive PII scanner; sensitive data could still be placed in a permitted string field.
