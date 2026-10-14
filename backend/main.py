from pathlib import Path

from datafusion import SessionContext, SQLOptions
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


DATA_PATH = Path(__file__).resolve().parent / "sales_data.parquet"
if not DATA_PATH.is_file():
    raise RuntimeError(
        f"Missing sales data: {DATA_PATH}. "
        "Run python backend/generate_mock_data.py from the repository root."
    )

ctx = SessionContext()
ctx.register_parquet("sales", str(DATA_PATH))
query_options = (
    SQLOptions()
    .with_allow_ddl(False)
    .with_allow_dml(False)
    .with_allow_statements(False)
)

app = FastAPI(title="Data Craft Query API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class QueryRequest(BaseModel):
    sql: str = Field(min_length=1)


@app.post("/query")
def query_data(request: QueryRequest):
    try:
        batches = ctx.sql(request.sql, options=query_options).collect()
        rows = [row for batch in batches for row in batch.to_pylist()]
        return JSONResponse(content=jsonable_encoder({"rows": rows}))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
