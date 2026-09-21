from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef
)
from ctl_engine.rules.base import AuditRule

class RuleCTL011(AuditRule):
    rule_id = "CTL-011"
    rule_name = "Policy or Consent Mismatch"
    category = FindingCategory.policy_consent
    severity = Severity.medium
    owner = "legal-marketing"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        for s in signals:
            if s.consent_granted is False:
                return FindingResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    category=self.category,
                    severity=Severity.medium,
                    order_id=order.id,
                    observed=f"Purchase signal fired with explicit consent_granted=False.",
                    source_records=[
                        EvidenceRef(source_id="signals", record_type="PurchaseSignal", record_id=s.id)
                    ],
                    assumptions=["Tracking signals should respect user consent."],
                    not_proven=["Does not prove intentional GDPR/CCPA violation."],
                    next_step="Review cookie banner integration with tracking scripts.",
                    owner=self.owner,
                    confidence="high",
                    explanation="Consent violation.",
                    recommended_action="Fix CMP integration."
                )
            elif s.consent_granted is None:
                return FindingResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    category=self.category,
                    severity=Severity.low,
                    order_id=order.id,
                    observed=f"Purchase signal has unknown consent state.",
                    source_records=[
                        EvidenceRef(source_id="signals", record_type="PurchaseSignal", record_id=s.id)
                    ],
                    assumptions=["Consent state should be explicitly tracked."],
                    not_proven=["Does not prove compliance failure."],
                    next_step="Enable consent mode or similar explicit state tracking.",
                    owner=self.owner,
                    confidence="medium",
                    explanation="Missing consent state.",
                    recommended_action="Implement explicit consent state logging."
                )
        return None
