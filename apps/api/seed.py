import asyncio
import os
import datetime
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database import Base, DB_PATH, DATABASE_URL
from models import Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, Finding

async def seed_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    
    async with SessionLocal() as db:
        now = datetime.datetime.now(datetime.timezone.utc)
        def d(days_ago): return (now - datetime.timedelta(days=days_ago)).isoformat()
        
        db.add_all([
            DataSource(id="ds-1", name="shopify_orders", source_type="shopify", date_range_start=d(30), date_range_end=d(0), currency="USD", coverage_status="full", completeness_status="good", last_processed=d(0), record_count=12),
            DataSource(id="ds-2", name="payment_gateway", source_type="stripe", date_range_start=d(30), date_range_end=d(0), currency="USD", coverage_status="full", completeness_status="good", last_processed=d(0), record_count=12),
            DataSource(id="ds-3", name="courier_settlements", source_type="courier", date_range_start=d(30), date_range_end=d(0), currency="AED", coverage_status="partial", completeness_status="needs_attention", last_processed=d(0), record_count=5),
            DataSource(id="ds-4", name="meta_capi", source_type="meta", date_range_start=d(30), date_range_end=d(0), currency="USD", coverage_status="full", completeness_status="good", last_processed=d(0), record_count=12)
        ])

        orders = [
            Order(id="ORD-001", store_id="store-1", created_at=d(11), currency="AED", total_amount_minor=25000, payment_method="COD", status="delivered", customer_id="CUST-1", is_synthetic=True),
            Order(id="ORD-002", store_id="store-1", created_at=d(13), currency="AED", total_amount_minor=8000, payment_method="COD", status="delivered", customer_id="CUST-2", is_synthetic=True),
            Order(id="ORD-003", store_id="store-1", created_at=d(5), currency="USD", total_amount_minor=12000, payment_method="prepaid", status="refunded", customer_id="CUST-3", is_synthetic=True),
            Order(id="ORD-004", store_id="store-1", created_at=d(5), currency="USD", total_amount_minor=12000, payment_method="prepaid", status="refunded", customer_id="CUST-4", is_synthetic=True),
            Order(id="ORD-005", store_id="store-1", created_at=d(2), currency="JPY", total_amount_minor=12000, payment_method="prepaid", status="delivered", customer_id="CUST-5", is_synthetic=True),
            Order(id="ORD-006", store_id="store-1", created_at=d(1), currency="KWD", total_amount_minor=15900, payment_method="prepaid", status="delivered", customer_id="CUST-6", is_synthetic=True),
            Order(id="ORD-007", store_id="store-1", created_at=d(4), currency="PKR", total_amount_minor=500000, payment_method="COD", status="delivered", customer_id="CUST-7", is_synthetic=True),
            Order(id="ORD-008", store_id="store-1", created_at=d(2), currency="USD", total_amount_minor=20000, payment_method="prepaid", status="delivered", customer_id="CUST-8", is_synthetic=True),
            Order(id="ORD-009", store_id="store-1", created_at=d(2), currency="USD", total_amount_minor=30000, payment_method="prepaid", status="delivered", customer_id="CUST-9", is_synthetic=True),
            Order(id="ORD-010", store_id="store-1", created_at=d(1), currency="GBP", total_amount_minor=15000, payment_method="prepaid", status="confirmed", customer_id="CUST-10", is_synthetic=True),
            Order(id="ORD-011", store_id="store-1", created_at=d(9), currency="AED", total_amount_minor=50000, payment_method="COD", status="delivered", customer_id="CUST-11", is_synthetic=True),
            Order(id="ORD-012", store_id="store-1", created_at=d(1), currency="EUR", total_amount_minor=9000, payment_method="prepaid", status="delivered", customer_id="CUST-12", is_synthetic=True),
        ]
        db.add_all(orders)

        db.add(CourierSettlement(id="SET-001", order_id="ORD-001", courier_name="DHL", delivered_at=d(10), collected_amount_minor=10000, settled_amount_minor=10000, collection_currency="AED", settlement_status="settled", grace_days=7))
        db.add(Finding(id="F-001", rule_id="CTL-005", rule_name="Partial COD Settlement", category="financial", severity="High", order_id="ORD-001", observed="Settled 10000 minor AED, expected 25000 minor AED", source_records={}, assumptions={}, not_proven={}, next_step="Check courier", owner="system", amount_minor=15000, amount_currency="AED", confidence="High", explanation="Partial settlement", recommended_action="Dispute", is_healthy_control=False))
        
        db.add(CourierSettlement(id="SET-002", order_id="ORD-002", courier_name="Aramex", delivered_at=d(12), collected_amount_minor=8000, settled_amount_minor=None, collection_currency="AED", settlement_status="pending", grace_days=7))
        db.add(Finding(id="F-002", rule_id="CTL-009", rule_name="Missing COD Settlement", category="financial", severity="High", order_id="ORD-002", observed="Delivered 12 days ago, not settled", source_records={}, assumptions={}, not_proven={}, next_step="Check courier", owner="system", amount_minor=8000, amount_currency="AED", confidence="High", explanation="No settlement beyond grace", recommended_action="Dispute", is_healthy_control=False))

        db.add(Refund(id="REF-003", order_id="ORD-003", refunded_at=d(2), currency="USD", amount_minor=12000, reason="returned"))
        db.add(Finding(id="F-003", rule_id="CTL-008", rule_name="Excessive Refund", category="financial", severity="Low", order_id="ORD-003", observed="Refund matches order amount exactly", source_records={}, assumptions={}, not_proven={}, next_step="None", owner="system", amount_minor=0, amount_currency="USD", confidence="High", explanation="Valid refund", recommended_action="None", is_healthy_control=True))

        db.add(Refund(id="REF-004", order_id="ORD-004", refunded_at=d(2), currency="USD", amount_minor=13000, reason="returned_with_compensation"))
        db.add(Finding(id="F-004", rule_id="CTL-008", rule_name="Excessive Refund", category="financial", severity="High", order_id="ORD-004", observed="Refunded 13000, initial order 12000", source_records={}, assumptions={}, not_proven={}, next_step="Review refund policy", owner="system", amount_minor=1000, amount_currency="USD", confidence="High", explanation="Refund exceeded captured amount", recommended_action="Audit staff", is_healthy_control=False))

        db.add(PurchaseSignal(id="SIG-005", order_id="ORD-005", signal_type="purchase", platform="meta", event_name="Purchase", event_id="E-005", reported_at=d(2), currency="JPY", value_minor=120, consent_granted=True, pixel_id="P1"))
        db.add(Finding(id="F-005", rule_id="CTL-003", rule_name="Tracking Value Mismatch", category="tracking", severity="Medium", order_id="ORD-005", observed="Signal 120 JPY vs Order 12000 JPY", source_records={}, assumptions={}, not_proven={}, next_step="Check decimal configuration", owner="system", amount_minor=0, amount_currency="JPY", confidence="High", explanation="100x mismatch", recommended_action="Fix pixel", is_healthy_control=False))

        db.add(PurchaseSignal(id="SIG-006", order_id="ORD-006", signal_type="purchase", platform="meta", event_name="Purchase", event_id="E-006", reported_at=d(1), currency="KWD", value_minor=15900, consent_granted=True, pixel_id="P1"))
        db.add(Finding(id="F-006", rule_id="CTL-003", rule_name="Tracking Value Mismatch", category="tracking", severity="Low", order_id="ORD-006", observed="Matching KWD tracking", source_records={}, assumptions={}, not_proven={}, next_step="None", owner="system", amount_minor=0, amount_currency="KWD", confidence="High", explanation="Matched", recommended_action="None", is_healthy_control=True))

        db.add(CourierSettlement(id="SET-007", order_id="ORD-007", courier_name="TCS", delivered_at=d(3), collected_amount_minor=500000, settled_amount_minor=None, collection_currency="PKR", settlement_status="pending", grace_days=7))
        db.add(Finding(id="F-007", rule_id="CTL-009", rule_name="Missing COD Settlement", category="financial", severity="Low", order_id="ORD-007", observed="Delivered 3 days ago, within grace", source_records={}, assumptions={}, not_proven={}, next_step="None", owner="system", amount_minor=0, amount_currency="PKR", confidence="High", explanation="Within 7 day grace", recommended_action="None", is_healthy_control=True))

        db.add(PurchaseSignal(id="SIG-008-1", order_id="ORD-008", signal_type="purchase", platform="meta", event_name="Purchase", event_id="EVT-DEDUP-008", reported_at=d(2), currency="USD", value_minor=20000, consent_granted=True, pixel_id="P1"))
        db.add(PurchaseSignal(id="SIG-008-2", order_id="ORD-008", signal_type="purchase", platform="meta_server", event_name="Purchase", event_id="EVT-DEDUP-008", reported_at=d(2), currency="USD", value_minor=20000, consent_granted=True, pixel_id="P1"))
        db.add(Finding(id="F-008", rule_id="CTL-001", rule_name="Duplicate Signals", category="tracking", severity="Low", order_id="ORD-008", observed="Same event_id", source_records={}, assumptions={}, not_proven={}, next_step="None", owner="system", amount_minor=0, amount_currency="USD", confidence="High", explanation="Valid deduplication", recommended_action="None", is_healthy_control=True))

        db.add(PurchaseSignal(id="SIG-009-1", order_id="ORD-009", signal_type="purchase", platform="meta", event_name="Purchase", event_id="EVT-A-009", reported_at=d(2), currency="USD", value_minor=30000, consent_granted=True, pixel_id="P1"))
        db.add(PurchaseSignal(id="SIG-009-2", order_id="ORD-009", signal_type="purchase", platform="meta_server", event_name="Purchase", event_id="EVT-B-009", reported_at=d(2), currency="USD", value_minor=30000, consent_granted=True, pixel_id="P1"))
        db.add(Finding(id="F-009", rule_id="CTL-001", rule_name="Duplicate Signals", category="tracking", severity="Medium", order_id="ORD-009", observed="Multiple signals with different event_ids", source_records={}, assumptions={}, not_proven={}, next_step="Fix deduplication logic", owner="system", amount_minor=0, amount_currency="USD", confidence="High", explanation="Failed deduplication", recommended_action="Fix CAPI", is_healthy_control=False))

        db.add(Finding(id="F-010", rule_id="CTL-002", rule_name="Missing Tracking Signal", category="tracking", severity="High", order_id="ORD-010", observed="No signals found for confirmed order", source_records={}, assumptions={}, not_proven={}, next_step="Review pixel firing", owner="system", amount_minor=0, amount_currency="GBP", confidence="High", explanation="Missing pixel event", recommended_action="Fix tracking", is_healthy_control=False))

        db.add(CourierSettlement(id="SET-011", order_id="ORD-011", courier_name="FedEx", delivered_at=d(8), collected_amount_minor=60000, settled_amount_minor=60000, collection_currency="AED", settlement_status="settled", grace_days=7))
        db.add(Finding(id="F-011", rule_id="CTL-007", rule_name="COD Over-collection", category="financial", severity="Medium", order_id="ORD-011", observed="Collected 60000, order 50000", source_records={}, assumptions={}, not_proven={}, next_step="Review", owner="system", amount_minor=10000, amount_currency="AED", confidence="High", explanation="Collected more than order", recommended_action="Investigate", is_healthy_control=False))

        db.add(PurchaseSignal(id="SIG-012", order_id="ORD-012", signal_type="purchase", platform="meta", event_name="Purchase", event_id="E-012", reported_at=d(1), currency="USD", value_minor=9000, consent_granted=True, pixel_id="P1"))
        db.add(Finding(id="F-012", rule_id="CTL-004", rule_name="Currency Mismatch", category="tracking", severity="Medium", order_id="ORD-012", observed="Signal USD, Order EUR", source_records={}, assumptions={}, not_proven={}, next_step="Fix pixel currency", owner="system", amount_minor=0, amount_currency="EUR", confidence="High", explanation="Mismatched currency", recommended_action="Update tracking code", is_healthy_control=False))

        await db.commit()
        print("Database seeded with synthetic data.")

if __name__ == "__main__":
    asyncio.run(seed_db())
