from backend.app.agents.state import AgentState
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def run_scraper_node(state: AgentState) -> dict:
    """
    Executes web scraping using Bright Data MCP via a ReAct Agent.
    Extracts pricing and reviews.
    """
    logger.info(f"[Scraper Node] Task {state['task_id']}: Scraping {state['target_url']}")
    
    # Configure MCP Client with Bright Data
    client = MultiServerMCPClient({
        "bright_data": {
            "url": f"https://mcp.brightdata.com/sse?token={settings.BRIGHTDATA_API_KEY}",
            "transport": "sse",
        }
    })
    
    tools = await client.get_tools()
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openai/gpt-4o-mini",
        max_tokens=4000
    )
    
    system_prompt = """
    You are an elite enterprise web scraper agent powered by Bright Data tools.
    Your mission is to visit a target search URL and extract the top products listed on the page.
    
    CRITICAL FILTERING RULE:
    You must ONLY extract products that are exactly the core target component you are instructed to find. 
    You MUST IGNORE and EXCLUDE any accessories, cases, programmer boards, downloader boards, or unrelated items. 
    For example, if the target is "ESP32-CAM", you must completely ignore "CH340 Programmer", "Development Board", or "Camera Module ONLY". If the target is "Arduino Uno", ignore "Arduino cases" or "Cables".
    
    For the filtered core products:
    1. Extract the name of each product.
    2. Extract the price of each product.
    3. Extract the rating or number of reviews if available.
    
    Use the available Bright Data MCP tools to accomplish this.
    Be extremely concise. Provide direct, brief, and to-the-point JSON without unnecessary fluff to save tokens.
    Return the final output strictly as JSON with a single key `products` containing a list of objects:
    {
      "products": [
        {"name": "string", "price": float, "rating": "string"}
      ]
    }
    """
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    
    prompt = f"Target Component: '{state['target_component']}'.\nTarget URL: '{state['target_url']}'.\nPlease extract pricing and reviews for this specific Target Component. Strictly apply the CRITICAL FILTERING RULE to only return products that are exactly '{state['target_component']}'."
    
    # In a real scenario, this LLM call executes the tool and parses the response.
    # We simulate parsing the result for this implementation plan scope.
    try:
        result = await agent.ainvoke({
            "messages": [("human", prompt)]
        })
        llm_output = result["messages"][-1].content
        
        # Parse the JSON response from the ReAct agent
        import re
        import json
        
        extracted_products = []
        
        match = re.search(r'\{.*\}', llm_output, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                extracted_products = data.get("products", [])
            except Exception as parse_err:
                logger.error(f"Failed to parse scraper JSON: {parse_err}")
        else:
            logger.warning("No JSON found in scraper output. Fallback to raw data.")
        
        return {
            "raw_web_data": llm_output,
            "extracted_products": extracted_products
        }
    except Exception as e:
        logger.error(f"Scraper failed: {e}")
        return {
            "raw_web_data": str(e),
            "extracted_products": []
        }
