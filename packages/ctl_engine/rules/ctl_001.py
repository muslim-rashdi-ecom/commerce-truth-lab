from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, FindingStatus
)
from ctl_engine.rules.base import AuditRule

class RuleCTL001(AuditRule):
    rule_id = "CTL-001"
    rule_name = "Duplicate Purchase Identities"
    category = FindingCategory.duplicate_identity
    severity = Severity.high
    owner = "marketing-analytics"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if not signals:
            return None
            
        event_ids = set()
        for s in signals:
            if s.event_id:
                event_ids.add(s.event_id)
                
        if len(event_ids) > 1:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=self.severity,
                order_id=order.id,
                observed=f"Order {order.id} has {len(event_ids)} distinct event_ids across purchase signals.",
                source_records=[EvidenceRef(source_id="signals", record_type="PurchaseSignal", record_id=s.id) for s in signals],
                assumptions=["Multiple event_ids for the same order imply duplicated tracking events rather than normal deduplication."],
                not_proven=["Does not prove intentional fraud or causal ROAS improvement."],
                next_step="Investigate pixel/CAPI configuration to ensure event_id consistency.",
                owner=self.owner,
                confidence="high",
                explanation="Multiple distinct event_ids prevent proper deduplication on ad platforms.",
                recommended_action="Fix tracking configuration."
            )
        elif len(event_ids) == 1 and len(signals) > 1:
            return FindingResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                category=self.category,
                severity=Severity.info,
                order_id=order.id,
                observed=f"Order {order.id} has consistent event_ids across multiple signals.",
                source_records=[],
                assumptions=[],
                not_proven=[],
                next_step="None",
                owner=self.owner,
                confidence="high",
                explanation="Normal deduplication observed.",
                recommended_action="None",
                is_healthy_control=True
            )
            
        return None
