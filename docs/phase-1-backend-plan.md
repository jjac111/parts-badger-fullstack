## Phase 1: Backend Plan — Async CSV Analyzer (Django + DRF + Celery + RabbitMQ)

### Scope
- Implement async CSV processing via Celery + RabbitMQ.
- Expose endpoints to upload CSV, check task status, and list results.
- Store `CsvResult` rows per `stock_code` with counts and price totals.

### Architecture (High level)
- Django API (DRF): receives upload, enqueues Celery task, serves listing.
- Celery worker: parses CSV, aggregates DB data, persists results.
- RabbitMQ: broker for Celery tasks. PostgreSQL: primary DB.

Flow:
1) POST /upload-csv → validate multipart file → enqueue task → return `task_id`.
2) Worker → parse CSV (require `stock_code`) → aggregate (joins on Part → QuoteLineItem) → bulk_create `CsvResult`.
3) Client polls GET /tasks/<task_id> or lists via GET /csv-results/ with filters/pagination.

### Data Models
- Part(stock_code, description)
- Quote(name, status, created_at)
- QuoteLineItem(quote_fk, part_fk, quantity, price)
- CsvResult(stock_code, number_quotes_found, total_price, file_uploaded, created_at)

### Endpoints (DRF)
- POST `/upload-csv/` → returns `{ task_id }`.
- GET `/tasks/<task_id>/` → `{ state, status, error? }`.
- GET `/csv-results/?search=<stock_code>&page=<n>` → paginated list.

### Services (pure, tested)
- parse_csv(file) → list[str] (validates header, trims, de-dupes optionally).
- aggregate_quotes(stock_codes) → list[DTO] with count and sum(price) via DB.
- persist_results(results, file_name) → bulk_create `CsvResult`.

### TDD Checklist (Phase 1)
1) Models: fields, constraints, index on `Part.stock_code`.
2) parse_csv tests: missing header, empty, bad mime, dupes/whitespace.
3) aggregate tests: 0-hit, multi-quote, decimal precision.
4) persist tests: bulk_create, file name propagation, created_at ordering.
5) API tests: upload happy path → returns task_id; error cases.
6) Task-status tests: unknown id, success, failure.
7) Results list tests: pagination, search, ordering.

### DevOps
- docker-compose: `db` (Postgres), `rabbitmq`, `backend`, `worker` (Celery).
- Celery app configured in Django; worker uses same codebase image.


### Tasks to Execute (Phase 1)
1) Bootstrap Django + DRF + Postgres settings.
2) Add models and migrations.
3) Configure Celery app + RabbitMQ; add worker service.
4) Implement parse/aggregate/persist services with tests.
5) Add Celery task orchestrating the pipeline with tests.
6) Implement API: POST /upload-csv, GET /tasks/<task_id>, GET /csv-results/ with tests.
7) Wire docker-compose and minimal README run steps.


