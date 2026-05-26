from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import json
import logging

from backend.app.models.schemas import SurveillanceRequest, SurveillanceResponse, TaskStatusResponse
from backend.app.models.domain import SurveillanceTask
from backend.app.db.session import get_db
from backend.app.db.vector_store import vector_store
from backend.app.agents.workflows import surveillance_app
from backend.app.services.notifier import notifier

logger = logging.getLogger(__name__)
router = APIRouter()

async def run_surveillance_background(task_id: int, url: str, component: str, db: Session):
    logger.info(f"Starting background surveillance for task {task_id}")
    try:
        # Update status to running
        task = db.query(SurveillanceTask).filter(SurveillanceTask.id == task_id).first()
        if not task:
            return
            
        task.status = "running"
        db.commit()
        
        # Execute LangGraph Agent
        initial_state = {
            "task_id": task_id,
            "target_url": url,
            "target_component": component
        }
        
        # Stream execution steps
        final_state = initial_state
        async for output in surveillance_app.astream(initial_state):
            for key, value in output.items():
                logger.info(f"Finished node: {key}")
                # Refresh task from DB in case it detached
                task = db.query(SurveillanceTask).filter(SurveillanceTask.id == task_id).first()
                task.status = f"running_{key.lower()}"
                db.commit()
                # Track the accumulating state
                final_state.update(value)
        
        # After streaming completes, final_state holds the final state data
        task = db.query(SurveillanceTask).filter(SurveillanceTask.id == task_id).first()
        task.status = "completed"
        task.result_data = json.dumps({
            "extracted_products": final_state.get("extracted_products"),
            "market_analysis": final_state.get("sentiment_analysis"),
            "price_anomaly": final_state.get("price_anomaly"),
            "recommendation": final_state.get("strategic_recommendation"),
            "decision": final_state.get("final_decision")
        })
        db.commit()
        
        # Save to vector store for semantic memory (optional context tracking)
        try:
            report = f"Component: {component}. Decision: {final_state.get('final_decision')}. Recommendation: {final_state.get('strategic_recommendation')}"
            metadata = {"task_id": task_id, "component": component, "url": url}
            vector_store.upsert_documents([report], [metadata], [str(task_id)])
            logger.info(f"Stored intelligence report to Pinecone for task {task_id}")
        except Exception as ve:
            logger.error(f"Vector store error: {ve}")
            
        # Trigger enterprise alerting system
        notifier.send_alert(
            task_id=task_id,
            component=component,
            analysis=final_state.get("sentiment_analysis", {}),
            recommendation=final_state.get("strategic_recommendation", ""),
            decision=final_state.get("final_decision", "")
        )
            
    except Exception as e:
        logger.error(f"Surveillance task {task_id} failed: {e}")
        task = db.query(SurveillanceTask).filter(SurveillanceTask.id == task_id).first()
        if task:
            task.status = "failed"
            task.result_data = json.dumps({"error": str(e)})
            db.commit()

@router.post("/analyze", response_model=SurveillanceResponse)
async def start_surveillance(
    request: SurveillanceRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create DB Task
    new_task = SurveillanceTask(
        target_url=request.target_url,
        target_component=request.target_component,
        status="pending"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Fire off background task
    background_tasks.add_task(
        run_surveillance_background,
        task_id=new_task.id,
        url=request.target_url,
        component=request.target_component,
        db=db
    )
    
    return SurveillanceResponse(
        task_id=new_task.id,
        status="pending",
        message="Surveillance task started successfully."
    )

@router.get("/task/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(SurveillanceTask).filter(SurveillanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/tasks", response_model=list[TaskStatusResponse])
def get_all_tasks(limit: int = 50, db: Session = Depends(get_db)):
    """
    Fetch history of surveillance tasks for the dashboard.
    """
    tasks = db.query(SurveillanceTask).order_by(SurveillanceTask.created_at.desc()).limit(limit).all()
    return tasks
