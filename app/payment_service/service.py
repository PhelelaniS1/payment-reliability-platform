from .models import PaymentStatus, PaymentTransaction


class PaymentService:
    """Core payment transaction service."""

    def create_payment(
        self,
        amount: int,
        currency: str,
    ) -> PaymentTransaction:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        if not currency:
            raise ValueError("Currency is required.")

        payment = PaymentTransaction(
            amount=amount,
            currency=currency.upper(),
        )

        return payment

    def authorise_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.AUTHORISED)
        return payment

    def start_processing(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.PROCESSING)
        return payment

    def complete_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.COMPLETED)
        return payment

    def fail_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.FAILED)
        return payment

    def start_reconciliation(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.RECONCILING)
        return payment