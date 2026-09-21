import secrets
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from database import get_db
from models import (
    User, Workspace, WorkspaceMember, Order, Payment, CourierSettlement, 
    Refund, PurchaseSignal, DataSource, Finding, AuditRun, AuditLog
)
from security import get_current_user, verify_workspace_access
from schemas.workspace_schemas import (
    CreateWorkspaceRequest, WorkspaceResponse, AuditLogResponse
)
from schemas.responses import (
    OrderSchema, FindingSchema, ReconciliationView, TimelineEvent, PaginatedFindings
)

router = APIRouter(prefix="/api/workspaces", tags=["Workspaces"])

@router.get("", response_model=List[WorkspaceResponse])
async def list_workspaces(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all private workspaces accessible to the authenticated merchant."""
    # Find all workspace IDs where user is owner or member
    stmt = (
        select(Workspace)
        .outerjoin(WorkspaceMember, Workspace.id == WorkspaceMember.workspace_id)
        .where(
            (Workspace.owner_id == user.id) | 
            (WorkspaceMember.user_id == user.id)
        )
        .distinct()
    )
    workspaces = (await db.execute(stmt)).scalars().all()
    
    result = []
    for ws in workspaces:
        # Calculate live counts
        order_count = (await db.execute(
            select(func.count(Order.id)).where(Order.workspace_id == ws.id)
        )).scalar() or 0
        
        finding_count = (await db.execute(
            select(func.count(Finding.id)).where(Finding.workspace_id == ws.id, Finding.is_healthy_control == False)
        )).scalar() or 0
        
        # Latest audit run
        latest_audit = (await db.execute(
            select(AuditRun).where(AuditRun.workspace_id == ws.id).order_by(desc(AuditRun.created_at))
        )).scalars().first()
        
        result.append(WorkspaceResponse(
            id=ws.id,
            name=ws.name,
            owner_id=ws.owner_id,
            currency=ws.currency,
            is_synthetic=ws.is_synthetic,
            created_at=ws.created_at,
            order_count=order_count,
            finding_count=finding_count,
            data_completeness_pct=100.0 if order_count > 0 else 0.0,
            latest_audit_status=latest_audit.status if latest_audit else "not_run"
        ))
    return result

@router.post("", response_model=WorkspaceResponse)
async def create_workspace(
    req: CreateWorkspaceRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new private isolated merchant workspace."""
    ws_id = f"ws_{secrets.token_hex(6)}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    ws = Workspace(
        id=ws_id,
        name=req.name.strip(),
        owner_id=user.id,
        currency=req.currency.upper(),
        is_synthetic=False,
        created_at=now_iso
    )
    db.add(ws)
    
    member = WorkspaceMember(
        id=f"mem_{secrets.token_hex(6)}",
        workspace_id=ws_id,
        user_id=user.id,
        role="admin",
        joined_at=now_iso
    )
    db.add(member)
    
    log = AuditLog(
        id=f"log_{secrets.token_hex(8)}",
        workspace_id=ws_id,
        user_id=user.id,
        action="workspace_created",
        details={"name": ws.name, "currency": ws.currency},
        timestamp=now_iso
    )
    db.add(log)
    
    await db.commit()
    await db.refresh(ws)
    
    return WorkspaceResponse(
        id=ws.id,
        name=ws.name,
        owner_id=ws.owner_id,
        currency=ws.currency,
        is_synthetic=ws.is_synthetic,
        created_at=ws.created_at,
        order_count=0,
        finding_count=0,
        data_completeness_pct=0.0,
        latest_audit_status="not_run"
    )

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Fetch details for a specific workspace with strict tenant access control."""
    ws = await verify_workspace_access(workspace_id, user, db)
    
    order_count = (await db.execute(
        select(func.count(Order.id)).where(Order.workspace_id == ws.id)
    )).scalar() or 0
    
    finding_count = (await db.execute(
        select(func.count(Finding.id)).where(Finding.workspace_id == ws.id, Finding.is_healthy_control == False)
    )).scalar() or 0
    
    latest_audit = (await db.execute(
        select(AuditRun).where(AuditRun.workspace_id == ws.id).order_by(desc(AuditRun.created_at))
    )).scalars().first()
    
    return WorkspaceResponse(
        id=ws.id,
        name=ws.name,
        owner_id=ws.owner_id,
        currency=ws.currency,
        is_synthetic=ws.is_synthetic,
        created_at=ws.created_at,
        order_count=order_count,
        finding_count=finding_count,
        data_completeness_pct=100.0 if order_count > 0 else 0.0,
        latest_audit_status=latest_audit.status if latest_audit else "not_run"
    )

@router.get("/{workspace_id}/orders", response_model=List[OrderSchema])
async def get_workspace_orders(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders strictly scoped to this merchant workspace."""
    await verify_workspace_access(workspace_id, user, db)
    orders = (await db.execute(
        select(Order).where(Order.workspace_id == workspace_id).order_by(desc(Order.created_at))
    )).scalars().all()
    
    res = []
    for o in orders:
        f_count = (await db.execute(
            select(func.count(Finding.id)).where(Finding.workspace_id == workspace_id, Finding.order_id == o.id)
        )).scalar() or 0
        res.append(OrderSchema(
            id=o.id,
            store_id=o.store_id,
            created_at=o.created_at,
            currency=o.currency,
            total_amount_minor=o.total_amount_minor,
            payment_method=o.payment_method,
            status=o.status,
            customer_id=o.customer_id,
            is_synthetic=o.is_synthetic,
            finding_count=f_count
        ))
    return res

@router.get("/{workspace_id}/findings", response_model=PaginatedFindings)
async def get_workspace_findings(
    workspace_id: str,
    severity: Optional[str] = None,
    category: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get findings strictly scoped to this merchant workspace."""
    await verify_workspace_access(workspace_id, user, db)
    stmt = select(Finding).where(Finding.workspace_id == workspace_id)
    if severity:
        stmt = stmt.where(Finding.severity.ilike(severity))
    if category:
        stmt = stmt.where(Finding.category.ilike(category))
    
    findings = (await db.execute(stmt)).scalars().all()
    items = [FindingSchema.model_validate(f.__dict__) for f in findings]
    
    return PaginatedFindings(
        items=items,
        total=len(items),
        page=1,
        per_page=len(items) or 20,
        total_pages=1
    )

@router.get("/{workspace_id}/reconciliation/{order_id}", response_model=ReconciliationView)
async def get_workspace_reconciliation(
    workspace_id: str,
    order_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Reconcile an order within the merchant's workspace boundary."""
    await verify_workspace_access(workspace_id, user, db)
    
    od = (await db.execute(
        select(Order).where(Order.workspace_id == workspace_id, Order.id == order_id)
    )).scalars().first()
    if not od:
        raise HTTPException(status_code=404, detail="Order not found in this workspace")
    
    payments = (await db.execute(
        select(Payment).where(Payment.workspace_id == workspace_id, Payment.order_id == order_id)
    )).scalars().all()
    
    settlements = (await db.execute(
        select(CourierSettlement).where(CourierSettlement.workspace_id == workspace_id, CourierSettlement.order_id == order_id)
    )).scalars().all()
    
    refunds = (await db.execute(
        select(Refund).where(Refund.workspace_id == workspace_id, Refund.order_id == order_id)
    )).scalars().all()
    
    signals = (await db.execute(
        select(PurchaseSignal).where(PurchaseSignal.workspace_id == workspace_id, PurchaseSignal.order_id == order_id)
    )).scalars().all()
    
    findings = (await db.execute(
        select(Finding).where(Finding.workspace_id == workspace_id, Finding.order_id == order_id)
    )).scalars().all()
    
    timeline = [
        TimelineEvent(timestamp=od.created_at, event_type="order_created", description=f"Order {od.id} created", source="shopify")
    ]
    for p in payments:
        timeline.append(TimelineEvent(timestamp=p.captured_at, event_type="payment_captured", description=f"Payment captured via {p.gateway or p.method}", source="gateway"))
    for s in settlements:
        timeline.append(TimelineEvent(timestamp=s.delivered_at, event_type="delivery_recorded", description=f"Delivered by {s.courier_name}", source="courier"))
    for r in refunds:
        timeline.append(TimelineEvent(timestamp=r.refunded_at, event_type="refund_issued", description=f"Refund issued: {r.reason}", source="shopify"))
    for sig in signals:
        timeline.append(TimelineEvent(timestamp=sig.reported_at, event_type="signal_tracked", description=f"Signal tracked on {sig.platform}", source="pixel"))
    
    timeline.sort(key=lambda x: x.timestamp)
    
    currencies = {od.currency}
    for p in payments: currencies.add(p.currency)
    for s in settlements: currencies.add(s.collection_currency)
    for r in refunds: currencies.add(r.currency)
    for sig in signals: currencies.add(sig.currency)
    
    order_schema = OrderSchema(
        id=od.id,
        store_id=od.store_id,
        created_at=od.created_at,
        currency=od.currency,
        total_amount_minor=od.total_amount_minor,
        payment_method=od.payment_method,
        status=od.status,
        customer_id=od.customer_id,
        is_synthetic=od.is_synthetic,
        finding_count=len(findings)
    )
    
    return ReconciliationView(
        order=order_schema,
        payment=payments[0].__dict__ if payments else None,
        settlements=[s.__dict__ for s in settlements],
        refunds=[r.__dict__ for r in refunds],
        purchase_signals=[sig.__dict__ for sig in signals],
        findings=[FindingSchema.model_validate(f.__dict__) for f in findings],
        timeline=timeline,
        currency_guard=len(currencies) > 1
    )

@router.get("/{workspace_id}/logs", response_model=List[AuditLogResponse])
async def get_workspace_audit_logs(
    workspace_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve immutable audit trail for the merchant workspace."""
    await verify_workspace_access(workspace_id, user, db)
    logs = (await db.execute(
        select(AuditLog).where(AuditLog.workspace_id == workspace_id).order_by(desc(AuditLog.timestamp)).limit(50)
    )).scalars().all()
    
    return [
        AuditLogResponse(
            id=l.id,
            action=l.action,
            details=l.details,
            timestamp=l.timestamp
        ) for l in logs
    ]
