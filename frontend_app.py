import streamlit as st
import requests
import json
import re
import google.generativeai as genai

# 🔐 Set your Gemini API Key
genai.configure(api_key="AIzaSyAzl7eYNnod5xEoZTJw9RpNpG8O-Oas62s")

# ✅ Use a lightweight, high-quota model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

st.set_page_config(page_title="ANSYS AI Assistant", layout="centered")
st.title("🤖 Gemini-Powered ANSYS Simulation Assistant")

# 🔌 Calls your ANSYS MCP server
def call_ansys_api(endpoint, params):
    try:
        url = f"http://localhost:8010/{endpoint}"
        if endpoint in ["run-simulation", "run-batch-simulation", "summarize-results"]:
            response = requests.post(url, json=params)
        else:
            response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 🧠 Ask Gemini to extract endpoint + params
def analyze_input(user_input):
    prompt = f"""
You are a backend-aware AI assistant. Respond ONLY in strict JSON with two keys:
- "endpoint": (use only the following exact strings)
  - "calculate-thermal-expansion"
  - "run-simulation"
  - "get-material-properties"
  - "list-available-models"
  - "load-analysis"
  - "heat-transfer"
  - "run-batch-simulation"
  - "summarize-results"

- "params": Dictionary or list of dictionaries depending on the endpoint.

EXAMPLES:

"Simulate thermal expansion of a steel rod 2m long at 80C"
️ {{
  "endpoint": "calculate-thermal-expansion",
  "params": {{
    "L": 2,
    "alpha": 0.000012,
    "delta_T": 80
  }}
}}

"Run a thermal simulation with copper"
️ {{
  "endpoint": "run-simulation",
  "params": {{
    "model_type": "thermal",
    "material": "copper"
  }}
}}

"Get material properties of aluminum"
️ {{
  "endpoint": "get-material-properties",
  "params": {{
    "material": "aluminum"
  }}
}}

"What simulation models are supported?"
️ {{
  "endpoint": "list-available-models",
  "params": {{}}
}}

"Calculate stress if 5000N applied over 25 sq.m"
️ {{
  "endpoint": "load-analysis",
  "params": {{
    "force": 5000,
    "area": 25
  }}
}}

"Calculate heat transfer for 3kg, c=4184, deltaT=60"
️ {{
  "endpoint": "heat-transfer",
  "params": {{
    "m": 3,
    "c": 4184,
    "delta_T": 60
  }}
}}

"Run batch simulations for thermal-steel and structural-aluminum"
️ {{
  "endpoint": "run-batch-simulation",
  "params": [
    {{
      "model_type": "thermal",
      "material": "steel"
    }},
    {{
      "model_type": "structural",
      "material": "aluminum"
    }}
  ]
}}

"Summarize simulation results of 350K and 390K"
️ {{
  "endpoint": "summarize-results",
  "params": [
    {{ "temperature_K": 350 }},
    {{ "temperature_K": 390 }}
  ]
}}

Respond ONLY with clean valid JSON. Now process this:
"{user_input}"
"""

    response = model.generate_content(prompt)
    text = response.text

    # Extract JSON object using regex
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return {"error": "Could not extract JSON from Gemini's response."}

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON from Gemini response."}

# 🌐 Streamlit UI
user_input = st.text_input("Ask a simulation 👇")

if user_input:
    with st.spinner("Thinking with Gemini..."):
        result = analyze_input(user_input)

        if "error" in result:
            st.error(result["error"])
        else:
            endpoint = result.get("endpoint")
            params = result.get("params", {})

            st.success(f"Calling `{endpoint}` with:")
            st.json(params)

            response = call_ansys_api(endpoint, params)
            st.subheader("📊 ANSYS MCP Response:")
            st.json(response)
