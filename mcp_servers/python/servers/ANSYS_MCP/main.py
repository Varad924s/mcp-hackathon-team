from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class SimulationInput(BaseModel):
    model_type: str
    material: Optional[str] = "steel"

@app.post("/run-simulation")
def run_simulation(input: SimulationInput):
    # Simulate a response
    result = {
        "thermal": "Max Temp: 430K, Avg Stress: 120MPa",
        "structural": "Deformation: 2.3mm, Yield Stress: 250MPa"
    }
    return {
        "status": "completed",
        "model": input.model_type,
        "material": input.material,
        "result": result.get(input.model_type, "Unknown simulation"),
        "report_url": "http://example.com/fake-ansys-report"
    }
