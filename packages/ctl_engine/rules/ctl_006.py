from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, PaymentMethod, OrderStatus
)
from ctl_engine.rules.base import AuditRule

class RuleCTL006(AuditRule):
    rule_id = "CTL-006"
    rule_name = "Delivered Order Cash Shortfall"
    category = FindingCategory.cod_collection
    severity = Severity.medium
    owner = "operations"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if order.payment_method == PaymentMethod.cod and order.status == OrderStatus.delivered:
            for s in settlements:
                if s.collected_amount_minor is not None and s.collection_currency == order.currency:
                    if s.collected_amount_minor < order.total_amount_minor:
                        return FindingResult(
                            rule_id=self.rule_id,
                            rule_name=self.rule_name,
                            category=self.category,
                            severity=self.severity,
                            order_id=order.id,
                            observed=f"Collected COD amount {s.collected_amount_minor} is less than order total {order.total_amount_minor}.",
                            source_records=[
                                EvidenceRef(source_id="orders", record_type="Order", record_id=order.id),
                                EvidenceRef(source_id="settlements", record_type="CourierSettlement", record_id=s.id)
                            ],
                            assumptions=["Courier should collect the full order amount."],
                            not_proven=["Does not prove courier fraud (could be agreed partial return)."],
                            next_step="Investigate reason for partial collection.",
                            owner=self.owner,
                            confidence="high",
                            explanation="Shortfall in COD collection.",
                            recommended_action="Verify with courier."
                        )
        return None
