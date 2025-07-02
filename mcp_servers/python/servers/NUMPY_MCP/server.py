from fastapi import FastAPI, Request
import numpy as np
import uvicorn

app = FastAPI(title="NumPy MCP Server")

# ——— Tools registry ———
def calculate_mean(numbers: list[float]) -> float:
    return float(np.mean(numbers))

def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return np.matmul(a, b).tolist()

def standard_deviation(numbers: list[float]) -> float:
    return float(np.std(numbers))

def linear_regression(x: list[float], y: list[float]) -> dict:
    slope, intercept = np.polyfit(x, y, 1)
    return {"slope": slope, "intercept": intercept}

# map tool names → functions
TOOLS = {
    "calculate_mean": calculate_mean,
    "matrix_multiply": matrix_multiply,
    "standard_deviation": standard_deviation,
    "linear_regression": linear_regression,
}


@app.post("/tool_call")
async def tool_call(request: Request):
    """
    Expects JSON:
    {
      "tool_name": "<one of: calculate_mean, matrix_multiply, standard_deviation, linear_regression>",
      "params": { ... }
    }
    """
    payload = await request.json()
    name = payload.get("tool_name")
    params = payload.get("params", {})

    if name not in TOOLS:
        return {"error": f"Unknown tool '{name}'"}

    try:
        result = TOOLS[name](**params)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    port = 7003
    print(f"🚀 NumPy MCP server running → http://localhost:{port}/tool_call")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
