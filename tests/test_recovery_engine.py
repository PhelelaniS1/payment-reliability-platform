from app.payment_service.models import PaymentStatus
from app.payment_service.service import PaymentService
from app.reconciliation.engine import ReconciliationEngine, ReconciliationResult
from app.recovery_engine.engine import RecoveryAction, RecoveryEngine


def create_processing_payment():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    return payment


def test_matching_payment_requires_no_recovery():
    service = PaymentService()
    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)
    service.complete_payment(payment)

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    recovery = recovery_engine.evaluate(reconciliation)

    assert reconciliation.result == ReconciliationResult.MATCHED
    assert recovery.action == RecoveryAction.NO_ACTION


def test_processing_completed_triggers_reversal_decision():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    recovery = recovery_engine.evaluate(reconciliation)

    assert recovery.action == RecoveryAction.REVERSE
    assert recovery.transaction_id == payment.transaction_id
    assert recovery.idempotency_key == f"recovery:{payment.transaction_id}"


def test_duplicate_recovery_is_blocked():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    first_recovery = recovery_engine.evaluate(reconciliation)
    second_recovery = recovery_engine.evaluate(reconciliation)

    assert first_recovery.action == RecoveryAction.REVERSE
    assert second_recovery.action == RecoveryAction.NO_ACTION


def test_processing_failed_triggers_retry():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.FAILED,
    )

    recovery = recovery_engine.evaluate(reconciliation)

    assert recovery.action == RecoveryAction.RETRY


def test_unknown_state_is_escalated():
    service = PaymentService()
    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.REVERSED,
    )

    recovery = recovery_engine.evaluate(reconciliation)

    assert recovery.action == RecoveryAction.ESCALATE