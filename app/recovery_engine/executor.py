from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.payment_service.models import PaymentStatus, PaymentTransaction
from app.recovery_engine.engine import RecoveryAction, RecoveryRecord


@dataclass
class AuditEvent:
    transaction_id: str
    event_type: str
    message: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class RecoveryExecutionResult:
    transaction_id: str
    action: RecoveryAction
    success: bool
    message: str
    audit_event: AuditEvent


class RecoveryExecutor:
    """
    Executes approved recovery actions against a simulated payment processor.

    The executor is intentionally separate from the RecoveryEngine:
    the engine decides what should happen; the executor performs it.
    """

    def __init__(self) -> None:
        self._executed_keys: set[str] = set()
        self.audit_events: list[AuditEvent] = []

    def execute(
        self,
        payment: PaymentTransaction,
        recovery: RecoveryRecord,
    ) -> RecoveryExecutionResult:

        if recovery.idempotency_key in self._executed_keys:
            event = self._record_event(
                transaction_id=payment.transaction_id,
                event_type="RECOVERY_DUPLICATE",
                message=(
                    "Recovery request ignored because the idempotency key "
                    "has already been executed."
                ),
            )

            return RecoveryExecutionResult(
                transaction_id=payment.transaction_id,
                action=RecoveryAction.NO_ACTION,
                success=False,
                message="Duplicate recovery request ignored.",
                audit_event=event,
            )

        if recovery.action == RecoveryAction.NO_ACTION:
            event = self._record_event(
                transaction_id=payment.transaction_id,
                event_type="RECOVERY_NO_ACTION",
                message="No recovery action was required.",
            )

            return RecoveryExecutionResult(
                transaction_id=payment.transaction_id,
                action=RecoveryAction.NO_ACTION,
                success=True,
                message="No recovery action required.",
                audit_event=event,
            )

        if recovery.action == RecoveryAction.ESCALATE:
            event = self._record_event(
                transaction_id=payment.transaction_id,
                event_type="RECOVERY_ESCALATED",
                message="Recovery requires manual investigation.",
            )

            return RecoveryExecutionResult(
                transaction_id=payment.transaction_id,
                action=RecoveryAction.ESCALATE,
                success=False,
                message="Recovery escalated for manual investigation.",
                audit_event=event,
            )

        self._executed_keys.add(recovery.idempotency_key)

        if recovery.action == RecoveryAction.REVERSE:
            return self._execute_reversal(payment)

        if recovery.action == RecoveryAction.RETRY:
            return self._execute_retry(payment)

        event = self._record_event(
            transaction_id=payment.transaction_id,
            event_type="RECOVERY_REJECTED",
            message="Unsupported recovery action.",
        )

        return RecoveryExecutionResult(
            transaction_id=payment.transaction_id,
            action=recovery.action,
            success=False,
            message="Unsupported recovery action.",
            audit_event=event,
        )

    def _execute_reversal(
        self,
        payment: PaymentTransaction,
    ) -> RecoveryExecutionResult:
        """
        Execute a controlled payment reversal.

        A payment in PROCESSING must first enter RECONCILING before
        it can transition to REVERSED.
        """

        if payment.status == PaymentStatus.PROCESSING:
            payment.transition_to(PaymentStatus.RECONCILING)

        payment.transition_to(PaymentStatus.REVERSED)

        event = self._record_event(
            transaction_id=payment.transaction_id,
            event_type="PAYMENT_REVERSED",
            message=(
                "Payment reversal successfully executed by the "
                "simulated payment processor."
            ),
        )

        return RecoveryExecutionResult(
            transaction_id=payment.transaction_id,
            action=RecoveryAction.REVERSE,
            success=True,
            message="Payment successfully reversed.",
            audit_event=event,
        )

    def _execute_retry(
        self,
        payment: PaymentTransaction,
    ) -> RecoveryExecutionResult:

        event = self._record_event(
            transaction_id=payment.transaction_id,
            event_type="PAYMENT_RETRY",
            message=(
                "Payment retry requested against the simulated "
                "payment processor."
            ),
        )

        return RecoveryExecutionResult(
            transaction_id=payment.transaction_id,
            action=RecoveryAction.RETRY,
            success=True,
            message="Payment retry successfully requested.",
            audit_event=event,
        )

    def _record_event(
        self,
        transaction_id: str,
        event_type: str,
        message: str,
    ) -> AuditEvent:

        event = AuditEvent(
            transaction_id=transaction_id,
            event_type=event_type,
            message=message,
        )

        self.audit_events.append(event)

        return event