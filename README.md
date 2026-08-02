# Payment Reliability Platform



> A production-style payment reliability platform demonstrating transaction-state reconciliation, automated recovery, observability, and reliability engineering practices.



\---



\## ðŸ“‹ Overview



The \*\*Payment Reliability Platform\*\* simulates a payment service communicating with an external payment processor.



The project models a common distributed-systems reliability problem:



> \*\*What happens when two systems disagree about the state of a transaction?\*\*



The platform detects transaction-state inconsistencies, evaluates recovery policies, executes recovery actions, and exposes operational metrics for monitoring.



\---



\## ðŸŽ¯ Objectives



\* Simulate a payment-processing environment

\* Model internal and external transaction states

\* Detect payment-state inconsistencies

\* Implement payment reconciliation

\* Automate recovery decisions

\* Track recovery actions and outcomes

\* Expose application and business-level metrics

\* Provide service health checks

\* Containerize the application

\* Provide monitoring through Prometheus

\* Provide observability through Grafana



\---



\## ðŸ—ï¸ Architecture



```text

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚       Client        â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;                                   â–¼

&#x20;                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                        â”‚      FastAPI        â”‚

&#x20;                        â”‚        API          â”‚

&#x20;                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                   â”‚

&#x20;             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;             â”‚                     â”‚                     â”‚

&#x20;             â–¼                     â–¼                     â–¼

&#x20;      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;      â”‚   Payment    â”‚      â”‚  Processor   â”‚      â”‚ Reconciliation   â”‚

&#x20;      â”‚   Service    â”‚      â”‚   Simulator   â”‚      â”‚   \& Recovery     â”‚

&#x20;      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                                           â”‚

&#x20;                                                           â–¼

&#x20;                                                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                                                  â”‚    Prometheus   â”‚

&#x20;                                                  â”‚     Metrics     â”‚

&#x20;                                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜

&#x20;                                                           â”‚

&#x20;                                                           â–¼

&#x20;                                                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”

&#x20;                                                  â”‚     Grafana     â”‚

&#x20;                                                  â”‚  Observability  â”‚

&#x20;                                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜



                                  Payment Request
      â”‚
      â–¼
Create Transaction
      â”‚
      â–¼
Payment Processor
      â”‚
      â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
      â”‚               â”‚
      â–¼               â–¼
Internal State    Processor State
      â”‚               â”‚
      â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
              â–¼
       Reconciliation
              â”‚
              â–¼
     State Consistent?
        â”‚          â”‚
       Yes         No
        â”‚           â”‚
        â–¼           â–¼
     Complete    Recovery
                    â”‚
                    â–¼
             Recovery Action
                    â”‚
                    â–¼
             Record Outcome

ðŸ§© Core Components
Payment API

The FastAPI application provides the HTTP interface for the platform.

Responsibilities include:

Payment creation
Transaction lifecycle management
Request validation
Health checks
Prometheus metrics
Payment Service

Manages the internal representation and lifecycle of payment transactions.

Simulated Payment Processor

Represents an external payment processor and allows the platform to model differences between internal and external transaction states.

Reconciliation Engine

Compares payment state across systems and identifies inconsistencies requiring further action.

Recovery Engine

Evaluates reconciliation results and selects appropriate recovery actions.

Recovery actions and execution outcomes are exposed through application metrics.

ðŸ“Š Observability

The platform exposes Prometheus-compatible metrics for technical and business-level monitoring.

Application Metrics
HTTP request count
HTTP request duration
Service health
Process information
Payment Metrics
Payments created
Payment failures
Reconciliation attempts
Reconciliation results
Recovery actions
Recovery execution outcomes

Example metrics:

http_requests_total
http_request_duration_seconds
payments_created_total
payment_failures_total
reconciliation_attempts_total
reconciliation_results_total
recovery_actions_total
recovery_executions_total
ðŸ› ï¸ Technology Stack
Technology	Purpose
Python 3.12	Application development
FastAPI	REST API
Pydantic	Data validation and models
Prometheus	Metrics collection
Grafana	Monitoring and visualization
Docker	Containerization
Docker Compose	Service orchestration
Uvicorn	ASGI application server
PowerShell	Local testing and administration
ðŸ“ Project Structure
payment-reliability-platform/
â”‚
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py
â”‚   â”œâ”€â”€ metrics.py
â”‚   â”‚
â”‚   â””â”€â”€ payment_service/
â”‚       â”œâ”€â”€ models.py
â”‚       â”œâ”€â”€ processor.py
â”‚       â”œâ”€â”€ reconciliation.py
â”‚       â””â”€â”€ recovery.py
â”‚
â”œâ”€â”€ monitoring/
â”‚   â”œâ”€â”€ prometheus/
â”‚   â”‚   â””â”€â”€ prometheus.yml
â”‚   â””â”€â”€ grafana/
â”‚
â”œâ”€â”€ tests/
â”‚
â”œâ”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .dockerignore
â”œâ”€â”€ .gitignore
â”œâ”€â”€ README.md
â””â”€â”€ CONTRIBUTORS.md

ðŸš€ Getting Started
Prerequisites
Docker
Docker Compose
Git
Python 3.12+
Clone the Repository
git clone https://github.com/PhelelaniS1/payment-reliability-platform.git
cd payment-reliability-platform
Start the Platform
docker compose up -d --build
Check Services
docker compose ps
â¤ï¸ Health Check

The application provides a health endpoint:

GET /health

Test it with PowerShell:

Invoke-RestMethod http://127.0.0.1:8000/health

Expected response:

status  service
------  -------
healthy payment-reliability-platform
ðŸ’³ Create a Payment

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
ðŸ“ˆ Prometheus

Prometheus is available at:

http://127.0.0.1:9090

Check Prometheus health:

Invoke-RestMethod http://127.0.0.1:9090/-/healthy

Expected response:

Prometheus Server is Healthy.
ðŸ“Š Grafana

Grafana is available at:

http://127.0.0.1:3000

Grafana can be used to visualize:

HTTP request rates
Request latency
Payment activity
Payment failures
Reconciliation activity
Recovery activity
Application health
ðŸ”Ž Inspect Application Metrics

The application's Prometheus metrics endpoint is:

http://127.0.0.1:8000/metrics

For example:

Invoke-RestMethod http://127.0.0.1:8000/metrics |
    Select-String "payments_created_total"
ðŸ³ Docker Services

The platform runs as a Docker Compose environment containing:

Service	Port	Purpose
FastAPI	8000	Payment API
Prometheus	9090	Metrics collection
Grafana	3000	Observability

Check running containers:

docker compose ps

View application logs:

docker logs --tail 100 payment-reliability-platform

Stop the platform:

docker compose down
ðŸ§ª Testing

Run the test suite with:

pytest

The tests cover the core payment reliability functionality, including payment processing, transaction state, reconciliation, recovery, API behaviour, and metrics.

ðŸ” Reliability Engineering Concepts

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
ðŸ’¡ Why This Project Matters

Payment systems can become inconsistent when multiple services maintain different representations of the same transaction.

For example, a payment could be:

Initiated internally but missing externally
Completed externally but still pending internally
Failed in one system while appearing successful in another
Temporarily inconsistent because of communication failures

This project demonstrates how reconciliation, automated recovery, and observability can be combined to improve the reliability of payment-processing systems.

ðŸ“Œ Project Status

Completed

The platform includes:

FastAPI payment API
Payment transaction models
Simulated payment processor
Payment reconciliation
Recovery workflow
Prometheus metrics
Grafana observability
Docker containerization
Docker Compose orchestration
Application health checks
Payment creation validation
ðŸ‘¤ Author
Phelelani Sithole

Cloud & Platform Engineering | AWS | Kubernetes | Docker | Terraform | CI/CD | Observability | Reliability Engineering

GitHub:
https://github.com/PhelelaniS1

LinkedIn:
https://www.linkedin.com/in/phelelanisithole/

ðŸ¤ Contributors

See CONTRIBUTORS.md.

ðŸ“„ License

This project is intended for educational, portfolio, and demonstration purposes.

â­ Acknowledgements

Built as a practical demonstration of modern cloud, platform engineering, DevOps, observability, and reliability engineering principles.


### 3. Save it correctly

In Notepad:

**File â†’ Save**

Make sure the filename is:

```text
README.md

If Notepad shows Save as type, select:

All Files (*.*)

Do not save it as:

README.md.txt
4. Close Notepad

Then run:

Get-Item README.md | Select-Object Name, Length

You should now get something like:

Name       Length
----       ------
README.md  7000

Then run:

Get-Content README.md -TotalCount 10

If you see:

# ðŸ’³ Payment Reliability Platform
