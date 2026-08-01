from app.payment_service.models import PaymentStatus
from app.payment_service.service import PaymentService
from app.reconciliation.engine import (
    ReconciliationEngine,
    ReconciliationResult,
)


def test_matching_payment_states_are_reconciled():
    service = PaymentService()
    engine = ReconciliationEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)
    service.complete_payment(payment)

    result = engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    assert result.result == ReconciliationResult.MATCHED


def test_processing_vs_completed_is_detected_as_mismatch():
    service = PaymentService()
    engine = ReconciliationEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    result = engine.reconcile(
        payment,
        PaymentStatus.COMPLETED,
    )

    assert result.result == ReconciliationResult.MISMATCH
    assert result.internal_status == PaymentStatus.PROCESSING
    assert result.external_status == PaymentStatus.COMPLETED


def test_processing_vs_failed_is_detected_as_mismatch():
    service = PaymentService()
    engine = ReconciliationEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    service.authorise_payment(payment)
    service.start_processing(payment)

    result = engine.reconcile(
        payment,
        PaymentStatus.FAILED,
    )

    assert result.result == ReconciliationResult.MISMATCH


def test_unrecognised_state_requires_investigation():
    service = PaymentService()
    engine = ReconciliationEngine()

    payment = service.create_payment(
        amount=10000,
        currency="ZAR",
    )

    result = engine.reconcile(
        payment,
        PaymentStatus.REVERSED,
    )

    assert result.result == ReconciliationResult.UNKNOWN