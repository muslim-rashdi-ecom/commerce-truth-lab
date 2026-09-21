from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, PaymentMethod
)
from ctl_engine.rules.base import AuditRule

class RuleCTL007(AuditRule):
    rule_id = "CTL-007"
    rule_name = "Overcollection Against Order Total"
    category = FindingCategory.cod_collection
    severity = Severity.medium
    owner = "operations"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if order.payment_method == PaymentMethod.cod:
            for s in settlements:
                if s.collected_amount_minor is not None and s.collection_currency == order.currency:
                    if s.collected_amount_minor > order.total_amount_minor:
                        return FindingResult(
                            rule_id=self.rule_id,
                            rule_name=self.rule_name,
                            category=self.category,
                            severity=self.severity,
                            order_id=order.id,
                            observed=f"Collected COD amount {s.collected_amount_minor} is greater than order total {order.total_amount_minor}.",
                            source_records=[
                                EvidenceRef(source_id="orders", record_type="Order", record_id=order.id),
                                EvidenceRef(source_id="settlements", record_type="CourierSettlement", record_id=s.id)
                            ],
                            assumptions=["Courier should collect exactly the order amount."],
                            not_proven=["Does not prove fraud (could be tip or fee addition)."],
                            next_step="Review collection policy.",
                            owner=self.owner,
                            confidence="high",
                            explanation="Overcollection in COD.",
                            recommended_action="Verify with courier."
                        )
        return None
