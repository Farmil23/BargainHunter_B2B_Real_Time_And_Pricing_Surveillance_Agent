from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class SurveillanceRequest(BaseModel):
    target_url: str
    target_component: str
    
class SurveillanceResponse(BaseModel):
    task_id: int
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    id: int
    target_url: str
    target_component: str
    status: str
    result_data: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
