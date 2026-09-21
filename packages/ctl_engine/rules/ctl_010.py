from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL010(AuditRule):
    rule_id = "CTL-010"
    rule_name = "Unsupported Source / Ambiguous Mapping"
    category = FindingCategory.mapping
    severity = Severity.info
    owner = "data-ops"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        for src in sources:
            if src.completeness_status in ('incomplete', 'ambiguous'):
                return FindingResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    category=self.category,
                    severity=self.severity,
                    order_id=order.id,
                    observed=f"Source {src.name} has completeness status {src.completeness_status}.",
                    source_records=[],
                    assumptions=["All sources should map cleanly without ambiguity."],
                    not_proven=["Does not prove data corruption."],
                    next_step="Review mapping rules for this source.",
                    owner=self.owner,
                    confidence="medium",
                    explanation="Ambiguous mapping.",
                    recommended_action="Refine mapper config."
                )
        return None
