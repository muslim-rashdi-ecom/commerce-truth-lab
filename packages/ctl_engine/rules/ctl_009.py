from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, PaymentMethod
)
from ctl_engine.rules.base import AuditRule

class RuleCTL009(AuditRule):
    rule_id = "CTL-009"
    rule_name = "Incomplete Evidence Coverage"
    category = FindingCategory.coverage
    severity = Severity.low
    owner = "operations"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if order.payment_method == PaymentMethod.cod and not settlements:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"COD order has no CourierSettlement records.",
                source_records=[EvidenceRef(source_id="orders", record_type="Order", record_id=order.id)],
                assumptions=["COD orders require settlement evidence."],
                not_proven=["Does not prove missing funds (could be missing data file)."],
                next_step="Upload missing courier settlement reports.",
                owner=self.owner,
                confidence="high",
                explanation="Missing settlement data.",
                recommended_action="Upload data."
            )
        elif order.payment_method != PaymentMethod.cod and not payments:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"Non-COD order has no Payment records.",
                source_records=[EvidenceRef(source_id="orders", record_type="Order", record_id=order.id)],
                assumptions=["Prepaid orders require payment gateway evidence."],
                not_proven=["Does not prove missing funds."],
                next_step="Upload missing payment gateway reports.",
                owner=self.owner,
                confidence="high",
                explanation="Missing payment data.",
                recommended_action="Upload data."
            )
        return None
