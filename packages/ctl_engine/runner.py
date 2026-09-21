from typing import List
from datetime import datetime, timezone
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, AuditRunResult
)
from ctl_engine.rules.ctl_001 import RuleCTL001
from ctl_engine.rules.ctl_002 import RuleCTL002
from ctl_engine.rules.ctl_003 import RuleCTL003
from ctl_engine.rules.ctl_004 import RuleCTL004
from ctl_engine.rules.ctl_005 import RuleCTL005
from ctl_engine.rules.ctl_006 import RuleCTL006
from ctl_engine.rules.ctl_007 import RuleCTL007
from ctl_engine.rules.ctl_008 import RuleCTL008
from ctl_engine.rules.ctl_009 import RuleCTL009
from ctl_engine.rules.ctl_010 import RuleCTL010
from ctl_engine.rules.ctl_011 import RuleCTL011
from ctl_engine.rules.ctl_012 import RuleCTL012

class AuditEngine:
    def __init__(self):
        self.rules = [
            RuleCTL001(),
            RuleCTL002(),
            RuleCTL003(),
            RuleCTL004(),
            RuleCTL005(),
            RuleCTL006(),
            RuleCTL007(),
            RuleCTL008(),
            RuleCTL009(),
            RuleCTL010(),
            RuleCTL011(),
            RuleCTL012()
        ]
        
    def run(self, orders: List[Order], payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource], reference_date: datetime = None) -> AuditRunResult:
        findings = []
        healthy_controls = []
        
        for order in orders:
            order_payments = [p for p in payments if p.order_id == order.id]
            order_settlements = [s for s in settlements if s.order_id == order.id]
            order_refunds = [r for r in refunds if r.order_id == order.id]
            order_signals = [s for s in signals if s.order_id == order.id]
            
            for rule in self.rules:
                result = rule.evaluate(order, order_payments, order_settlements, order_refunds, order_signals, sources)
                if result:
                    if result.is_healthy_control:
                        healthy_controls.append(result)
                    else:
                        findings.append(result)
                        
        return AuditRunResult(
            workspace_id="default",
            run_at=datetime.now(timezone.utc),
            findings=findings,
            healthy_controls=healthy_controls,
            total_orders=len(orders),
            evaluated_orders=len(orders),
            skipped_orders_insufficient_data=0
        )
