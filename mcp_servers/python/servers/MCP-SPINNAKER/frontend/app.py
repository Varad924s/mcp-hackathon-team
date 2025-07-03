# # import streamlit as st
# # import requests

# # st.set_page_config(page_title="MCP Spinnaker Frontend")
# # st.title("🚀 MCP Spinnaker - Manual Judgment Portal")

# # # User input
# # content = st.text_area("🔍 Enter pipeline-related message:", height=100)

# # # Backend URL (make sure it matches FastAPI route)
# # BACKEND_URL = "http://127.0.0.1:8000/process"

# # # Submit button
# # if st.button("Submit for Processing"):
# #     if not content.strip():
# #         st.warning("⚠️ Please enter some text.")
# #     else:
# #         with st.spinner("Sending to backend..."):
# #             try:
# #                 response = requests.post(BACKEND_URL, json={"content": content})
# #                 if response.status_code == 200:
# #                     result = response.json()
# #                     st.success("✅ Result received!")
# #                     st.subheader("🔎 Backend Response:")
# #                     st.json(result)
# #                 else:
# #                     st.error(f"❌ {response.status_code} Error from backend")
# #                     st.code(response.text, language="json")
# #             except Exception as e:
# #                 st.error("🔌 Could not reach backend!")
# #                 st.code(str(e))

# import streamlit as st
# import requests

# # Title
# st.set_page_config(page_title="MCP Spinnaker Frontend")
# st.title("🚀 MCP Spinnaker - Manual Judgment Portal")

# # Input from user
# content = st.text_area("🔍 Enter pipeline-related message:", height=200)

# # Backend endpoint for triggering pipeline
# BACKEND_TRIGGER_URL = "http://127.0.0.1:8000/process"  # Your FastAPI POST endpoint

# if st.button("Submit for Processing"):
#     if not content.strip():
#         st.warning("⚠️ Please enter some text.")
#     else:
#         with st.spinner("🚀 Sending to backend..."):
#             try:
#                 response = requests.post(BACKEND_TRIGGER_URL, json={"content": content})
#                 if response.status_code == 200:
#                     result = response.json()
#                     st.success("✅ Result received!")
#                     st.subheader("🔎 Backend Response:")
#                     st.json(result)

#                     # Check for pipeline ref and get execution status
#                     if "ref" in result:
#                         execution_id = result["ref"].split("/")[-1]  # Extract ID
#                         st.info(f"📡 Checking execution status for ID: `{execution_id}`...")

#                         status_response = requests.get(
#                             f"http://127.0.0.1:8000/execution-status/{execution_id}"
#                         )
#                         if status_response.status_code == 200:
#                             st.subheader("📊 Current Execution Status:")
#                             st.json(status_response.json())
#                         else:
#                             st.warning("⚠️ Could not retrieve execution status.")
#                     else:
#                         st.warning("⚠️ No execution ID found in response.")
#                 else:
#                     st.error(f"❌ {response.status_code} Error from backend")
#                     st.code(response.text, language="json")
#             except Exception as e:
#                 st.error("🔌 Could not reach backend!")
#                 st.code(str(e))

# import streamlit as st
# import requests
# import json

# # Set page configuration
# st.set_page_config(page_title="MCP Spinnaker Control Panel", layout="centered")
# st.title("🚀 MCP Spinnaker Control Panel")
# st.markdown("#### Interact with your pipeline endpoints using this elegant UI!")

# BASE_URL = "http://127.0.0.1:8000"

# # Available endpoints
# endpoints = {
#     "Trigger a Pipeline": {
#         "method": "POST",
#         "path": "/trigger-pipeline",
#         "fields": ["application", "pipeline_name", "payload (JSON)"]
#     },
#     "Get Execution Status": {
#         "method": "GET",
#         "path": "/execution-status/{execution_id}",
#         "fields": ["execution_id"]
#     },
#     "List Pipelines": {
#         "method": "GET",
#         "path": "/pipelines/{application}",
#         "fields": ["application"]
#     },
#     "Get Pipeline Config": {
#         "method": "GET",
#         "path": "/pipeline-config/{application}/{pipeline_name}",
#         "fields": ["application", "pipeline_name"]
#     },
#     "Get Pipeline Executions": {
#         "method": "GET",
#         "path": "/executions/{application}/{pipeline_name}",
#         "fields": ["application", "pipeline_name"]
#     },
#     "Execution Control": {
#         "method": "POST",
#         "path": "/execution-control",
#         "fields": ["execution_id", "action"]
#     },
#     "Manual Judgment": {
#         "method": "POST",
#         "path": "/manual-judgment",
#         "fields": ["execution_id", "judgment"]
#     },
#     "Get Pipeline History": {
#         "method": "GET",
#         "path": "/pipeline-history/{application}",
#         "fields": ["application"]
#     },
#     "Process Message": {
#         "method": "POST",
#         "path": "/process",
#         "fields": ["content"]
#     }
# }

# # UI: Select endpoint
# st.markdown("### 🔧 Select Endpoint to Interact With")
# selected = st.selectbox("", list(endpoints.keys()))
# api = endpoints[selected]

# st.markdown("---")
# st.markdown(f"### 📄 {selected}")

# # Input Form
# with st.form("endpoint_form"):
#     inputs = {}
#     for field in api["fields"]:
#         key = field.split()[0]
#         height = 150 if "JSON" in field or "content" in field.lower() else 80
#         inputs[key] = st.text_area(f"✏️ {field}", height=height)

#     submitted = st.form_submit_button("🚀 Send Request")

# # Logic on submit
# if submitted:
#     st.markdown("---")
#     st.markdown("## ⏳ Processing Request...")

#     try:
#         url = BASE_URL + api["path"]
#         payload = {}

#         if api["method"] == "GET":
#             for k, v in inputs.items():
#                 url = url.replace(f"{{{k}}}", v)
#             response = requests.get(url)

#         else:  # POST request
#             for k, v in inputs.items():
#                 if "payload" in k or "content" in k:
#                     try:
#                         payload[k] = json.loads(v)
#                     except:
#                         st.error(f"❌ Invalid JSON for `{k}`.")
#                         st.stop()
#                 else:
#                     payload[k] = v
#             response = requests.post(url, json=payload)

#         # Display result
#         with st.expander("✅ Response Received (click to expand)", expanded=True):
#             st.code(f"Status: {response.status_code} - {response.reason}")
#             try:
#                 st.json(response.json())
#             except:
#                 st.text(response.text)

#     except Exception as e:
#         st.error("⚠️ Failed to connect to backend!")
#         st.code(str(e), language="bash")

import streamlit as st
import requests

st.set_page_config(page_title="MCP Spinnaker Manual Portal", layout="centered")

st.title("🚀 MCP Spinnaker - Manual Judgment & Control Portal")

st.markdown("Select the endpoint you want to interact with:")

option = st.selectbox(
    "📌 Choose an API endpoint",
    (
        "Process Message (/process)",
        "Trigger Pipeline (/trigger-pipeline)",
        "Execution Status (/execution-status/{execution_id})",
        "List Pipelines (/pipelines/{application})",
        "Pipeline Config (/pipeline-config/{application}/{pipeline_name})",
        "Pipeline Executions (/executions/{application}/{pipeline_name})",
        "Execution Control (/execution-control)",
        "Manual Judgment (/manual-judgment)",
        "Pipeline History (/pipeline-history/{application})"
    )
)

BASE_URL = "http://127.0.0.1:8000"

st.markdown("---")

if option == "Process Message (/process)":
    content = st.text_area("✏️ Message Content", height=100)
    if st.button("🚀 Send Request"):
        if not content.strip():
            st.warning("⚠️ Please enter message content.")
        else:
            with st.spinner("⏳ Processing Request..."):
                try:
                    response = requests.post(f"{BASE_URL}/process", json={"content": content})
                    st.success("✅ Response Received")
                    st.code(f"Status: {response.status_code}")
                    st.json(response.json())
                except Exception as e:
                    st.error("❌ Backend unreachable")
                    st.code(str(e))


elif option == "Trigger Pipeline (/trigger-pipeline)":
    application = st.text_input("🧱 Application Name")
    pipeline_name = st.text_input("📄 Pipeline Name")
    payload = st.text_area("📦 Payload (JSON)", value='{}', height=150)
    if st.button("🚀 Trigger Pipeline"):
        try:
            json_payload = {
                "application": application,
                "pipeline_name": pipeline_name,
                "payload": eval(payload)
            }
            response = requests.post(f"{BASE_URL}/trigger-pipeline", json=json_payload)
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Execution Status (/execution-status/{execution_id})":
    execution_id = st.text_input("📎 Execution ID")
    if st.button("🔍 Get Status"):
        try:
            response = requests.get(f"{BASE_URL}/execution-status/{execution_id}")
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "List Pipelines (/pipelines/{application})":
    app_name = st.text_input("📦 Application Name")
    if st.button("📋 List Pipelines"):
        try:
            response = requests.get(f"{BASE_URL}/pipelines/{app_name}")
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Pipeline Config (/pipeline-config/{application}/{pipeline_name})":
    app_name = st.text_input("📦 Application Name")
    pipeline = st.text_input("📄 Pipeline Name")
    if st.button("⚙️ Get Config"):
        try:
            response = requests.get(f"{BASE_URL}/pipeline-config/{app_name}/{pipeline}")
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Pipeline Executions (/executions/{application}/{pipeline_name})":
    app_name = st.text_input("📦 Application Name")
    pipeline = st.text_input("📄 Pipeline Name")
    if st.button("📜 Get Executions"):
        try:
            response = requests.get(f"{BASE_URL}/executions/{app_name}/{pipeline}")
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Execution Control (/execution-control)":
    execution_id = st.text_input("📎 Execution ID")
    action = st.selectbox("🛠 Action", ["cancel", "pause", "resume"])
    if st.button("🎛 Control Execution"):
        try:
            response = requests.post(f"{BASE_URL}/execution-control", json={
                "execution_id": execution_id,
                "action": action
            })
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Manual Judgment (/manual-judgment)":
    execution_id = st.text_input("📎 Execution ID")
    judgment = st.selectbox("🧠 Judgment", ["continue", "stop"])
    if st.button("🧾 Submit Judgment"):
        try:
            response = requests.post(f"{BASE_URL}/manual-judgment", json={
                "execution_id": execution_id,
                "judgment": judgment
            })
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))


elif option == "Pipeline History (/pipeline-history/{application})":
    app_name = st.text_input("📦 Application Name")
    if st.button("🕘 Get History"):
        try:
            response = requests.get(f"{BASE_URL}/pipeline-history/{app_name}")
            st.success("✅ Response Received")
            st.json(response.json())
        except Exception as e:
            st.error("❌ Error")
            st.code(str(e))
