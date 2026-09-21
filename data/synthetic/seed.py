import json
from datetime import datetime, timezone, timedelta
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, Currency, PaymentMethod, OrderStatus, SettlementStatus, SignalType, DataSource
)

now = datetime.now(timezone.utc)
ten_days_ago = now - timedelta(days=10)
three_days_ago = now - timedelta(days=3)

orders = [
    Order(id="ORD-001", store_id="S1", created_at=ten_days_ago, currency=Currency.AED, total_amount_minor=25000, payment_method=PaymentMethod.cod, status=OrderStatus.delivered, customer_id="C1", tags=[]),
    Order(id="ORD-002", store_id="S1", created_at=ten_days_ago, currency=Currency.AED, total_amount_minor=8000, payment_method=PaymentMethod.cod, status=OrderStatus.delivered, customer_id="C2", tags=[]),
    Order(id="ORD-003", store_id="S1", created_at=ten_days_ago, currency=Currency.USD, total_amount_minor=12000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C3", tags=[]),
    Order(id="ORD-004", store_id="S1", created_at=ten_days_ago, currency=Currency.USD, total_amount_minor=12000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C4", tags=[]),
    Order(id="ORD-005", store_id="S1", created_at=ten_days_ago, currency=Currency.JPY, total_amount_minor=12000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C5", tags=[]),
    Order(id="ORD-006", store_id="S1", created_at=ten_days_ago, currency=Currency.KWD, total_amount_minor=15900, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C6", tags=[]),
    Order(id="ORD-007", store_id="S1", created_at=three_days_ago, currency=Currency.PKR, total_amount_minor=500000, payment_method=PaymentMethod.cod, status=OrderStatus.delivered, customer_id="C7", tags=[]),
    Order(id="ORD-008", store_id="S1", created_at=ten_days_ago, currency=Currency.USD, total_amount_minor=20000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C8", tags=[]),
    Order(id="ORD-009", store_id="S1", created_at=ten_days_ago, currency=Currency.USD, total_amount_minor=30000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C9", tags=[]),
    Order(id="ORD-010", store_id="S1", created_at=ten_days_ago, currency=Currency.GBP, total_amount_minor=15000, payment_method=PaymentMethod.prepaid, status=OrderStatus.confirmed, customer_id="C10", tags=[]),
    Order(id="ORD-011", store_id="S1", created_at=ten_days_ago, currency=Currency.AED, total_amount_minor=50000, payment_method=PaymentMethod.cod, status=OrderStatus.delivered, customer_id="C11", tags=[]),
    Order(id="ORD-012", store_id="S1", created_at=ten_days_ago, currency=Currency.EUR, total_amount_minor=9000, payment_method=PaymentMethod.prepaid, status=OrderStatus.delivered, customer_id="C12", tags=[])
]

payments = [
    Payment(id="P-003", order_id="ORD-003", currency=Currency.USD, amount_minor=12000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-004", order_id="ORD-004", currency=Currency.USD, amount_minor=12000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-005", order_id="ORD-005", currency=Currency.JPY, amount_minor=12000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-006", order_id="ORD-006", currency=Currency.KWD, amount_minor=15900, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-008", order_id="ORD-008", currency=Currency.USD, amount_minor=20000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-009", order_id="ORD-009", currency=Currency.USD, amount_minor=30000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-010", order_id="ORD-010", currency=Currency.GBP, amount_minor=15000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded"),
    Payment(id="P-012", order_id="ORD-012", currency=Currency.EUR, amount_minor=9000, method=PaymentMethod.prepaid, gateway="stripe", status="succeeded")
]

settlements = [
    CourierSettlement(id="S-001", order_id="ORD-001", courier_name="DHL", delivered_at=ten_days_ago, collected_amount_minor=25000, settled_amount_minor=10000, collection_currency=Currency.AED, settlement_status=SettlementStatus.partial, grace_days=7),
    CourierSettlement(id="S-007", order_id="ORD-007", courier_name="TCS", delivered_at=three_days_ago, collected_amount_minor=500000, settled_amount_minor=None, collection_currency=Currency.PKR, settlement_status=SettlementStatus.pending, grace_days=7),
    CourierSettlement(id="S-011", order_id="ORD-011", courier_name="Aramex", delivered_at=ten_days_ago, collected_amount_minor=60000, settled_amount_minor=60000, collection_currency=Currency.AED, settlement_status=SettlementStatus.settled, grace_days=7),
]

refunds = [
    Refund(id="R-003", order_id="ORD-003", refunded_at=now, currency=Currency.USD, amount_minor=12000, reason="Return"),
    Refund(id="R-004", order_id="ORD-004", refunded_at=now, currency=Currency.USD, amount_minor=13000, reason="Return+Bonus")
]

signals = [
    PurchaseSignal(id="SIG-001", order_id="ORD-001", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.AED, value_minor=25000, consent_granted=True),
    PurchaseSignal(id="SIG-003", order_id="ORD-003", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.USD, value_minor=12000, consent_granted=True),
    PurchaseSignal(id="SIG-004", order_id="ORD-004", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.USD, value_minor=12000, consent_granted=True),
    PurchaseSignal(id="SIG-005", order_id="ORD-005", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.JPY, value_minor=120, consent_granted=True),
    PurchaseSignal(id="SIG-006", order_id="ORD-006", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.KWD, value_minor=15900, consent_granted=True),
    PurchaseSignal(id="SIG-007", order_id="ORD-007", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=three_days_ago, currency=Currency.PKR, value_minor=500000, consent_granted=True),
    PurchaseSignal(id="SIG-008a", order_id="ORD-008", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="EVT-008", reported_at=ten_days_ago, currency=Currency.USD, value_minor=20000, consent_granted=True),
    PurchaseSignal(id="SIG-008b", order_id="ORD-008", signal_type=SignalType.server, platform="Meta", event_name="Purchase", event_id="EVT-008", reported_at=ten_days_ago, currency=Currency.USD, value_minor=20000, consent_granted=True),
    PurchaseSignal(id="SIG-009a", order_id="ORD-009", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="EVT-A", reported_at=ten_days_ago, currency=Currency.USD, value_minor=30000, consent_granted=True),
    PurchaseSignal(id="SIG-009b", order_id="ORD-009", signal_type=SignalType.server, platform="Meta", event_name="Purchase", event_id="EVT-B", reported_at=ten_days_ago, currency=Currency.USD, value_minor=30000, consent_granted=True),
    PurchaseSignal(id="SIG-011", order_id="ORD-011", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.AED, value_minor=50000, consent_granted=True),
    PurchaseSignal(id="SIG-012", order_id="ORD-012", signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=ten_days_ago, currency=Currency.USD, value_minor=9000, consent_granted=True)
]

dataset = {
    "orders": [o.model_dump(mode='json') for o in orders],
    "payments": [p.model_dump(mode='json') for p in payments],
    "settlements": [s.model_dump(mode='json') for s in settlements],
    "refunds": [r.model_dump(mode='json') for r in refunds],
    "signals": [s.model_dump(mode='json') for s in signals]
}

if __name__ == "__main__":
    with open("data/synthetic/dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print("Synthetic dataset generated.")
