"""
BargainHunter B2B — Market Intelligence Dashboard
Premium Streamlit Frontend with UX-first design principles.
"""

import streamlit as st
import requests
import time
import json
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from landing import render_landing_page

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
API_BASE_URL = "http://127.0.0.1:8000/api/v1/surveillance"

st.set_page_config(
    page_title="BargainHunter — Market Intelligence",
    page_icon="🎯😢😢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Load CSS & Icons
# ──────────────────────────────────────────────
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Page Routing
# ──────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────
def get_decision_badge(decision: str) -> str:
    """Return styled HTML badge for AI decision."""
    badge_map = {
        "MAINTAIN": ("badge-maintain", '<i class="fa-solid fa-shield"></i>'),
        "ADJUST_PRICE": ("badge-adjust", '<i class="fa-solid fa-money-bill-trend-up"></i>'),
        "MARKETING_BLITZ": ("badge-blitz", '<i class="fa-solid fa-rocket"></i>'),
    }
    cls, icon = badge_map.get(decision, ("badge-maintain", '<i class="fa-solid fa-chart-simple"></i>'))
    return f'<span class="decision-badge {cls}">{icon} {decision.replace("_", " ")}</span>'


def get_status_dot(status: str) -> str:
    """Return a colored status indicator dot."""
    if status == "completed":
        return '<span class="status-dot status-completed"></span>'
    elif status.startswith("running"):
        return '<span class="status-dot status-running"></span>'
    elif status == "pending":
        return '<span class="status-dot status-pending"></span>'
    else:
        return '<span class="status-dot status-failed"></span>'


def render_pipeline_tracker(current_status: str) -> str:
    """Render the AI pipeline progress as visual steps."""
    steps = [
        ("scraper", '<i class="fa-solid fa-spider"></i>', "Scraper", "Web data extraction via Bright Data"),
        ("analyzer", '<i class="fa-solid fa-brain"></i>', "Analyzer", "Price anomaly & sentiment detection"),
        ("recommender", '<i class="fa-solid fa-lightbulb"></i>', "Recommender", "Strategic recommendation + RAG"),
        ("critique", '<i class="fa-solid fa-scale-balanced"></i>', "Critique", "Business rules validation"),
    ]

    current_node = ""
    if current_status.startswith("running_"):
        current_node = current_status.replace("running_", "")

    passed_nodes = []
    if current_status == "completed":
        passed_nodes = [s[0] for s in steps]
    elif current_node:
        for s_id, _, _, _ in steps:
            if s_id == current_node:
                break
            passed_nodes.append(s_id)

    html = ""
    for s_id, icon, name, desc in steps:
        if current_status == "completed":
            state_cls = "completed"
            indicator = '<i class="fa-solid fa-check" style="color:#10b981;"></i>'
        elif s_id == current_node:
            state_cls = "active"
            indicator = '<i class="fa-solid fa-circle-notch fa-spin" style="color:#3b82f6;"></i>'
        elif s_id in passed_nodes:
            state_cls = "completed"
            indicator = '<i class="fa-solid fa-check" style="color:#10b981;"></i>'
        else:
            state_cls = ""
            indicator = '<i class="fa-regular fa-circle" style="color:#64748b;"></i>'

        html += f"""
        <div class="pipeline-step {state_cls}">
            <div style="font-size:24px; width:40px; text-align:center;">{icon}</div>
            <div style="flex:1;">
                <div style="font-weight:600;color:#f1f5f9;font-size:14px;display:flex;align-items:center;gap:8px;">
                    {indicator} {name}
                </div>
                <div style="font-size:12px;color:#64748b;margin-top:2px;">
                    {desc}
                </div>
            </div>
        </div>
        """
    return html


def parse_user_input(text: str) -> tuple[str, str] | tuple[None, None]:
    """Return (url, component) if both are found, else (None, None)."""
    url_match = re.search(r"https?://\S+", text)
    if not url_match:
        return None, None
    url = url_match.group(0)
    component = text.replace(url, "").strip()
    return url, component if component else None


def fetch_task_history() -> list:
    """Fetch recent tasks from backend."""
    try:
        res = requests.get(f"{API_BASE_URL}/tasks", params={"limit": 20}, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


def check_backend_health() -> bool:
    """Check if backend is reachable."""
    try:
        res = requests.get("http://127.0.0.1:8000/health", timeout=3)
        return res.status_code == 200
    except Exception:
        return False

@st.dialog("Search chats...")
def search_dialog():
    search_query = st.text_input("Search history...", placeholder="🔍 Search...", label_visibility="collapsed")
    history = fetch_task_history()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if history:
        if search_query:
            history = [t for t in history if search_query.lower() in str(t.get("target_component", "")).lower() or search_query.lower() in str(t.get("target_url", "")).lower()]
        
        if not history:
            st.markdown(
                '<p style="color:#475569;font-size:13px;text-align:center;padding:12px 0;">'
                "No results found.</p>",
                unsafe_allow_html=True,
            )
        else:
            for task in history:
                t_id = task["id"]
                component_name = task.get("target_component", f"Task #{t_id}").title()
                if len(component_name) > 30:
                    component_name = component_name[:30] + "..."
                
                status_dot = "🟢" if task["status"] == "completed" else "🔴" if task["status"] == "failed" else "🟡"
                if st.button(
                    f"{status_dot} {component_name}",
                    key=f"hist_search_{t_id}",
                    use_container_width=True,
                ):
                    st.session_state["active_task"] = t_id
                    st.rerun()
    else:
        st.markdown(
            '<p style="color:#475569;font-size:13px;text-align:center;padding:12px 0;">'
            "No tasks yet.</p>",
            unsafe_allow_html=True,
        )



# ──────────────────────────────────────────────
# Page Routing: Landing vs Dashboard
# ──────────────────────────────────────────────
if st.session_state["current_page"] == "landing":
    render_landing_page()
    # CTA button to enter dashboard
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("🚀 Launch Agent Dashboard", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "dashboard"
            st.rerun()
else:
    # ──────────────────────────────────────────────
    # Chat-style Interface (Dashboard)
    # ──────────────────────────────────────────────
    with st.sidebar:
        # Logo / Brand
        st.markdown(
            """
            <div style=\"text-align:center; padding: 16px 0 8px 0;\">
                <div style=\"font-size:36px; color:#3b82f6; margin-bottom:8px;\"><i class=\"fa-solid fa-bullseye\"></i></div>
                <h2 style=\"margin:8px 0 0 0; font-weight:700;
                            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;\">BargainHunter</h2>
                <p style=\"color:#64748b; font-size:12px; margin-top:4px;
                           letter-spacing:1.5px; text-transform:uppercase;\">B2B Intelligence Agent</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        # Backend status indicator
        is_online = check_backend_health()
        status_color = "#10b981" if is_online else "#f43f5e"
        status_text = "Online" if is_online else "Offline"
        st.markdown(
            f"""
            <div style=\"display:flex; align-items:center; gap:8px;
                        padding:10px 14px; border-radius:10px;
                        background:rgba(255,255,255,0.03);
                        border:1px solid rgba(255,255,255,0.06);
                        margin-bottom:20px;\">
                <span style=\"width:8px;height:8px;border-radius:50%;
                              background:{status_color};
                              box-shadow:0 0 6px {status_color};\"></span>
                <span style=\"font-size:13px;color:#94a3b8;\">
                    Backend: <strong style=\"color:{status_color};\">{status_text}</strong>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # New Search Button
        if st.button("➕ New Search", use_container_width=True):
            st.session_state["active_task"] = None
            st.session_state["messages"] = []
            st.rerun()

        # Search Tasks Popup Button
        if st.button("🔍 Search chats...", use_container_width=True):
            search_dialog()

        # Recent Tasks in Sidebar
        st.markdown(
            '<p style="font-size:12px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;margin-top:16px;">Recent Tasks</p>',
            unsafe_allow_html=True,
        )
        history = fetch_task_history()
        if history:
            for task in history[:5]: # Show only recent 5 in sidebar to save space
                t_id = task["id"]
                component_name = task.get("target_component", f"Task #{t_id}").title()
                if len(component_name) > 22:
                    component_name = component_name[:22] + "..."
            
                status_dot = "🟢" if task["status"] == "completed" else "🔴" if task["status"] == "failed" else "🟡"
                if st.button(
                    f"{status_dot} {component_name}",
                    key=f"hist_{t_id}",
                    use_container_width=True,
                ):
                    st.session_state["active_task"] = t_id
                    st.rerun()
        else:
            st.markdown(
                '<p style="color:#475569;font-size:13px;text-align:center;padding:12px 0;">'
                "No tasks yet. Launch your first agent!</p>",
                unsafe_allow_html=True,
            )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div style='background:#1e293b;color:#f1f5f9;padding:10px;border-radius:8px;margin:4px 0;'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#172554;color:#cbd5e1;padding:10px;border-radius:8px;margin:4px 0;text-align:left;'>{msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Enter command (URL + component)…")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        url, component = parse_user_input(user_input)
        if not url or not component:
            error_msg = "⚠️ Please provide a valid URL followed by the component name."
            st.session_state["messages"].append({"role": "assistant", "content": error_msg})
            st.rerun()
        else:
            # Launch agent request
            try:
                response = requests.post(
                    f"{API_BASE_URL}/analyze",
                    json={"target_url": url, "target_component": component},
                    timeout=10,
                )
                if response.status_code == 200:
                    task_id = response.json()["task_id"]
                    st.session_state["active_task"] = task_id
                    st.session_state["messages"].append({"role": "assistant", "content": f"✅ Task #{task_id} launched!"})
                    st.rerun()
                else:
                    st.session_state["messages"].append({"role": "assistant", "content": "❌ Failed to start task. Check backend logs."})
                    st.rerun()
            except requests.exceptions.ConnectionError:
                st.session_state["messages"].append({"role": "assistant", "content": "🔌 Cannot connect to backend. Is it running?"})
                st.rerun()
            except Exception as e:
                st.session_state["messages"].append({"role": "assistant", "content": f"❌ Error: {e}"})
                st.rerun()


    # ──────────────────────────────────────────────
    # Main Content Area
    # ──────────────────────────────────────────────
    active_task = st.session_state.get("active_task", None)

    if active_task:
        # ── Header ──
        st.markdown(
            f"""
            <div style="margin-bottom:24px;">
                <h1 style="font-size:28px;font-weight:800;margin:0;">
                    📊 Intelligence Report
                    <span style="font-size:16px;font-weight:400;color:#64748b;">
                        — Task #{active_task}
                    </span>
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Polling for status ──
        pipeline_placeholder = st.empty()
        status_msg_placeholder = st.empty()
        result_placeholder = st.empty()

        is_completed = False
        max_retries = 80
        retries = 0

        while not is_completed and retries < max_retries:
            try:
                res = requests.get(f"{API_BASE_URL}/task/{active_task}", timeout=5)
                if res.status_code == 200:
                    task_data = res.json()
                    status = task_data["status"]

                    if status.startswith("running_") or status in ("pending", "running"):
                        # Pipeline tracker (Visual Feedback)
                        pipeline_html = render_pipeline_tracker(status)
                        pipeline_placeholder.markdown(
                            f"""
                            <div class="glass-card" style="margin-bottom:20px;">
                                <p style="font-size:11px;text-transform:uppercase;
                                          letter-spacing:1.2px;color:#64748b;
                                          font-weight:600;margin-bottom:12px;">
                                    🔄 Agent Pipeline
                                </p>
                                {pipeline_html}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        if status in ("pending", "running"):
                            status_msg_placeholder.info(
                                "⏳ Initializing agent workflow..."
                            )
                        else:
                            node_name = status.replace("running_", "").title()
                            status_msg_placeholder.info(
                                f"⚡ Executing **{node_name}** node..."
                            )

                        time.sleep(1.5)
                        retries += 1

                    elif status == "completed":
                        # Final pipeline state
                        pipeline_html = render_pipeline_tracker("completed")
                        pipeline_placeholder.markdown(
                            f"""
                            <div class="glass-card" style="margin-bottom:20px;
                                 border-color:rgba(16,185,129,0.2);">
                                <p style="font-size:11px;text-transform:uppercase;
                                          letter-spacing:1.2px;color:#10b981;
                                          font-weight:600;margin-bottom:12px;">
                                    ✅ Pipeline Complete
                                </p>
                                {pipeline_html}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        status_msg_placeholder.empty()
                        is_completed = True

                        # Parse results
                        result_json = json.loads(task_data["result_data"])
                        extracted_products = result_json.get("extracted_products") or []
                        analysis = result_json.get("market_analysis") or {}
                        cheapest = analysis.get("cheapest") or {}
                        best = analysis.get("best") or {}
                        decision = result_json.get("decision", "MAINTAIN")
                        recommendation = result_json.get(
                            "recommendation", "No recommendation available."
                        )

                        with result_placeholder.container():
                            # ── Key Metrics Row ──
                            st.markdown(
                                '<p style="font-size:11px;text-transform:uppercase;'
                                "letter-spacing:1.2px;color:#64748b;font-weight:600;"
                                'margin-bottom:12px;">📈 Key Metrics</p>',
                                unsafe_allow_html=True,
                            )
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Products Found", len(extracted_products))
                            m2.metric(
                                "Lowest Price",
                                f"Rp {cheapest.get('price', 'N/A'):,}"
                                if isinstance(cheapest.get("price"), (int, float))
                                else f"Rp {cheapest.get('price', 'N/A')}",
                            )
                            m3.metric(
                                "Top Rating",
                                best.get("rating", "N/A"),
                            )
                            with m4:
                                st.markdown(
                                    '<p style="font-size:13px;color:#64748b;'
                                    "font-weight:500;text-transform:uppercase;"
                                    'letter-spacing:0.8px;margin-bottom:8px;">'
                                    "AI Decision</p>",
                                    unsafe_allow_html=True,
                                )
                                st.markdown(
                                    get_decision_badge(decision),
                                    unsafe_allow_html=True,
                                )

                            st.markdown("<br>", unsafe_allow_html=True)

                            # ── Tabbed Content (Hierarchy & Proximity) ──
                            tab_strategy, tab_leaders, tab_data = st.tabs(
                                [
                                    "AI Strategy",
                                    "Market Leaders",
                                    "Raw Data",
                                ]
                            )

                            with tab_strategy:
                                st.markdown(
                                    f"""<div class="glass-card" style="margin-top:8px;">
    <h3 style="font-size:18px;font-weight:700;margin:0 0 12px 0;color:#f1f5f9;">Strategic Recommendation</h3>
    <p style="color:#cbd5e1;line-height:1.7;font-size:15px;">{recommendation}</p>
    <div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);">
    <span style="color:#64748b;font-size:12px;margin-right:8px;">Final Decision:</span>{get_decision_badge(decision)}
    </div>
    </div>""",
                                    unsafe_allow_html=True,
                                )

                            with tab_leaders:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    c_name = cheapest.get("name", "N/A")
                                    c_price = cheapest.get("price", "N/A")
                                    if isinstance(c_price, (int, float)):
                                        c_price = f"{c_price:,}"
                                    st.markdown(
                                        f"""<div class="glass-card" style="margin-top:8px; border-color:rgba(16,185,129,0.2);">
    <div style="font-size:24px;margin-bottom:8px;color:#10b981;"><i class="fa-solid fa-money-bill-wave"></i></div>
    <p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#10b981;font-weight:600;margin-bottom:8px;">Cheapest Product</p>
    <h3 style="font-size:16px;font-weight:700;color:#f1f5f9;margin:0 0 8px 0;">{c_name}</h3>
    <p style="font-size:24px;font-weight:800;color:#10b981;margin:0;">Rp {c_price}</p>
    </div>""",
                                        unsafe_allow_html=True,
                                    )
                                with col_b:
                                    b_name = best.get("name", "N/A")
                                    b_rating = best.get("rating", "N/A")
                                    st.markdown(
                                        f"""<div class="glass-card" style="margin-top:8px; border-color:rgba(245,158,11,0.2);">
    <div style="font-size:24px;margin-bottom:8px;color:#f59e0b;"><i class="fa-solid fa-star"></i></div>
    <p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#f59e0b;font-weight:600;margin-bottom:8px;">Best Rated</p>
    <h3 style="font-size:16px;font-weight:700;color:#f1f5f9;margin:0 0 8px 0;">{b_name}</h3>
    <p style="font-size:24px;font-weight:800;color:#f59e0b;margin:0;"><i class="fa-solid fa-star" style="font-size:16px;"></i> {b_rating}</p>
    </div>""",
                                        unsafe_allow_html=True,
                                    )

                            with tab_data:
                                if extracted_products:
                                    df = pd.DataFrame(extracted_products)
                                    st.markdown(
                                        f'<p style="color:#64748b;font-size:13px;margin:8px 0 12px 0;">'
                                        f"Showing {len(df)} products extracted from target URL</p>",
                                        unsafe_allow_html=True,
                                    )
                                    st.dataframe(
                                        df,
                                        use_container_width=True,
                                        hide_index=True,
                                    )
                                else:
                                    st.info("No product data was extracted.")

                    elif status == "failed":
                        pipeline_placeholder.empty()
                        status_msg_placeholder.empty()
                        is_completed = True

                        with result_placeholder.container():
                            st.markdown(
                                """
                                <div class="glass-card" style="border-color:rgba(244,63,94,0.3);
                                     text-align:center;padding:40px;">
                                    <div style="font-size:48px;margin-bottom:12px;color:#f43f5e;"><i class="fa-solid fa-triangle-exclamation"></i></div>
                                    <h3 style="color:#f43f5e;font-weight:700;margin:0 0 8px 0;">
                                        Task Failed
                                    </h3>
                                    <p style="color:#94a3b8;font-size:14px;">
                                        The agent encountered an error during execution.
                                        Check backend logs for details.
                                    </p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            with st.expander("🔍 View Error Details"):
                                st.json(task_data)
                else:
                    status_msg_placeholder.warning("⏳ Waiting for backend response...")
                    time.sleep(2)
                    retries += 1
            except requests.exceptions.ConnectionError:
                status_msg_placeholder.error(
                    "🔌 Lost connection to backend. Retrying..."
                )
                time.sleep(3)
                retries += 1
            except Exception as e:
                status_msg_placeholder.error(f"❌ Unexpected error: {e}")
                break

        if retries >= max_retries and not is_completed:
            status_msg_placeholder.warning(
                "⏱️ Task is taking longer than expected. "
                "Refresh the page to check again."
            )

    else:
        # ── Empty State (Clear visual hierarchy) ──
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon" style="color:#3b82f6;"><i class="fa-solid fa-bullseye"></i></div>
                <h2 style="font-size:24px;font-weight:700;color:#f1f5f9;
                           margin:0 0 12px 0;">
                    Ready to Hunt for Bargains
                </h2>
                <p style="color:#64748b;font-size:15px;max-width:480px;
                          margin:0 auto 32px auto;line-height:1.6;">
                    Enter an e-commerce search URL and target component in the
                    sidebar to launch the AI surveillance agent.
                </p>
                <div style="display:flex;gap:32px;justify-content:center;
                            flex-wrap:wrap;margin-top:20px;">
                    <div class="glass-card" style="text-align:center;
                         width:180px;padding:20px;">
                        <div style="font-size:32px;margin-bottom:8px;color:#3b82f6;"><i class="fa-solid fa-spider"></i></div>
                        <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                                  margin:0 0 4px 0;">Scrape</p>
                        <p style="font-size:11px;color:#64748b;margin:0;">
                            Extract competitor data
                        </p>
                    </div>
                    <div class="glass-card" style="text-align:center;
                         width:180px;padding:20px;">
                        <div style="font-size:32px;margin-bottom:8px;color:#8b5cf6;"><i class="fa-solid fa-brain"></i></div>
                        <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                                  margin:0 0 4px 0;">Analyze</p>
                        <p style="font-size:11px;color:#64748b;margin:0;">
                            Detect price anomalies
                        </p>
                    </div>
                    <div class="glass-card" style="text-align:center;
                         width:180px;padding:20px;">
                        <div style="font-size:32px;margin-bottom:8px;color:#f59e0b;"><i class="fa-solid fa-lightbulb"></i></div>
                        <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                                  margin:0 0 4px 0;">Recommend</p>
                        <p style="font-size:11px;color:#64748b;margin:0;">
                            AI-driven strategy
                        </p>
                    </div>
                    <div class="glass-card" style="text-align:center;
                         width:180px;padding:20px;">
                        <div style="font-size:32px;margin-bottom:8px;color:#10b981;"><i class="fa-solid fa-scale-balanced"></i></div>
                        <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                                  margin:0 0 4px 0;">Validate</p>
                        <p style="font-size:11px;color:#64748b;margin:0;">
                            Business rules check
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
            )
