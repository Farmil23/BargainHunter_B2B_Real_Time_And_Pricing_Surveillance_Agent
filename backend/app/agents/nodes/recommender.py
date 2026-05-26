from backend.app.agents.state import AgentState
from langchain_openai import ChatOpenAI
from backend.app.core.config import settings
from backend.app.db.vector_store import vector_store
import json
import re
import logging

logger = logging.getLogger(__name__)

async def run_recommender_node(state: AgentState) -> dict:
    """
    Generates strategic recommendations based on analysis.
    """
    logger.info(f"[Recommender Node] Task {state['task_id']}: Generating strategy for {state['target_component']}")
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openai/gpt-4o-mini",
        max_tokens=2000
    )
    
    analysis = state.get("sentiment_analysis", {})
    price_anomaly = state.get("price_anomaly", False)
    
    # Retrieve past memory (RAG)
    past_context = ""
    try:
        results = vector_store.similarity_search(state['target_component'], top_k=2)
        if results:
            past_context = "\n".join([r['text'] for r in results])
    except Exception as e:
        logger.error(f"Failed to fetch Pinecone memory: {e}")
        
    critique_feedback = state.get("critique_feedback", "")
    
    prompt = f"""
    Based on the following competitor analysis for '{state['target_component']}':
    - Cheapest Competitor: {(analysis or {}).get('cheapest') or {}}
    - Best-Rated Competitor: {(analysis or {}).get('best') or {}}
    - Price Anomaly Detected: {price_anomaly}
    
    Historical context from previous intelligence reports:
    {past_context if past_context else "No historical context available."}
    
    {f"CRITIQUE FROM MANAGER: {critique_feedback}" if critique_feedback else ""}
    
    Recommend a comprehensive, highly detailed pricing and marketing strategy for our enterprise.
    Provide actionable business value, considering the market conditions, pricing dynamics, and competitor positioning.
    Write in a professional, enterprise consultant tone.
    Conclude with a final decision keyword: 'ADJUST_PRICE', 'MARKETING_BLITZ', or 'MAINTAIN'.
    Return strictly as a JSON object:
    {{
      "recommendation": "string (detailed paragraph)",
      "decision": "keyword"
    }}
    """
    
    try:
        response = await llm.ainvoke(prompt)
        content = response.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            recommendation = data.get("recommendation", "")
            decision = data.get("decision", "MAINTAIN")
        else:
            raise ValueError("No JSON object found")
            
        return {
            "strategic_recommendation": recommendation,
            "final_decision": decision,
            "revision_count": state.get("revision_count", 0) + 1
        }
    except Exception as e:
        logger.error(f"Recommender failed: {e}")
        return {
            "strategic_recommendation": "Maintain current strategy.",
            "final_decision": "MAINTAIN",
            "revision_count": state.get("revision_count", 0) + 1
        }
