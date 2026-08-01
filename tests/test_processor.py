from app.payment_service.models import PaymentStatus
from app.payment_service.processor import SimulatedPaymentProcessor
from app.payment_service.service import PaymentService


def create_payment():
    service = PaymentService()

    payment = service.create_payment(
        amount=12500,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    return payment


def test_processor_accepts_payment():
    payment = create_payment()

    processor = SimulatedPaymentProcessor()

    result = processor.submit_payment(payment)

    assert result.transaction_id == payment.transaction_id
    assert result.status == PaymentStatus.PROCESSING


def test_processor_state_can_diverge_from_internal_state():
    payment = create_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)

    processor.update_status(
        payment.transaction_id,
        PaymentStatus.COMPLETED,
    )

    service = PaymentService()
    service.complete_payment(payment)

    assert payment.status == PaymentStatus.COMPLETED
    assert (
        processor.get_payment(payment.transaction_id).status
        == PaymentStatus.COMPLETED
    )


def test_processor_payment_can_be_retrieved():
    payment = create_payment()

    processor = SimulatedPaymentProcessor()
    processor.submit_payment(payment)

    result = processor.get_payment(payment.transaction_id)

    assert result.transaction_id == payment.transaction_id