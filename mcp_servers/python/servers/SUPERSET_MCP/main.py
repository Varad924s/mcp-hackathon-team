from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str
    database: str

@app.get("/list-dashboards")
def list_dashboards():
    # Simulated list of dashboards
    return {
        "dashboards": [
            {"id": 1, "name": "Sales KPIs"},
            {"id": 2, "name": "User Retention"},
            {"id": 3, "name": "System Metrics"}
        ]
    }

@app.post("/run-query")
def run_query(data: QueryRequest):
    # Simulate running a SQL query (mock)
    return {
        "status": "success",
        "sql": data.sql,
        "database": data.database,
        "result": [
            {"month": "Jan", "revenue": 12000},
            {"month": "Feb", "revenue": 15300},
            {"month": "Mar", "revenue": 13400}
        ]
    }
