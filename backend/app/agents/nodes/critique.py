from backend.app.agents.state import AgentState
from langchain_openai import ChatOpenAI
from backend.app.core.config import settings
import json
import re
import logging

logger = logging.getLogger(__name__)

async def run_critique_node(state: AgentState) -> dict:
    """
    Acts as a Manager that critiques the Recommender's strategy.
    Rejects the strategy if it violates business rules.
    """
    logger.info(f"[Critique Node] Task {state['task_id']}: Evaluating strategy for {state['target_component']}")
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openai/gpt-4o-mini",
        max_tokens=1000
    )
    
    recommendation = state.get("strategic_recommendation", "")
    decision = state.get("final_decision", "")
    price_anomaly = state.get("price_anomaly", False)
    
    prompt = f"""
    You are the Senior Business Manager reviewing a proposed strategy for '{state['target_component']}'.
    
    Proposed Recommendation: "{recommendation}"
    Proposed Decision: "{decision}"
    Price Anomaly Detected by System: {price_anomaly}
    
    CRITICAL BUSINESS RULES:
    1. We must NEVER lower our prices (ADJUST_PRICE) unless there is a confirmed Price Anomaly (Price Anomaly == True).
    2. If the recommendation is MARKETING_BLITZ, it must clearly state WHY (e.g. better features, higher rating).
    
    Evaluate the proposed strategy against these rules.
    If it passes, set "passed" to true. 
    If it violates a rule, set "passed" to false and provide strict, concise feedback on what needs to change.
    
    Return strictly as a JSON object:
    {{
      "passed": true/false,
      "feedback": "string"
    }}
    """
    
    try:
        response = await llm.ainvoke(prompt)
        content = response.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            passed = data.get("passed", True)
            feedback = data.get("feedback", "")
            
            logger.info(f"[Critique Node] Strategy Passed: {passed}. Feedback: {feedback}")
            return {
                "critique_passed": passed,
                "critique_feedback": feedback
            }
        else:
            raise ValueError("No JSON object found")
    except Exception as e:
        logger.error(f"Critique failed: {e}")
        # Fail open to prevent system crash
        return {
            "critique_passed": True,
            "critique_feedback": ""
        }
