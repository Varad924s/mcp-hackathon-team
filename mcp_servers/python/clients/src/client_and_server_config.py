ClientsConfig = [
    "MCP_CLIENT_OPENAI",
    "MCP_CLIENT_GEMINI"
]

ServersConfig = [
    {
        "server_name": "MCP-GSUITE",  # Prebuilt server
        "command": "uv",              # Uses 'uv' Poetry tool, works as expected
        "args": [
            "--directory",
            "../servers/MCP-GSUITE/mcp-gsuite",
            "run",
            "mcp-gsuite"
        ]
    },
    # {
    #     "server_name": "MCP-SUPERSET",  # Your custom server
    #     "command": "uvicorn",           # ✅ uvicorn is correct here
    #     "args": [
    #         "--app-dir",
    #         "../servers/MCP-SUPERSET/mcp-superset",
    #         "main:app",                 # ✅ main.py must exist and contain `app = FastAPI()`
    #         "--port", "8001",           # ✅ Optional but safer to be explicit
    #         "--host", "0.0.0.0"         # ✅ Makes it accessible on localhost
    #     ]
    # },
    {
        "server_name": "ANSYS_MCP",
        "command": "uvicorn",
        "args": [
            "--app-dir",
            "../servers/ANSYS_MCP",
            "main:app",
            "--port", "8010"
        ]
    }

    # Commented out for now – enable later
    {
        "server_name": "NUMPY_MCP",
        "command": "uv",
        "args": [
            "--directory",
            "../servers/NUMPY_MCP",
            "run",
            "server"
        ]
    }
    {
        "server_name": "MCP-SPINNAKER",
        "command": "uvicorn",
        "args": [
            "--app-dir",
            "../servers/MCP-SPINNAKER/mcp_spinnaker",
            "main:app",
            "--reload"
        ]
    }

]
