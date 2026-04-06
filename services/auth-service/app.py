from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import random

app = FastAPI()

# -----------------------------
# Metrics
# -----------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status", "service"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency",
    ["endpoint", "service"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total Errors",
    ["endpoint", "service"]
)

SERVICE_NAME = "auth-service"

# -----------------------------
# Middleware
# -----------------------------

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        raise

    latency = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=status_code,
        service=SERVICE_NAME
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path,
        service=SERVICE_NAME
    ).observe(latency)

    return response

# -----------------------------
# Auth Endpoint
# -----------------------------

@app.get("/auth")
async def auth():
    # Simulate slower auth
    delay = random.uniform(0.2, 0.6)
    time.sleep(delay)

    # Simulate failures
    if random.random() < 0.2:
        ERROR_COUNT.labels(endpoint="/auth", service=SERVICE_NAME).inc()
        raise HTTPException(status_code=500, detail="Auth Failed")

    return {"message": "Auth Success"}

# -----------------------------
# Metrics Endpoint
# -----------------------------

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)