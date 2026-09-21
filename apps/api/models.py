import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON, DateTime, Text, Index
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    created_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), index=True, nullable=True)
    currency = Column(String, default="USD")
    is_synthetic = Column(Boolean, default=False)
    created_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"), index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    role = Column(String, default="admin")  # admin, auditor, viewer
    joined_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class Order(Base):
    __tablename__ = "orders"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    store_id = Column(String, default="store-1")
    created_at = Column(String)
    currency = Column(String)
    total_amount_minor = Column(Integer)
    payment_method = Column(String)
    status = Column(String)
    customer_id = Column(String)  # Always pseudonymized hash, never plaintext PII
    is_synthetic = Column(Boolean, default=False)

class Payment(Base):
    __tablename__ = "payments"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    order_id = Column(String, index=True)
    captured_at = Column(String)
    currency = Column(String)
    amount_minor = Column(Integer)
    method = Column(String)
    gateway = Column(String)
    status = Column(String)

class CourierSettlement(Base):
    __tablename__ = "courier_settlements"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    order_id = Column(String, index=True)
    courier_name = Column(String)
    delivered_at = Column(String)
    collected_amount_minor = Column(Integer)
    settled_amount_minor = Column(Integer, nullable=True)
    collection_currency = Column(String)
    settlement_status = Column(String)
    grace_days = Column(Integer, default=7)

class Refund(Base):
    __tablename__ = "refunds"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    order_id = Column(String, index=True)
    refunded_at = Column(String)
    currency = Column(String)
    amount_minor = Column(Integer)
    reason = Column(String)

class PurchaseSignal(Base):
    __tablename__ = "purchase_signals"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    order_id = Column(String, index=True)
    signal_type = Column(String)
    platform = Column(String)
    event_name = Column(String)
    event_id = Column(String)
    reported_at = Column(String)
    currency = Column(String)
    value_minor = Column(Integer)
    consent_granted = Column(Boolean, default=True)
    pixel_id = Column(String, default="P1")

class DataSource(Base):
    __tablename__ = "data_sources"
    workspace_id = Column(String, primary_key=True, default="demo")
    id = Column(String, primary_key=True)
    name = Column(String)
    source_type = Column(String)
    date_range_start = Column(String)
    date_range_end = Column(String)
    currency = Column(String)
    coverage_status = Column(String)
    completeness_status = Column(String)
    last_processed = Column(String)
    record_count = Column(Integer, default=0)


class Finding(Base):
    __tablename__ = "findings"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, index=True, default="demo")
    rule_id = Column(String)
    rule_name = Column(String)
    category = Column(String)
    severity = Column(String)
    order_id = Column(String)
    observed = Column(String)
    source_records = Column(JSON)
    assumptions = Column(JSON)
    not_proven = Column(JSON)
    next_step = Column(String)
    owner = Column(String)
    amount_minor = Column(Integer, nullable=True)
    amount_currency = Column(String, nullable=True)
    confidence = Column(String)
    explanation = Column(String)
    recommended_action = Column(String)
    status = Column(String, default="open")
    is_healthy_control = Column(Boolean, default=False)

class UploadMetadata(Base):
    __tablename__ = "upload_metadata"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, index=True, nullable=False)
    source_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size_bytes = Column(Integer, default=0)
    row_count = Column(Integer, default=0)
    mapped_columns = Column(JSON, default=dict)
    warnings = Column(JSON, default=list)
    status = Column(String, default="staged")  # staged, committed, failed
    created_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class AuditRun(Base):
    __tablename__ = "audit_runs"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, index=True, nullable=False)
    status = Column(String, default="completed")  # running, completed, failed
    evaluated_orders = Column(Integer, default=0)
    total_findings = Column(Integer, default=0)
    healthy_controls_count = Column(Integer, default=0)
    summary = Column(JSON, default=dict)
    created_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    completed_at = Column(String, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    workspace_id = Column(String, index=True, nullable=False)
    user_id = Column(String, nullable=True)
    action = Column(String, nullable=False)  # user_register, login, workspace_created, csv_staged, csv_committed, audit_run, report_exported
    details = Column(JSON, default=dict)
    ip_address = Column(String, nullable=True)
    timestamp = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
