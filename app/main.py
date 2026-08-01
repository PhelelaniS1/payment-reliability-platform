from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.payment_service.models import PaymentStatus, PaymentTransaction
from app.payment_service.processor import (
    PaymentProcessor,
    ProcessorPayment,
)
from app.payment_service.repository import PaymentRepository
from app.payment_service.service import PaymentService
from app.recovery_engine.coordinator import (
    RecoveryCoordinator,
    RecoveryWorkflowResult,
)


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
processor = PaymentProcessor()
recovery_coordinator = RecoveryCoordinator()


class CreatePaymentRequest(BaseModel):
    amount: int = Field(
        gt=0,
        description="Amount in the smallest currency unit",
    )
    currency: str = Field(
        min_length=3,
        max_length=3,
    )


class UpdateProcessorStatusRequest(BaseModel):
    status: PaymentStatus


class PaymentStatusRequest(BaseModel):
    status: PaymentStatus


class PaymentResponse(BaseModel):
    transaction_id: str
    amount: int
    currency: str
    status: str


class ProcessorPaymentResponse(BaseModel):
    transaction_id: str
    status: str


class ReconciliationResponse(BaseModel):
    transaction_id: str
    internal_status: str
    external_status: str
    result: str
    reason: str


class RecoveryPolicyResponse(BaseModel):
    action: str
    reason: str
    confidence: str


class RecoveryExecutionResponse(BaseModel):
    transaction_id: str
    action: str
    success: bool
    message: str
    event_type: str
    event_message: str
    timestamp: str


class RecoveryWorkflowResponse(BaseModel):
    reconciliation: ReconciliationResponse
    policy: RecoveryPolicyResponse
    execution: RecoveryExecutionResponse | None


def payment_to_response(
    payment: PaymentTransaction,
) -> PaymentResponse:
    return PaymentResponse(
        transaction_id=payment.transaction_id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status.value,
    )


def processor_to_response(
    processor_payment: ProcessorPayment,
) -> ProcessorPaymentResponse:
    return ProcessorPaymentResponse(
        transaction_id=processor_payment.transaction_id,
        status=processor_payment.status.value,
    )


def workflow_to_response(
    result: RecoveryWorkflowResult,
) -> RecoveryWorkflowResponse:
    execution = None

    if result.execution is not None:
        execution = RecoveryExecutionResponse(
            transaction_id=result.execution.transaction_id,
            action=result.execution.action.value,
            success=result.execution.success,
            message=result.execution.message,
            event_type=result.execution.audit_event.event_type,
            event_message=result.execution.audit_event.message,
            timestamp=result.execution.audit_event.timestamp.isoformat(),
        )

    return RecoveryWorkflowResponse(
        reconciliation=ReconciliationResponse(
            transaction_id=result.reconciliation.transaction_id,
            internal_status=result.reconciliation.internal_status.value,
            external_status=result.reconciliation.external_status.value,
            result=result.reconciliation.result.value,
            reason=result.reconciliation.reason,
        ),
        policy=RecoveryPolicyResponse(
            action=result.policy.action.value,
            reason=result.policy.reason,
            confidence=result.policy.confidence,
        ),
        execution=execution,
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

        processor.submit_payment(payment)

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


@app.put(
    "/payments/{transaction_id}/status",
    response_model=PaymentResponse,
)
def update_payment_status(
    transaction_id: str,
    request: PaymentStatusRequest,
) -> PaymentResponse:
    try:
        payment = payment_service.get_payment(transaction_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    try:
        payment.transition_to(request.status)
        payment_service._save(payment)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return payment_to_response(payment)


@app.get(
    "/payments/{transaction_id}/processor",
    response_model=ProcessorPaymentResponse,
)
def get_processor_payment(
    transaction_id: str,
) -> ProcessorPaymentResponse:
    try:
        processor_payment = processor.get_payment(transaction_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return processor_to_response(processor_payment)


@app.put(
    "/payments/{transaction_id}/processor",
    response_model=ProcessorPaymentResponse,
)
def update_processor_status(
    transaction_id: str,
    request: UpdateProcessorStatusRequest,
) -> ProcessorPaymentResponse:
    try:
        processor_payment = processor.update_status(
            transaction_id=transaction_id,
            status=request.status,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return processor_to_response(processor_payment)


@app.post(
    "/payments/{transaction_id}/reconcile",
    response_model=RecoveryWorkflowResponse,
)
def reconcile_payment(
    transaction_id: str,
) -> RecoveryWorkflowResponse:
    try:
        payment = payment_service.get_payment(transaction_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    try:
        processor_payment = processor.get_payment(transaction_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    result = recovery_coordinator.process(
        payment=payment,
        processor_payment=processor_payment,
    )

    payment_service._save(payment)

    return workflow_to_response(result)