from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import numpy as np
import uvicorn

# Create FastAPI app and FastMCP wrapper
app = FastAPI()
mcp = FastMCP("NumPyMCP", app=app)

# Define tools
@mcp.tool()
def calculate_mean(numbers: list[float]) -> float:
    """Return the mean of a list of numbers."""
    return float(np.mean(numbers))

@mcp.tool()
def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Return result of multiplying two matrices."""
    result = np.matmul(a, b)
    return result.tolist()

@mcp.tool()
def standard_deviation(numbers: list[float]) -> float:
    """Return standard deviation of a list of numbers."""
    return float(np.std(numbers))

@mcp.tool()
def linear_regression(x: list[float], y: list[float]) -> dict:
    """Simple linear regression: returns slope and intercept."""
    slope, intercept = np.polyfit(x, y, 1)
    return {"slope": slope, "intercept": intercept}

# Run server
if __name__ == "__main__":
    print("🚀 Starting NumPy MCP at http://localhost:7003")
    uvicorn.run("server:app", host="0.0.0.0", port=7003, reload=True)
