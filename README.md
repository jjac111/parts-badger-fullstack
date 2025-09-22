## Parts Badger — CSV Quote Analyzer

A full‑stack application that ingests a CSV of stock codes and returns aggregated quote counts and total prices.

### How it works
- **Upload**: Submit a CSV with a required `stock_code` header.
- **Parse**: The backend validates input, deduplicates codes, and enqueues a Celery task.
- **Aggregate**: Distinct quotes per part are counted and prices summed in PostgreSQL.
- **Persist**: Results are stored in `CsvResult` with the original file name and timestamp.
- **Deliver**: REST endpoints provide paginated JSON; the frontend presents a searchable table.

### Technology stack
- **Backend**: Django 5, Django REST Framework, Celery + RabbitMQ, PostgreSQL
- **Frontend**: Next.js (React), TanStack Query, Material UI
- **Tooling**: Docker Compose, pytest

### Quick start
1) Start services
```bash
docker compose up -d db rabbitmq backend worker
```
2) Start the frontend
```bash
cd frontend
npm install
export NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
npm run dev
```
3) Open http://localhost:3000 and upload `samples/valid.csv`.

### API overview
- `POST /upload-csv/` → `{ "task_id": "..." }`
- `GET /tasks/{task_id}/` → Celery status and info
- `GET /csv-results/?search=ABC&page=1` → paginated results

### CSV requirements
- Header must include `stock_code` (case‑sensitive)
- Encoding: UTF‑8
- Empty `stock_code` rows are ignored; duplicates are deduplicated

### Configuration
- **Pagination**: `DJANGO_PAGE_SIZE` (default 25)
- **CORS**: Development allows `http://localhost:3000`
- **Database**: See `docker-compose.yml` for default credentials

### Testing
```bash
docker compose exec backend pytest -q
```

### Project structure
```text
backend/    # Django app, DRF endpoints, Celery tasks
frontend/   # Next.js app
samples/    # Example CSVs
docs/       # Planning notes
```



