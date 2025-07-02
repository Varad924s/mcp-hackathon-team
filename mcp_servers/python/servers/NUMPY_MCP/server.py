# from fastapi import FastAPI, Request
# import numpy as np
# import uvicorn

# app = FastAPI(title="NumPy MCP Server")

# # ——— Tools registry ———
# def calculate_mean(numbers: list[float]) -> float:
#     return float(np.mean(numbers))

# def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
#     return np.matmul(a, b).tolist()

# def standard_deviation(numbers: list[float]) -> float:
#     return float(np.std(numbers))

# def linear_regression(x: list[float], y: list[float]) -> dict:
#     slope, intercept = np.polyfit(x, y, 1)
#     return {"slope": slope, "intercept": intercept}

# # map tool names → functions
# TOOLS = {
#     "calculate_mean": calculate_mean,
#     "matrix_multiply": matrix_multiply,
#     "standard_deviation": standard_deviation,
#     "linear_regression": linear_regression,
# }


# @app.post("/tool_call")
# async def tool_call(request: Request):
#     """
#     Expects JSON:
#     {
#       "tool_name": "<one of: calculate_mean, matrix_multiply, standard_deviation, linear_regression>",
#       "params": { ... }
#     }
#     """
#     payload = await request.json()
#     name = payload.get("tool_name")
#     params = payload.get("params", {})

#     if name not in TOOLS:
#         return {"error": f"Unknown tool '{name}'"}

#     try:
#         result = TOOLS[name](**params)
#         return {"result": result}
#     except Exception as e:
#         return {"error": str(e)}


# if __name__ == "__main__":
#     port = 7003
#     print(f"🚀 NumPy MCP server running → http://localhost:{port}/tool_call")
#     uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)

# server.py
from fastapi import FastAPI, Request
import numpy as np
import uvicorn

app = FastAPI(title="NumPy MCP Server")

# ——— Define your eight tools ———

def calculate_mean(numbers: list[float]) -> float:
    return float(np.mean(numbers))

def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return np.matmul(a, b).tolist()

def standard_deviation(numbers: list[float]) -> float:
    return float(np.std(numbers))

def linear_regression(x: list[float], y: list[float]) -> dict:
    slope, intercept = np.polyfit(x, y, 1)
    return {"slope": slope, "intercept": intercept}

def eigen_decomposition(matrix: list[list[float]]) -> dict:
    vals, vecs = np.linalg.eig(np.array(matrix))
    return {"eigenvalues": vals.tolist(), "eigenvectors": vecs.tolist()}

def fft(signal: list[float]) -> dict:
    comp = np.fft.fft(signal)
    return {"real": comp.real.tolist(), "imag": comp.imag.tolist()}

def convolve(a: list[float], b: list[float], mode: str = "full") -> list[float]:
    return np.convolve(a, b, mode=mode).tolist()

def random_sample(dist: str, size: int, **kwargs) -> list[float]:
    if dist == "normal":
        return np.random.normal(loc=kwargs.get("loc", 0),
                                scale=kwargs.get("scale", 1),
                                size=size).tolist()
    if dist == "uniform":
        return np.random.uniform(low=kwargs.get("low", 0),
                                 high=kwargs.get("high", 1),
                                 size=size).tolist()
    if dist == "poisson":
        return np.random.poisson(lam=kwargs.get("lam", 1),
                                 size=size).tolist()
    # fallback
    return []

# Map tool names → functions
TOOLS = {
    "calculate_mean": calculate_mean,
    "matrix_multiply": matrix_multiply,
    "standard_deviation": standard_deviation,
    "linear_regression": linear_regression,
    "eigen_decomposition": eigen_decomposition,
    "fft": fft,
    "convolve": convolve,
    "random_sample": random_sample,
}

@app.post("/tool_call")
async def tool_call(request: Request):
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
