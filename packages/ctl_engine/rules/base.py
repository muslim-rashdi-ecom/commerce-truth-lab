from typing import List, Optional
from shared.models import (
    Order, Payment, CourierSettlement, Refund, PurchaseSignal, DataSource, FindingResult, FindingCategory, Severity
)

class AuditRule:
    rule_id: str
    rule_name: str
    category: FindingCategory
    severity: Severity
    owner: str
    
    def evaluate(self, order: Order, payments: List[Payment], settlements: List[CourierSettlement], refunds: List[Refund], signals: List[PurchaseSignal], sources: List[DataSource]) -> Optional[FindingResult]:
        raise NotImplementedError
