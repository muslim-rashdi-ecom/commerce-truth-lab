from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL004(AuditRule):
    rule_id = "CTL-004"
    rule_name = "Purchase Currency Mismatch"
    category = FindingCategory.currency_mismatch
    severity = Severity.high
    owner = "marketing-analytics"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        for s in signals:
            if s.currency != order.currency:
                return FindingResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    category=self.category,
                    severity=self.severity,
                    order_id=order.id,
                    observed=f"Signal currency {s.currency} does not match order currency {order.currency}.",
                    source_records=[
                        EvidenceRef(source_id="orders", record_type="Order", record_id=order.id),
                        EvidenceRef(source_id="signals", record_type="PurchaseSignal", record_id=s.id)
                    ],
                    assumptions=["Signals should report in the base currency of the order."],
                    not_proven=["Does not prove ad network failed to convert currency correctly."],
                    next_step="Check base currency settings in tracking integration.",
                    owner=self.owner,
                    confidence="high",
                    explanation="Currency mismatch.",
                    recommended_action="Ensure signal passes correct currency."
                )
        return None
