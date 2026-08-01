from app.payment_service.models import PaymentTransaction


class PaymentRepository:
    """In-memory repository for payment transactions."""

    def __init__(self) -> None:
        self._payments: dict[str, PaymentTransaction] = {}

    def save(self, payment: PaymentTransaction) -> PaymentTransaction:
        self._payments[payment.transaction_id] = payment
        return payment

    def get(self, transaction_id: str) -> PaymentTransaction | None:
        return self._payments.get(transaction_id)

    def exists(self, transaction_id: str) -> bool:
        return transaction_id in self._payments

    def all(self) -> list[PaymentTransaction]:
        return list(self._payments.values())