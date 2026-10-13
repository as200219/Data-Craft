# Data-Craft
A modern, open-source Business Intelligence platform with vectorized execution engine, semantic layer, and composable Next.js frontend

## Architecture

- `backend/`: planned Python FastAPI + DataFusion execution tier for columnar queries.
- `cube/schema/`: planned Cube semantic tier for shared metrics, access control, and APIs.
- `frontend/`: planned Next.js + Tailwind presentation tier for interactive dashboards.

Phases 1–2 provide the repository foundation and mock sales data. The API, Cube
service, and frontend application are not implemented yet.

## Local setup and mock data

Use GitHub Codespaces or reopen this repository in a VS Code Dev Container.
The container provides Python 3.11, Node.js 20, and Docker-in-Docker, and forwards
ports 3000 (frontend), 4000 (Cube), and 8000 (backend) for later phases.
For setup outside the container, install Python 3.11+, Node.js 20, and Docker
(Node.js and Docker are only needed for the later application tiers).

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python backend/generate_mock_data.py
```

On Windows, activate with `.venv\Scripts\activate` instead.

The generator prints its row count and writes `backend/sales_data.parquet`,
regardless of the current working directory. This generated file is ignored by
Git; rerun the command to recreate it. The fixed seed produces 10,000 repeatable
orders dated 2024–2026 with unique string IDs, datetime order dates, string
regions/categories, and floating-point revenue/profit. Category-dependent,
right-skewed revenue and margins that include occasional losses approximate
retail sales.
