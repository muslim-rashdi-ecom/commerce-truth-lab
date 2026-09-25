from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator, field_validator

CURRENCY_META = {
    'AED': {'decimals': 2, 'symbol': 'AED'},
    'USD': {'decimals': 2, 'symbol': '$'},
    'JPY': {'decimals': 0, 'symbol': '¥'},
    'KWD': {'decimals': 3, 'symbol': 'KD'},
    'PKR': {'decimals': 2, 'symbol': '₨'},
    'GBP': {'decimals': 2, 'symbol': '£'},
    'EUR': {'decimals': 2, 'symbol': '€'},
}

class Currency(str, Enum):
    AED = "AED"
    USD = "USD"
    JPY = "JPY"
    KWD = "KWD"
    PKR = "PKR"
    GBP = "GBP"
    EUR = "EUR"

class PaymentMethod(str, Enum):
    prepaid = "prepaid"
    cod = "cod"
    bank_transfer = "bank_transfer"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"

class SettlementStatus(str, Enum):
    pending = "pending"
    partial = "partial"
    settled = "settled"
    overdue = "overdue"

class SignalType(str, Enum):
    browser = "browser"
    server = "server"
    enhanced = "enhanced"

class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"

class FindingCategory(str, Enum):
    duplicate_identity = "duplicate_identity"
    missing_signal = "missing_signal"
    value_mismatch = "value_mismatch"
    currency_mismatch = "currency_mismatch"
    cod_collection = "cod_collection"
    reconciliation = "reconciliation"
    coverage = "coverage"
    mapping = "mapping"
    policy_consent = "policy_consent"
    guard = "guard"

class FindingStatus(str, Enum):
    open = "open"
    reviewing = "reviewing"
    verified = "verified"
    dismissed = "dismissed"

class Order(BaseModel):
    id: str
    store_id: str
    created_at: datetime
    currency: Currency
    total_amount_minor: int
    payment_method: PaymentMethod
    status: OrderStatus
    customer_id: str
    tags: List[str]

class Payment(BaseModel):
    id: str
    order_id: str
    captured_at: Optional[datetime] = None
    currency: Currency
    amount_minor: int
    method: PaymentMethod
    gateway: str
    status: str

class CourierSettlement(BaseModel):
    id: str
    order_id: str
    courier_name: str
    delivered_at: Optional[datetime] = None
    collected_amount_minor: Optional[int] = None
    settled_amount_minor: Optional[int] = None
    collection_currency: Currency
    settlement_status: SettlementStatus
    grace_days: int = 7

class Refund(BaseModel):
    id: str
    order_id: str
    refunded_at: datetime
    currency: Currency
    amount_minor: int
    reason: Optional[str] = None

class PurchaseSignal(BaseModel):
    id: str
    order_id: str
    signal_type: SignalType
    platform: str
    event_name: str
    event_id: Optional[str] = None
    reported_at: datetime
    currency: Currency
    value_minor: int
    consent_granted: Optional[bool] = None
    pixel_id: Optional[str] = None

class DataSource(BaseModel):
    id: str
    name: str
    source_type: str
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    currency: Optional[str] = None
    coverage_status: str
    completeness_status: str
    last_processed: Optional[datetime] = None
    record_count: int

class EvidenceRef(BaseModel):
    source_id: str
    record_type: str
    record_id: str
    field: Optional[str] = None
    value: Optional[str] = None

class FindingResult(BaseModel):
    rule_id: str
    rule_name: str
    category: FindingCategory
    severity: Severity
    order_id: Optional[str] = None
    observed: str
    source_records: List[EvidenceRef]
    assumptions: List[str]
    not_proven: List[str]
    next_step: str
    owner: str
    amount_minor: Optional[int] = None
    amount_currency: Optional[Currency] = None
    confidence: str
    explanation: str
    recommended_action: str
    status: FindingStatus = FindingStatus.open
    is_healthy_control: bool = False

class WorkspaceMetadata(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_synthetic: bool
    data_sources: List[DataSource]
    order_count: int
    finding_count: int
    affected_order_count: int
    data_completeness_pct: float
    tracking_confidence_pct: float

class AuditRunResult(BaseModel):
    workspace_id: str
    run_at: datetime
    findings: List[FindingResult]
    healthy_controls: List[FindingResult]
    total_orders: int
    evaluated_orders: int
    skipped_orders_insufficient_data: int


class DatasetClassification(str, Enum):
    PUBLIC_BENCHMARK = "PUBLIC_BENCHMARK"
    PUBLIC_PLUS_SYNTHETIC_COMPOSITE = "PUBLIC_PLUS_SYNTHETIC_COMPOSITE"
    SYNTHETIC_DEMO = "SYNTHETIC_DEMO"
    REAL_AUTHORIZED_PILOT = "REAL_AUTHORIZED_PILOT"


class BenchmarkProvenance(BaseModel):
    dataset_name: str
    source_url: str
    license: str
    citation: str
    download_date: str
    fields_used: List[str]
    fields_unavailable: List[str]
    transformations_performed: List[str]
    is_synthetic_composite: bool = False
    synthetic_companion_description: Optional[str] = None
    what_it_can_prove: List[str]
    what_it_cannot_prove: List[str]


class BenchmarkCaseSummary(BaseModel):
    id: str
    title: str
    description: str
    classification: DatasetClassification
    category: str
    dataset_name: str
    license: str
    order_count: int
    record_count: int
    findings_count: int
    healthy_controls_count: int
    is_synthetic_composite: bool = False
    synthetic_warning: Optional[str] = None


class BenchmarkCaseDetail(BaseModel):
    id: str
    title: str
    description: str
    classification: DatasetClassification
    category: str
    provenance: BenchmarkProvenance
    order_count: int
    record_count: int
    findings: List[FindingResult]
    healthy_controls: List[FindingResult]
    warnings: List[str]
    non_claims: List[str]
    reproduction_command: str
