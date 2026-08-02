# Payment Reliability Platform

> A production-style payment reliability platform demonstrating transaction-state reconciliation, automated recovery, observability, and reliability engineering practices.

---

## Overview

The **Payment Reliability Platform** simulates a payment service interacting with an external payment processor.

The project models a common distributed-systems reliability problem:

> **What happens when two systems disagree about the state of a transaction?**

The platform detects transaction-state inconsistencies, evaluates recovery policies, executes recovery actions, and exposes operational metrics for monitoring and observability.

---

## Project Objectives

- Simulate a payment-processing environment
- Model internal and external transaction states
- Detect payment-state inconsistencies
- Implement payment-state reconciliation
- Automate recovery decisions
- Track recovery actions and outcomes
- Expose application and business-level metrics
- Provide service health checks
- Containerize the application
- Provide monitoring with Prometheus
- Provide observability with Grafana
- Demonstrate practical reliability engineering principles

---

## Architecture

```text
                         +----------------------+
                         |        Client        |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |       FastAPI        |
                         |         API          |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
      +---------------+     +---------------+     +-------------------+
      |    Payment    |     |   Processor   |     |  Reconciliation   |
      |    Service    |     |   Simulator   |     |    & Recovery     |
      +---------------+     +---------------+     +---------+---------+
                                                          |
                                                          v
                                                +-------------------+
                                                |    Prometheus     |
                                                |      Metrics      |
                                                +---------+---------+
                                                          |
                                                          v
                                                +-------------------+
                                                |      Grafana      |
                                                |   Observability   |
                                                +-------------------+


Payment Reliability Workflow
Payment Request
       |
       v
Create Transaction
       |
       v
Payment Processor
       |
       +-----------------------+
       |                       |
       v                       v
Internal State          Processor State
       |                       |
       +-----------+-----------+
                   |
                   v
            Reconciliation
                   |
                   v
          States Consistent?
             /           \
           Yes            No
            |              |
            v              v
        Complete       Recovery
                           |
                           v
                    Recovery Action
                           |
                           v
                    Record Outcome
Core Components
Payment API

The FastAPI application provides the HTTP interface for the platform.

Responsibilities include:

Payment creation
Request validation
Transaction lifecycle management
Health checks
Prometheus metrics
API responses
Payment Service

The Payment Service manages the internal representation and lifecycle of payment transactions.

It is responsible for maintaining payment state and coordinating payment processing.

Simulated Payment Processor

The simulated processor represents an external payment provider.

It allows the platform to model situations where the processor's transaction state differs from the internal application's state.

Reconciliation Engine

The reconciliation engine compares transaction state between the internal payment service and the external processor.

It identifies inconsistencies that require further action.

Recovery Engine

The recovery engine evaluates reconciliation results and determines the appropriate recovery action.

Recovery actions and their execution outcomes are tracked through application metrics.

Observability

The platform exposes Prometheus-compatible metrics covering both technical and business-level activity.

Application Metrics
HTTP request count
HTTP request duration
Process information
Application health
Payment Metrics
Payments created
Payment failures
Reconciliation Metrics
Reconciliation attempts
Reconciliation results
Recovery Metrics
Recovery actions selected
Recovery execution outcomes
Key Metrics
http_requests_total
http_request_duration_seconds
payments_created_total
payment_failures_total
reconciliation_attempts_total
reconciliation_results_total
recovery_actions_total
recovery_executions_total
Technology Stack
Technology	Purpose
Python 3.12	Application development
FastAPI	REST API
Pydantic	Data validation and models
Uvicorn	ASGI application server
Prometheus	Metrics collection
Grafana	Monitoring and visualization
Docker	Application containerization
Docker Compose	Service orchestration
Pytest	Automated testing
PowerShell	Local administration and testing
Project Structure
payment-reliability-platform/
|
+-- app/
|   +-- main.py
|   +-- metrics.py
|   +-- payment_service/
|       +-- models.py
|       +-- processor.py
|       +-- reconciliation.py
|       +-- recovery.py
|
+-- monitoring/
|   +-- prometheus/
|   |   +-- prometheus.yml
|   |
|   +-- grafana/
|
+-- tests/
|
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- .dockerignore
+-- .gitignore
+-- README.md
+-- CONTRIBUTORS.md
Getting Started
Prerequisites

Before running the platform, ensure the following are installed:

Docker
Docker Compose
Git
Python 3.12+
Clone the Repository
git clone https://github.com/PhelelaniS1/payment-reliability-platform.git
cd payment-reliability-platform
Start the Platform

Build and start all services:

docker compose up -d --build

Check the running services:

docker compose ps

Expected services:

Service	Port	Purpose
FastAPI	8000	Payment API
Prometheus	9090	Metrics collection
Grafana	3000	Monitoring and visualization
Health Check

The application exposes a health endpoint:

GET /health

Test it with PowerShell:

Invoke-RestMethod http://127.0.0.1:8000/health

Expected result:

status  service
------  -------
healthy payment-reliability-platform
Create a Payment

Create a payment using the API:

Invoke-WebRequest `
    -UseBasicParsing `
    -Method POST `
    -Uri "http://127.0.0.1:8000/payments" `
    -ContentType "application/json" `
    -Body '{"amount":10000,"currency":"ZAR"}'

Example response:

{
  "transaction_id": "00937e88-ac10-4195-912d-96314d1566e2",
  "amount": 10000,
  "currency": "ZAR",
  "status": "INITIATED"
}
Prometheus

Prometheus is available at:

http://127.0.0.1:9090

Check Prometheus health:

Invoke-RestMethod http://127.0.0.1:9090/-/healthy

Expected result:

Prometheus Server is Healthy.
Grafana

Grafana is available at:

http://127.0.0.1:3000

Grafana can be used to visualize platform activity including:

HTTP request rates
Request latency
Payment activity
Payment failures
Reconciliation activity
Recovery activity
Application health
Application Metrics

The application's Prometheus metrics endpoint is:

http://127.0.0.1:8000/metrics

Inspect payment metrics with PowerShell:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "payments_created_total"

Inspect payment failure metrics:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "payment_failures_total"
Docker Operations

Check running containers:

docker compose ps

View application logs:

docker logs --tail 100 payment-reliability-platform

Stop the platform:

docker compose down

Rebuild the platform:

docker compose up -d --build
Testing

Run the automated test suite with:

pytest

The test suite covers the core payment reliability functionality, including:

Payment processing
Transaction state
Payment processor behaviour
Reconciliation
Recovery
API behaviour
Metrics
Reliability Engineering Concepts

This project demonstrates practical reliability engineering concepts including:

Health checks
Observability
Metrics-driven monitoring
Distributed-state reconciliation
Failure detection
Automated recovery
Recovery tracking
Containerized services
API reliability
Business-level telemetry
Operational visibility
Why This Project Matters

Payment systems commonly depend on multiple services and external providers.

When these systems maintain separate representations of a transaction, temporary inconsistencies can occur.

For example:

Internal System       External Processor
     INITIATED              COMPLETED
          \                    /
           \                  /
            +----------------+
            | Reconciliation |
            +----------------+
                    |
                    v
             Recovery Logic

A reliable payment platform must be able to detect these inconsistencies, determine the correct course of action, and provide sufficient observability for operators to understand what happened.

This project demonstrates that workflow through a simplified, production-style architecture.

Project Status

Completed

The platform includes:

FastAPI payment API
Payment transaction models
Simulated payment processor
Payment-state reconciliation
Recovery workflow
Recovery execution tracking
Prometheus metrics
Grafana observability
Docker containerization
Docker Compose orchestration
Application health checks
Payment creation validation
Automated tests
Author

Phelelani Sithole

Cloud & Platform Engineering | AWS | Kubernetes | Docker | Terraform | CI/CD | Observability | Reliability Engineering

GitHub:

https://github.com/PhelelaniS1

LinkedIn:

https://www.linkedin.com/in/phelelanisithole/

Contributors

See CONTRIBUTORS.md.

License

This project is intended for educational, portfolio, and demonstration purposes.

Acknowledgements

Built as a practical demonstration of modern:

Cloud Engineering
Platform Engineering
DevOps
Site Reliability Engineering
Observability
Distributed Systems
Payment Reliability