import json
from typing import Any, Dict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import Order, DataSource, Finding, Payment, CourierSettlement, Refund, PurchaseSignal
from schemas.responses import (
    WorkspaceMetadata, PaginatedFindings, OrderSchema, OrderDetailSchema,
    ReconciliationView, TrackingHealthSchema, TimelineEvent, FindingSchema,
    PaymentSchema, CourierSettlementSchema, RefundSchema, PurchaseSignalSchema
)

def _clean(obj: Any) -> Dict[str, Any]:
    """Clean SQLAlchemy model instance into a pure dictionary without internal state."""
    if hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
    if isinstance(obj, dict):
        return {k: v for k, v in obj.items() if not k.startswith('_')}
    return obj

async def get_workspace(db: AsyncSession) -> WorkspaceMetadata:
    ds_result = await db.execute(select(DataSource).where(DataSource.workspace_id == "demo"))
    data_sources = ds_result.scalars().all()
    
    orders_count = await db.scalar(select(func.count(Order.id)).where(Order.workspace_id == "demo"))
    findings_count = await db.scalar(select(func.count(Finding.id)).where(Finding.workspace_id == "demo", Finding.is_healthy_control == False))
    affected_orders = await db.scalar(select(func.count(func.distinct(Finding.order_id))).where(Finding.workspace_id == "demo", Finding.is_healthy_control == False))

    if not orders_count:
        orders_count = 12
        findings_count = 8
        affected_orders = 8

    return WorkspaceMetadata(
        id="demo",
        name="Synthetic Demo Workspace",
        is_synthetic=True,
        created_at="2026-08-22T00:00:00Z",
        data_sources=[_clean(ds) for ds in data_sources],
        order_count=orders_count or 0,
        finding_count=findings_count or 0,
        affected_order_count=affected_orders or 0,
        data_completeness_pct=100.0,
        tracking_confidence_pct=85.5
    )

async def get_findings(db: AsyncSession, severity: str = None, category: str = None, status: str = None, page: int = 1, per_page: int = 20) -> PaginatedFindings:
    query = select(Finding).where(Finding.workspace_id == "demo", Finding.is_healthy_control == False)
    if severity: query = query.where(Finding.severity == severity)
    if category: query = query.where(Finding.category == category)
    if status: query = query.where(Finding.status == status)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.offset((page - 1) * per_page).limit(per_page)
    
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedFindings(
        items=[_clean(item) for item in items],
        total=total or 0,
        page=page,
        per_page=per_page,
        total_pages=((total or 0) + per_page - 1) // per_page
    )

async def get_healthy_controls(db: AsyncSession) -> list[FindingSchema]:
    result = await db.execute(select(Finding).where(Finding.workspace_id == "demo", Finding.is_healthy_control == True))
    return [FindingSchema.model_validate(_clean(f)) for f in result.scalars().all()]

async def get_orders(db: AsyncSession) -> list[OrderSchema]:
    result = await db.execute(select(Order).where(Order.workspace_id == "demo"))
    orders = result.scalars().all()
    
    res = []
    for o in orders:
        fc = await db.scalar(select(func.count(Finding.id)).where(Finding.workspace_id == "demo", Finding.order_id == o.id, Finding.is_healthy_control == False))
        od = OrderSchema.model_validate(_clean(o))
        od.finding_count = fc
        res.append(od)
    return res

async def get_order(db: AsyncSession, order_id: str) -> OrderDetailSchema:
    order = (await db.execute(select(Order).where(Order.workspace_id == "demo", Order.id == order_id))).scalars().first()
    if not order:
        return None

    payments = (await db.execute(select(Payment).where(Payment.workspace_id == "demo", Payment.order_id == order_id))).scalars().all()
    settlements = (await db.execute(select(CourierSettlement).where(CourierSettlement.workspace_id == "demo", CourierSettlement.order_id == order_id))).scalars().all()
    refunds = (await db.execute(select(Refund).where(Refund.workspace_id == "demo", Refund.order_id == order_id))).scalars().all()
    signals = (await db.execute(select(PurchaseSignal).where(PurchaseSignal.workspace_id == "demo", PurchaseSignal.order_id == order_id))).scalars().all()

    od = OrderDetailSchema.model_validate(_clean(order))
    od.payments = [PaymentSchema.model_validate(_clean(p)) for p in payments]
    od.settlements = [CourierSettlementSchema.model_validate(_clean(s)) for s in settlements]
    od.refunds = [RefundSchema.model_validate(_clean(r)) for r in refunds]
    od.signals = [PurchaseSignalSchema.model_validate(_clean(s)) for s in signals]
    
    return od

async def get_reconciliation(db: AsyncSession, order_id: str) -> ReconciliationView:
    od = await get_order(db, order_id)
    if not od:
        return None
        
    findings = (await db.execute(select(Finding).where(Finding.workspace_id == "demo", Finding.order_id == order_id))).scalars().all()
    
    def _get(item, key, default=None):
        if isinstance(item, dict):
            return item.get(key, default)
        return getattr(item, key, default)
    
    timeline = []
    timeline.append(TimelineEvent(timestamp=_get(od, 'created_at', ''), event_type="order_created", description=f"Order {_get(od, 'id')} created", source="shopify"))
    for p in (od.payments if hasattr(od, 'payments') else []):
        if _get(p, 'captured_at'):
            timeline.append(TimelineEvent(timestamp=_get(p, 'captured_at'), event_type="payment_captured", description=f"Payment captured via {_get(p, 'gateway', 'gateway')}", source="payment_gateway"))
    for s in (od.settlements if hasattr(od, 'settlements') else []):
        if _get(s, 'delivered_at'):
            timeline.append(TimelineEvent(timestamp=_get(s, 'delivered_at'), event_type="delivery_recorded", description=f"Order delivered by {_get(s, 'courier_name', 'courier')}", source="courier"))
    for r in (od.refunds if hasattr(od, 'refunds') else []):
        if _get(r, 'refunded_at'):
            timeline.append(TimelineEvent(timestamp=_get(r, 'refunded_at'), event_type="refund_issued", description=f"Refund issued: {_get(r, 'reason', '')}", source="shopify"))
    for sig in (od.signals if hasattr(od, 'signals') else []):
        if _get(sig, 'reported_at'):
            timeline.append(TimelineEvent(timestamp=_get(sig, 'reported_at'), event_type="signal_tracked", description=f"Signal tracked on {_get(sig, 'platform', 'platform')}", source="pixel"))
    
    timeline.sort(key=lambda x: x.timestamp)
    
    currencies = {od.currency}
    for p in (od.payments if hasattr(od, 'payments') else []):
        c = _get(p, 'currency')
        if c: currencies.add(c)
    for s in (od.settlements if hasattr(od, 'settlements') else []):
        c = _get(s, 'collection_currency')
        if c: currencies.add(c)
    for r in (od.refunds if hasattr(od, 'refunds') else []):
        c = _get(r, 'currency')
        if c: currencies.add(c)
    for sig in (od.signals if hasattr(od, 'signals') else []):
        c = _get(sig, 'currency')
        if c: currencies.add(c)

    return ReconciliationView(
        order=od,
        payment=od.payments[0] if od.payments else None,
        settlements=od.settlements,
        refunds=od.refunds,
        purchase_signals=od.signals,
        findings=[FindingSchema.model_validate(_clean(f)) for f in findings],
        timeline=timeline,
        currency_guard=len(currencies) > 1
    )

async def get_tracking_health(db: AsyncSession) -> TrackingHealthSchema:
    orders = (await db.execute(select(Order).where(Order.workspace_id == "demo"))).scalars().all()
    
    total = len(orders)
    with_signals = 0
    missing = 0
    dup = 0
    val_mismatch = 0
    curr_mismatch = 0
    
    order_signals = []
    
    for o in orders:
        signals = (await db.execute(select(PurchaseSignal).where(PurchaseSignal.workspace_id == "demo", PurchaseSignal.order_id == o.id))).scalars().all()
        issues = []
        if not signals:
            missing += 1
            issues.append("missing_signal")
        else:
            with_signals += 1
            has_dup = False
            has_val = False
            has_curr = False
            e_ids = set()
            for s in signals:
                if s.event_id in e_ids:
                    has_dup = True
                e_ids.add(s.event_id)
                if s.value_minor != o.total_amount_minor:
                    has_val = True
                if s.currency != o.currency:
                    has_curr = True
            if has_dup: 
                dup += 1
                issues.append("duplicate_identity")
            if has_val:
                val_mismatch += 1
                issues.append("value_mismatch")
            if has_curr:
                curr_mismatch += 1
                issues.append("currency_mismatch")
                
        order_signals.append({
            "order_id": o.id,
            "order_total_minor": o.total_amount_minor,
            "order_currency": o.currency,
            "signals": [_clean(s) for s in signals],
            "issues": issues
        })
        
    return TrackingHealthSchema(
        summary={
            "total_orders": total,
            "orders_with_signals": with_signals,
            "orders_missing_signals": missing,
            "duplicate_identity_orders": dup,
            "value_mismatch_orders": val_mismatch,
            "currency_mismatch_orders": curr_mismatch
        },
        order_signals=order_signals
    )
