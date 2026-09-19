# Three-minute founder demonstration

This is a demo guide, not a claim about a client's business. Keep the SYNTHETIC label visible throughout.

## 0:00 — The question

Open `examples/demo/report.html` locally. Explain that order creation, tracked purchase, customer payment and merchant receipt are not interchangeable. The project checks a specified export, not an arbitrary public website.

## 0:30 — A concrete operational exception

Find DEMO-003. The synthetic courier collected AED 250 and only AED 100 of gross liability is settled. After the configured seven-day interval, AED 150 is flagged as overdue unsettled balance. Expand source evidence. Explain that contractual terms, fees and bank allocation must be checked before calling it a real issue.

Do not describe this as recovered or lost revenue.

## 1:10 — A measurement exception

Find DEMO-002. Two observations use different normalized purchase identities for one order/destination. This is a reason to inspect deduplication, not proof Meta counted twice. Contrast DEMO-001: matching browser/server identities and an exact retry do not produce that finding.

## 1:45 — The healthy controls

Show DEMO-005: USD 120 captured and fully refunded results in zero net customer cash, but the original purchase observation is not automatically a bug. Show DEMO-008: new COD collection has not aged past its settlement grace.

## 2:15 — Replay, do not promise

Run the `settle-overdue-cod` replay from the README, then inspect `replay-comparison.json`. One finding is no longer flagged after a **simulated** settlement.

Next run `incomplete-cash-export`. Monetary findings disappear because checks are withheld, not because the store was repaired. This is the central trust demonstration.

## 2:50 — A specific next step

Offer a small, merchant-authorized pilot using pseudonymized exports and agreed scope. The deliverable is an evidence-backed investigation report. Live connectors, a verified client result and translations are later milestones—not existing capabilities.
