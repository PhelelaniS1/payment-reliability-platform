# 💳 Payment Reliability Platform

> A production-style payment reliability platform demonstrating **transaction-state reconciliation, automated recovery, observability, and reliability engineering practices**.

<p align="center">

**FastAPI** • **Python 3.12** • **Docker** • **Prometheus** • **Grafana** • **Pytest**

</p>

---

## 📋 Overview

The **Payment Reliability Platform** simulates a payment service interacting with an external payment processor.

The project focuses on a common distributed-systems reliability problem:

> **What happens when two systems disagree about the state of a transaction?**

The platform is designed to detect transaction-state inconsistencies, evaluate recovery policies, execute recovery actions, and provide operational visibility through application and business-level metrics.

### The platform demonstrates

- 💳 Payment transaction processing
- 🔄 Transaction-state reconciliation
- 🧠 Automated recovery decisions
- 🛠️ Recovery execution tracking
- 📊 Prometheus metrics
- 📈 Grafana observability
- ❤️ Application health checks
- 🐳 Docker containerisation
- 🧪 Automated testing
- ⚙️ Reliability engineering principles

---

## 🎯 Project Objectives

The primary objectives of this project are to:

- Simulate a production-style payment-processing environment
- Model internal and external transaction states
- Detect transaction-state inconsistencies
- Implement payment-state reconciliation
- Automate recovery decisions
- Track recovery actions and outcomes
- Expose technical and business-level telemetry
- Provide application health monitoring
- Containerise the application
- Orchestrate services with Docker Compose
- Monitor the platform using Prometheus
- Visualise operational data using Grafana

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │        Client        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │         API          │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────────┐
      │    Payment    │     │   Processor   │     │  Reconciliation   │
      │    Service    │     │   Simulator   │     │    & Recovery     │
      └───────────────┘     └───────────────┘     └─────────┬─────────┘
                                                            │
                                                            ▼
                                                   ┌───────────────────┐
                                                   │    Prometheus     │
                                                   │      Metrics      │
                                                   └─────────┬─────────┘
                                                             │
                                                             ▼
                                                   ┌───────────────────┐
                                                   │      Grafana      │
                                                   │   Observability   │
                                                   └───────────────────┘
🔄 Payment Reliability Workflow
                         Payment Request
                                │
                                ▼
                       Create Transaction
                                │
                                ▼
                       Payment Processor
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          Internal State                Processor State
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                         Reconciliation
                                │
                                ▼
                      States Consistent?
                         │           │
                       YES           NO
                         │           │
                         ▼           ▼
                     Complete     Recovery
                                     │
                                     ▼
                              Recovery Action
                                     │
                                     ▼
                              Record Outcome

🎯 Why This Project Is Relevant to Electrum

This project was developed as a practical demonstration of the reliability challenges that can arise in payment-processing environments.

The design focuses on problems that are particularly relevant to payment technology platforms, including:

- 🔄 Transaction-state inconsistencies
- 🛡️ Failure detection and recovery
- 📊 Application and business-level observability
- 🚨 Operational visibility
- ♻️ Automated recovery workflows
- 🔍 Reconciliation between distributed systems
- 📈 Reliability-focused metrics
- 🐳 Containerized service operations
- ☁️ Production-oriented engineering practices

The project was also designed with the **Core Reliability Engineer / SRE challenges at Electrum** in mind, particularly around payment reliability, observability, resilience, automation, and safe recovery.

> **Note:** This is an independent portfolio project and is not affiliated with, sponsored by, or endorsed by Electrum.

🧩 Core Components
💳 Payment API

The FastAPI application provides the HTTP interface for the platform.

Responsibilities
Payment creation
Request validation
Transaction lifecycle management
API responses
Health checks
Prometheus metrics
⚙️ Payment Service

The Payment Service manages the internal representation and lifecycle of payment transactions.

Responsibilities
Maintain transaction state
Create payment transactions
Coordinate payment processing
Track payment lifecycle information
🌐 Simulated Payment Processor

The simulated processor represents an external payment provider.

It allows the platform to model situations where the external processor's transaction state differs from the internal application's state.

This provides a controlled environment for testing reconciliation and recovery behaviour.

🔄 Reconciliation Engine

The Reconciliation Engine compares transaction state between the internal payment service and the external processor.

It identifies situations where the two systems disagree and determines whether additional recovery processing is required.

Example
Internal System              External Processor
      │                              │
      │   INITIATED                  │
      │                              │
      │                         COMPLETED
      │                              │
      └──────────────┬───────────────┘
                     │
                     ▼
              Reconciliation
                     │
                     ▼
              State Difference
                     │
                     ▼
              Recovery Logic
🛠️ Recovery Engine

The Recovery Engine evaluates reconciliation results and selects an appropriate recovery action.

The platform records:

Recovery actions selected
Recovery execution attempts
Recovery execution outcomes
Recovery-related metrics

This provides visibility into how the system responds to inconsistent payment states.

📊 Observability

Observability is a core part of the platform.

The application exposes Prometheus-compatible metrics covering both technical and business-level activity.

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
🛠️ Technology Stack
Technology	Purpose
Python 3.12	Application development
FastAPI	REST API framework
Pydantic	Data validation and models
Uvicorn	ASGI application server
Prometheus	Metrics collection
Grafana	Monitoring and visualisation
Docker	Application containerisation
Docker Compose	Service orchestration
Pytest	Automated testing
PowerShell	Local administration and testing
📁 Project Structure
payment-reliability-platform/
│
├── app/
│   ├── main.py
│   ├── metrics.py
│   │
│   └── payment_service/
│       ├── models.py
│       ├── processor.py
│       ├── reconciliation.py
│       └── recovery.py
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   │
│   └── grafana/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
└── CONTRIBUTORS.md
🚀 Getting Started
Prerequisites

Before running the platform, make sure you have:

Docker
Docker Compose
Git
Python 3.12+
1️⃣ Clone the Repository
git clone https://github.com/PhelelaniS1/payment-reliability-platform.git
cd payment-reliability-platform
2️⃣ Start the Platform

Build and start all services:

docker compose up -d --build

Check the running services:

docker compose ps

Expected services:

Service	Port	Purpose
FastAPI	8000	Payment API
Prometheus	9090	Metrics collection
Grafana	3000	Monitoring and visualisation
❤️ Health Check

The application exposes a health endpoint:

GET /health

Test it with PowerShell:

Invoke-RestMethod http://127.0.0.1:8000/health

Expected response:

status  service
------  -------
healthy payment-reliability-platform
💳 Create a Payment

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
📈 Prometheus

Prometheus is available at:

http://127.0.0.1:9090

Check Prometheus health:

Invoke-RestMethod http://127.0.0.1:9090/-/healthy

Expected response:

Prometheus Server is Healthy.

Prometheus collects application and business-level telemetry from the FastAPI service.

📊 Grafana

Grafana is available at:

http://127.0.0.1:3000

Grafana can be used to visualise:

📈 HTTP request rates
⏱️ Request latency
💳 Payment activity
❌ Payment failures
🔄 Reconciliation activity
🛠️ Recovery activity
❤️ Application health
🔎 Application Metrics

The application's Prometheus metrics endpoint is:

http://127.0.0.1:8000/metrics

Inspect payment metrics:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "payments_created_total"

Inspect payment failure metrics:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "payment_failures_total"

Inspect reconciliation metrics:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "reconciliation"

Inspect recovery metrics:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "recovery"
🐳 Docker Operations
Check running containers
docker compose ps
View application logs
docker logs --tail 100 payment-reliability-platform
Follow application logs
docker logs -f payment-reliability-platform
Stop the platform
docker compose down
Rebuild the platform
docker compose up -d --build
🧪 Testing

Run the automated test suite with:

pytest

The test suite covers core payment reliability functionality, including:

Payment processing
Transaction state
Payment processor behaviour
Reconciliation
Recovery
API behaviour
Metrics
🔐 Reliability Engineering Concepts

This project demonstrates practical reliability engineering concepts including:

❤️ Health checks
📊 Observability
📈 Metrics-driven monitoring
🔄 Distributed-state reconciliation
🚨 Failure detection
🛠️ Automated recovery
📝 Recovery tracking
🐳 Containerised services
🌐 API reliability
💼 Business-level telemetry
🔎 Operational visibility
💡 Why This Project Matters

Payment systems commonly depend on multiple services and external providers.

When these systems maintain separate representations of a transaction, temporary inconsistencies can occur.

For example:

Internal System	External Processor	Potential Problem
INITIATED	COMPLETED	Internal state is behind
COMPLETED	PENDING	External state is behind
FAILED	COMPLETED	Transaction states conflict
PENDING	FAILED	Recovery may be required

A reliable payment platform must be able to:

Detect state inconsistencies
Compare transaction states
Determine the appropriate recovery action
Execute recovery logic
Record the outcome
Expose sufficient telemetry for operators

This project demonstrates that workflow through a simplified, production-style architecture.

📌 Project Status
✅ Completed

The platform currently includes:

✅ FastAPI payment API
✅ Payment transaction models
✅ Simulated payment processor
✅ Payment-state reconciliation
✅ Recovery workflow
✅ Recovery execution tracking
✅ Prometheus metrics
✅ Grafana observability
✅ Docker containerisation
✅ Docker Compose orchestration
✅ Application health checks
✅ Payment creation validation
✅ Automated tests
👤 Author
Phelelani Sithole

Cloud & Platform Engineering | AWS | Kubernetes | Docker | Terraform | CI/CD | Observability | Reliability Engineering

GitHub

https://github.com/PhelelaniS1

LinkedIn

https://www.linkedin.com/in/phelelanisithole/

🤝 Contributors

Contributions and improvements are welcome.

See CONTRIBUTORS.md for contributor information and contribution guidelines.

📄 License

This project is intended for:

Educational purposes
Portfolio demonstration
Reliability engineering experimentation
Cloud and platform engineering learning
⭐ Acknowledgements

Built as a practical demonstration of modern:

Cloud Engineering
Platform Engineering
DevOps
Site Reliability Engineering
Observability
Distributed Systems
Payment Reliability
Automated Recovery
