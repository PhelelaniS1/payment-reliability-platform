from dataclasses import dataclass
from enum import Enum

from app.payment_service.models import PaymentStatus, PaymentTransaction


class ReconciliationResult(str, Enum):
    MATCHED = "MATCHED"
    MISMATCH = "MISMATCH"
    UNKNOWN = "UNKNOWN"


@dataclass
class ReconciliationRecord:
    transaction_id: str
    internal_status: PaymentStatus
    external_status: PaymentStatus
    result: ReconciliationResult
    reason: str


class ReconciliationEngine:
    """Compares internal payment state with external processor state."""

    def reconcile(
        self,
        payment: PaymentTransaction,
        external_status: PaymentStatus,
    ) -> ReconciliationRecord:

        if payment.status == external_status:
            return ReconciliationRecord(
                transaction_id=payment.transaction_id,
                internal_status=payment.status,
                external_status=external_status,
                result=ReconciliationResult.MATCHED,
                reason="Internal and external payment states match.",
            )

        if (
            payment.status == PaymentStatus.PROCESSING
            and external_status == PaymentStatus.COMPLETED
        ):
            return ReconciliationRecord(
                transaction_id=payment.transaction_id,
                internal_status=payment.status,
                external_status=external_status,
                result=ReconciliationResult.MISMATCH,
                reason=(
                    "External processor completed the payment while "
                    "the internal system still reports processing."
                ),
            )

        if (
            payment.status == PaymentStatus.PROCESSING
            and external_status == PaymentStatus.FAILED
        ):
            return ReconciliationRecord(
                transaction_id=payment.transaction_id,
                internal_status=payment.status,
                external_status=external_status,
                result=ReconciliationResult.MISMATCH,
                reason=(
                    "External processor failed the payment while "
                    "the internal system still reports processing."
                ),
            )

        return ReconciliationRecord(
            transaction_id=payment.transaction_id,
            internal_status=payment.status,
            external_status=external_status,
            result=ReconciliationResult.UNKNOWN,
            reason="Payment state combination requires manual investigation.",
        )