from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, OrderStatus
)
from ctl_engine.rules.base import AuditRule

class RuleCTL002(AuditRule):
    rule_id = "CTL-002"
    rule_name = "Missing Purchase Signal"
    category = FindingCategory.missing_signal
    severity = Severity.medium
    owner = "marketing-analytics"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if order.status in (OrderStatus.cancelled, OrderStatus.returned):
            return None
            
        if order.status in (OrderStatus.delivered, OrderStatus.confirmed) and not signals:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"Order {order.id} is {order.status} but has no associated purchase signals.",
                source_records=[EvidenceRef(source_id="orders", record_type="Order", record_id=order.id)],
                assumptions=["All confirmed/delivered orders should have at least one purchase signal recorded."],
                not_proven=["Does not prove technical failure (could be user blocking tracking)."],
                next_step="Check tracking coverage for this order path.",
                owner=self.owner,
                confidence="medium",
                explanation="Missing signal for a successful order.",
                recommended_action="Review tracking setup for potential gaps."
            )
            
        return None
