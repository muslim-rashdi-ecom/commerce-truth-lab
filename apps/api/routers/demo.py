from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from database import get_db
from services import demo_service, report_service
from schemas.responses import WorkspaceMetadata, PaginatedFindings, FindingSchema, OrderSchema, OrderDetailSchema, ReconciliationView, TrackingHealthSchema
from typing import List

router = APIRouter(prefix="/api/demo", tags=["Demo"])

@router.get("/workspace", response_model=WorkspaceMetadata)
async def get_workspace(db: AsyncSession = Depends(get_db)):
    return await demo_service.get_workspace(db)

@router.get("/findings", response_model=PaginatedFindings)
async def get_findings(
    severity: str = Query(None),
    category: str = Query(None),
    status: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await demo_service.get_findings(db, severity, category, status, page, per_page)

@router.get("/healthy-controls", response_model=List[FindingSchema])
async def get_healthy_controls(db: AsyncSession = Depends(get_db)):
    return await demo_service.get_healthy_controls(db)

@router.get("/orders", response_model=List[OrderSchema])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await demo_service.get_orders(db)

@router.get("/orders/{order_id}", response_model=OrderDetailSchema)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    od = await demo_service.get_order(db, order_id)
    if not od:
        raise HTTPException(status_code=404, detail="Order not found")
    return od

@router.get("/reconciliation/{order_id}", response_model=ReconciliationView)
async def get_reconciliation(order_id: str, db: AsyncSession = Depends(get_db)):
    rec = await demo_service.get_reconciliation(db, order_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Order not found")
    return rec

@router.get("/tracking-health", response_model=TrackingHealthSchema)
async def get_tracking_health(db: AsyncSession = Depends(get_db)):
    return await demo_service.get_tracking_health(db)

@router.get("/reports/html", response_class=HTMLResponse)
async def get_report_html(db: AsyncSession = Depends(get_db)):
    f = await demo_service.get_findings(db, per_page=1000)
    hc = await demo_service.get_healthy_controls(db)
    ws = await demo_service.get_workspace(db)
    stats = {"total_orders": ws.order_count, "total_findings": ws.finding_count}
    return report_service.generate_html_report(f.items, hc, stats)

@router.get("/reports/markdown", response_class=PlainTextResponse)
async def get_report_markdown(db: AsyncSession = Depends(get_db)):
    f = await demo_service.get_findings(db, per_page=1000)
    hc = await demo_service.get_healthy_controls(db)
    ws = await demo_service.get_workspace(db)
    stats = {"total_orders": ws.order_count, "total_findings": ws.finding_count}
    return report_service.generate_markdown_report(f.items, hc, stats)

@router.get("/reports/json")
async def get_report_json(db: AsyncSession = Depends(get_db)):
    f = await demo_service.get_findings(db, per_page=1000)
    hc = await demo_service.get_healthy_controls(db)
    ws = await demo_service.get_workspace(db)
    return {
        "workspace": ws.model_dump(),
        "findings": [x.model_dump() for x in f.items],
        "healthy_controls": [x.model_dump() for x in hc]
    }
