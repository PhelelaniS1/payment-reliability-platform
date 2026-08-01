from dataclasses import dataclass

from app.payment_service.models import PaymentStatus, PaymentTransaction
from app.payment_service.processor import ProcessorPayment
from app.recovery_engine.engine import RecoveryAction


@dataclass(frozen=True)
class RecoveryPolicyDecision:
    action: RecoveryAction
    reason: str
    confidence: str


class RecoveryPolicy:
    """
    Determines whether a payment mismatch is eligible for automated
    recovery.

    The policy is deliberately separate from the RecoveryEngine.
    The RecoveryEngine determines what recovery action is appropriate
    from reconciliation evidence, while this policy determines whether
    that action is safe to execute automatically.
    """

    def evaluate(
        self,
        payment: PaymentTransaction,
        processor_payment: ProcessorPayment,
        proposed_action: RecoveryAction,
    ) -> RecoveryPolicyDecision:

        if proposed_action == RecoveryAction.NO_ACTION:
            return RecoveryPolicyDecision(
                action=RecoveryAction.NO_ACTION,
                reason="No recovery is required.",
                confidence="HIGH",
            )

        if proposed_action == RecoveryAction.ESCALATE:
            return RecoveryPolicyDecision(
                action=RecoveryAction.ESCALATE,
                reason="Recovery engine requires manual investigation.",
                confidence="LOW",
            )

        if payment.status == PaymentStatus.REVERSED:
            return RecoveryPolicyDecision(
                action=RecoveryAction.ESCALATE,
                reason="Payment has already been reversed.",
                confidence="HIGH",
            )

        if payment.transaction_id != processor_payment.transaction_id:
            return RecoveryPolicyDecision(
                action=RecoveryAction.ESCALATE,
                reason="Internal and processor transaction IDs do not match.",
                confidence="HIGH",
            )

        if proposed_action == RecoveryAction.REVERSE:
            if (
                payment.status == PaymentStatus.PROCESSING
                and processor_payment.status == PaymentStatus.COMPLETED
            ):
                return RecoveryPolicyDecision(
                    action=RecoveryAction.REVERSE,
                    reason=(
                        "Processor completed the payment while the internal "
                        "system remains in processing."
                    ),
                    confidence="HIGH",
                )

            return RecoveryPolicyDecision(
                action=RecoveryAction.ESCALATE,
                reason=(
                    "Payment does not meet the conditions for an "
                    "automated reversal."
                ),
                confidence="MEDIUM",
            )

        if proposed_action == RecoveryAction.RETRY:
            if (
                payment.status == PaymentStatus.PROCESSING
                and processor_payment.status == PaymentStatus.FAILED
            ):
                return RecoveryPolicyDecision(
                    action=RecoveryAction.RETRY,
                    reason=(
                        "Processor reports failure while the internal "
                        "payment remains processing."
                    ),
                    confidence="HIGH",
                )

            return RecoveryPolicyDecision(
                action=RecoveryAction.ESCALATE,
                reason=(
                    "Payment does not meet the conditions for an "
                    "automated retry."
                ),
                confidence="MEDIUM",
            )

        return RecoveryPolicyDecision(
            action=RecoveryAction.ESCALATE,
            reason="Recovery action is not recognised by the policy.",
            confidence="LOW",
        )