# Contributing Guide

## How to add a new audit rule
1. Create `packages/engine/rules/ctl_XYZ.py` subclassing `AuditRule`.
2. Add it to `AuditEngine` in `runner.py`.
3. Never claim fraud or recovered revenue.

## Code Style
- Python: `black`, `ruff`
- TS: `ESLint`

## Test Requirements
Every rule needs positive + negative tests.

## PR Checklist
- [ ] No fake claims
- [ ] All findings have evidence refs
- [ ] Positive and negative tests added

## How to add a new synthetic test case
Modify `data/synthetic/seed.py` and run it to regenerate `dataset.json`.
