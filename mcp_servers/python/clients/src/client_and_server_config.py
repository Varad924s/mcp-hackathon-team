ClientsConfig = [
    "MCP_CLIENT_AZURE_AI",
    "MCP_CLIENT_OPENAI",
    "MCP_CLIENT_GEMINI"
]

ServersConfig = [
    {
        "server_name": "MCP-GSUITE",
        "command": "uv",
        "args": [
            "--directory",
            "../servers/MCP-GSUITE/mcp-gsuite",
            "run",
            "mcp-gsuite"
        ]
    },
    # {
    #     "server_name": "ANSYS_MCP",
    #     "command": "uvicorn",
    #     "args": [
    #         "--app-dir",
    #         "../servers/ANSYS_MCP",
    #         "main:app",
    #         "--port",
    #         "8010"
    #     ]
    # }
     {
        "server_name": "ANSYS_MCP",
        "command": "uvicorn",
        "args": [
            "--app-dir",
            "../../servers/ANSYS_MCP",
            "main:app",
            "--port",
            "8010"
        ]
    }
]
