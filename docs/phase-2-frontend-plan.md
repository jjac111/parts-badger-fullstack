## Phase 2: Frontend Plan — CSV Analyzer (Next.js + MUI)

### Scope
- Single page to upload CSV and view results in a paginated filterable table.
- Async flow: upload → show task id → poll task → refresh results.

### Tech Choices
- Next.js (App Router) + TypeScript
- UI: Material UI (MUI)
- State: Zustand (local/UI state)
- Data: TanStack Query for fetching/caching/pagination

### Pages/Components
- Page: `/` CSV Analyzer
  - UploadSection: file input + submit → calls POST `/upload-csv/`
  - TaskStatus: shows `task_id` and live status (polls GET `/tasks/<id>/`)
  - BadgerTable: GET `/csv-results/` with pagination + search by stock code

### API Contracts
- POST `/upload-csv/` (multipart file) → `{ task_id }`
- GET `/tasks/<id>/` → `{ task_id, state, info }`
- GET `/csv-results/?search=&page=` → DRF paginated `{ count, next, previous, results[] }`

### UX Notes
- Disable upload button while pending; show success/error message.
- Debounced search input updates table query.
- Auto refresh table when task goes SUCCESS.

### Todos
1) Bootstrap Next.js (TS) + MUI + TanStack Query + Zustand; env config.
2) API client (fetch wrapper), React Query hooks for endpoints.
3) UploadSection with validation (.csv only) and submit.
4) TaskStatus with polling and simple badges.
5) Results table with columns: Stock Code, Number Of Quotes Found, Total Price, Created At.
6) Wire: after SUCCESS, refetch results and focus search by last uploaded code(s) (optional).
7) Minimal README with run instructions.


