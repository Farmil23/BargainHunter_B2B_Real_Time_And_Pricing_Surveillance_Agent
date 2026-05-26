import pytest
from backend.app.agents.state import AgentState
from backend.app.agents.nodes.recommender import run_recommender_node

@pytest.mark.asyncio
async def test_recommender_node(monkeypatch):
    state: AgentState = {
        "task_id": 1,
        "target_url": "http://test.com",
        "target_component": "Widget",
        "raw_web_data": None,
        "extracted_prices": [10.0],
        "extracted_reviews": ["Bad quality"],
        "sentiment_analysis": {"summary": "Negative", "weaknesses": ["quality"]},
        "price_anomaly": False,
        "strategic_recommendation": None,
        "final_decision": None
    }
    
    # Mock LLM call to avoid API billing
    async def mock_ainvoke(*args, **kwargs):
        class MockResponse:
            content = "Recommendation: Improve quality.\nDecision: MAINTAIN"
        return MockResponse()

    # Patch the ChatOpenAI ainvoke
    from backend.app.agents.nodes import recommender
    monkeypatch.setattr("app.agents.nodes.recommender.ChatOpenAI.ainvoke", mock_ainvoke)
    
    result = await run_recommender_node(state)
    
    assert "strategic_recommendation" in result
    assert result["final_decision"] == "MAINTAIN"
