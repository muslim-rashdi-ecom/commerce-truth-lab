"""Portable founder briefing and exact machine-readable evidence."""

from html import escape
import json


def money(amount, currency, exponents):
    if amount is None:
        return "Not quantified"
    exponent = exponents[currency]
    sign = "-" if amount < 0 else ""
    absolute = abs(amount)
    if not exponent:
        return f"{currency} {sign}{absolute:,}"
    whole, fraction = divmod(absolute, 10**exponent)
    return f"{currency} {sign}{whole:,}.{fraction:0{exponent}d}"


def safe_md(value):
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;").replace("`", "\\`").replace("\n", " ")


def markdown_report(report):
    s = report["summary"]
    lines = ["# Commerce Truth Lab", "", "## Evidence before action", "",
             f"Data: **{report['data_kind'].upper()}** · As of {report['as_of']} · Engine {report['engine_version']}", "",
             "This is an offline prototype audit. Findings are exceptions under supplied assumptions, not verified causes or recovered revenue.", "",
             f"{s['orders']} orders · {s['findings']} findings · {s['affected_orders']} affected orders · {s['checks_not_evaluated']} checks not evaluated.", "",
             s["amount_warning"], "", "## Investigation queue", ""]
    for f in report["findings"]:
        amount = money(f["amount_minor"], f["currency"], report["currency_exponents"])
        lines += [f"### {safe_md(f['order_id'])} — {f['title']}", "",
                  f"Priority: {f['severity']} · Rule: `{f['rule']}` · Destination: {safe_md(f['destination'] or 'operations')}", "",
                  f["explanation"], "", f"Amount: {amount}. {f['amount_basis'] or 'No monetary impact inferred.'}", "",
                  f"Next verification: {f['next_step']}", "", "Evidence: " + ", ".join(f["evidence_refs"]), ""]
    if not report["findings"]:
        lines += ["No exceptions flagged by these rules. This does not establish that the store is healthy; inspect withheld checks and coverage.", ""]
    lines += ["## Order-level cash evidence", "", "Observed collections are not bank payouts or accounting revenue. COD collection means courier-held cash. No total is combined across currencies.", "",
              "| Order | Method | Order total | Observed net customer cash | Cash coverage |", "|---|---|---:|---:|---|"]
    for row in report["orders"]:
        lines += ["| " + " | ".join([safe_md(row["order_id"]), row["payment_method"], money(row["order_total_minor"], row["currency"], report["currency_exponents"]), money(row["observed_customer_cash_net_minor"], row["currency"], report["currency_exponents"]), "declared complete" if row["cash_complete"] else "INCOMPLETE / unresolved"]) + " |"]
    lines += ["", "## Reproducibility", "", f"Canonical input SHA-256: `{report['input_sha256']}`", "", "See report.json for every rule decision, coverage interval, timeline and source record. Compare the original source systems before taking action.", ""]
    return "\n".join(lines)


def html_report(report):
    def h(value):
        return escape(str(value), quote=True)

    s = report["summary"]
    cards = []
    for f in report["findings"]:
        records = "".join(f'<h4>{h(ref)}</h4><pre>{h(json.dumps(report["evidence"][ref], ensure_ascii=False, indent=2))}</pre>' for ref in f["evidence_refs"])
        amount = money(f["amount_minor"], f["currency"], report["currency_exponents"])
        cards.append(f'''<article class="finding"><div class="eyebrow"><span class="severity {h(f['severity'])}">{h(f['severity'])}</span> {h(f['order_id'])} / {h(f['destination'] or 'operations')}</div><h3>{h(f['title'])}</h3><p>{h(f['explanation'])}</p><div class="amount">{h(amount)}</div><p class="muted">{h(f['amount_basis'] or 'No monetary impact inferred.')}</p><div class="action"><strong>Next verification</strong><p>{h(f['next_step'])}</p></div><details><summary>Inspect source evidence · {len(f['evidence_refs'])} records</summary>{records}<p>{h(f['confidence'])}</p></details></article>''')
    ledger = "".join(f'<tr><td>{h(r["order_id"])}</td><td>{h(r["market"])} / {h(r["locale"])}</td><td>{h(r["payment_method"])}</td><td>{h(money(r["order_total_minor"],r["currency"],report["currency_exponents"]))}</td><td>{h(money(r["observed_customer_cash_net_minor"],r["currency"],report["currency_exponents"]))}</td><td>{"Declared complete" if r["cash_complete"] else "WITHHELD / partial"}</td></tr>' for r in report["orders"])
    checks = "".join(f'<tr><td>{h(c["order_id"])}</td><td>{h(c["rule"])}<br>{h(c["destination"] or "")}</td><td>{h(c["status"])}</td><td>{h(c["reason"])}</td></tr>' for c in report["checks"])
    timelines = "".join(f'<details><summary>{h(r["order_id"])} · {len(r["timeline_refs"])} observed events</summary><ol>' + "".join(f'<li><strong>{h(report["evidence"][ref]["at"])} — {h(report["evidence"][ref]["kind"])}</strong><pre>{h(json.dumps(report["evidence"][ref], ensure_ascii=False, indent=2))}</pre></li>' for ref in r["timeline_refs"]) + '</ol></details>' for r in report["orders"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>Commerce Truth Lab — Evidence briefing</title><style>
:root{{color-scheme:dark;--bg:#0c1519;--panel:#142228;--line:#2a3b42;--muted:#adc0c7;--text:#f1f6f5;--accent:#87e4bf}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,sans-serif}}main{{max-width:1240px;margin:auto;padding:40px 28px}}nav{{display:flex;justify-content:space-between;gap:18px;border-bottom:1px solid var(--line);padding-bottom:20px}}nav strong{{letter-spacing:.08em}}a{{color:var(--accent)}}.tag,.eyebrow{{font-size:12px;letter-spacing:.09em;text-transform:uppercase}}.tag{{color:var(--accent)}}header{{padding:54px 0 32px;max-width:840px}}h1{{font-size:clamp(36px,6vw,64px);line-height:1.08;letter-spacing:-.045em;margin:18px 0}}h2{{font-size:28px;margin-top:46px}}h3{{font-size:23px;line-height:1.25}}.lead{{font-size:19px;color:var(--muted)}}.muted{{color:var(--muted);font-size:14px}}.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.metric,.finding{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:24px}}.metric b{{display:block;font-size:36px;color:var(--accent)}}.metric span{{color:var(--muted);font-size:14px}}.notice{{border-left:3px solid var(--accent);padding:12px 18px;background:#11251f;margin:22px 0}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}.severity{{padding:4px 8px;border-radius:5px;margin-right:10px;color:#ffd0a0;background:#49301c}}.critical{{color:#ffc1c8;background:#4d202c}}.amount{{font-size:26px;font-weight:700;margin-top:22px}}.action{{border-top:1px solid var(--line);padding-top:18px;margin-top:20px}}.action p{{font-size:14px}}details{{border-top:1px solid var(--line);margin-top:20px;padding-top:16px}}summary{{cursor:pointer;color:var(--accent);font-weight:600}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#091216;padding:14px;border-radius:7px;font-size:12px;direction:ltr}}.scroll{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{text-align:left;padding:14px 12px;border-bottom:1px solid var(--line);vertical-align:top}}th{{color:var(--accent)}}footer{{margin:46px 0 16px;color:var(--muted);font-size:13px}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{main{{padding:24px 16px}}.metrics{{grid-template-columns:repeat(2,1fr)}}.grid{{grid-template-columns:1fr}}nav{{flex-direction:column}}}}@media print{{:root{{--bg:white;--panel:white;--text:#142228;--muted:#34464e;--line:#ccc;--accent:#12674c}}body{{color:var(--text)}}.grid{{display:block}}.finding{{break-inside:avoid;margin-bottom:18px}}.notice{{background:#eef7f2}}}}
</style></head><body><main><nav><strong>COMMERCE / TRUTH LAB</strong><span class="tag">{h(report['data_kind'])} data · offline prototype · v{h(report['engine_version'])}</span></nav><header><div class="tag">Founder evidence briefing</div><h1>Sales recorded.<br>Cash verified?</h1><p class="lead">Inspect the gaps between orders, customer collections and purchase signals. Every finding links back to its source evidence.</p><p class="muted">Audit cutoff: {h(report['as_of'])}. No live store connected. The report uses only the supplied export.</p></header><section class="metrics" aria-label="Audit summary"><div class="metric"><b>{s['orders']}</b><span>Orders examined</span></div><div class="metric"><b>{s['findings']}</b><span>Investigation findings</span></div><div class="metric"><b>{s['affected_orders']}</b><span>Distinct affected orders</span></div><div class="metric"><b>{s['checks_not_evaluated']}</b><span>Checks not evaluated</span></div></section><p class="notice">{h(s['amount_warning'])} A configured-policy exception is not a legal finding.</p><h2>Start with the evidence.</h2><p class="muted">Priorities are rule-based, not a financial ranking. Expand a finding to inspect the records before acting.</p><section class="grid">{''.join(cards) or '<p>No exceptions flagged. This does not establish store health; inspect coverage and withheld checks.</p>'}</section><h2>Order-level cash evidence</h2><p class="muted">Observed net customer cash = captures minus refunds, or courier collections for COD. This is not profit, accounting revenue, or bank payout. Currency totals are never combined.</p><div class="scroll"><table><thead><tr><th>Order</th><th>Market / locale</th><th>Method</th><th>Order total</th><th>Observed net customer cash</th><th>Cash evidence</th></tr></thead><tbody>{ledger}</tbody></table></div><h2>Replay the recorded journey</h2><p class="muted">Ordered by source timestamp; ties are deterministic but do not prove causal ordering.</p>{timelines}<details><summary>Inspect every rule decision</summary><div class="scroll"><table><thead><tr><th>Order</th><th>Rule</th><th>Status</th><th>Reason</th></tr></thead><tbody>{checks}</tbody></table></div></details><details><summary>Coverage declarations and audit policy</summary><pre>{h(json.dumps({'coverage': report['coverage'], 'policy': report['policy']}, indent=2))}</pre></details><footer><p>Built by Syed Muslim Shah · Commerce Truth Lab · No autonomous financial or advertising actions.</p><p>Canonical input SHA-256: <code>{h(report['input_sha256'])}</code></p><p>All demo figures are synthetic. Findings require source-system verification; no causal lift or recovered revenue is claimed.</p></footer></main></body></html>'''
