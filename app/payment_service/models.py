from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    AUTHORISED = "AUTHORISED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RECONCILING = "RECONCILING"
    REVERSED = "REVERSED"


@dataclass
class PaymentTransaction:
    amount: int
    currency: str
    transaction_id: str = field(default_factory=lambda: str(uuid4()))
    status: PaymentStatus = PaymentStatus.INITIATED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def transition_to(self, new_status: PaymentStatus) -> None:
        allowed_transitions = {
            PaymentStatus.INITIATED: {
                PaymentStatus.AUTHORISED,
                PaymentStatus.FAILED,
            },
            PaymentStatus.AUTHORISED: {
                PaymentStatus.PROCESSING,
                PaymentStatus.FAILED,
            },
            PaymentStatus.PROCESSING: {
                PaymentStatus.COMPLETED,
                PaymentStatus.FAILED,
                PaymentStatus.RECONCILING,
            },
            PaymentStatus.COMPLETED: {
                PaymentStatus.RECONCILING,
            },
            PaymentStatus.FAILED: {
                PaymentStatus.RECONCILING,
            },
            PaymentStatus.RECONCILING: {
                PaymentStatus.COMPLETED,
                PaymentStatus.REVERSED,
                PaymentStatus.FAILED,
            },
            PaymentStatus.REVERSED: set(),
        }

        if new_status not in allowed_transitions[self.status]:
            raise ValueError(
                f"Invalid payment transition: "
                f"{self.status.value} -> {new_status.value}"
            )

        self.status = new_status