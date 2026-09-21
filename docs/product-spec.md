# Product Specification

## Mission
To provide truthful, evidence-based e-commerce audits.

## What it does
Flags discrepancies in tracking and reconciliation.

## What it does NOT claim
- Recovered revenue
- Causal ROAS improvement
- Intentional fraud

## Rules
| ID | Name | Category | Severity |
|---|---|---|---|
| CTL-001 | Duplicate Purchase Identities | duplicate_identity | high |
| ... | ... | ... | ... |
(See audit methodology for details)

## Data Model Overview
Shared schemas via Pydantic using minor units for currency.

## Synthetic Dataset
12 deterministic order paths simulating typical issues.

## Quality & Security
- Unit tests
- No PII storage
- Immutable data evaluation
