import pytest

from app.payment_service.models import PaymentStatus
from app.payment_service.service import PaymentService


def test_payment_can_complete_successfully():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)
    service.complete_payment(payment)

    assert payment.status == PaymentStatus.COMPLETED


def test_payment_can_enter_reconciliation():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)
    service.start_reconciliation(payment)

    assert payment.status == PaymentStatus.RECONCILING


def test_invalid_transition_is_rejected():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    with pytest.raises(ValueError, match="Invalid payment transition"):
        payment.transition_to(PaymentStatus.COMPLETED)


def test_payment_amount_must_be_positive():
    service = PaymentService()

    with pytest.raises(ValueError, match="greater than zero"):
        service.create_payment(
            amount=0,
            currency="ZAR",
        )


def test_currency_is_normalised():
    service = PaymentService()

    payment = service.create_payment(
        amount=10000,
        currency="zar",
    )

    assert payment.currency == "ZAR"