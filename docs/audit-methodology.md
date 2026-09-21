# Audit Methodology

Covers rules CTL-001 through CTL-012. Each rule specifies trigger conditions, required evidence, assumptions, what is NOT proven, next steps, and ownership.

## CTL-001: Duplicate Purchase Identities
Flags when multiple PurchaseSignals for the same order have DIFFERENT event_id values.

## CTL-002: Missing Purchase Signal
Flags when a delivered order has NO purchase signals.

## CTL-003: Purchase Value Mismatch
Flags >5% difference between signal value and order total.

## CTL-004: Purchase Currency Mismatch
Flags different currencies between signal and order.

## CTL-005: COD Collection Overdue
Flags overdue settlements.

## CTL-006: Delivered Order Cash Shortfall
Flags partial collection.

## CTL-007: Overcollection Against Order Total
Flags overcollection.

## CTL-008: Refund Greater Than Original Order Value
Flags excess refunds.

## CTL-009: Incomplete Evidence Coverage
Flags missing settlement or payment records.

## CTL-010: Unsupported Source / Ambiguous Mapping
Flags mapping ambiguity.

## CTL-011: Policy or Consent Mismatch
Flags missing or denied consent on tracking signals.

## CTL-012: Cross-Currency Comparison Guard
Prevents invalid multi-currency comparisons.
