from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import random
import requests

app = FastAPI()

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status", "service"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency",
    ["endpoint", "service"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP Errors",
    ["endpoint"]
)

SERVICE_NAME = "api-gateway"

# Middleware to Track Metrics
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    latency = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
        service=SERVICE_NAME
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path,
        service=SERVICE_NAME
    ).observe(latency)

    return response

# Sample API Endpoint
@app.get("/")
async def home():
    try:
        auth_response = requests.get("http://auth-service:8001/auth", timeout=2)
        data_response = requests.get("http://data-service:8002/data", timeout=2)

        return {
            "auth": auth_response.json(),
            "data": data_response.json()
        }

    except Exception:
        ERROR_COUNT.labels(endpoint="/", service="api-gateway").inc()
        return {"error": "Service communication failed"}
    
# Error Simulation Endpoint
@app.get("/error")
async def error():
    if random.random() < 0.3:  # 30% chance of failure
        ERROR_COUNT.labels(endpoint="/error").inc()
        return {"error": "Simulated failure"}

    return {"message": "Success"}
# Metrics Endpoint

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)