from prometheus_client import Counter, Histogram


# HTTP / Golden Signals

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests.",
    ["method", "path", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)


# Payment reliability

PAYMENTS_CREATED_TOTAL = Counter(
    "payments_created_total",
    "Total number of payments successfully created.",
)

PAYMENT_FAILURES_TOTAL = Counter(
    "payment_failures_total",
    "Total number of payment processing failures.",
)


# Reconciliation reliability

RECONCILIATION_ATTEMPTS_TOTAL = Counter(
    "reconciliation_attempts_total",
    "Total number of reconciliation attempts.",
)

RECONCILIATION_RESULTS_TOTAL = Counter(
    "reconciliation_results_total",
    "Total reconciliation results by outcome.",
    ["result"],
)


# Recovery reliability

RECOVERY_ACTIONS_TOTAL = Counter(
    "recovery_actions_total",
    "Total recovery actions selected by the recovery engine.",
    ["action"],
)

RECOVERY_EXECUTIONS_TOTAL = Counter(
    "recovery_executions_total",
    "Total recovery executions by action and outcome.",
    ["action", "outcome"],
)
