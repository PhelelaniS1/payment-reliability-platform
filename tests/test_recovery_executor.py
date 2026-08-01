from app.payment_service.models import PaymentStatus
from app.payment_service.service import PaymentService
from app.reconciliation.engine import ReconciliationEngine
from app.recovery_engine.engine import RecoveryEngine, RecoveryAction
from app.recovery_engine.executor import RecoveryExecutor


def create_processing_payment():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    return payment


def test_reversal_is_executed_successfully():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()
    executor = RecoveryExecutor()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    recovery = recovery_engine.evaluate(reconciliation)
    result = executor.execute(payment, recovery)

    assert recovery.action == RecoveryAction.REVERSE
    assert result.success is True
    assert result.action == RecoveryAction.REVERSE
    assert payment.status == PaymentStatus.REVERSED


def test_reversal_creates_audit_event():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()
    executor = RecoveryExecutor()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    recovery = recovery_engine.evaluate(reconciliation)
    result = executor.execute(payment, recovery)

    assert result.audit_event.transaction_id == payment.transaction_id
    assert result.audit_event.event_type == "PAYMENT_REVERSED"
    assert len(executor.audit_events) == 1


def test_duplicate_execution_is_blocked():
    payment = create_processing_payment()

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()
    executor = RecoveryExecutor()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    recovery = recovery_engine.evaluate(reconciliation)

    first_result = executor.execute(payment, recovery)
    second_result = executor.execute(payment, recovery)

    assert first_result.success is True
    assert second_result.success is False
    assert second_result.action == RecoveryAction.NO_ACTION
    assert len(executor.audit_events) == 2


def test_unknown_recovery_is_escalated():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    reconciliation_engine = ReconciliationEngine()
    recovery_engine = RecoveryEngine()
    executor = RecoveryExecutor()

    reconciliation = reconciliation_engine.reconcile(
        payment,
        PaymentStatus.REVERSED,
    )

    recovery = recovery_engine.evaluate(reconciliation)
    result = executor.execute(payment, recovery)

    assert recovery.action == RecoveryAction.ESCALATE
    assert result.success is False
    assert result.action == RecoveryAction.ESCALATE
    assert payment.status == PaymentStatus.INITIATED