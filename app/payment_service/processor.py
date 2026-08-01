from dataclasses import dataclass
from typing import Dict

from .models import PaymentStatus, PaymentTransaction


@dataclass
class ProcessorPayment:
    transaction_id: str
    status: PaymentStatus


class SimulatedPaymentProcessor:
    """
    Simulates an external payment processor.

    This deliberately lives outside PaymentService so that the platform
    can model the real-world problem of two systems having different
    transaction states.
    """

    def __init__(self) -> None:
        self._payments: Dict[str, ProcessorPayment] = {}

    def submit_payment(
        self,
        payment: PaymentTransaction,
    ) -> ProcessorPayment:
        processor_payment = ProcessorPayment(
            transaction_id=payment.transaction_id,
            status=payment.status,
        )

        self._payments[payment.transaction_id] = processor_payment

        return processor_payment

    def get_payment(
        self,
        transaction_id: str,
    ) -> ProcessorPayment:
        if transaction_id not in self._payments:
            raise KeyError(
                f"Payment {transaction_id} was not found in processor."
            )

        return self._payments[transaction_id]

    def update_status(
        self,
        transaction_id: str,
        status: PaymentStatus,
    ) -> ProcessorPayment:
        processor_payment = self.get_payment(transaction_id)
        processor_payment.status = status

        return processor_payment