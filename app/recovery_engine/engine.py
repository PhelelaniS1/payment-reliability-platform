from dataclasses import dataclass
from enum import Enum

from app.payment_service.models import PaymentStatus, PaymentTransaction
from app.reconciliation.engine import (
    ReconciliationRecord,
    ReconciliationResult,
)


class RecoveryAction(str, Enum):
    RETRY = "RETRY"
    REVERSE = "REVERSE"
    ESCALATE = "ESCALATE"
    NO_ACTION = "NO_ACTION"


@dataclass
class RecoveryRecord:
    transaction_id: str
    idempotency_key: str
    action: RecoveryAction
    reason: str


class RecoveryEngine:
    """Determines safe recovery actions for payment inconsistencies."""

    def __init__(self) -> None:
        self._processed_recoveries: set[str] = set()

    def evaluate(
        self,
        reconciliation: ReconciliationRecord,
    ) -> RecoveryRecord:

        transaction_id = reconciliation.transaction_id
        idempotency_key = f"recovery:{transaction_id}"

        if reconciliation.result == ReconciliationResult.MATCHED:
            return RecoveryRecord(
                transaction_id=transaction_id,
                idempotency_key=idempotency_key,
                action=RecoveryAction.NO_ACTION,
                reason="Payment states are consistent.",
            )

        if reconciliation.result == ReconciliationResult.UNKNOWN:
            return RecoveryRecord(
                transaction_id=transaction_id,
                idempotency_key=idempotency_key,
                action=RecoveryAction.ESCALATE,
                reason="Payment state requires manual investigation.",
            )

        if (
            reconciliation.internal_status == PaymentStatus.PROCESSING
            and reconciliation.external_status == PaymentStatus.COMPLETED
        ):
            if idempotency_key in self._processed_recoveries:
                return RecoveryRecord(
                    transaction_id=transaction_id,
                    idempotency_key=idempotency_key,
                    action=RecoveryAction.NO_ACTION,
                    reason="Recovery has already been initiated for this transaction.",
                )

            self._processed_recoveries.add(idempotency_key)

            return RecoveryRecord(
                transaction_id=transaction_id,
                idempotency_key=idempotency_key,
                action=RecoveryAction.REVERSE,
                reason=(
                    "External payment completed while the internal system "
                    "remained in processing."
                ),
            )

        if (
            reconciliation.internal_status == PaymentStatus.PROCESSING
            and reconciliation.external_status == PaymentStatus.FAILED
        ):
            return RecoveryRecord(
                transaction_id=transaction_id,
                idempotency_key=idempotency_key,
                action=RecoveryAction.RETRY,
                reason=(
                    "External payment failed while the internal system "
                    "remained in processing."
                ),
            )

        return RecoveryRecord(
            transaction_id=transaction_id,
            idempotency_key=idempotency_key,
            action=RecoveryAction.ESCALATE,
            reason="No safe automated recovery policy exists for this state.",
        )