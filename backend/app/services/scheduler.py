from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import json
from backend.app.db.session import SessionLocal
from backend.app.models.domain import SurveillanceTask
from backend.app.agents.workflows import surveillance_app

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def process_pending_tasks():
    logger.info("🤖 Autonomous Scheduler: Checking for pending tasks...")
    db = SessionLocal()
    try:
        # Find all pending tasks
        pending_tasks = db.query(SurveillanceTask).filter(SurveillanceTask.status == "pending").all()
        
        if not pending_tasks:
            return

        for task in pending_tasks:
            logger.info(f"Processing Task ID {task.id} for {task.target_url}")
            
            # Update status to running
            task.status = "running"
            db.commit()
            
            try:
                # Initialize agent state
                initial_state = {
                    "task_id": task.id,
                    "target_url": task.target_url,
                    "target_component": task.target_component,
                    "revision_count": 0,
                }
                
                # Run the autonomous agent
                final_state = surveillance_app.invoke(initial_state)
                
                # Process final state
                task.status = "completed"
                # Save the final decision or entire state
                result_data = {
                    "strategic_recommendation": final_state.get("strategic_recommendation"),
                    "final_decision": final_state.get("final_decision", "Decision made by agent"),
                    "revision_count": final_state.get("revision_count", 0),
                    "critique_passed": final_state.get("critique_passed", False)
                }
                task.result_data = json.dumps(result_data)
                logger.info(f"Task ID {task.id} completed autonomously.")
            except Exception as e:
                logger.error(f"Error processing Task ID {task.id}: {str(e)}")
                task.status = "failed"
                task.result_data = json.dumps({"error": str(e)})
            
            db.commit()
    except Exception as e:
        logger.error(f"Database error in scheduler: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Run once a day at 08:00 AM for production
        scheduler.add_job(
            process_pending_tasks,
            trigger=CronTrigger(hour=8, minute=0),
            id='process_pending_tasks_job',
            name='Process pending surveillance tasks daily at 8 AM',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Background scheduler started. Autonomous agent is awake.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler stopped.")
