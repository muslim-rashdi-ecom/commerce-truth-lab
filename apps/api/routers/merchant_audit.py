import secrets
import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User, Workspace, Finding as FindingORM, Order as OrderORM, AuditLog as AuditLogORM
from security import get_current_user, verify_workspace_access
from schemas.workspace_schemas import AuditRunResponse
from services.merchant_audit_service import run_merchant_workspace_audit

router = APIRouter(prefix="/api/workspaces/{workspace_id}", tags=["Merchant Audit"])


@router.post("/audit/run", response_model=AuditRunResponse)
async def trigger_audit_run(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute the deterministic audit engine on tenant-isolated merchant workspace data."""
    await verify_workspace_access(workspace_id, user, db, min_role="auditor")
    try:
        res = await run_merchant_workspace_audit(workspace_id, user.id, db)
        return AuditRunResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit execution error: {str(e)}")


def build_prioritized_fixes(findings: list[FindingORM]) -> list[dict]:
    """Deterministically synthesize up to 3 prioritized fixes (P0, P1, P2) from findings."""
    fixes = []
    by_rule = {}
    for f in findings:
        by_rule.setdefault(f.rule_id, []).append(f)

    p0_candidates = [f for f in findings if f.rule_id in ("CTL-001", "CTL-002", "CTL-010") or f.severity == "critical"]
    p1_candidates = [f for f in findings if f.rule_id in ("CTL-005", "CTL-006", "CTL-007", "CTL-009") or f.severity == "high"]
    p2_candidates = [f for f in findings if f.rule_id in ("CTL-008", "CTL-003", "CTL-004", "CTL-012") or f.severity in ("medium", "low")]

    used_rule_ids = set()

    if p0_candidates:
        f0 = p0_candidates[0]
        used_rule_ids.add(f0.rule_id)
        fixes.append({
            "priority": "P0",
            "title": f"Resolve {f0.rule_name}",
            "target_rule": f0.rule_id,
            "severity": f0.severity.upper(),
            "count": len(by_rule.get(f0.rule_id, [])),
            "impact": f0.observed,
            "action_required": f0.recommended_action or f0.next_step,
            "assigned_owner": f0.owner or "Lead Web Developer / Tracking Specialist",
            "status": "Pending Remediation"
        })

    p1_remaining = [f for f in p1_candidates if f.rule_id not in used_rule_ids]
    if p1_remaining:
        f1 = p1_remaining[0]
        used_rule_ids.add(f1.rule_id)
        fixes.append({
            "priority": "P1",
            "title": f"Reconcile {f1.rule_name}",
            "target_rule": f1.rule_id,
            "severity": f1.severity.upper(),
            "count": len(by_rule.get(f1.rule_id, [])),
            "impact": f1.observed,
            "action_required": f1.recommended_action or f1.next_step,
            "assigned_owner": f1.owner or "Operations & Logistics Manager",
            "status": "Pending Remediation"
        })

    p2_remaining = [f for f in p2_candidates if f.rule_id not in used_rule_ids]
    if p2_remaining:
        f2 = p2_remaining[0]
        used_rule_ids.add(f2.rule_id)
        fixes.append({
            "priority": "P2",
            "title": f"Standardize {f2.rule_name}",
            "target_rule": f2.rule_id,
            "severity": f2.severity.upper(),
            "count": len(by_rule.get(f2.rule_id, [])),
            "impact": f2.observed,
            "action_required": f2.recommended_action or f2.next_step,
            "assigned_owner": f2.owner or "Finance Lead / Store Operations",
            "status": "Pending Remediation"
        })

    if len(fixes) < 3:
        for f in findings:
            if f.rule_id not in used_rule_ids:
                used_rule_ids.add(f.rule_id)
                p_level = f"P{len(fixes)}"
                fixes.append({
                    "priority": p_level,
                    "title": f"Address {f.rule_name}",
                    "target_rule": f.rule_id,
                    "severity": f.severity.upper(),
                    "count": len(by_rule.get(f.rule_id, [])),
                    "impact": f.observed,
                    "action_required": f.recommended_action or f.next_step,
                    "assigned_owner": f.owner or "Store Operations",
                    "status": "Pending Remediation"
                })
                if len(fixes) >= 3:
                    break

    return fixes


def build_before_after_verification_summary(findings: list[FindingORM], healthy_controls: list[FindingORM], total_orders: int) -> list[dict]:
    """Construct structured before-and-after reconciliation verification metrics."""
    by_rule = {}
    for f in findings:
        by_rule.setdefault(f.rule_id, []).append(f)

    capi_dup_count = len(by_rule.get("CTL-001", []))
    overdue_cod_count = len(by_rule.get("CTL-005", []))
    shortfall_cod_count = len(by_rule.get("CTL-006", []))
    excess_refund_count = len(by_rule.get("CTL-008", []))

    total_findings = len(findings)
    error_rate_pct = round((total_findings / total_orders * 100), 2) if total_orders > 0 else 0.0

    return [
        {
            "metric": "Total Reconciliation Exceptions",
            "pre_audit_baseline": f"{total_findings} exceptions ({error_rate_pct}% order error rate)",
            "post_fix_target": "0 unresolved exceptions",
            "verification_status": "Remediation verification pending" if total_findings > 0 else "Compliant (0 exceptions)"
        },
        {
            "metric": "Purchase Signal Deduplication (CTL-001)",
            "pre_audit_baseline": f"{capi_dup_count} duplicate signals detected" if capi_dup_count else "0 duplicate signals",
            "post_fix_target": "100% 1:1 CAPI to Browser event alignment",
            "verification_status": "Pending theme/pixel sync" if capi_dup_count else "Verified compliant"
        },
        {
            "metric": "Courier COD Remittance & Settlement (CTL-005/006)",
            "pre_audit_baseline": f"{overdue_cod_count + shortfall_cod_count} settlement variance exceptions",
            "post_fix_target": "100% cash reconciliation within contractual grace period",
            "verification_status": "Pending courier remittance claims" if (overdue_cod_count + shortfall_cod_count) > 0 else "Verified compliant"
        },
        {
            "metric": "Refund Precision & Policy Compliance (CTL-008)",
            "pre_audit_baseline": f"{excess_refund_count} excess/unauthorized refunds detected",
            "post_fix_target": "Zero refunds exceeding captured invoice balance",
            "verification_status": "Pending refund ceiling enforcement" if excess_refund_count > 0 else "Verified compliant"
        },
        {
            "metric": "Verified Healthy Controls",
            "pre_audit_baseline": f"{len(healthy_controls)} validated control transactions",
            "post_fix_target": "Baseline data consistency verified across all clean orders",
            "verification_status": "Verified (Rules confirmed non-triggering on valid records)"
        }
    ]


@router.get("/reports/{format}")
async def export_workspace_report(
    workspace_id: str,
    format: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Export an evidence-based audit report for this private merchant workspace."""
    ws = await verify_workspace_access(workspace_id, user, db, min_role="viewer")
    
    if format not in ["html", "json", "markdown", "md"]:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{format}'. Supported formats: html, json, markdown")
        
    findings = (await db.execute(
        select(FindingORM).where(FindingORM.workspace_id == workspace_id, FindingORM.is_healthy_control == False)
    )).scalars().all()
    
    healthy = (await db.execute(
        select(FindingORM).where(FindingORM.workspace_id == workspace_id, FindingORM.is_healthy_control == True)
    )).scalars().all()
    
    order_rows = (await db.execute(
        select(OrderORM.id, OrderORM.created_at).where(OrderORM.workspace_id == workspace_id)
    )).all()
    
    total_orders = len(order_rows)
    created_dates = [r[1] for r in order_rows if r[1] is not None]

    def to_iso_str(val):
        if hasattr(val, "isoformat"):
            return val.isoformat()
        return str(val) if val else None

    date_start_str = to_iso_str(min(created_dates)) if created_dates else None
    date_end_str = to_iso_str(max(created_dates)) if created_dates else None
    date_range_display = f"{date_start_str[:10]} to {date_end_str[:10]}" if date_start_str and date_end_str else "Not Specified"

    prioritized_fixes = build_prioritized_fixes(findings)
    verification_summary = build_before_after_verification_summary(findings, healthy, total_orders)
    
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Record AuditLog
    db.add(AuditLogORM(
        id=f"log_{secrets.token_hex(8)}",
        workspace_id=workspace_id,
        user_id=user.id,
        action="report_exported",
        details={"format": format, "findings_count": len(findings)},
        timestamp=now_iso
    ))
    await db.commit()
    
    if format == "json":
        export_payload = {
            "workspace_id": workspace_id,
            "workspace_name": ws.name,
            "exported_at": now_iso,
            "date_range": {
                "start": date_start_str,
                "end": date_end_str,
                "display": date_range_display
            },
            "total_orders": total_orders,
            "findings_count": len(findings),
            "healthy_controls_count": len(healthy),
            "prioritized_fixes": prioritized_fixes,
            "before_after_verification": verification_summary,
            "findings": [
                {
                    "id": f.id,
                    "rule_id": f.rule_id,
                    "rule_name": f.rule_name,
                    "category": f.category,
                    "severity": f.severity,
                    "order_id": f.order_id,
                    "observed": f.observed,
                    "amount_minor": f.amount_minor,
                    "amount_currency": f.amount_currency,
                    "confidence": f.confidence,
                    "explanation": f.explanation,
                    "recommended_action": f.recommended_action,
                    "not_proven": f.not_proven,
                    "next_step": f.next_step,
                    "status": f.status
                }
                for f in findings
            ],
            "boundary_disclaimer": "CONFIDENTIAL AUDIT REPORT — Deterministic discrepancy analysis. Does not constitute proof of fraud or legal certification."
        }
        return Response(
            content=json.dumps(export_payload, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=ctl-audit-{workspace_id}.json"}
        )
        
    elif format in ["markdown", "md"]:
        md_lines = [
            f"# Audit Report — {ws.name}",
            "",
            "> **CONFIDENTIAL MERCHANT AUDIT REPORT**",
            "> Generated by Commerce Truth Lab (CTL Engine v1.0).",
            "> Discrepancies represent deterministic reconciliation gaps based strictly on provided records.",
            "> *Anti-Hype Notice: Does not prove fraud, causal ROAS, or guarantee recovered cash.*",
            "",
            "## 1. Executive Summary",
            f"- **Workspace:** {ws.name} (`{workspace_id}`)",
            f"- **Audit Date Range:** {date_range_display}",
            f"- **Generated At:** {now_iso}",
            f"- **Total Orders Audited:** {total_orders}",
            f"- **Reconciliation Exceptions (Findings):** {len(findings)}",
            f"- **Verified Healthy Controls:** {len(healthy)}",
            "",
            "## 2. Identified Discrepancies",
            "| Rule | Severity | Order ID | Observation | Next Step |",
            "|---|---|---|---|---|"
        ]
        if findings:
            for f in findings:
                md_lines.append(f"| {f.rule_id}: {f.rule_name} | {f.severity.upper()} | {f.order_id or 'N/A'} | {f.observed} | {f.next_step} |")
        else:
            md_lines.append("| None | INFO | N/A | No discrepancies detected across checked records. | Maintain standard monitoring. |")

        md_lines.extend([
            "",
            "## 3. Prioritized Remediations (Action Plan)",
            "| Priority | Title | Severity | Impacted Area | Action Required | Owner | Status |",
            "|---|---|---|---|---|---|---|"
        ])
        if prioritized_fixes:
            for fix in prioritized_fixes:
                md_lines.append(f"| {fix['priority']} | {fix['title']} | {fix['severity']} | {fix['impact']} | {fix['action_required']} | {fix['assigned_owner']} | {fix['status']} |")
        else:
            md_lines.append("| P0-P2 | All Clear | LOW | Baseline records healthy | Maintain continuous cross-source reconciliation | All Teams | Compliant |")

        md_lines.extend([
            "",
            "## 4. Before-and-After Verification Summary",
            "| Audit Metric / Area | Pre-Audit Baseline | Post-Fix Target | Verification Status |",
            "|---|---|---|---|"
        ])
        for row in verification_summary:
            md_lines.append(f"| {row['metric']} | {row['pre_audit_baseline']} | {row['post_fix_target']} | {row['verification_status']} |")

        md_lines.extend([
            "",
            "## 5. Methodological Guardrails",
            "1. **Zero False Claims:** Findings indicate data discrepancies between sources, not confirmed theft or recovered revenue.",
            "2. **Evidence Completeness:** Incomplete evidence states are flagged explicitly (CTL-009) rather than guessed.",
            "3. **Customer Privacy:** All customer identifiers in this audit were pseudonymized with cryptographic salting prior to persistence.",
            "",
            "---",
            "*Commerce Truth Lab v1.0 — Syed Muslim Shah (Portfolio: https://syed-muslim-shah-portfolio.vercel.app/)*"
        ])
        return PlainTextResponse(
            content="\n".join(md_lines),
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=ctl-audit-{workspace_id}.md"}
        )
        
    else:  # html
        rows_html = "".join([
            f"<tr>"
            f"<td><strong>{f.rule_id}</strong><br><small>{f.rule_name}</small></td>"
            f"<td><span class='badge badge-{f.severity.lower()}'>{f.severity.upper()}</span></td>"
            f"<td><code>{f.order_id or 'N/A'}</code></td>"
            f"<td>{f.observed}</td>"
            f"<td>{f.next_step}</td>"
            f"</tr>"
            for f in findings
        ])

        fixes_html = "".join([
            f"<tr>"
            f"<td><span class='badge badge-{fix['priority'].lower()}'><strong>{fix['priority']}</strong></span></td>"
            f"<td><strong>{fix['title']}</strong><br><small>{fix['target_rule']} ({fix['severity']})</small></td>"
            f"<td>{fix['impact']}</td>"
            f"<td>{fix['action_required']}</td>"
            f"<td>{fix['assigned_owner']}</td>"
            f"</tr>"
            for fix in prioritized_fixes
        ])

        verification_html = "".join([
            f"<tr>"
            f"<td><strong>{v['metric']}</strong></td>"
            f"<td>{v['pre_audit_baseline']}</td>"
            f"<td>{v['post_fix_target']}</td>"
            f"<td><em>{v['verification_status']}</em></td>"
            f"</tr>"
            for v in verification_summary
        ])
        
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Commerce Truth Lab — Audit Report: {ws.name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.5; color: #1e293b; background: #f8fafc; padding: 32px; max-width: 1100px; margin: 0 auto; }}
        .header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 24px; }}
        .banner {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 4px; margin-bottom: 24px; font-size: 14px; color: #1e40af; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }}
        .card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card h4 {{ margin: 0 0 8px 0; font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }}
        .card .num {{ font-size: 24px; font-weight: 700; color: #0f172a; }}
        table {{ width: 100%; border-collapse: collapse; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin-bottom: 32px; }}
        th {{ background: #f1f5f9; text-align: left; padding: 12px; font-size: 12px; text-transform: uppercase; color: #475569; letter-spacing: 0.05em; }}
        td {{ padding: 12px; border-top: 1px solid #e2e8f0; font-size: 13px; vertical-align: top; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }}
        .badge-critical, .badge-p0 {{ background: #fee2e2; color: #991b1b; }}
        .badge-high, .badge-p1 {{ background: #ffedd5; color: #9a3412; }}
        .badge-medium, .badge-p2 {{ background: #fef9c3; color: #854d0e; }}
        .badge-low {{ background: #e0e7ff; color: #3730a3; }}
        code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; }}
        .footer {{ font-size: 12px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 24px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Commerce Truth Lab — Audit Report</h1>
        <p style="color: #64748b; margin: 4px 0 0 0;">Workspace: <strong>{ws.name}</strong> ({workspace_id}) &bull; Date Range: <strong>{date_range_display}</strong> &bull; Generated: {now_iso}</p>
    </div>
    
    <div class="banner">
        <strong>Confidential Merchant Audit:</strong> Deterministic discrepancy detection based strictly on uploaded records. Customer identifiers are pseudonymized with salted cryptographic hashes. Discrepancies reflect reconciliation variance and missing signals, not verified fraud or recovered cash.
    </div>
    
    <div class="metrics">
        <div class="card">
            <h4>Audited Orders</h4>
            <div class="num">{total_orders}</div>
        </div>
        <div class="card">
            <h4>Date Range</h4>
            <div class="num" style="font-size: 16px; padding-top: 6px;">{date_range_display}</div>
        </div>
        <div class="card">
            <h4>Exceptions Detected</h4>
            <div class="num" style="color: #dc2626;">{len(findings)}</div>
        </div>
        <div class="card">
            <h4>Healthy Controls</h4>
            <div class="num" style="color: #16a34a;">{len(healthy)}</div>
        </div>
    </div>
    
    <h2>1. Prioritized Remediation Action Plan</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">Priority</th>
                <th style="width: 25%;">Target Rule / Title</th>
                <th style="width: 25%;">Impact Observation</th>
                <th>Remediation Action Required</th>
                <th style="width: 18%;">Owner</th>
            </tr>
        </thead>
        <tbody>
            {fixes_html if prioritized_fixes else "<tr><td colspan='5' style='text-align: center; color: #64748b; padding: 20px;'>No prioritized fixes needed — all records compliant.</td></tr>"}
        </tbody>
    </table>

    <h2>2. Before-and-After Verification Summary</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Audit Metric / Area</th>
                <th style="width: 26%;">Pre-Audit Baseline</th>
                <th style="width: 26%;">Post-Fix Target</th>
                <th>Verification Status</th>
            </tr>
        </thead>
        <tbody>
            {verification_html}
        </tbody>
    </table>

    <h2>3. Reconciliation Discrepancies ({len(findings)})</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Rule</th>
                <th style="width: 12%;">Severity</th>
                <th style="width: 15%;">Order ID</th>
                <th>Observation</th>
                <th style="width: 22%;">Recommended Next Step</th>
            </tr>
        </thead>
        <tbody>
            {rows_html if findings else "<tr><td colspan='5' style='text-align: center; color: #64748b; padding: 32px;'>No audit discrepancies detected. All checked records conform to reconciliation rules.</td></tr>"}
        </tbody>
    </table>
    
    <div class="footer">
        Commerce Truth Lab v1.0 &bull; Evidence-First E-Commerce Audit Engine &bull; Founded by <a href="https://syed-muslim-shah-portfolio.vercel.app/" target="_blank">Syed Muslim Shah</a>
    </div>
</body>
</html>"""
        return HTMLResponse(
            content=html_doc,
            headers={"Content-Disposition": f"inline; filename=ctl-audit-{workspace_id}.html"}
        )

