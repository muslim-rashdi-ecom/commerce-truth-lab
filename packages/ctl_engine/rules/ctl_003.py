from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL003(AuditRule):
    rule_id = "CTL-003"
    rule_name = "Purchase Value Mismatch"
    category = FindingCategory.value_mismatch
    severity = Severity.medium
    owner = "marketing-analytics"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        for s in signals:
            if s.currency == order.currency:
                diff = abs(s.value_minor - order.total_amount_minor)
                if diff > 0 and order.total_amount_minor > 0:
                    pct = diff / order.total_amount_minor
                    if pct > 0.05:
                        sev = Severity.high if pct > 0.5 else Severity.medium
                        return FindingResult(
                            rule_id=self.rule_id,
                            rule_name=self.rule_name,
                            category=self.category,
                            severity=sev,
                            order_id=order.id,
                            observed=f"Signal value {s.value_minor} differs from order total {order.total_amount_minor} by > 5%.",
                            source_records=[
                                EvidenceRef(source_id="orders", record_type="Order", record_id=order.id),
                                EvidenceRef(source_id="signals", record_type="PurchaseSignal", record_id=s.id)
                            ],
                            assumptions=["Signal value should match order total exactly in the same currency."],
                            not_proven=["Does not prove lost revenue or direct ROAS loss."],
                            next_step="Verify if tracking payload passes order total including/excluding taxes/shipping correctly.",
                            owner=self.owner,
                            confidence="high",
                            explanation="Value mismatch detected.",
                            recommended_action="Review value configuration in tracking."
                        )
        return None
