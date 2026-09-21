from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL008(AuditRule):
    rule_id = "CTL-008"
    rule_name = "Refund Greater Than Original Order Value"
    category = FindingCategory.reconciliation
    severity = Severity.high
    owner = "finance"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        total_refund_minor = sum(r.amount_minor for r in refunds if r.currency == order.currency)
        
        if total_refund_minor > order.total_amount_minor:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"Total refunded amount {total_refund_minor} exceeds original order total {order.total_amount_minor}.",
                source_records=[
                    EvidenceRef(source_id="orders", record_type="Order", record_id=order.id)
                ] + [EvidenceRef(source_id="refunds", record_type="Refund", record_id=r.id) for r in refunds],
                assumptions=["Total refunds should not exceed original order value."],
                not_proven=["Does not prove intentional fraud (could be system bug or manual override)."],
                next_step="Review refund authorization logs.",
                owner=self.owner,
                confidence="high",
                explanation="Excessive refund detected.",
                recommended_action="Audit refund processes."
            )
        return None
