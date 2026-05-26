from backend.app.agents.state import AgentState
from langchain_openai import ChatOpenAI
from backend.app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

async def run_analyzer_node(state: AgentState) -> dict:
    """
    Analyzes sentiment of reviews and detects pricing anomalies.
    """
    logger.info(f"[Analyzer Node] Task {state['task_id']}: Analyzing data for {state['target_component']}")
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openai/gpt-4o-mini",
        max_tokens=1000
    )
    
    products_text = json.dumps(state.get("extracted_products", []), indent=2)
    
    prompt = f"""
    Analyze the following competitor products found for '{state['target_component']}':
    Products: 
    {products_text}
    
    CRITICAL FILTERING STEP:
    Before doing any analysis, rigorously filter the list to REMOVE any accessories, components, cases, downloader boards, or programmers. 
    You MUST ONLY consider the exact core product: '{state['target_component']}'. For example, if searching for ESP32-CAM, ignore "CH340 Programmer", "Development Board", or "Camera Module only".
    
    1. From the FILTERED list only, identify the cheapest true product and note its price.
    2. From the FILTERED list only, identify the best product based on rating/reviews.
    3. Output your findings as a JSON object with keys:
    {{
        "cheapest_product": {{"name": "string", "price": float}},
        "best_product": {{"name": "string", "rating": "string"}},
        "price_anomaly": true/false
    }}
    Be extremely concise to save tokens. Do not include extra text.
    """
    
    try:
        response = await llm.ainvoke(prompt)
        content = response.content
        
        # Use regex to find JSON block to be robust against markdown or extra text
        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            clean_json = match.group(0)
            analysis = json.loads(clean_json)
        else:
            raise ValueError("No JSON object found in response")
        
        return {
            "sentiment_analysis": {
                "cheapest": analysis.get("cheapest_product", {}),
                "best": analysis.get("best_product", {})
            },
            "price_anomaly": analysis.get("price_anomaly", False)
        }
    except Exception as e:
        logger.error(f"Analyzer failed: {e}")
        return {
            "sentiment_analysis": {"cheapest": {}, "best": {}},
            "price_anomaly": False
        }
