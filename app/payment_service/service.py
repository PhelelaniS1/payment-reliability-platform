from typing import Optional

from .models import PaymentStatus, PaymentTransaction


class PaymentService:
    """Core payment transaction service.

    The repository is optional during the in-memory development phase.
    This preserves backwards compatibility with the existing unit tests
    while allowing persistence to be introduced incrementally.
    """

    def __init__(self, repository: Optional[object] = None) -> None:
        self.repository = repository

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

        self._save(payment)

        return payment

    def get_payment(
        self,
        transaction_id: str,
    ) -> PaymentTransaction:
        """Retrieve a payment by transaction ID."""

        if self.repository is None:
            raise ValueError(
                "Payment repository is not configured."
            )

        get_method = getattr(self.repository, "get", None)

        if get_method is None:
            raise AttributeError(
                "Configured payment repository must provide a get() method."
            )

        payment = get_method(transaction_id)

        if payment is None:
            raise ValueError(
                f"Payment {transaction_id} was not found."
            )

        return payment

    def authorise_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.AUTHORISED)
        self._save(payment)
        return payment

    def start_processing(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.PROCESSING)
        self._save(payment)
        return payment

    def complete_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.COMPLETED)
        self._save(payment)
        return payment

    def fail_payment(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.FAILED)
        self._save(payment)
        return payment

    def start_reconciliation(
        self,
        payment: PaymentTransaction,
    ) -> PaymentTransaction:
        payment.transition_to(PaymentStatus.RECONCILING)
        self._save(payment)
        return payment

    def _save(self, payment: PaymentTransaction) -> None:
        """Persist the payment when a repository is configured.

        The repository interface will be introduced properly in the
        persistence layer. For now, this keeps the domain service usable
        without external infrastructure.
        """

        if self.repository is None:
            return

        save_method = getattr(self.repository, "save", None)

        if save_method is None:
            raise AttributeError(
                "Configured payment repository must provide a save() method."
            )

        save_method(payment)