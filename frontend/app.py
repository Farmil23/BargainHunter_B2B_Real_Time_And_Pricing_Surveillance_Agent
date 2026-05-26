import streamlit as st
import requests
import time
import json
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000/api/v1/surveillance"

st.set_page_config(page_title="Market Intelligence Dashboard", page_icon="📈", layout="wide")

st.title("📈 B2B Market Surveillance & Intelligence")
st.markdown("Monitor competitors in real-time, extract pricing, and get AI-driven strategic recommendations.")

# Sidebar for new task
st.sidebar.header("Start New Surveillance")
target_url = st.sidebar.text_input("Target URL (e.g., Search Page)", value="https://www.tokopedia.com/find/esp32-cam")
target_component = st.sidebar.text_input("Target Component / Product", value="ESP32-CAM")

if st.sidebar.button("Run Intelligence Agent", type="primary"):
    with st.spinner("Initializing Agent..."):
        try:
            response = requests.post(f"{API_BASE_URL}/analyze", json={
                "target_url": target_url,
                "target_component": target_component
            })
            if response.status_code == 200:
                task_id = response.json()["task_id"]
                st.session_state["active_task"] = task_id
                st.sidebar.success(f"Task #{task_id} Started!")
            else:
                st.sidebar.error("Failed to start task.")
        except Exception as e:
            st.sidebar.error(f"API Error: {e}")

st.divider()

# Main dashboard area
active_task = st.session_state.get("active_task", None)

if active_task:
    st.subheader(f"Live Intelligence Report (Task #{active_task})")
    
    status_placeholder = st.empty()
    content_placeholder = st.empty()
    
    # Polling logic
    is_completed = False
    max_retries = 60 # 2 minutes max
    retries = 0
    
    while not is_completed and retries < max_retries:
        try:
            res = requests.get(f"{API_BASE_URL}/task/{active_task}")
            if res.status_code == 200:
                task_data = res.json()
                status = task_data["status"]
                
                if status.startswith("running_"):
                    node_name = status.split("_")[1].title()
                    icon_map = {
                        "Scraper": "🕷️",
                        "Analyzer": "🧠",
                        "Recommender": "💡",
                        "Critique": "⚖️"
                    }
                    icon = icon_map.get(node_name, "🔄")
                    status_placeholder.info(f"{icon} **Status**: Executing {node_name} Node...")
                    time.sleep(1.5)
                    retries += 1
                elif status == "pending" or status == "running":
                    status_placeholder.info(f"⏳ **Status**: {status.upper()} - Initializing agent workflow...")
                    time.sleep(1.5)
                    retries += 1
                elif status == "completed":
                    status_placeholder.success("✅ Analysis Complete!")
                    is_completed = True
                    
                    # Parse result_data string back to JSON
                    result_json = json.loads(task_data["result_data"])
                    extracted_products = result_json.get("extracted_products", [])
                    analysis = result_json.get("market_analysis") or {}
                    cheapest = analysis.get("cheapest") or {}
                    best = analysis.get("best") or {}
                    decision = result_json.get("decision", "MAINTAIN")
                    recommendation = result_json.get("recommendation", "No recommendation.")
                    
                    with content_placeholder.container():
                        # Top Metrics
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Products Scraped", len(extracted_products))
                        col2.metric("Cheapest Price", f"Rp {cheapest.get('price', 'N/A')}")
                        col3.metric("AI Decision", decision)
                        
                        st.markdown("### 🤖 AI Strategic Recommendation")
                        st.info(recommendation)
                        
                        st.markdown("### 🏆 Market Leaders Identified")
                        col_cheap, col_best = st.columns(2)
                        with col_cheap:
                            st.markdown("**💸 Cheapest Product**")
                            st.success(f"**{cheapest.get('name', 'N/A')}**\n\n💰 Price: Rp {cheapest.get('price', 'N/A')}")
                        with col_best:
                            st.markdown("**⭐ Best Rated Product**")
                            st.warning(f"**{best.get('name', 'N/A')}**\n\n⭐ Rating: {best.get('rating', 'N/A')}")
                        
                        if extracted_products:
                            st.markdown("### 📊 Raw Market Data")
                            df = pd.DataFrame(extracted_products)
                            st.dataframe(df, use_container_width=True)
                            
                elif status == "failed":
                    status_placeholder.error("❌ Task Failed.")
                    st.json(task_data)
                    is_completed = True
            else:
                status_placeholder.warning("Waiting for API...")
                time.sleep(2)
                retries += 1
        except Exception as e:
            status_placeholder.error(f"Connection Error: {e}")
            break
            
else:
    st.info("👈 Enter a URL in the sidebar and run the agent to see real-time intelligence.")
