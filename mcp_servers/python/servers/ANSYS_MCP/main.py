from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

class SimulationInput(BaseModel):
    model_type: str
    material: str

@app.post("/run-simulation")
def run_simulation(input: SimulationInput):
    temp = 300 + len(input.material) * 10
    stress = 100 + len(input.model_type) * 5
    return {
        "model": input.model_type,
        "material": input.material,
        "temperature_K": temp,
        "stress_MPa": stress
    }

materials_db = {
    "steel": {"density": 7850, "elasticity": 200e9},
    "aluminum": {"density": 2700, "elasticity": 70e9},
    "copper": {"density": 8960, "elasticity": 110e9}
}

@app.get("/get-material-properties")
def get_material_properties(material: str):
    return materials_db.get(material.lower(), {"error": "Material not found"})

@app.get("/list-available-models")
def list_models():
    return {
        "models": ["thermal", "structural", "vibration", "fatigue", "heat-transfer"]
    }

@app.get("/calculate-thermal-expansion")
def thermal_expansion(L: float, alpha: float, delta_T: float):
    delta_L = alpha * L * delta_T
    return {"change_in_length_mm": delta_L * 1000}

@app.post("/run-batch-simulation")
def run_batch(data: List[SimulationInput]):
    return [
        {
            "model": i.model_type,
            "material": i.material,
            "result": {
                "temperature_K": 300 + len(i.material) * 10,
                "stress_MPa": 100 + len(i.model_type) * 5
            }
        } for i in data
    ]

@app.get("/load-analysis")
def load_analysis(force: float, area: float):
    if area == 0:
        return {"error": "Area cannot be zero"}
    stress = force / area
    return {"stress_MPa": stress}

@app.get("/heat-transfer")
def heat_transfer(m: float, c: float, delta_T: float):
    Q = m * c * delta_T
    return {"heat_Joules": Q}

@app.post("/summarize-results")
def summarize(results: List[Dict]):
    temps = [r["temperature_K"] for r in results if "temperature_K" in r]
    avg_temp = sum(temps) / len(temps) if temps else 0
    return {"total_runs": len(results), "average_temp_K": avg_temp}
