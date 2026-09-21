import secrets
import datetime
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from models import (
    Order as OrderORM, Payment as PaymentORM, CourierSettlement as CourierSettlementORM,
    Refund as RefundORM, PurchaseSignal as PurchaseSignalORM, DataSource as DataSourceORM,
    Finding as FindingORM, AuditRun as AuditRunORM, AuditLog as AuditLogORM, Workspace as WorkspaceORM
)
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult,
    PaymentMethod, OrderStatus, SettlementStatus, Currency
)
from ctl_engine.runner import AuditEngine

def _normalize_payment_method(val: str) -> PaymentMethod:
    v = (val or "").lower().strip()
    if "cod" in v or "cash" in v:
        return PaymentMethod.cod
    elif "bank" in v or "wire" in v:
        return PaymentMethod.bank_transfer
    return PaymentMethod.prepaid

def _normalize_order_status(val: str) -> OrderStatus:
    v = (val or "").lower().strip()
    if v in ["delivered", "fulfilled", "completed"]:
        return OrderStatus.delivered
    elif v in ["shipped", "in_transit", "dispatch"]:
        return OrderStatus.shipped
    elif v in ["confirmed", "paid", "authorized"]:
        return OrderStatus.confirmed
    elif v in ["cancelled", "void", "voided"]:
        return OrderStatus.cancelled
    elif v in ["returned", "refunded"]:
        return OrderStatus.returned
    return OrderStatus.pending

def _normalize_settlement_status(val: str) -> SettlementStatus:
    v = (val or "").lower().strip()
    if v in ["settled", "paid", "completed"]:
        return SettlementStatus.settled
    elif v in ["partial", "partially_settled"]:
        return SettlementStatus.partial
    elif v in ["overdue"]:
        return SettlementStatus.overdue
    return SettlementStatus.pending

async def run_merchant_workspace_audit(
    workspace_id: str,
    user_id: str,
    db: AsyncSession
) -> Dict[str, Any]:
    # 1. Fetch workspace records
    orders_orm = (await db.execute(
        select(OrderORM).where(OrderORM.workspace_id == workspace_id)
    )).scalars().all()
    
    if not orders_orm:
        raise ValueError("No orders uploaded in this workspace yet. Please upload Shopify orders first.")
        
    payments_orm = (await db.execute(
        select(PaymentORM).where(PaymentORM.workspace_id == workspace_id)
    )).scalars().all()
    
    settlements_orm = (await db.execute(
        select(CourierSettlementORM).where(CourierSettlementORM.workspace_id == workspace_id)
    )).scalars().all()
    
    refunds_orm = (await db.execute(
        select(RefundORM).where(RefundORM.workspace_id == workspace_id)
    )).scalars().all()
    
    signals_orm = (await db.execute(
        select(PurchaseSignalORM).where(PurchaseSignalORM.workspace_id == workspace_id)
    )).scalars().all()
    
    sources_orm = (await db.execute(
        select(DataSourceORM).where(DataSourceORM.workspace_id == workspace_id)
    )).scalars().all()
    
    # 2. Convert ORM records to shared Pydantic models for the audit engine
    orders = [
        Order(
            id=o.id,
            store_id=o.store_id or "store",
            created_at=datetime.datetime.fromisoformat(o.created_at.replace("Z", "+00:00")) if "T" in o.created_at else datetime.datetime.now(datetime.timezone.utc),
            currency=o.currency,
            total_amount_minor=o.total_amount_minor,
            payment_method=_normalize_payment_method(o.payment_method),
            status=_normalize_order_status(o.status),
            customer_id=o.customer_id or "CUST_ANONYMOUS",
            tags=[]
        ) for o in orders_orm
    ]
    
    payments = [
        Payment(
            id=p.id,
            order_id=p.order_id,
            captured_at=datetime.datetime.fromisoformat(p.captured_at.replace("Z", "+00:00")) if "T" in p.captured_at else datetime.datetime.now(datetime.timezone.utc),
            currency=p.currency,
            amount_minor=p.amount_minor,
            method=_normalize_payment_method(p.method),
            gateway=p.gateway or "stripe",
            status=p.status or "captured"
        ) for p in payments_orm
    ]
    
    settlements = [
        CourierSettlement(
            id=s.id,
            order_id=s.order_id,
            courier_name=s.courier_name,
            delivered_at=datetime.datetime.fromisoformat(s.delivered_at.replace("Z", "+00:00")) if "T" in s.delivered_at else datetime.datetime.now(datetime.timezone.utc),
            collected_amount_minor=s.collected_amount_minor,
            settled_amount_minor=s.settled_amount_minor,
            collection_currency=s.collection_currency,
            settlement_status=_normalize_settlement_status(s.settlement_status),
            grace_days=s.grace_days
        ) for s in settlements_orm
    ]

    
    refunds = [
        Refund(
            id=r.id,
            order_id=r.order_id,
            refunded_at=datetime.datetime.fromisoformat(r.refunded_at.replace("Z", "+00:00")) if "T" in r.refunded_at else datetime.datetime.now(datetime.timezone.utc),
            currency=r.currency,
            amount_minor=r.amount_minor,
            reason=r.reason or "return"
        ) for r in refunds_orm
    ]
    
    signals = [
        PurchaseSignal(
            id=sig.id,
            order_id=sig.order_id,
            signal_type=sig.signal_type or "browser",
            platform=sig.platform or "meta",
            event_name=sig.event_name or "Purchase",
            event_id=sig.event_id or "evt_none",
            reported_at=datetime.datetime.fromisoformat(sig.reported_at.replace("Z", "+00:00")) if "T" in sig.reported_at else datetime.datetime.now(datetime.timezone.utc),
            currency=sig.currency,
            value_minor=sig.value_minor,
            consent_granted=sig.consent_granted if sig.consent_granted is not None else True,
            pixel_id=sig.pixel_id or "P1"
        ) for sig in signals_orm
    ]
    
    sources = [
        DataSource(
            id=ds.id,
            name=ds.name,
            source_type=ds.source_type,
            date_range_start=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
            date_range_end=datetime.datetime.now(datetime.timezone.utc),
            currency=ds.currency or "USD",
            coverage_status=ds.coverage_status or "full",
            completeness_status=ds.completeness_status or "good",
            last_processed=datetime.datetime.now(datetime.timezone.utc),
            record_count=ds.record_count
        ) for ds in sources_orm
    ]
    
    # 3. Execute backend deterministic audit engine
    engine = AuditEngine()
    audit_result = engine.run(orders, payments, settlements, refunds, signals, sources)
    
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    audit_id = f"aud_{secrets.token_hex(8)}"
    
    # 4. Clear previous findings for this workspace
    await db.execute(delete(FindingORM).where(FindingORM.workspace_id == workspace_id))
    
    # 5. Persist new findings
    for f in audit_result.findings:
        f_orm = FindingORM(
            id=f"f_{secrets.token_hex(8)}",
            workspace_id=workspace_id,
            rule_id=f.rule_id,
            rule_name=f.rule_name,
            category=f.category.value if hasattr(f.category, "value") else str(f.category),
            severity=f.severity.value if hasattr(f.severity, "value") else str(f.severity),
            order_id=f.order_id,
            observed=f.observed,
            source_records=[r.model_dump() if hasattr(r, "model_dump") else r for r in f.source_records] if f.source_records else [],
            assumptions=f.assumptions or [],
            not_proven=f.not_proven or [],
            next_step=f.next_step,
            owner=f.owner,
            amount_minor=f.amount_minor,
            amount_currency=f.amount_currency.value if hasattr(f.amount_currency, "value") else (str(f.amount_currency) if f.amount_currency else None),
            confidence=f.confidence,
            explanation=f.explanation,
            recommended_action=f.recommended_action,
            status="open",
            is_healthy_control=False
        )
        db.add(f_orm)
        
    for hc in audit_result.healthy_controls:
        hc_orm = FindingORM(
            id=f"hc_{secrets.token_hex(8)}",
            workspace_id=workspace_id,
            rule_id=hc.rule_id,
            rule_name=hc.rule_name,
            category=hc.category.value if hasattr(hc.category, "value") else str(hc.category),
            severity=hc.severity.value if hasattr(hc.severity, "value") else str(hc.severity),
            order_id=hc.order_id,
            observed=hc.observed,
            source_records=[r.model_dump() if hasattr(r, "model_dump") else r for r in hc.source_records] if hc.source_records else [],
            assumptions=hc.assumptions or [],
            not_proven=hc.not_proven or [],
            next_step=hc.next_step,
            owner=hc.owner,
            amount_minor=hc.amount_minor,
            amount_currency=hc.amount_currency.value if hasattr(hc.amount_currency, "value") else (str(hc.amount_currency) if hc.amount_currency else None),
            confidence=hc.confidence,
            explanation=hc.explanation,
            recommended_action=hc.recommended_action,
            status="verified",
            is_healthy_control=True
        )
        db.add(hc_orm)

        
    # 6. Record AuditRun
    run_record = AuditRunORM(
        id=audit_id,
        workspace_id=workspace_id,
        status="completed",
        evaluated_orders=len(orders),
        total_findings=len(audit_result.findings),
        healthy_controls_count=len(audit_result.healthy_controls),
        summary={
            "total_orders": len(orders),
            "findings_count": len(audit_result.findings),
            "healthy_controls": len(audit_result.healthy_controls),
            "run_at": now_iso
        },
        created_at=now_iso,
        completed_at=now_iso
    )
    db.add(run_record)
    
    # 7. Record AuditLog
    db.add(AuditLogORM(
        id=f"log_{secrets.token_hex(8)}",
        workspace_id=workspace_id,
        user_id=user_id,
        action="audit_executed",
        details={"audit_id": audit_id, "findings": len(audit_result.findings), "orders": len(orders)},
        timestamp=now_iso
    ))
    
    await db.commit()
    
    return {
        "audit_id": audit_id,
        "status": "completed",
        "evaluated_orders": len(orders),
        "total_findings": len(audit_result.findings),
        "healthy_controls_count": len(audit_result.healthy_controls),
        "completed_at": now_iso
    }
