from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    task_id: int
    target_url: str
    target_component: str
    
    # Scraper Outputs
    raw_web_data: Optional[str]
    extracted_products: Optional[list[dict]]
    
    # Analyzer Outputs
    sentiment_analysis: Optional[Dict[str, Any]]
    price_anomaly: Optional[bool]
    
    # Recommender Outputs
    strategic_recommendation: Optional[str]
    final_decision: Optional[str]
    
    # Critique & Loop
    critique_feedback: Optional[str]
    critique_passed: Optional[bool]
    revision_count: int
