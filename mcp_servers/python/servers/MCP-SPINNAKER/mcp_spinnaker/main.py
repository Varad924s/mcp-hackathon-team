# from fastapi import FastAPI, HTTPException
# from mcp_spinnaker import spinnaker_client
# from mcp_spinnaker.models import TriggerPipelineRequest, TriggerPipelineResponse, ExecutionStatusResponse

# app = FastAPI(title="MCP-Spinnaker Server")

# @app.post("/trigger-pipeline", response_model=TriggerPipelineResponse)
# async def trigger_pipeline(request: TriggerPipelineRequest):
#     try:
#         result = await spinnaker_client.trigger_pipeline(
#             application=request.application,
#             pipeline_name=request.pipeline_name,
#             payload=request.payload
#         )
#         return {"ref": result.get("ref")}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/execution-status/{execution_id}", response_model=ExecutionStatusResponse)
# async def get_execution_status(execution_id: str):
#     try:
#         result = await spinnaker_client.get_execution_status(execution_id)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from mcp_spinnaker import spinnaker_client
from mcp_spinnaker.models import TriggerPipelineRequest, TriggerPipelineResponse, ExecutionStatusResponse, ListPipelinesResponse, PipelineConfigResponse
from mcp_spinnaker.models import ListPipelineExecutionsResponse
from mcp_spinnaker.models import ExecutionControlRequest, ExecutionControlResponse
from mcp_spinnaker.models import ManualJudgmentRequest, ManualJudgmentResponse
from mcp_spinnaker.models import PipelineConfigResponse
from mcp_spinnaker.models import PipelineHistoryResponse


app = FastAPI(title="MCP-Spinnaker Server")

@app.post("/trigger-pipeline", response_model=TriggerPipelineResponse)
async def trigger_pipeline(request: TriggerPipelineRequest):
    try:
        result = await spinnaker_client.trigger_pipeline(
            application=request.application,
            pipeline_name=request.pipeline_name,
            payload=request.payload
        )
        
        # Get the 'ref' key or fallback to a dummy string to satisfy response model
        ref = result.get("ref") or "dummy-ref-id"
        return {"ref": ref}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/execution-status/{execution_id}", response_model=ExecutionStatusResponse)
# async def get_execution_status(execution_id: str):
#     try:
#         result = await spinnaker_client.get_execution_status(execution_id)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/execution-status/{execution_id}", response_model=ExecutionStatusResponse)
async def get_execution_status(execution_id: str):
    try:
        result = await spinnaker_client.get_execution_status(execution_id)
        return ExecutionStatusResponse(**result) # ✅ Enforce model compliance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pipelines/{application}", response_model=ListPipelinesResponse)
async def get_pipelines(application: str):
    try:
        result = await spinnaker_client.list_pipelines(application)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pipeline-config/{application}/{pipeline_name}", response_model=PipelineConfigResponse)
async def get_pipeline_config(application: str, pipeline_name: str):
    try:
        result = await spinnaker_client.get_pipeline_config(application, pipeline_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    

@app.get("/executions/{application}/{pipeline_name}", response_model=ListPipelineExecutionsResponse)
async def get_pipeline_executions(application: str, pipeline_name: str):
    try:
        result = await spinnaker_client.list_pipeline_executions(application, pipeline_name)
        return {"executions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/execution-control", response_model=ExecutionControlResponse)
async def execution_control(request: ExecutionControlRequest):
    try:
        result = await spinnaker_client.control_execution(
            execution_id=request.execution_id,
            action=request.action
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/manual-judgment", response_model=ManualJudgmentResponse)
async def manual_judgment(request: ManualJudgmentRequest):
    try:
        result = await spinnaker_client.handle_manual_judgment(
            execution_id=request.execution_id,
            judgment=request.judgment
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/pipeline-history/{application}", response_model=PipelineHistoryResponse)
async def get_pipeline_history(application: str):
    try:
        result = await spinnaker_client.get_pipeline_history(application)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))