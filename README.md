# Commerce Truth Lab

### Sales recorded. Cash verified?

An evidence-first audit of the gaps between **orders, customer collections, COD settlements and purchase signals**. Every finding includes source records, assumptions and a next verification step.

**Status: working offline prototype · synthetic demonstration · Python 3.11+ · zero runtime dependencies.** No live store or advertising account is connected. No recovered revenue, client deployment or universal integration is claimed.

Built by [Syed Muslim Shah](https://github.com/muslim-rashdi-ecom) as a technical performance-marketing portfolio project.

## Why this project

A purchase event, a paid order, a courier collection and a bank payout are different facts. A founder needs to know which fact is supported before changing budgets or operations.

Commerce Truth Lab answers a narrower question than attribution or accounting software:

**Which order-level exceptions can I substantiate from the evidence I have—and which checks must I withhold?**

It is not a world-first claim or a replacement for Triple Whale, A2X, a payment processor, or an accountant. The portfolio angle is transparent, reproducible investigation across operational and measurement records, with an offline fault-replay lab. See [research and positioning](docs/research.md).

## Open the demonstration first

- [Founder briefing](examples/demo/report.md): readable on GitHub.
- [Interactive evidence report](examples/demo/report.html): download and open locally in a browser; expand evidence and timelines. GitHub displays HTML source, not a live app.
- [Exact results](examples/demo/report.json): machine-readable findings, all rule decisions and evidence references.
- [Synthetic input](examples/demo/input.json): no client/customer information.
- [Three-minute walkthrough](docs/demo-walkthrough.md).
- [Verification record and limitations](docs/verification.md).

The included casebook contains **12 synthetic orders, 5 currencies, 8 findings and 4 orders with no flagged exceptions**. A clean result means only that these rules did not flag that supplied case—not that a business is healthy.

| Synthetic case | Engine behavior | Why it matters |
|---|---|---|
| Browser/server purchase observations share an identity | Does not flag duplicate purchase identities | Two observations are not automatically two purchases |
| One order has two purchase identities | Flags a deduplication investigation | Does not claim the destination actually counted twice |
| AED 250 collected by courier, AED 100 settled | Flags AED 150 overdue under the configured grace | Collection and settlement are separate |
| Delivered AED 80 order lacks collection evidence | Flags a shortfall only with complete cash coverage | An incomplete export is not proof of unpaid money |
| USD 120 capture followed by USD 120 refund | Shows zero net customer cash, no fault solely for refund | Gross signals are not retained cash |
| JPY purchase has a 100× value error | Flags the configured value mismatch | Decimal conventions cannot be assumed globally |
| KWD 15.900 order | Formats and compares integer minor units correctly | Three-decimal currencies stay precise |
| Fresh PKR COD collection | Does not label settlement overdue | Respect lifecycle maturity and grace periods |

**Never add finding amounts together:** they have different meanings and can overlap. There is intentionally no “total revenue recovered” card.

## Run it in two minutes

No accounts, API keys, paid services or runtime package installation are required.

### Windows PowerShell

From the extracted repository folder, with Python 3.11+ installed:

```powershell
$env:PYTHONPATH = "src"
py -m commerce_truth demo --out local-reports/my-first-demo
Start-Process local-reports/my-first-demo/report.html
py -m unittest discover -s tests -v
```

### macOS / Linux

```bash
PYTHONPATH=src python3 -m commerce_truth demo --out local-reports/my-first-demo
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Open `local-reports/my-first-demo/report.html` in your browser. Choose a new output directory for each run; existing report files are never overwritten.

Optional installation: `python -m pip install .`, then `commerce-truth demo --out local-reports/installed-demo`. Installation may need build tooling from the Python package registry; the no-install commands above do not.

## Four offline replay scenarios

```bash
PYTHONPATH=src python3 -m commerce_truth replay \
  --input examples/demo/input.json \
  --scenario settle-overdue-cod \
  --out local-reports/settlement-replay
```

PowerShell users: set `PYTHONPATH` as above and use the same command on one line starting with `py`.

| Scenario | What changes in the copy | What to inspect |
|---|---|---|
| `settle-overdue-cod` | Adds a simulated allocated settlement | One COD finding disappears; this is not money actually recovered |
| `duplicate-signal` | Adds a new normalized purchase identity | One additional investigation finding |
| `incomplete-cash-export` | Withdraws declared cash completeness | Cash checks become not evaluated; disappearing flags do not mean repairs |
| `drop-collection` | Models a collection that never happened | Observed cash changes; an order-placement signal alone does not prove payment |

Replay refuses `merchant_export` data. It does not edit the source input or call any outside service. It outputs a new input, report and `replay-comparison.json`.

## What is actually implemented

- Strict canonical JSON contract; explicit currencies, timezone-aware timestamps and policy booleans.
- Store-scoped identities; exact retry suppression and conflicting-record rejection.
- Twelve rule types covering collections, refunds, COD maturity and purchase-signal integrity.
- Required coverage gates for missing/negative financial evidence.
- Per-destination value expectations; no assumption that analytics value equals tax-inclusive order total.
- Per-order timeline, evidence references, input digest and complete rule-decision log.
- Segmentation by supplied market/locale; Unicode values preserved.
- Self-contained HTML, Markdown and JSON reports with no external scripts or assets.
- Synthetic-only fault replay and an automated test suite.

## Not implemented—and not implied

- No Shopify, Stripe, Meta, TikTok, Google Ads, GA4, GTM or Triple Whale live connector.
- No production webhook receiver, authentication, encrypted database, scheduler, SaaS tenancy or access control.
- No crawler that discovers a store's private cash/operations from a public URL.
- No universal deduplication model: adapters must normalize each platform's actual identity semantics.
- No FX conversion, bank-payout reconciliation, accounting revenue recognition, tax engine, profit attribution, causal lift, or automatic budget decisions.
- No subscriptions, gift-card/store-credit accounting, split tenders, COD returns/refunds, chargebacks or multi-invoice terms in v0.1. Unsupported cases must be excluded and documented, not coerced into supported states.
- The report interface is English. Locale labels are supported, but this is not a fully translated worldwide product.

For real data, use only merchant-authorized, pseudonymized exports and complete [the pilot checklist](docs/pilot-checklist.md). The tool can audit a properly mapped export; the included demonstration is not real-store validation.

## Repository map

| Path | Purpose |
|---|---|
| `src/commerce_truth/schema.py` | Strict input validation |
| `src/commerce_truth/engine.py` | Deterministic evidence rules |
| `src/commerce_truth/replay.py` | Synthetic-only scenarios |
| `src/commerce_truth/report.py` | Portable evidence reports |
| `src/commerce_truth/cli.py` | Local command-line workflow |
| `tests/` | Automated behavioral and contract tests |
| `examples/demo/` | Reproducible synthetic casebook and outputs |
| `docs/` | Research, architecture, data contract, demo and pilot guidance |

## How this fits the portfolio

The Livora case study shows an investigation. The measurement gateway explores signal transport. The growth control tower explores reporting. This project examines the **trustworthiness of the evidence behind operational and marketing decisions**.

It provides inspectable evidence of Python, measurement reasoning, reconciliation, testing and technical communication. It does **not** demonstrate unimplemented Liquid customization or prove hands-on mastery of every advertising platform. Add verified implementation work separately.

## License and contributions

MIT licensed. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not publish merchant exports, customer information, credentials or access tokens in issues, examples or commits.
