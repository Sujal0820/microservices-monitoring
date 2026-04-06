# Step 2: Building First Microservice with Metrics

## Overview

In this step, the first microservice (API Gateway) was implemented using FastAPI. The service was instrumented with Prometheus metrics to enable real-time monitoring of requests, latency, and errors.

This step marks the transition from project setup to actual system behavior.

---

## Objective

* Build a functional microservice
* Integrate Prometheus-compatible metrics
* Simulate real-world API behavior (latency and failures)
* Expose a `/metrics` endpoint for monitoring

---

## Tech Stack Used

* FastAPI (Python web framework)
* prometheus_client (metrics instrumentation)
* Uvicorn (ASGI server)

---

## Implemented Features

### 1. API Endpoints

* `/` → Basic service response
* `/error` → Simulates random failures
* `/metrics` → Exposes Prometheus metrics

---

### 2. Metrics Collected

#### Request Count

Tracks total number of HTTP requests with labels:

* Method (GET, POST, etc.)
* Endpoint
* Status code

#### Request Latency

Measures response time for each request:

* Unit: seconds
* Stored as histogram for percentile calculations (p95, p99)

#### Error Count

Tracks number of failed requests for specific endpoints

---

### 3. Middleware-Based Monitoring

A middleware was implemented to:

* Capture request start time
* Measure latency
* Record metrics automatically for every request

This approach ensures:

* No duplication of monitoring logic
* Centralized observability

---

### 4. Realistic Simulation

#### Latency Simulation

Random delay added to endpoints to mimic real-world response times.

#### Error Simulation

Random failures introduced (30% probability) to simulate unstable systems.

This helps in:

* Testing monitoring dashboards
* Observing error spikes and latency changes

---

## Metrics Endpoint

The service exposes metrics at:

```id="b5y3zt"
/metrics
```

This endpoint is scraped by Prometheus to collect time-series data.

---

## Example Metrics Observed

* http_requests_total
* http_request_duration_seconds
* http_errors_total

These metrics form the foundation for:

* Traffic analysis
* Latency monitoring
* Error tracking

---

## Key Learning

* Observability starts at the application level, not the dashboard
* Metrics must be designed thoughtfully (labels, structure)
* Simulating real-world behavior is essential for meaningful dashboards

---

## Challenges Faced

* Understanding how Prometheus metrics work internally
* Designing meaningful labels for metrics
* Handling latency simulation without affecting structure

---

## Outcome

A fully functional microservice capable of:

* Handling API requests
* Generating real-time metrics
* Simulating real-world system behavior

---

## Next Step

Containerize the service using Docker and integrate it into a multi-service environment.
