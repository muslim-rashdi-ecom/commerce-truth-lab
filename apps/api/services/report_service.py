import json
from typing import List
from schemas.responses import FindingSchema

def generate_html_report(findings: List[FindingSchema], healthy_controls: List[FindingSchema], stats: dict) -> str:
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Commerce Truth Lab — Audit Report</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
            .warning {{ background: #fff3cd; color: #856404; padding: 10px; border-left: 4px solid #ffeeba; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            .severity-high {{ color: #dc3545; font-weight: bold; }}
            .severity-medium {{ color: #fd7e14; font-weight: bold; }}
            .severity-low {{ color: #ffc107; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Commerce Truth Lab — Audit Report</h1>
        <div class="warning">
            <strong>NOTE:</strong> All data in this report is SYNTHETIC and generated for demonstration purposes only.
        </div>
        
        <h2>Executive Summary</h2>
        <p>Total Orders Audited: {stats.get('total_orders', 0)}</p>
        <p>Total Findings: {stats.get('total_findings', 0)}</p>
        
        <h2>Findings</h2>
        <table>
            <tr><th>Severity</th><th>Rule</th><th>Order ID</th><th>Observation</th></tr>
            """
    for f in findings:
        html += f"<tr><td class='severity-{f.severity.lower()}'>{f.severity}</td><td>{f.rule_name}</td><td>{f.order_id}</td><td>{f.observed}</td></tr>"
        
    html += """
        </table>

        <h2>Methodology</h2>
        <p>CTL-001: Identifies duplicate purchase signals for a single order by checking identity signals.</p>
        <p>CTL-002: Detects missing purchase signals for confirmed orders.</p>
        <p>CTL-003: Flags orders with misaligned tracking values (e.g. currency mismatch by 100x).</p>
        <p>CTL-004: Flags orders with currency discrepancies between shop and pixel tracking.</p>
        <p>CTL-005: Flags COD orders where settled amount differs from collected amount.</p>
        <p>CTL-007: Flags COD over-collection anomalies.</p>
        <p>CTL-008: Flags refunds that exceed the initial transaction minor amount.</p>
        <p>CTL-009: Detects missing settlements after grace period.</p>

        <h2>Assumptions & Limitations</h2>
        <p>The rules rely on accurate and un-tampered data ingestion. Timezones are standardized to UTC.</p>
        <p>This is a synthetic demonstration limited to specific test vectors.</p>

        <h2>Next Steps</h2>
        <p>Investigate High severity alerts, starting with COD settlement anomalies and missing tracking events.</p>

        <footer>
            <p>Built by Syed Muslim Shah — <a href="https://syed-muslim-shah-portfolio.vercel.app/">https://syed-muslim-shah-portfolio.vercel.app/</a></p>
        </footer>
    </body>
    </html>
    """
    return html

def generate_markdown_report(findings: List[FindingSchema], healthy_controls: List[FindingSchema], stats: dict) -> str:
    md = f"""# Commerce Truth Lab — Audit Report

> **NOTE:** All data in this report is SYNTHETIC and generated for demonstration purposes only.

## Executive Summary
- **Total Orders Audited:** {stats.get('total_orders', 0)}
- **Total Findings:** {stats.get('total_findings', 0)}

## Findings
| Severity | Rule | Order ID | Observation |
|---|---|---|---|
"""
    for f in findings:
        md += f"| {f.severity} | {f.rule_name} | {f.order_id} | {f.observed} |\n"
        
    md += """
## Methodology
- **CTL-001**: Identifies duplicate purchase signals.
- **CTL-002**: Detects missing purchase signals.
- **CTL-003**: Flags value mismatches in tracking.
- **CTL-004**: Flags currency mismatches in tracking.
- **CTL-005**: Flags COD partial settlements.
- **CTL-007**: Flags COD over-collections.
- **CTL-008**: Flags excessive refunds.
- **CTL-009**: Detects missing settlements after grace period.

## Assumptions & Limitations
The rules rely on accurate and un-tampered data ingestion. Timezones are standardized to UTC. This is a synthetic demonstration limited to specific test vectors.

## Next Steps
Investigate High severity alerts, starting with COD settlement anomalies and missing tracking events.

---
*Built by Syed Muslim Shah — [https://syed-muslim-shah-portfolio.vercel.app/](https://syed-muslim-shah-portfolio.vercel.app/)*
"""
    return md
