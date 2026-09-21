from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL012(AuditRule):
    rule_id = "CTL-012"
    rule_name = "Cross-Currency Comparison Guard"
    category = FindingCategory.guard
    severity = Severity.info
    owner = "data-ops"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        currencies = {order.currency}
        for p in payments:
            currencies.add(p.currency)
        for s in settlements:
            currencies.add(s.collection_currency)
        for r in refunds:
            currencies.add(r.currency)
        for s in signals:
            currencies.add(s.currency)
            
        if len(currencies) > 1:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"Multiple currencies involved: {', '.join([c.value for c in currencies])}. Direct value comparisons may be skipped.",
                source_records=[EvidenceRef(source_id="orders", record_type="Order", record_id=order.id)],
                assumptions=["Rules require matching currencies for valid numeric comparisons."],
                not_proven=["Does not prove errors in actual conversion rates."],
                next_step="Ensure daily exchange rates are provided for cross-currency audits.",
                owner=self.owner,
                confidence="high",
                explanation="Currencies differ, preventing exact math.",
                recommended_action="Provide conversion rates."
            )
        return None
