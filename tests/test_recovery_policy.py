from app.payment_service.models import PaymentStatus
from app.payment_service.processor import SimulatedPaymentProcessor
from app.payment_service.service import PaymentService
from app.recovery_engine.engine import RecoveryAction
from app.recovery_engine.policy import RecoveryPolicy


def create_processing_payment():
    service = PaymentService()

    payment = service.create_payment(
        amount=12500,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    return payment


def test_processing_vs_completed_is_eligible_for_automatic_reversal():
    payment = create_processing_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)
    processor.update_status(
        payment.transaction_id,
        PaymentStatus.COMPLETED,
    )

    policy = RecoveryPolicy()

    decision = policy.evaluate(
        payment=payment,
        processor_payment=processor.get_payment(payment.transaction_id),
        proposed_action=RecoveryAction.REVERSE,
    )

    assert decision.action == RecoveryAction.REVERSE
    assert decision.confidence == "HIGH"


def test_processing_vs_failed_is_eligible_for_retry():
    payment = create_processing_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)
    processor.update_status(
        payment.transaction_id,
        PaymentStatus.FAILED,
    )

    policy = RecoveryPolicy()

    decision = policy.evaluate(
        payment=payment,
        processor_payment=processor.get_payment(payment.transaction_id),
        proposed_action=RecoveryAction.RETRY,
    )

    assert decision.action == RecoveryAction.RETRY
    assert decision.confidence == "HIGH"


def test_unknown_recovery_action_is_escalated():
    payment = create_processing_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)

    policy = RecoveryPolicy()

    decision = policy.evaluate(
        payment=payment,
        processor_payment=processor.get_payment(payment.transaction_id),
        proposed_action=RecoveryAction.ESCALATE,
    )

    assert decision.action == RecoveryAction.ESCALATE
    assert decision.confidence == "LOW"


def test_already_reversed_payment_cannot_be_automatically_reversed():
    payment = create_processing_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)

    payment.status = PaymentStatus.REVERSED

    policy = RecoveryPolicy()

    decision = policy.evaluate(
        payment=payment,
        processor_payment=processor.get_payment(payment.transaction_id),
        proposed_action=RecoveryAction.REVERSE,
    )

    assert decision.action == RecoveryAction.ESCALATE
    assert "already been reversed" in decision.reason


def test_mismatched_transaction_ids_are_escalated():
    payment = create_processing_payment()

    processor = SimulatedPaymentProcessor()

    other_payment = create_processing_payment()
    processor.submit_payment(other_payment)

    policy = RecoveryPolicy()

    decision = policy.evaluate(
        payment=payment,
        processor_payment=processor.get_payment(
            other_payment.transaction_id
        ),
        proposed_action=RecoveryAction.REVERSE,
    )

    assert decision.action == RecoveryAction.ESCALATE
    assert "transaction IDs do not match" in decision.reason