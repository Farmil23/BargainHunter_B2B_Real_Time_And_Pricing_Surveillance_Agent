# Supply Chain Intelligence System API Documentation

Welcome to the API Documentation for the Real-Time Market & Pricing Surveillance Agent. This backend is built using FastAPI and provides endpoints to trigger background web data scraping, analyze supply chain components, and monitor tasks.

## Base URL

By default, the backend runs locally at: `http://localhost:8000`

> [!TIP]
> **Interactive Documentation**
> Because this project is built with FastAPI, you get interactive documentation for free! Once the server is running, you can visit:
> - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) (Best for testing endpoints interactively)
> - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) (Great for readable, static documentation)

---

## 1. System Health

### `GET /health`

Checks if the API is running correctly.

**Response:**
```json
{
  "status": "ok",
  "project": "Supply Chain System"
}
```

---

## 2. Surveillance Operations

All surveillance endpoints are located under the `/api/v1/surveillance` prefix.

### `POST /api/v1/surveillance/analyze`

Triggers a new background surveillance task for a specific target URL and component. The scraping and AI analysis (LangGraph) will run asynchronously in the background.

**Request Body (`application/json`):**
```json
{
  "target_url": "https://example.com/products/cpu",
  "target_component": "Processor"
}
```
*   `target_url` (string, required): The URL to scrape and analyze.
*   `target_component` (string, required): The specific supply chain component to evaluate (e.g., "Processor", "GPU", "Lithium").

**Response (`200 OK`):**
```json
{
  "task_id": 1,
  "status": "pending",
  "message": "Surveillance task started successfully."
}
```
*   `task_id` (integer): The unique identifier for the initiated task. You can use this ID to poll for status.

---

### `GET /api/v1/surveillance/task/{task_id}`

Retrieves the current status and results of a specific surveillance task.

**Path Parameters:**
*   `task_id` (integer, required): The ID of the task.

**Response (`200 OK`):**
```json
{
  "id": 1,
  "target_url": "https://example.com/products/cpu",
  "target_component": "Processor",
  "status": "completed",
  "result_data": "{\"extracted_products\": [...], \"market_analysis\": \"...\", \"price_anomaly\": \"...\", \"recommendation\": \"...\", \"decision\": \"...\"}",
  "created_at": "2026-05-26T10:00:00.000Z"
}
```
*   `status` (string): The current state of the task (e.g., `pending`, `running`, `running_scraper`, `completed`, `failed`).
*   `result_data` (string, nullable): A JSON string containing the final analytical results from the AI agent. Only populated once the status is `completed` or `failed`.

**Error Response (`404 Not Found`):**
```json
{
  "detail": "Task not found"
}
```

---

### `GET /api/v1/surveillance/tasks`

Fetches a history list of surveillance tasks, ordered by creation date descending. Useful for populating the frontend dashboard.

**Query Parameters:**
*   `limit` (integer, optional): Maximum number of tasks to return. Default is `50`.

**Response (`200 OK`):**
```json
[
  {
    "id": 2,
    "target_url": "https://example.com/products/gpu",
    "target_component": "Graphics Card",
    "status": "running",
    "result_data": null,
    "created_at": "2026-05-26T10:15:00.000Z"
  },
  {
    "id": 1,
    "target_url": "https://example.com/products/cpu",
    "target_component": "Processor",
    "status": "completed",
    "result_data": "...",
    "created_at": "2026-05-26T10:00:00.000Z"
  }
]
```

---

## Data Structures

### `result_data` JSON Schema

When a task completes successfully, the `result_data` string field will parse into the following JSON structure:

```json
{
  "extracted_products": [ ... ],
  "market_analysis": { ... },
  "price_anomaly": { ... },
  "recommendation": "String detailing the strategic recommendation",
  "decision": "String indicating the final business decision"
}
```
*(Structure varies slightly depending on the output of the LangGraph AI nodes)*
