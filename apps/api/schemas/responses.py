from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DataSourceSchema(BaseModel):
    id: str
    name: str
    source_type: str
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None
    currency: Optional[str] = None
    coverage_status: Optional[str] = None
    completeness_status: Optional[str] = None
    last_processed: Optional[str] = None
    record_count: Optional[int] = None
    
    class Config:
        from_attributes = True

class WorkspaceMetadata(BaseModel):
    id: str
    name: str
    is_synthetic: bool
    created_at: str
    data_sources: List[DataSourceSchema]
    order_count: int
    finding_count: int
    affected_order_count: int
    data_completeness_pct: float
    tracking_confidence_pct: float

class FindingSchema(BaseModel):
    id: str
    rule_id: str
    rule_name: str
    category: str
    severity: str
    order_id: str
    observed: str
    source_records: Any
    assumptions: Any
    not_proven: Any
    next_step: str
    owner: str
    amount_minor: Optional[int] = None
    amount_currency: Optional[str] = None
    confidence: str
    explanation: str
    recommended_action: str
    status: str
    is_healthy_control: bool
    workspace_id: str

    class Config:
        from_attributes = True

class PaginatedFindings(BaseModel):
    items: List[FindingSchema]
    total: int
    page: int
    per_page: int
    total_pages: int

class OrderSchema(BaseModel):
    id: str
    store_id: str
    created_at: str
    currency: str
    total_amount_minor: int
    payment_method: str
    status: str
    customer_id: str
    is_synthetic: bool
    finding_count: Optional[int] = 0

    class Config:
        from_attributes = True

class PaymentSchema(BaseModel):
    id: str
    order_id: str
    captured_at: str
    currency: str
    amount_minor: int
    method: str
    gateway: str
    status: str

    class Config:
        from_attributes = True

class CourierSettlementSchema(BaseModel):
    id: str
    order_id: str
    courier_name: str
    delivered_at: str
    collected_amount_minor: int
    settled_amount_minor: Optional[int] = None
    collection_currency: str
    settlement_status: str
    grace_days: int

    class Config:
        from_attributes = True

class RefundSchema(BaseModel):
    id: str
    order_id: str
    refunded_at: str
    currency: str
    amount_minor: int
    reason: str

    class Config:
        from_attributes = True

class PurchaseSignalSchema(BaseModel):
    id: str
    order_id: str
    signal_type: str
    platform: str
    event_name: str
    event_id: str
    reported_at: str
    currency: str
    value_minor: int
    consent_granted: bool
    pixel_id: str

    class Config:
        from_attributes = True

class OrderDetailSchema(OrderSchema):
    payments: List[PaymentSchema] = []
    settlements: List[CourierSettlementSchema] = []
    refunds: List[RefundSchema] = []
    signals: List[PurchaseSignalSchema] = []

class TimelineEvent(BaseModel):
    timestamp: str
    event_type: str
    description: str
    source: str

class ReconciliationView(BaseModel):
    order: OrderSchema
    payment: Optional[PaymentSchema] = None
    settlements: List[CourierSettlementSchema] = []
    refunds: List[RefundSchema] = []
    purchase_signals: List[PurchaseSignalSchema] = []
    findings: List[FindingSchema] = []
    timeline: List[TimelineEvent] = []
    currency_guard: bool = False

class TrackingSummary(BaseModel):
    total_orders: int
    orders_with_signals: int
    orders_missing_signals: int
    duplicate_identity_orders: int
    value_mismatch_orders: int
    currency_mismatch_orders: int

class OrderSignalSummary(BaseModel):
    order_id: str
    order_total_minor: int
    order_currency: str
    signals: List[PurchaseSignalSchema]
    issues: List[str]

class TrackingHealthSchema(BaseModel):
    summary: TrackingSummary
    order_signals: List[OrderSignalSummary]

class UploadResponse(BaseModel):
    file_name: str
    detected_headers: List[str]
    preview_rows: List[List[str]]
    suggested_mappings: Dict[str, str]
    warnings: List[str]
    errors: List[str]
