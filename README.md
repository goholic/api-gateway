# 🛡️ High-Performance API Gateway & Observability Service

A production-ready Middleware Proxy built with **FastAPI** and **Redis** to demonstrate scalable backend patterns: Distributed Tracing, Rate Limiting, and Traffic Shaping.

## 🚀 Why I Built This
Most backend tutorials stop at CRUD. I wanted to build the "invisible" infrastructure that keeps APIs alive in production. This project demonstrates how to handle **non-functional requirements** like reliability, observability, and security at the gateway level.

## 🏗️ Architecture
**Request Flow:**
`Client` -> `[Logging Middleware]` -> `[Rate Limiter (Token Bucket)]` -> `[API Endpoint]`

* **Correlation IDs:** Traces requests across distributed boundaries (Scenario B logic).
* **Rate Limiting:** Implemented the **Token Bucket** algorithm using Redis for distributed state management.
* **Atomic Operations:** Uses Redis `INCR` to prevent race conditions during high concurrency.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI (Asynchronous)
* **Data Store:** Redis (In-memory caching & locking)
* **Infrastructure:** Docker & Docker Compose
* **Package Manager:** uv

## 🔮 Roadmap & Future Improvements
I am actively working on scaling this gateway to support enterprise-level patterns:

1.  **🌍 Geo-Distributed Rate Limiting (CRDTs)**
    * **Goal:** Solve the "split-brain" problem where users get double allowances in multi-region deployments (e.g., NY vs. Singapore).
    * **Plan:** Implement Active-Active Redis replication or CRDTs (Conflict-free Replicated Data Types) to sync token usage across regions asynchronously.

2.  **🔌 Circuit Breaker Pattern**
    * **Goal:** Prevent cascading failures when a downstream service is struggling.
    * **Plan:** Integrate a "fail-fast" mechanism that temporarily blocks requests to a failing service (returning 503 immediately) to allow it time to recover.

3.  **📊 Real-time Traffic Dashboard**
    * **Goal:** Visualize the invisible.
    * **Plan:** Build a lightweight Streamlit or Grafana dashboard that connects to Redis to show live Request-Per-Second (RPS) metrics and "Top Blocked IPs."

4.  **🔑 API Key Management & Auth**
    * **Goal:** Move from IP-based limiting to User-Tier based limiting.
    * **Plan:** Add JWT validation middleware and distinct rate limits for "Free" vs. "Premium" users.

## ⚡ Quick Start

1.  **Clone the repo**
    ```bash
    git clone https://github.com/goholic/api-gateway.git
    cd api-gateway
    ```

2.  **Run with Docker (Recommended)**
    This spins up both the API and the Redis container in a private network.
    ```bash
    docker-compose up --build
    ```

3.  **Test the Rate Limiter**
    Hit the endpoint 6 times quickly to see the 429 Rejection:
    ```bash
    curl -v http://localhost:8000/ping
    ```

---

## 👨‍💻 Author

**Abir Sarkar** - *Senior Software Engineer (Systems & Backend)*
* [LinkedIn Profile](https://www.linkedin.com/in/abir-sarkar-dev/)