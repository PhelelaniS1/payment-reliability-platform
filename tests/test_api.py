from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_payment() -> dict:
    response = client.post(
        "/payments",
        json={
            "amount": 12500,
            "currency": "ZAR",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "payment-reliability-platform",
    }


def test_create_payment_through_api() -> None:
    payment = create_payment()

    assert payment["amount"] == 12500
    assert payment["currency"] == "ZAR"
    assert payment["status"] == "INITIATED"
    assert payment["transaction_id"]


def test_get_payment_through_api() -> None:
    payment = create_payment()
    transaction_id = payment["transaction_id"]

    response = client.get(
        f"/payments/{transaction_id}",
    )

    assert response.status_code == 200

    result = response.json()

    assert result["transaction_id"] == transaction_id
    assert result["amount"] == 12500
    assert result["currency"] == "ZAR"
    assert result["status"] == "INITIATED"


def test_payment_status_can_progress_through_api() -> None:
    payment = create_payment()
    transaction_id = payment["transaction_id"]

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "AUTHORISED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "AUTHORISED"

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "PROCESSING"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "PROCESSING"


def test_processor_status_can_be_updated_through_api() -> None:
    payment = create_payment()
    transaction_id = payment["transaction_id"]

    response = client.put(
        f"/payments/{transaction_id}/processor",
        json={"status": "COMPLETED"},
    )

    assert response.status_code == 200

    result = response.json()

    assert result["transaction_id"] == transaction_id
    assert result["status"] == "COMPLETED"


def test_processing_vs_completed_triggers_automatic_reversal() -> None:
    payment = create_payment()
    transaction_id = payment["transaction_id"]

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "AUTHORISED"},
    )
    assert response.status_code == 200

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "PROCESSING"},
    )
    assert response.status_code == 200

    response = client.put(
        f"/payments/{transaction_id}/processor",
        json={"status": "COMPLETED"},
    )
    assert response.status_code == 200

    response = client.post(
        f"/payments/{transaction_id}/reconcile",
    )

    assert response.status_code == 200

    result = response.json()

    assert result["reconciliation"]["internal_status"] == "PROCESSING"
    assert result["reconciliation"]["external_status"] == "COMPLETED"

    assert result["policy"]["action"] == "REVERSE"
    assert result["policy"]["confidence"] == "HIGH"

    assert result["execution"]["action"] == "REVERSE"
    assert result["execution"]["success"] is True
    assert result["execution"]["event_type"] == "PAYMENT_REVERSED"

    response = client.get(
        f"/payments/{transaction_id}",
    )

    assert response.status_code == 200
    assert response.json()["status"] == "REVERSED"


def test_processing_vs_failed_triggers_retry() -> None:
    payment = create_payment()
    transaction_id = payment["transaction_id"]

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "AUTHORISED"},
    )
    assert response.status_code == 200

    response = client.put(
        f"/payments/{transaction_id}/status",
        json={"status": "PROCESSING"},
    )
    assert response.status_code == 200

    response = client.put(
        f"/payments/{transaction_id}/processor",
        json={"status": "FAILED"},
    )
    assert response.status_code == 200

    response = client.post(
        f"/payments/{transaction_id}/reconcile",
    )

    assert response.status_code == 200

    result = response.json()

    assert result["reconciliation"]["internal_status"] == "PROCESSING"
    assert result["reconciliation"]["external_status"] == "FAILED"

    assert result["policy"]["action"] == "RETRY"
    assert result["policy"]["confidence"] == "HIGH"

    assert result["execution"]["action"] == "RETRY"
    assert result["execution"]["success"] is True
    assert result["execution"]["event_type"] == "PAYMENT_RETRY"


def test_unknown_payment_returns_404() -> None:
    response = client.get(
        "/payments/does-not-exist",
    )

    assert response.status_code == 404


def test_unknown_processor_payment_returns_404() -> None:
    response = client.get(
        "/payments/does-not-exist/processor",
    )

    assert response.status_code == 404