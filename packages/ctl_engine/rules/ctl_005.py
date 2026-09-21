from typing import List, Optional
from datetime import datetime, timezone
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity, EvidenceRef, PaymentMethod, OrderStatus
)
from ctl_engine.rules.base import AuditRule

class RuleCTL005(AuditRule):
    rule_id = "CTL-005"
    rule_name = "COD Collection Overdue"
    category = FindingCategory.cod_collection
    severity = Severity.medium
    owner = "operations"
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        if order.payment_method == PaymentMethod.cod and order.status == OrderStatus.delivered:
            for s in settlements:
                if s.delivered_at:
                    now = datetime.now(timezone.utc).replace(tzinfo=None)
                    delivered_at = s.delivered_at.replace(tzinfo=None)
                    days_since = (now - delivered_at).days
                    
                    if days_since > s.grace_days and (s.settled_amount_minor is None or s.settled_amount_minor == 0):
                        return FindingResult(
                            rule_id=self.rule_id,
                            rule_name=self.rule_name,
                            category=self.category,
                            severity=self.severity,
                            order_id=order.id,
                            observed=f"COD order delivered {days_since} days ago (past {s.grace_days} day grace period) with no settlement.",
                            source_records=[
                                EvidenceRef(source_id="orders", record_type="Order", record_id=order.id),
                                EvidenceRef(source_id="settlements", record_type="CourierSettlement", record_id=s.id)
                            ],
                            assumptions=["Delivered COD orders should be settled within the grace period."],
                            not_proven=["Does not prove the courier stole the funds (could be batch processing delay)."],
                            next_step="Follow up with courier for settlement status.",
                            owner=self.owner,
                            confidence="high",
                            explanation="Overdue COD settlement.",
                            recommended_action="Chase courier."
                        )
                    elif days_since <= s.grace_days:
                        return FindingResult(
                            rule_id=self.rule_id,
                            rule_name=self.rule_name,
                            category=self.category,
                            severity=Severity.info,
                            order_id=order.id,
                            observed=f"COD order delivered recently (within grace period).",
                            source_records=[],
                            assumptions=[],
                            not_proven=[],
                            next_step="None",
                            owner=self.owner,
                            confidence="high",
                            explanation="Healthy COD order.",
                            recommended_action="None",
                            is_healthy_control=True
                        )
        return None
