from app.payment_service.service import PaymentService
from app.payment_service.processor import PaymentProcessor
from app.recovery_engine.coordinator import RecoveryCoordinator
from app.recovery_engine.engine import RecoveryAction


def create_processing_payment():
    service = PaymentService()

    payment = service.create_payment(
        amount=12500,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    return payment


def test_matching_payment_requires_no_recovery():
    payment = create_processing_payment()

    processor = PaymentProcessor()
    processor.accept_payment(payment)

    coordinator = RecoveryCoordinator()

    result = coordinator.process(
        payment=payment,
        processor_payment=processor.get_payment(
            payment.transaction_id
        ),
    )

    assert result.reconciliation.status == "MATCH"
    assert result.policy.action == RecoveryAction.NO_ACTION
    assert result.execution is None


def test_processing_completed_triggers_automatic_reversal():
    payment = create_processing_payment()

    processor = PaymentProcessor()
    processor.accept_payment(payment)
    processor.complete_payment(payment.transaction_id)

    coordinator = RecoveryCoordinator()

    result = coordinator.process(
        payment=payment,
        processor_payment=processor.get_payment(
            payment.transaction_id
        ),
    )

    assert result.reconciliation.status == "MISMATCH"
    assert result.policy.action == RecoveryAction.REVERSE
    assert result.execution is not None
    assert result.execution.success is True


def test_processing_failed_triggers_retry_policy():
    payment = create_processing_payment()

    processor = PaymentProcessor()
    processor.accept_payment(payment)
    processor.fail_payment(payment.transaction_id)

    coordinator = RecoveryCoordinator()

    result = coordinator.process(
        payment=payment,
        processor_payment=processor.get_payment(
            payment.transaction_id
        ),
    )

    assert result.reconciliation.status == "MISMATCH"
    assert result.policy.action == RecoveryAction.RETRY
    assert result.execution is not None
    assert result.execution.success is True


def test_unknown_reconciliation_state_is_escalated():
    payment = create_processing_payment()

    processor = PaymentProcessor()
    processor.accept_payment(payment)

    processor_payment = processor.get_payment(
        payment.transaction_id
    )

    processor_payment.status = "UNKNOWN"

    coordinator = RecoveryCoordinator()

    result = coordinator.process(
        payment=payment,
        processor_payment=processor_payment,
    )

    assert result.policy.action == RecoveryAction.ESCALATE
    assert result.execution is None