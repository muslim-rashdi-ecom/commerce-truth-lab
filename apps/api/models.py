from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON
from database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    store_id = Column(String)
    created_at = Column(String)
    currency = Column(String)
    total_amount_minor = Column(Integer)
    payment_method = Column(String)
    status = Column(String)
    customer_id = Column(String)
    is_synthetic = Column(Boolean, default=True)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    captured_at = Column(String)
    currency = Column(String)
    amount_minor = Column(Integer)
    method = Column(String)
    gateway = Column(String)
    status = Column(String)

class CourierSettlement(Base):
    __tablename__ = "courier_settlements"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    courier_name = Column(String)
    delivered_at = Column(String)
    collected_amount_minor = Column(Integer)
    settled_amount_minor = Column(Integer, nullable=True)
    collection_currency = Column(String)
    settlement_status = Column(String)
    grace_days = Column(Integer, default=7)

class Refund(Base):
    __tablename__ = "refunds"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    refunded_at = Column(String)
    currency = Column(String)
    amount_minor = Column(Integer)
    reason = Column(String)

class PurchaseSignal(Base):
    __tablename__ = "purchase_signals"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    signal_type = Column(String)
    platform = Column(String)
    event_name = Column(String)
    event_id = Column(String)
    reported_at = Column(String)
    currency = Column(String)
    value_minor = Column(Integer)
    consent_granted = Column(Boolean)
    pixel_id = Column(String)

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(String, primary_key=True)
    name = Column(String)
    source_type = Column(String)
    date_range_start = Column(String)
    date_range_end = Column(String)
    currency = Column(String)
    coverage_status = Column(String)
    completeness_status = Column(String)
    last_processed = Column(String)
    record_count = Column(Integer)

class Finding(Base):
    __tablename__ = "findings"
    id = Column(String, primary_key=True)
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
    workspace_id = Column(String, default="demo")
