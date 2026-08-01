from dataclasses import dataclass

from app.payment_service.models import PaymentTransaction
from app.payment_service.processor import ProcessorPayment
from app.recovery_engine.engine import (
    RecoveryAction,
    RecoveryEngine,
    RecoveryRecord,
)
from app.recovery_engine.executor import (
    RecoveryExecutionResult,
    RecoveryExecutor,
)
from app.recovery_engine.policy import (
    RecoveryPolicy,
    RecoveryPolicyDecision,
)
from app.reconciliation.engine import (
    ReconciliationEngine,
    ReconciliationRecord,
)


@dataclass
class RecoveryWorkflowResult:
    reconciliation: ReconciliationRecord
    policy: RecoveryPolicyDecision
    execution: RecoveryExecutionResult | None


class RecoveryCoordinator:
    """
    Orchestrates the complete payment recovery workflow.

    Responsibilities are deliberately separated:

    ReconciliationEngine:
        Determines whether internal and external states agree.

    RecoveryEngine:
        Determines the recovery action based on reconciliation evidence.

    RecoveryPolicy:
        Determines whether the proposed recovery action is safe to automate.

    RecoveryExecutor:
        Executes an approved recovery action.
    """

    def __init__(
        self,
        reconciliation_engine: ReconciliationEngine | None = None,
        recovery_engine: RecoveryEngine | None = None,
        recovery_policy: RecoveryPolicy | None = None,
        recovery_executor: RecoveryExecutor | None = None,
    ) -> None:
        self.reconciliation_engine = (
            reconciliation_engine or ReconciliationEngine()
        )
        self.recovery_engine = recovery_engine or RecoveryEngine()
        self.recovery_policy = recovery_policy or RecoveryPolicy()
        self.recovery_executor = recovery_executor or RecoveryExecutor()

    def process(
        self,
        payment: PaymentTransaction,
        processor_payment: ProcessorPayment,
    ) -> RecoveryWorkflowResult:
        reconciliation = self.reconciliation_engine.reconcile(
            payment=payment,
            external_status=processor_payment.status,
        )

        recovery = self.recovery_engine.evaluate(
            reconciliation=reconciliation,
        )

        policy = self.recovery_policy.evaluate(
            payment=payment,
            processor_payment=processor_payment,
            proposed_action=recovery.action,
        )

        execution = None

        if policy.action in {
            RecoveryAction.REVERSE,
            RecoveryAction.RETRY,
        }:
            approved_recovery = RecoveryRecord(
                transaction_id=payment.transaction_id,
                idempotency_key=recovery.idempotency_key,
                action=policy.action,
                reason=policy.reason,
            )

            execution = self.recovery_executor.execute(
                payment=payment,
                recovery=approved_recovery,
            )

        return RecoveryWorkflowResult(
            reconciliation=reconciliation,
            policy=policy,
            execution=execution,
        )