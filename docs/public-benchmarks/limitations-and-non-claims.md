# Public Benchmark Limitations, Boundaries, and Non-Claims

**Commerce Truth Lab — Public Benchmark Validation Track**  
*Document Version: 1.0.0 &middot; Date: September 25, 2026*  
*Author: Syed Muslim Shah &middot; Portfolio: [syed-muslim-shah-portfolio.vercel.app](https://syed-muslim-shah-portfolio.vercel.app/)*

---

## 1. Absolute Boundary: Public Data is Not Commercial Evidence

Under no circumstances should the results from the Public Benchmark Validation Track be construed or represented as commercial validation, real-world case studies, or proof of client revenue recovery.

### Strict Prohibitions
1. **Never Call Public Benchmarks a "Client Pilot":** Public datasets originated from open-source repositories and research archives (Kaggle, UCI, Criteo). They do not involve a private merchant client contract or pilot authorization.
2. **Never Claim Recovered Merchant Revenue:** Variances observed in historical public data (e.g. Olist 2017 orders or UCI 2011 invoices) cannot be retroactively recovered or claimed as recovered cash.
3. **Never Accuse Parties of Fraud:** Exceptions detected by audit rules represent arithmetic or operational discrepancies based on available tables. Without merchant bank deposit statements, internal fraud investigation files, or courier contracts, fraud cannot be alleged.
4. **Never Alter Commercial Funnel Counters:** External outreach metrics in the Commercial Funnel Tracker (`docs/commercial/commercial-funnel-tracker.md`) remain strictly at **0 contacted, 0 replies, 0 discovery calls, 0 signed pilots, and 0 paid engagements**. Public benchmark development does not advance Milestone 4 external execution.

---

## 2. Inherent Limitations of Public Datasets

| Dataset | Available Telemetry | Missing Telemetry (Inherent Limit) | Impact on Conclusions |
|---|---|---|---|
| **Olist Brazilian E-Commerce** | Orders, items, customer payments, delivery dates | Merchant bank payout slips, interchange fee breakdowns, chargebacks | Cannot verify whether merchant received net settlement in their corporate bank account. |
| **UCI Online Retail** | Invoices, item codes, quantities, prices | Payment gateway logs, refund remittance slips, return shipping labels | Cancellations are strictly billing adjustments, not verified payment refunds. |
| **Criteo Sponsored Search** | Ad click timestamps, conversion timestamps, tokens | Shopify checkout session IDs, customer identities, courier delivery scans | Ad log analysis proves signal timing only; cannot be cross-joined to store sales. |
| **Public-Plus-Synthetic Composite** | Real Olist order foundations | Real courier remittance manifests, real Meta CAPI payloads | Companion tables are synthetic fixtures used to stress-test multi-table pipeline mechanics. |

---

## 3. Clear Terminology Governance

To maintain total documentation integrity across all materials:

- **"PUBLIC_BENCHMARK":** An evaluation performed on 100% publicly available, un-synthesized historical dataset records.
- **"PUBLIC_PLUS_SYNTHETIC_COMPOSITE":** An evaluation combining real public order identifiers with explicitly labeled synthetic companion tables (COD courier and Meta CAPI).
- **"SYNTHETIC_DEMO":** The interactive 12-order test workspace used for product demonstrations.
- **"REAL_AUTHORIZED_PILOT":** A private, signed engagement with a live Shopify/DTC merchant using sanitized merchant data under an executed SOW and pilot authorization agreement. (Currently 0).

---

## 4. Summary of Affirmative Claims

What Commerce Truth Lab **does** claim based on public benchmarks:
- The deterministic audit pipeline processes real-world multi-part payment sequence structures without IEEE-754 precision loss.
- The chronological parser correctly flags delivery timestamp overruns beyond merchant-estimated dates.
- Negative quantity credit notes can be programmatically matched against original invoices.
- Ad conversion latency beyond standard attribution windows can be isolated.
- The system generates verifiable HTML, Markdown, and JSON forensic reports with complete data lineage.
