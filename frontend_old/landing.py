"""
BargainHunter B2B — Landing Page & Dashboard
Inspired by Sumsub's sharp, bold, and corporate compliance design.
"""

import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────

def inject_tailwind():
    components.html(
        """
        <script>
            const parentDoc = window.parent.document;
            
            // Skenario 2: Streamlit Rerun (Tailwind sudah tertanam di browser)
            if (parentDoc.getElementById('tailwind-cdn')) {
                // Trik memancing MutationObserver Tailwind agar men-scan ulang HTML baru
                const trigger = parentDoc.createElement('div');
                parentDoc.body.appendChild(trigger);
                setTimeout(() => trigger.remove(), 10);
            } 
            // Skenario 1: First Load (Tailwind belum ada)
            else {
                // 1. Suntik Konfigurasi Tailwind
                const configScript = parentDoc.createElement('script');
                configScript.id = 'tailwind-config';
                configScript.innerHTML = `
                    window.tailwind = {
                        config: {
                            important: true // SUPER PENTING: Paksa Tailwind menang dari CSS Streamlit
                        }
                    };
                `;
                parentDoc.head.appendChild(configScript);

                // 2. Suntik CDN Tailwind
                const script = parentDoc.createElement('script');
                script.id = 'tailwind-cdn';
                script.src = 'https://cdn.tailwindcss.com';
                parentDoc.head.appendChild(script);
            }
        </script>
        """,
        height=0,
        width=0,
    )


st.set_page_config(
    page_title="BargainHunter — B2B Price Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_tailwind()

# Load FontAwesome Icons globally
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
    unsafe_allow_html=True,
)


def render_landing_page():
    """Render the full landing page using bold, sharp corporate SaaS design principles."""

    landing_html = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /*
    .landing-root {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-color);
        background-color: var(--background-color);
        overflow-x: hidden;
    }
    */

    /* ── Remove Streamlit Default Margins/Padding ── */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* ── Navbar (Tegas & Solid) ── */
    
    .nav-cta {
        background: #3b82f6; color: var(--text-color) !important; 
        padding: 10px 24px; border-radius: 6px; /* Sudut lebih kotak/tegas */
        font-weight: 700; font-size: 14px; text-decoration: none;
        border: 2px solid #2563eb;
    }

    /* ── Hero Section (Fokus Bebas Kode / No-Code) ── */
    .hero-section {
        text-align: center; padding: 120px 48px 80px;
        background: var(--background-color);
        border-bottom: 2px solid rgba(128, 128, 128, 0.2);
    }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(128, 128, 128, 0.2); border: 2px solid #3b82f6;
        padding: 6px 16px; border-radius: 4px; font-size: 12px; color: #3b82f6;
        font-weight: 800; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 1px;
    }
    .hero-title {
        font-size: clamp(38px, 5vw, 60px); font-weight: 900; line-height: 1.15;
        margin: 0 auto 24px; max-width: 900px; color: var(--text-color);
    }
    .hero-subtitle {
        font-size: 18px; color: rgba(128, 128, 128, 0.8); max-width: 700px; margin: 0 auto 40px;
        line-height: 1.6;
    }
    .hero-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
    
    .btn-primary {
        background: #3b82f6; color: var(--text-color); padding: 14px 32px; 
        border-radius: 6px; font-weight: 700; font-size: 15px; 
        text-decoration: none; display: inline-flex; align-items: center; gap: 8px;
        border: 2px solid #2563eb; cursor: pointer;
    }
    .btn-secondary {
        background: rgba(128, 128, 128, 0.2); border: 2px solid rgba(128, 128, 128, 0.4);
        color: var(--text-color); padding: 14px 32px; border-radius: 6px; font-weight: 700;
        font-size: 15px; text-decoration: none; display: inline-flex; align-items: center; gap: 8px;
        cursor: pointer;
    }

    /* ── Stats Row (Kotak Informasi Tegas) ── */
    .stats-row {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        background: var(--secondary-background-color); border-bottom: 2px solid rgba(128, 128, 128, 0.2);
    }
    .stat-item { 
        text-align: center; padding: 40px 24px; 
        border-right: 2px solid rgba(128, 128, 128, 0.2);
    }
    .stat-item:last-child { border-right: none; }
    .stat-value { font-size: 46px; font-weight: 900; color: #3b82f6; }
    .stat-label { font-size: 13px; color: rgba(128, 128, 128, 0.8); margin-top: 6px; font-weight: 700; text-transform: uppercase; }

    /* ── Features Grid (Gaya Grid Solid Sumsub) ── */
    .section-header { text-align: center; padding: 100px 48px 50px; background: var(--background-color);}
    .section-tag {
        display: inline-block; color: #3b82f6; font-size: 13px;
        font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
        margin-bottom: 12px;
    }
    .section-title { font-size: 36px; font-weight: 900; margin: 0 0 16px; color: var(--text-color); }
    .section-desc { font-size: 16px; color: rgba(128, 128, 128, 0.8); max-width: 650px; margin: 0 auto; line-height: 1.6; }
    
    .features-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        border-top: 2px solid rgba(128, 128, 128, 0.2); border-left: 2px solid rgba(128, 128, 128, 0.2);
        max-width: 1280px; margin: 0 auto 100px;
    }
    .feature-card {
        background: var(--secondary-background-color); 
        border-right: 2px solid rgba(128, 128, 128, 0.2); border-bottom: 2px solid rgba(128, 128, 128, 0.2);
        padding: 40px; transition: background 0.2s;
    }
    .feature-card:hover { background: var(--background-color); }
    .feature-icon {
        font-size: 28px; color: #3b82f6; margin-bottom: 24px;
    }
    .feature-card h3 { font-size: 20px; font-weight: 800; margin: 0 0 12px; color: var(--text-color); }
    .feature-card p { font-size: 14px; color: rgba(128, 128, 128, 0.8); line-height: 1.6; margin: 0; }

    /* ── Workflow (No-Code Blueprint Layout) ── */
    .steps-section { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px; padding: 0 48px 100px; max-width: 1280px; margin: 0 auto; 
    }
    .step-box {
        background: var(--secondary-background-color); border: 2px solid rgba(128, 128, 128, 0.2); border-radius: 6px; padding: 32px;
    }
    .step-number {
        font-size: 14px; font-weight: 900; color: #3b82f6; 
        background: rgba(59,130,246,0.1); padding: 4px 12px; 
        border-radius: 4px; display: inline-block; margin-bottom: 20px;
    }
    .step-box h4 { font-size: 18px; font-weight: 800; margin: 0 0 10px; color: var(--text-color); }
    .step-box p { font-size: 14px; color: rgba(128, 128, 128, 0.8); margin: 0; line-height: 1.5; }

    /* ── Metrics / Trust Banner ── */
    .metrics-banner {
        background: var(--secondary-background-color); border-top: 2px solid rgba(128, 128, 128, 0.2); border-bottom: 2px solid rgba(128, 128, 128, 0.2);
        padding: 80px 48px; text-align: center;
    }
    .metrics-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        border: 2px solid rgba(128, 128, 128, 0.2); max-width: 1100px; margin: 40px auto 0;
    }
    .metric-card {
        background: var(--background-color); padding: 40px 24px; text-align: center;
        border-right: 2px solid rgba(128, 128, 128, 0.2);
    }
    .metric-card:last-child { border-right: none; }
    .metric-card .metric-val { font-size: 42px; font-weight: 900; color: #10b981; }
    .metric-card .metric-lbl { font-size: 13px; color: rgba(128, 128, 128, 0.8); font-weight: 700; margin-top: 8px; text-transform: uppercase;}

    /* ── FAQ ── */
    .faq-section { padding: 0 48px 100px; max-width: 900px; margin: 0 auto; }
    .faq-item {
        background: var(--secondary-background-color); border: 2px solid rgba(128, 128, 128, 0.2); border-radius: 6px;
        padding: 24px; margin-bottom: 16px;
    }
    .faq-q { font-size: 16px; font-weight: 800; color: var(--text-color); margin: 0 0 10px; }
    .faq-a { font-size: 14px; color: rgba(128, 128, 128, 0.8); line-height: 1.6; margin: 0; }

    /* ── Footer ── */
    .landing-footer {
        background: var(--secondary-background-color); border-top: 2px solid rgba(128, 128, 128, 0.2);
        padding: 60px 48px; text-align: center;
    }
    .footer-brand { font-size: 22px; font-weight: 800; color: #3b82f6; margin-bottom: 16px; }
    .footer-copy { font-size: 13px; color: rgba(128, 128, 128, 0.7); }
    .footer-links { display: flex; gap: 32px; justify-content: center; margin-top: 24px; }
    .footer-links a { color: rgba(128, 128, 128, 0.8); text-decoration: none; font-size: 13px; font-weight: 600;}
    .footer-links a:hover { color: var(--text-color); }

    /* ── CTA Banner ── */
    .cta-banner {
        text-align: center; padding: 100px 48px; background: var(--background-color);
        border-top: 2px solid rgba(128, 128, 128, 0.2);
    }
    .cta-banner h2 { font-size: 38px; font-weight: 900; margin: 0 0 16px; color: var(--text-color); }
    .cta-banner p { font-size: 18px; color: rgba(128, 128, 128, 0.8); margin: 0 0 32px; }
    </style>

    <div class="landing-root">
    <!-- ═══ NAVBAR ═══ -->
        <nav class="fixed top-0 left-0 right-0 z-[99999] flex items-center justify-between w-full px-12 py-5 bg-[#0e1117]/85 backdrop-blur-md border-b-2 border-gray-500/20">
            <div class="flex items-center gap-2.5 text-2xl font-extrabold text-blue-500">
                <i class="fa-solid fa-bullseye"></i> BargainHunter
            </div>
            <div class="flex items-center gap-8">
                <a href="#features" class="text-sm font-semibold text-gray-400 no-underline transition-colors duration-200 hover:text-blue-500">Capabilities</a>
                <a href="#how-it-works" class="text-sm font-semibold text-gray-400 no-underline transition-colors duration-200 hover:text-blue-500">No-Code Workflow</a>
                <a href="#metrics" class="text-sm font-semibold text-gray-400 no-underline transition-colors duration-200 hover:text-blue-500">Compliance Results</a>
                <a href="#faq" class="text-sm font-semibold text-gray-400 no-underline transition-colors duration-200 hover:text-blue-500">FAQ</a>
            </div>
            <div class="flex items-center gap-6">
                <a href="#signup" class="text-sm font-semibold text-gray-400 no-underline transition-colors duration-200 hover:text-blue-500">Sign up</a>
                <a href="#launch" class="px-6 py-2.5 text-sm font-bold text-white bg-blue-500 border-2 border-blue-600 rounded-md no-underline transition-all duration-200 hover:bg-blue-600 hover:border-blue-700">Get started</a>
            </div>  
        </nav>
    </div>

    <!-- ═══ HERO ═══ -->
    <div class="hero-section">
        <div class="hero-badge"><i class="fa-solid fa-lock"></i> Automated B2B Price Compliance</div>
        <h1 class="hero-title">Deploy Price Surveillance Flows Without Code maca ci</h1>
        <p class="hero-subtitle">Set up autonomous monitoring pipelines, detect market positioning anomalies, and secure margins using an intuitive, developer-free infrastructure.</p>
        <div class="hero-buttons">
            <a class="btn-primary" href="#launch">Launch Automation Flow <i class="fa-solid fa-arrow-right"></i></a>
            <a class="btn-secondary" href="#how-it-works">See Blueprint Blueprint</a>
        </div>
    </div>

    <!-- ═══ STATS ROW ═══ -->
    <div class="stats-row">
        <div class="stat-item"><div class="stat-value">99.9%</div><div class="stat-label">Guaranteed Uptime</div></div>
        <div class="stat-item"><div class="stat-value">&lt;30s</div><div class="stat-label">Verification Speed</div></div>
        <div class="stat-item"><div class="stat-value">100%</div><div class="stat-label">No-Code System</div></div>
        <div class="stat-item"><div class="stat-value">24/7</div><div class="stat-label">Continuous Audit</div></div>
    </div>

    <!-- ═══ FEATURES ═══ -->
    <div id="features">
        <div class="section-header">
            <div class="section-tag">Platform Features</div>
            <h2 class="section-title">Enterprise Price Guardrails</h2>
            <p class="section-desc">Complete toolkit designed for business operations, legal officers, and commerce executives to track pricing compliance.</p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon"><i class="fa-solid fa-shield-halved"></i></div>
                <h3>Intelligent Tracking</h3>
                <p>Extract precise product data, SKU structures, and current stock status across multi-channel environments instantly.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fa-solid fa-chart-pie"></i></div>
                <h3>Anomaly Auditing</h3>
                <p>Instantly flag violations of minimum advertised pricing (MAP) or deep competitive drops with high precision.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fa-solid fa-gavel"></i></div>
                <h3>Rule Validation</h3>
                <p>Run pricing intelligence past built-in business governance guardrails to secure margin safety and legal compliance.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fa-solid fa-sliders"></i></div>
                <h3>Visual Flow Builder</h3>
                <p>Orchestrate complex target verification structures completely code-free via a drag-and-drop dashboard.</p>
            </div>
        </div>
    </div>

    <!-- ═══ HOW IT WORKS (BLUEPRINT) ═══ -->
    <div id="how-it-works">
        <div class="section-header">
            <div class="section-tag">Architecture</div>
            <h2 class="section-title">The 4-Step Automation Flow</h2>
            <p class="section-desc">How our secure system processes competitive pricing data into immediate compliance actions.</p>
        </div>
        <div class="steps-section">
            <div class="step-box">
                <div class="step-number">Step 01</div>
                <h4>Set Target Parameters</h4>
                <p>Paste the direct marketplace query or SKU category URL into the workflow system.</p>
            </div>
            <div class="step-box">
                <div class="step-number">Step 02</div>
                <h4>Secure Data Extraction</h4>
                <p>Automated cloud infrastructure pulls text-based price listings safely and reliably.</p>
            </div>
            <div class="step-box">
                <div class="step-number">Step 03</div>
                <h4>Compliance Audit</h4>
                <p>The processing module benchmarks data fields against historical records and margins.</p>
            </div>
            <div class="step-box">
                <div class="step-number">Step 04</div>
                <h4>Executive Report</h4>
                <p>Get clean, high-level structural advice (MAINTAIN / ADJUST / ACTION) ready for decision makers.</p>
            </div>
        </div>
    </div>

    <!-- ═══ METRICS BANNER ═══ -->
    <div id="metrics" class="metrics-banner">
        <div class="section-tag">Audit Impact</div>
        <h2 class="section-title">Engineered for High Trust Operations</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-val">94%</div>
                <div class="metric-lbl">Manual Labor Reduction</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">30s</div>
                <div class="metric-lbl">Audit Turnaround Time</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">99.2%</div>
                <div class="metric-lbl">Data Accuracy Rating</div>
            </div>
        </div>
    </div>

    <!-- ═══ FAQ ═══ -->
    <div id="faq">
        <div class="section-header">
            <div class="section-tag">FAQ</div>
            <h2 class="section-title">Frequently Asked Questions</h2>
        </div>
        <div class="faq-section">
            <div class="faq-item">
                <p class="faq-q">Do I need engineering experience to use this?</p>
                <p class="faq-a">No. The entire system is built with a strictly code-free interface allowing product and operational leads to schedule or run audit tracking independently.</p>
            </div>
            <div class="faq-item">
                <p class="faq-q">How safe is our internal pricing rulebook?</p>
                <p class="faq-a">Extremely safe. Every rule checking engine operates strictly within secure database boundaries and does not expose corporate goals externally.</p>
            </div>
        </div>
    </div>

    <!-- ═══ CTA BANNER ═══ -->
    <div id="launch" class="cta-banner">
        <h2>Secure Your Pricing Infrastructure Today</h2>
        <p>No deployment pipeline setup required. Immediate access.</p>
    </div>

    <!-- ═══ FOOTER ═══ -->
    <div class="landing-footer">
        <div class="footer-brand"><i class="fa-solid fa-bullseye"></i> BargainHunter</div>
        <p class="footer-copy">&copy; 2026 BargainHunter Operations. Standardized B2B Intelligence Infrastructure.</p>
    </div>

    </div>
    """
    st.markdown(landing_html, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Dashboard Styles (Tegas, Kotak, Solid)
# ──────────────────────────────────────────────
dashboard_css = """
<style>
    /* Global Overrides untuk tema tegas */
    .stApp { background-color: var(--background-color) !important; }
    
    /* Box Chat & Hasil Pipeline yang Solid */
    .custom-chat-box {
        background-color: var(--secondary-background-color) !important;
        border: 2px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 6px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }
    
    /* Badge Status Hukum / Korporat */
    .decision-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 8px 16px; border-radius: 4px; font-weight: 800;
        font-size: 13px; border: 2px solid transparent;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .badge-maintain { background: rgba(16,185,129,0.1); color: #10b981; border-color: #10b981; }
    .badge-adjust { background: rgba(245,158,11,0.1); color: #f59e0b; border-color: #f59e0b; }
    .badge-blitz { background: rgba(239,68,68,0.1); color: #ef4444; border-color: #ef4444; }

    /* Pipeline Tracker Node */
    .pipeline-step {
        display: flex; gap: 16px; padding: 20px;
        background: var(--secondary-background-color); border: 2px solid rgba(128, 128, 128, 0.2);
        border-radius: 6px; margin-bottom: 12px;
    }
    .pipeline-step.active { border-color: #3b82f6; background: rgba(59, 130, 246, 0.1); }
    .pipeline-step.completed { border-color: #10b981; }
</style>
"""
st.markdown(dashboard_css, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Page Routing Execution
# ──────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "landing"

if st.session_state["current_page"] == "landing":
    render_landing_page()

    # Center Call-To-Action Button to enter Dashboard
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "👉 Open No-Code Dashboard System",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "dashboard"
            st.rerun()
else:
    # ──────────────────────────────────────────────
    # Chat-style Dashboard (Clean & Highly Structured)
    # ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 16px 0 8px 0;">
                <h2 style="margin:0; font-weight:900; color:var(--text-color); letter-spacing:-0.5px;">
                    <i class="fa-solid fa-bullseye" style="color:#3b82f6;"></i> BargainHunter
                </h2>
                <p style="color:rgba(128, 128, 128, 0.7); font-size:11px; margin-top:4px;
                           letter-spacing:1.5px; text-transform:uppercase; font-weight:700;">
                    B2B Compliance Engine
                </p>
            </div>
            <hr style="border: 1px solid rgba(128, 128, 128, 0.2); margin: 16px 0;">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:8px;
                        padding:10px 14px; border-radius:4px;
                        background:var(--secondary-background-color); border:2px solid rgba(128, 128, 128, 0.2); margin-bottom:20px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#10b981;"></span>
                <span style="font-size:13px;color:rgba(128, 128, 128, 0.8);font-weight:600;">System State: SECURE</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("➕ Create New Audit Tracker", use_container_width=True):
            st.session_state["active_task"] = None
            st.session_state["messages"] = []
            st.rerun()

    # Workspace Header
    st.markdown(
        "<h2 style='font-weight:900; color:var(--text-color); margin-bottom:4px;'>Compliance Pipeline Control</h2>"
        "<p style='color:rgba(128, 128, 128, 0.7); font-size:14px; margin-bottom:24px;'>Input URLs to execute safe data tracking workflows instantly without engineering oversight.</p>",
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Rendering Messages / Results in Box Container Formats
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="custom-chat-box" style="border-left: 4px solid #3b82f6 !important;">'
                f'<small style="color:rgba(128, 128, 128, 0.7); font-weight:800; text-transform:uppercase;">User Input</small>'
                f'<p style="margin:8px 0 0 0; font-weight:500;">{msg["content"]}</p></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="custom-chat-box" style="border-left: 4px solid #10b981 !important;">'
                f'<small style="color:rgba(128, 128, 128, 0.7); font-weight:800; text-transform:uppercase;">Audit Decision Output</small>'
                f'<p style="margin:8px 0 0 0; line-height:1.6;">{msg["content"]}</p></div>',
                unsafe_allow_html=True,
            )

    # Simplified No-Code Form Interface alternative to standard bare text chat
    user_input = st.chat_input(
        "Paste e-commerce target link here to analyze compliance status..."
    )
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Demo Execution Flow Simulating No-Code Processing UI
        compliance_demo_output = f"""
        <div style="margin-bottom: 12px;">
            <span class="decision-badge badge-maintain"><i class="fa-solid fa-shield"></i> MAINTAIN POSITION</span>
        </div>
        <strong>Target Verified:</strong> {user_input[:50]}...<br>
        <strong>Audit Conclusion:</strong> Marketplace prices align completely within your company's safe profile margin limits. No manual engineering correction or structural pricing changes required.
        """
        st.session_state["messages"].append(
            {"role": "assistant", "content": compliance_demo_output}
        )
        st.rerun()