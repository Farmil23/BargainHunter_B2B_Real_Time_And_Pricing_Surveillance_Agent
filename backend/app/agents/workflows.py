from langgraph.graph import StateGraph, END
from backend.app.agents.state import AgentState
from backend.app.agents.nodes.scraper import run_scraper_node
from backend.app.agents.nodes.analyzer import run_analyzer_node
from backend.app.agents.nodes.recommender import run_recommender_node
from backend.app.agents.nodes.critique import run_critique_node

def create_surveillance_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("Scraper", run_scraper_node)
    workflow.add_node("Analyzer", run_analyzer_node)
    workflow.add_node("Recommender", run_recommender_node)
    workflow.add_node("Critique", run_critique_node)
    
    workflow.set_entry_point("Scraper")
    
    workflow.add_edge("Scraper", "Analyzer")
    workflow.add_edge("Analyzer", "Recommender")
    workflow.add_edge("Recommender", "Critique")
    
    def evaluate_critique(state: AgentState):
        if state.get("critique_passed") or state.get("revision_count", 0) >= 3:
            return END
        return "Recommender"

    workflow.add_conditional_edges("Critique", evaluate_critique)
    
    return workflow.compile()

surveillance_app = create_surveillance_graph()
