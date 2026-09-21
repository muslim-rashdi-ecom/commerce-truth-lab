import pytest
from datetime import datetime, timezone
from shared.models import Order, Payment, CourierSettlement, Refund, PurchaseSignal, Currency, PaymentMethod, OrderStatus, SignalType, SettlementStatus

@pytest.fixture
def base_order():
    return Order(
        id="O-TEST",
        store_id="S1",
        created_at=datetime.now(timezone.utc),
        currency=Currency.USD,
        total_amount_minor=10000,
        payment_method=PaymentMethod.prepaid,
        status=OrderStatus.delivered,
        customer_id="C1",
        tags=[]
    )
