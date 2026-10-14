# Data-Craft
A modern, open-source Business Intelligence platform with vectorized execution engine, semantic layer, and composable Next.js frontend

## Phase 3: FastAPI + DataFusion query backend

Run these commands from the repository root (Python 3.11+):

```bash
python -m pip install -r backend/requirements.txt
# Generate the deterministic 10,000-row dataset if it is missing.
python backend/generate_mock_data.py
uvicorn backend.main:app --reload --port 8000
```

The API fails fast with a generation command if `backend/sales_data.parquet`
is missing. The data path is resolved relative to the backend module, not the
working directory. Generated Parquet files are not committed.

In another terminal:

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region ORDER BY region"}'
```

Responses have the form `{"rows":[{"region":"East","total_revenue":123.45},...]}`;
an empty result returns `{"rows":[]}`. Dates/timestamps are serialized as ISO
strings. SQL planning/execution errors return HTTP 400 with a `detail` message;
malformed request bodies return HTTP 422. All Arrow result batches are included.
Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

CORS allows `http://localhost:3000` and `http://127.0.0.1:3000`.
Queries are read-only: DDL, DML, and session-changing statements are disabled.
This unauthenticated raw-SQL API is for trusted local development only; keep
Uvicorn bound to its default loopback interface. Authentication and query
resource limits are required before exposing it publicly.
