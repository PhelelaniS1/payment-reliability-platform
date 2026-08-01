from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.payment_service.models import PaymentTransaction
from app.payment_service.repository import PaymentRepository
from app.payment_service.service import PaymentService


app = FastAPI(
    title="Payment Reliability Platform",
    description=(
        "A reliability-focused payment recovery platform "
        "for detecting and safely handling payment inconsistencies."
    ),
    version="0.1.0",
)


repository = PaymentRepository()
payment_service = PaymentService(repository)


class CreatePaymentRequest(BaseModel):
    amount: int = Field(
        gt=0,
        description="Amount in the smallest currency unit",
    )
    currency: str = Field(
        min_length=3,
        max_length=3,
    )


class PaymentResponse(BaseModel):
    transaction_id: str
    amount: int
    currency: str
    status: str


def payment_to_response(
    payment: PaymentTransaction,
) -> PaymentResponse:
    return PaymentResponse(
        transaction_id=payment.transaction_id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status.value,
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "payment-reliability-platform",
    }


@app.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=201,
)
def create_payment(
    request: CreatePaymentRequest,
) -> PaymentResponse:
    try:
        payment = payment_service.create_payment(
            amount=request.amount,
            currency=request.currency,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return payment_to_response(payment)


@app.get(
    "/payments/{transaction_id}",
    response_model=PaymentResponse,
)
def get_payment(
    transaction_id: str,
) -> PaymentResponse:
    try:
        payment = payment_service.get_payment(transaction_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return payment_to_response(payment)