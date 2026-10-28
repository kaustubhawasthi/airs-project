import streamlit as st
import os
from pipeline import handle_customer_issue
from db import setup_database, get_company_details, log_query, get_stats, get_recent_logs
from vector_store import build_vector_db
from escalation_card import show_escalation_card

# 1. Initialize databases
setup_database()
if not os.path.exists("vector_db.json"):
    build_vector_db()

# 2. Page Configuration & Custom Styling
st.set_page_config(page_title="A.I.R.S. Support Hub", page_icon="🛡️", layout="wide")

# Custom CSS for a modern, sleek appearance
st.markdown("""
<style>
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
    .badge {
        background-color: #1e293b;
        color: #38bdf8;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
st.sidebar.markdown("## 🏢 Control Center")

ALL_COMPANIES = [
    "Amazon", "Flipkart", "Swiggy", "Zomato",
    "Uber", "Ola", "Paytm", "PhonePe", "Netflix", "Jio"
]
selected_company = st.sidebar.selectbox("🎯 Target Company / App:", ALL_COMPANIES)

# Multi-Language Selector
LANGUAGES = [
    "English",
    "Hindi (हिंदी)",
    "Hinglish (Hindi in English Script)",
    "Marathi (मराठी)",
    "Tamil (தமிழ்)",
    "Bengali (বাংলা)",
    "Telugu (తెలుగు)"
]
selected_language = st.sidebar.selectbox("🌐 Response Language:", LANGUAGES)

if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Live Analytics Display
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live System Analytics")
stats = get_stats()
col1, col2, col3 = st.sidebar.columns(3)
col1.metric("Total", stats["total"])
col2.metric("AI Fixed", stats["resolved"])
col3.metric("Escalated", stats["escalated"])

# Developer Credits in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background-color: #0f172a; padding: 14px; border-radius: 10px; border: 1px solid #1e293b;">
    <p style="margin: 0; color: #38bdf8; font-weight: 700; font-size: 0.95rem;">👨‍💻 Project Developer</p>
    <p style="margin: 2px 0 0 0; color: #f8fafc; font-size: 1.05rem; font-weight: 600;">Kaustubh Awasthi</p>
    <p style="margin: 0; color: #94a3b8; font-size: 0.8rem;">B.Tech 2nd Year • Solo Project</p>
    <span class="badge" style="margin-top: 6px; display: inline-block;">A.I.R.S. v2.0 Pro</span>
</div>
""", unsafe_allow_html=True)

# 4. Main Page Header
st.markdown('<p class="hero-title">🛡️ A.I.R.S. Intelligence Hub</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="hero-subtitle">Automated Issue Resolution & Verified Human Escalation Gateway for <b>{selected_company}</b> '
    f'<span class="badge">Language: {selected_language}</span></p>',
    unsafe_allow_html=True
)

# 5. Top Navigation Tabs
tab_chat, tab_logs, tab_about = st.tabs(["💬 AI Resolution Desk", "📋 Live Database Logs", "👨‍💻 About Developer & Architecture"])

# --- TAB 1: Chat Interface ---
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Suggested Prompts (shown when chat is empty)
    SAMPLE_QUESTIONS = {
        "Amazon": ["How do I return an item?", "When will my refund arrive?", "My parcel was stolen!"],
        "Flipkart": ["Where can I track my order?", "Replace damaged electronics", "Delivery box had a stone inside!"],
        "Swiggy": ["Can I cancel my order in 60s?", "Why is my coupon not applying?", "Driver never arrived!"],
        "Zomato": ["What are Zomato Gold benefits?", "Cancel food order", "Spilled food inside bag!"],
        "Uber": ["What is the ride cancellation fee?", "Forgot item in cab", "Driver demanded extra cash!"],
        "Ola": ["How long for Ola Money refund?", "Download ride invoice", "Driver took wrong route!"],
        "Paytm": ["Pending UPI payment refund time", "How to reset UPI PIN?", "Account got unauthorized charge!"],
        "PhonePe": ["Failed transaction refund time", "Check bank balance", "UPI money deducted twice!"],
        "Netflix": ["How to cancel subscription?", "Update household device limit", "Account hacked!"],
        "Jio": ["Check daily data balance", "How to activate eSIM?", "Sim card blocked without reason!"]
    }

    if len(st.session_state.messages) == 0:
        st.markdown("##### ⚡ Quick Suggested Inquiries:")
        cols = st.columns(3)
        prompts = SAMPLE_QUESTIONS.get(selected_company, ["How to cancel?", "Refund policy?", "Help with issue"])
        for idx, col in enumerate(cols):
            if idx < len(prompts):
                if col.button(f"👉 {prompts[idx]}", key=f"quick_{idx}", use_container_width=True):
                    st.session_state.auto_query = prompts[idx]
                    st.rerun()

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "escalation":
                show_escalation_card(msg["company"], msg["contacts"], msg["query"])
            else:
                st.markdown(msg["content"])

    # Chat Input Box
    user_query = st.chat_input(f"Type your complaint or query for {selected_company} in any language...")

    # Handle auto-submitted quick prompt
    if "auto_query" in st.session_state:
        user_query = st.session_state.pop("auto_query")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner(f"Searching {selected_company} knowledge in {selected_language}..."):
                try:
                    result = handle_customer_issue(selected_company, user_query, language=selected_language)
                except Exception:
                    result = {
                        "status": "ESCALATED",
                        "contacts": get_company_details(selected_company)
                    }

            log_query(selected_company, user_query, result["status"])

            if result["status"] == "RESOLVED":
                reply = f"✅ **Step-by-Step Resolution ({selected_company}):**\n\n{result['solution']}"
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                show_escalation_card(selected_company, result["contacts"], user_query)
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "escalation",
                    "company": selected_company,
                    "contacts": result["contacts"],
                    "query": user_query
                })
        st.rerun()

# --- TAB 2: Live Database Logs ---
with tab_logs:
    st.markdown("### 📋 Real-Time SQLite Query Audit Logs")
    st.caption("Demonstrating persistent SQLite storage: every customer question is recorded automatically.")
    # NEW:
    logs = get_recent_logs(limit=15)
    if logs:
        import pandas as pd

        df = pd.DataFrame(logs, columns=["Timestamp", "Company", "Customer Query", "Resolution Status"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No queries recorded yet. Ask a question in the chat tab to see it log here live!")

# --- TAB 3: About Developer & Architecture ---
with tab_about:
    st.markdown("""
    ### 👨‍💻 Project Developer Profile
    - **Developer:** **Kaustubh Awasthi**
    - **Project Title:** A.I.R.S. (AI-Powered Issue Resolution & Escalation System)
    - **Engineering Domain:** Generative AI • Agentic AI • Full-Stack Development
    """)