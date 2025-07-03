from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from typing import Literal

# 1
class TriggerPipelineRequest(BaseModel):
    application: str
    pipeline_name: str
    payload: Dict

class TriggerPipelineResponse(BaseModel):
    ref: str

# class ExecutionStatusResponse(BaseModel):
#     id: str
#     status: str
#     startTime: Optional[int] = None
#     endTime: Optional[int] = None

# 2
class ExecutionStatusResponse(BaseModel):
    execution_id: str
    status: str
    
    
# 3
class ListPipelinesResponse(BaseModel):
    application: str
    pipelines: List[str]
    
    
# 4 
class Stage(BaseModel):
    name: str
    type: str

class Trigger(BaseModel):
    type: str
    branch: str

class PipelineConfigResponse(BaseModel):
    application: str
    pipeline_name: str
    stages: List[Stage]
    triggers: List[Trigger]
    parameters: Dict[str, Any]
    
    
# 5
class PipelineExecution(BaseModel):
    execution_id: str
    status: str
    start_time: str
    duration: str

class ListPipelineExecutionsResponse(BaseModel):
    executions: List[PipelineExecution]

# 6
class ExecutionControlRequest(BaseModel):
    execution_id: str
    action: Literal["pause", "resume", "cancel"]

class ExecutionControlResponse(BaseModel):
    execution_id: str
    action: str
    result: str

# 7
class ManualJudgmentRequest(BaseModel):
    execution_id: str
    judgment: Literal["continue", "stop"]

class ManualJudgmentResponse(BaseModel):
    execution_id: str
    judgment: str
    result: str

# 8
class PipelineHistory(BaseModel):
    pipeline_name: str
    total_runs: int
    successes: int
    failures: int
    last_run: str

class PipelineHistoryResponse(BaseModel):
    application: str
    history: List[PipelineHistory]
