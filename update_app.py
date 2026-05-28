import os

new_code = """# ──────────────────────────────────────────────
# Chat State Management
# ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ──────────────────────────────────────────────
# Sidebar — Chat History & Controls
# ──────────────────────────────────────────────
with st.sidebar:
    # Logo / Brand
    st.markdown(
        '''
        <div style="text-align:center; padding: 16px 0 8px 0;">
            <div style="font-size:36px; color:#3b82f6; margin-bottom:8px;"><i class="fa-solid fa-bullseye"></i></div>
            <h2 style="margin:8px 0 0 0; font-weight:700;
                        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;">
                BargainHunter
            </h2>
            <p style="color:#64748b; font-size:12px; margin-top:4px;
                       letter-spacing:1.5px; text-transform:uppercase;">
                B2B Intelligence Agent
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        if "active_task" in st.session_state:
            del st.session_state["active_task"]
        st.rerun()

    # Backend status indicator
    is_online = check_backend_health()
    status_color = "#10b981" if is_online else "#f43f5e"
    status_text = "Online" if is_online else "Offline"
    st.markdown(
        f'''
        <div style="display:flex; align-items:center; gap:8px;
                    padding:10px 14px; border-radius:10px;
                    background:rgba(255,255,255,0.03);
                    border:1px solid rgba(255,255,255,0.06);
                    margin-top:20px; margin-bottom:20px;">
            <span style="width:8px;height:8px;border-radius:50%;
                         background:{status_color};
                         box-shadow:0 0 6px {status_color};"></span>
            <span style="font-size:13px;color:#94a3b8;">
                Backend: <strong style="color:{status_color};">{status_text}</strong>
            </span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Task history (Chat History)
    st.markdown(
        '<p style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;'
        'color:#64748b;font-weight:600;margin-bottom:8px;"><i class="fa-solid fa-clock-rotate-left"></i> Chat History</p>',
        unsafe_allow_html=True,
    )

    history = fetch_task_history()
    if history:
        for task in history[:10]:
            t_id = task["id"]
            t_status = task["status"]
            t_comp = task["target_component"]
            dot = get_status_dot(t_status)

            is_active = st.session_state.get("active_task") == t_id
            border_style = "border-color: rgba(59,130,246,0.4);" if is_active else ""

            st.markdown(
                f'''
                <div class="history-item" style="{border_style}">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:13px;font-weight:600;color:#f1f5f9;
                                     white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            {t_comp}
                        </span>
                        <span style="font-size:11px;color:#64748b;flex-shrink:0;">
                            {dot}{t_status}
                        </span>
                    </div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

            if st.button(f"Load Task #{t_id}", key=f"hist_{t_id}", use_container_width=True):
                st.session_state["active_task"] = t_id
                st.session_state.messages = [
                    {"role": "user", "type": "text", "content": f"Show me the analysis for `{t_comp}` (Task #{t_id})"},
                    {"role": "assistant", "type": "result", "task_id": t_id}
                ]
                st.rerun()
    else:
        st.markdown(
            '<p style="color:#475569;font-size:13px;text-align:center;padding:12px 0;">'
            "No chat history yet.</p>",
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# Main Chat Area
# ──────────────────────────────────────────────
def render_task_result(task_data):
    result_json = json.loads(task_data["result_data"])
    extracted_products = result_json.get("extracted_products") or []
    analysis = result_json.get("market_analysis") or {}
    cheapest = analysis.get("cheapest") or {}
    best = analysis.get("best") or {}
    decision = result_json.get("decision", "MAINTAIN")
    recommendation = result_json.get("recommendation", "No recommendation available.")

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
        f"Rp {cheapest.get('price', 'N/A'):,}" if isinstance(cheapest.get("price"), (int, float)) else f"Rp {cheapest.get('price', 'N/A')}",
    )
    m3.metric("Top Rating", best.get("rating", "N/A"))
    with m4:
        st.markdown(
            '<p style="font-size:13px;color:#64748b;'
            "font-weight:500;text-transform:uppercase;"
            'letter-spacing:0.8px;margin-bottom:8px;">'
            "AI Decision</p>",
            unsafe_allow_html=True,
        )
        st.markdown(get_decision_badge(decision), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_strategy, tab_leaders, tab_data = st.tabs(["AI Strategy", "Market Leaders", "Raw Data"])
    
    with tab_strategy:
        st.markdown(
            f'''<div class="glass-card" style="margin-top:8px;">
<h3 style="font-size:18px;font-weight:700;margin:0 0 12px 0;color:#f1f5f9;">Strategic Recommendation</h3>
<p style="color:#cbd5e1;line-height:1.7;font-size:15px;">{recommendation}</p>
<div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);">
<span style="color:#64748b;font-size:12px;margin-right:8px;">Final Decision:</span>{get_decision_badge(decision)}
</div>
</div>''',
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
                f'''<div class="glass-card" style="margin-top:8px; border-color:rgba(16,185,129,0.2);">
<div style="font-size:24px;margin-bottom:8px;color:#10b981;"><i class="fa-solid fa-money-bill-wave"></i></div>
<p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#10b981;font-weight:600;margin-bottom:8px;">Cheapest Product</p>
<h3 style="font-size:16px;font-weight:700;color:#f1f5f9;margin:0 0 8px 0;">{c_name}</h3>
<p style="font-size:24px;font-weight:800;color:#10b981;margin:0;">Rp {c_price}</p>
</div>''',
                unsafe_allow_html=True,
            )
        with col_b:
            b_name = best.get("name", "N/A")
            b_rating = best.get("rating", "N/A")
            st.markdown(
                f'''<div class="glass-card" style="margin-top:8px; border-color:rgba(245,158,11,0.2);">
<div style="font-size:24px;margin-bottom:8px;color:#f59e0b;"><i class="fa-solid fa-star"></i></div>
<p style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#f59e0b;font-weight:600;margin-bottom:8px;">Best Rated</p>
<h3 style="font-size:16px;font-weight:700;color:#f1f5f9;margin:0 0 8px 0;">{b_name}</h3>
<p style="font-size:24px;font-weight:800;color:#f59e0b;margin:0;"><i class="fa-solid fa-star" style="font-size:16px;"></i> {b_rating}</p>
</div>''',
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
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No product data was extracted.")


# Display empty state if no messages
if not st.session_state.messages:
    st.markdown(
        '''
        <div class="empty-state" style="margin-top:60px;">
            <div class="empty-state-icon" style="color:#3b82f6;"><i class="fa-solid fa-bullseye"></i></div>
            <h2 style="font-size:28px;font-weight:800;color:#f1f5f9;
                       margin:0 0 12px 0;">
                How can I help you hunt today?
            </h2>
            <p style="color:#64748b;font-size:15px;max-width:480px;
                      margin:0 auto 32px auto;line-height:1.6;">
                Type a message with an e-commerce URL followed by the component name. <br/>
                <b>Example:</b> <span style="color:#cbd5e1;">https://tokopedia.com/find/esp32 ESP32-CAM</span>
            </p>
            <div style="display:flex;gap:32px;justify-content:center;
                        flex-wrap:wrap;margin-top:20px;">
                <div class="glass-card" style="text-align:center;
                     width:160px;padding:20px;">
                    <div style="font-size:28px;margin-bottom:8px;color:#3b82f6;"><i class="fa-solid fa-spider"></i></div>
                    <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                              margin:0 0 4px 0;">Scrape</p>
                </div>
                <div class="glass-card" style="text-align:center;
                     width:160px;padding:20px;">
                    <div style="font-size:28px;margin-bottom:8px;color:#8b5cf6;"><i class="fa-solid fa-brain"></i></div>
                    <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                              margin:0 0 4px 0;">Analyze</p>
                </div>
                <div class="glass-card" style="text-align:center;
                     width:160px;padding:20px;">
                    <div style="font-size:28px;margin-bottom:8px;color:#f59e0b;"><i class="fa-solid fa-lightbulb"></i></div>
                    <p style="font-size:13px;font-weight:600;color:#f1f5f9;
                              margin:0 0 4px 0;">Recommend</p>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "text" or "type" not in msg:
            st.markdown(msg["content"])
        elif msg.get("type") == "result":
            t_id = msg["task_id"]
            try:
                res = requests.get(f"{API_BASE_URL}/task/{t_id}", timeout=5)
                if res.status_code == 200:
                    task_data = res.json()
                    status = task_data["status"]
                    if status == "completed":
                        st.markdown(f"**Task #{t_id} Completed!** Here is the intelligence report:")
                        render_task_result(task_data)
                    elif status == "failed":
                        st.error(f"Task #{t_id} failed. Check backend logs.")
                        with st.expander("🔍 View Error Details"):
                            st.json(task_data)
                    else:
                        st.info(f"Task #{t_id} is currently {status}.")
            except Exception as e:
                st.error("Failed to load task result.")


# ──────────────────────────────────────────────
# Chat Input & Processing
# ──────────────────────────────────────────────
prompt = st.chat_input("Enter URL and component name (e.g. https://... ESP32-CAM)")
if prompt:
    if not is_online:
        st.error("Backend is offline. Cannot start task.")
    else:
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        words = prompt.split()
        target_url = None
        component_words = []
        for w in words:
            if w.startswith("http://") or w.startswith("https://"):
                target_url = w
            else:
                component_words.append(w)
        target_component = " ".join(component_words)

        with st.chat_message("assistant"):
            if not target_url:
                err_msg = "Please provide a valid e-commerce URL starting with `http://` or `https://`."
                st.markdown(err_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": err_msg})
            elif not target_component:
                err_msg = "Please specify the component name you want to track (e.g., `https://example.com/search ESP32-CAM`)."
                st.markdown(err_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": err_msg})
            else:
                st.markdown(f"Starting surveillance task for **{target_component}** at `{target_url}`...")
                
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/analyze",
                        json={"target_url": target_url, "target_component": target_component},
                        timeout=10,
                    )
                    if response.status_code == 200:
                        task_id = response.json()["task_id"]
                        st.session_state["active_task"] = task_id
                        
                        pipeline_placeholder = st.empty()
                        status_msg_placeholder = st.empty()
                        result_placeholder = st.empty()

                        is_completed = False
                        max_retries = 80
                        retries = 0

                        while not is_completed and retries < max_retries:
                            res = requests.get(f"{API_BASE_URL}/task/{task_id}", timeout=5)
                            if res.status_code == 200:
                                task_data = res.json()
                                status = task_data["status"]

                                if status.startswith("running_") or status in ("pending", "running"):
                                    pipeline_html = render_pipeline_tracker(status)
                                    pipeline_placeholder.markdown(
                                        f'''<div class="glass-card" style="margin-bottom:20px;">
                                        <p style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#64748b;font-weight:600;margin-bottom:12px;">🔄 Agent Pipeline</p>
                                        {pipeline_html}</div>''', unsafe_allow_html=True
                                    )
                                    if status in ("pending", "running"):
                                        status_msg_placeholder.info("⏳ Initializing agent workflow...")
                                    else:
                                        node_name = status.replace("running_", "").title()
                                        status_msg_placeholder.info(f"⚡ Executing **{node_name}** node...")
                                    time.sleep(1.5)
                                    retries += 1
                                elif status == "completed":
                                    pipeline_html = render_pipeline_tracker("completed")
                                    pipeline_placeholder.markdown(
                                        f'''<div class="glass-card" style="margin-bottom:20px;border-color:rgba(16,185,129,0.2);">
                                        <p style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#10b981;font-weight:600;margin-bottom:12px;">✅ Pipeline Complete</p>
                                        {pipeline_html}</div>''', unsafe_allow_html=True
                                    )
                                    status_msg_placeholder.empty()
                                    is_completed = True
                                    
                                    with result_placeholder.container():
                                        st.markdown(f"**Task #{task_id} Completed!** Here is the intelligence report:")
                                        render_task_result(task_data)
                                        
                                    st.session_state.messages.append({"role": "assistant", "type": "result", "task_id": task_id})
                                elif status == "failed":
                                    pipeline_placeholder.empty()
                                    status_msg_placeholder.error("Task failed. Check backend logs.")
                                    is_completed = True
                                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": "Task failed."})
                            else:
                                time.sleep(2)
                                retries += 1
                                
                        if not is_completed:
                            status_msg_placeholder.warning("Task is taking too long. Please check history later.")
                            st.session_state.messages.append({"role": "assistant", "type": "text", "content": f"Task #{task_id} started, but polling timed out. Check history later."})
                            
                    else:
                        err_msg = "❌ Failed to start task. Check backend logs."
                        st.error(err_msg)
                        st.session_state.messages.append({"role": "assistant", "type": "text", "content": err_msg})
                except Exception as e:
                    err_msg = f"❌ Error: {e}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": err_msg})
"""

with open('/home/kizzu/Project/Outside/BargainHunter_B2B_Real_Time_And_Pricing_Surveillance_Agent/frontend/app.py', 'r') as f:
    content = f.read()

idx = content.find('# ──────────────────────────────────────────────\\n# Sidebar')
if idx != -1:
    content = content[:idx] + new_code

with open('/home/kizzu/Project/Outside/BargainHunter_B2B_Real_Time_And_Pricing_Surveillance_Agent/frontend/app.py', 'w') as f:
    f.write(content)
