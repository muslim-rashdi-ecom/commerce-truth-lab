import pytest
from datetime import datetime, timezone, timedelta
from shared.models import PurchaseSignal, SignalType, Currency, CourierSettlement, SettlementStatus, PaymentMethod, Refund, OrderStatus, Payment
from ctl_engine.rules.ctl_001 import RuleCTL001
from ctl_engine.rules.ctl_002 import RuleCTL002
from ctl_engine.rules.ctl_003 import RuleCTL003
from ctl_engine.rules.ctl_004 import RuleCTL004
from ctl_engine.rules.ctl_005 import RuleCTL005
from ctl_engine.rules.ctl_006 import RuleCTL006
from ctl_engine.rules.ctl_007 import RuleCTL007
from ctl_engine.rules.ctl_008 import RuleCTL008
from ctl_engine.rules.ctl_009 import RuleCTL009
from ctl_engine.rules.ctl_011 import RuleCTL011

def test_ctl001_positive(base_order):
    rule = RuleCTL001()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=base_order.total_amount_minor)
    s2 = PurchaseSignal(id="2", order_id=base_order.id, signal_type=SignalType.server, platform="Meta", event_name="Purchase", event_id="B", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=base_order.total_amount_minor)
    res = rule.evaluate(base_order, [], [], [], [s1, s2], [])
    assert res is not None
    assert res.rule_id == "CTL-001"
    assert res.is_healthy_control is False

def test_ctl001_negative(base_order):
    rule = RuleCTL001()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=base_order.total_amount_minor)
    res = rule.evaluate(base_order, [], [], [], [s1], [])
    assert res is None

def test_ctl001_healthy_control(base_order):
    rule = RuleCTL001()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=base_order.total_amount_minor)
    s2 = PurchaseSignal(id="2", order_id=base_order.id, signal_type=SignalType.server, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=base_order.total_amount_minor)
    res = rule.evaluate(base_order, [], [], [], [s1, s2], [])
    assert res is not None
    assert res.is_healthy_control is True

def test_ctl002_positive(base_order):
    rule = RuleCTL002()
    res = rule.evaluate(base_order, [], [], [], [], [])
    assert res is not None
    assert res.rule_id == "CTL-002"

def test_ctl002_negative(base_order):
    rule = RuleCTL002()
    base_order.status = OrderStatus.cancelled
    res = rule.evaluate(base_order, [], [], [], [], [])
    assert res is None

def test_ctl003_positive(base_order):
    rule = RuleCTL003()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=100) # mismatch
    res = rule.evaluate(base_order, [], [], [], [s1], [])
    assert res is not None
    assert res.rule_id == "CTL-003"

def test_ctl003_negative(base_order):
    rule = RuleCTL003()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=10000)
    res = rule.evaluate(base_order, [], [], [], [s1], [])
    assert res is None

def test_ctl004_positive(base_order):
    rule = RuleCTL004()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=Currency.EUR, value_minor=10000)
    res = rule.evaluate(base_order, [], [], [], [s1], [])
    assert res is not None
    assert res.rule_id == "CTL-004"

def test_ctl004_negative(base_order):
    rule = RuleCTL004()
    s1 = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", event_id="A", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=10000)
    res = rule.evaluate(base_order, [], [], [], [s1], [])
    assert res is None

def test_ctl005_positive(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL005()
    delivered_date = datetime.now(timezone.utc) - timedelta(days=10)
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", delivered_at=delivered_date, collected_amount_minor=10000, settled_amount_minor=0, collection_currency=base_order.currency, settlement_status=SettlementStatus.pending)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is not None
    assert res.rule_id == "CTL-005"

def test_ctl005_negative(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL005()
    delivered_date = datetime.now(timezone.utc) - timedelta(days=3)
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", delivered_at=delivered_date, collected_amount_minor=10000, settled_amount_minor=0, collection_currency=base_order.currency, settlement_status=SettlementStatus.pending)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is not None
    assert res.is_healthy_control is True

def test_ctl006_positive(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL006()
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", collected_amount_minor=9000, settled_amount_minor=9000, collection_currency=base_order.currency, settlement_status=SettlementStatus.settled)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is not None
    assert res.rule_id == "CTL-006"

def test_ctl006_negative(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL006()
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", collected_amount_minor=10000, settled_amount_minor=10000, collection_currency=base_order.currency, settlement_status=SettlementStatus.settled)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is None

def test_ctl006_no_evidence(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL006()
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", collected_amount_minor=None, settled_amount_minor=None, collection_currency=base_order.currency, settlement_status=SettlementStatus.pending)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is None

def test_ctl007_positive(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL007()
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", collected_amount_minor=11000, settled_amount_minor=11000, collection_currency=base_order.currency, settlement_status=SettlementStatus.settled)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is not None
    assert res.rule_id == "CTL-007"

def test_ctl007_negative(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL007()
    settle = CourierSettlement(id="S", order_id=base_order.id, courier_name="T", collected_amount_minor=10000, settled_amount_minor=10000, collection_currency=base_order.currency, settlement_status=SettlementStatus.settled)
    res = rule.evaluate(base_order, [], [settle], [], [], [])
    assert res is None

def test_ctl008_positive(base_order):
    rule = RuleCTL008()
    r = Refund(id="R", order_id=base_order.id, refunded_at=datetime.now(timezone.utc), currency=base_order.currency, amount_minor=11000)
    res = rule.evaluate(base_order, [], [], [r], [], [])
    assert res is not None
    assert res.rule_id == "CTL-008"

def test_ctl008_negative(base_order):
    rule = RuleCTL008()
    r = Refund(id="R", order_id=base_order.id, refunded_at=datetime.now(timezone.utc), currency=base_order.currency, amount_minor=10000)
    res = rule.evaluate(base_order, [], [], [r], [], [])
    assert res is None

def test_ctl009_positive_no_settlement(base_order):
    base_order.payment_method = PaymentMethod.cod
    rule = RuleCTL009()
    res = rule.evaluate(base_order, [], [], [], [], [])
    assert res is not None
    assert res.rule_id == "CTL-009"

def test_ctl009_negative(base_order):
    base_order.payment_method = PaymentMethod.prepaid
    rule = RuleCTL009()
    p = Payment(id="P", order_id=base_order.id, currency=base_order.currency, amount_minor=10000, method=PaymentMethod.prepaid, gateway="s", status="s")
    res = rule.evaluate(base_order, [p], [], [], [], [])
    assert res is None

def test_ctl011_positive_false(base_order):
    rule = RuleCTL011()
    s = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=10000, consent_granted=False)
    res = rule.evaluate(base_order, [], [], [], [s], [])
    assert res is not None
    assert res.rule_id == "CTL-011"
    
def test_ctl011_positive_none(base_order):
    rule = RuleCTL011()
    s = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=10000, consent_granted=None)
    res = rule.evaluate(base_order, [], [], [], [s], [])
    assert res is not None
    assert res.rule_id == "CTL-011"

def test_ctl011_negative(base_order):
    rule = RuleCTL011()
    s = PurchaseSignal(id="1", order_id=base_order.id, signal_type=SignalType.browser, platform="Meta", event_name="Purchase", reported_at=datetime.now(timezone.utc), currency=base_order.currency, value_minor=10000, consent_granted=True)
    res = rule.evaluate(base_order, [], [], [], [s], [])
    assert res is None
