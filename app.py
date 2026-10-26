import streamlit as st
import os
from pipeline import handle_customer_issue
from db import setup_database, get_company_details, log_query, get_stats
from vector_store import build_vector_db
from escalation_card import show_escalation_card

# 1. Ensure databases are ready
setup_database()
if not os.path.exists("vector_db.json"):
    build_vector_db()

# 2. Page setup
st.set_page_config(page_title="A.I.R.S. Support", page_icon="🤖", layout="centered")

# 3. Left Sidebar: Company Selector
st.sidebar.title("🏢 Select Company")
selected_company = st.sidebar.selectbox(
    "Choose a company:",
    ["Amazon", "Swiggy", "Flipkart"]
)

if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 4. Left Sidebar: Live Database Analytics
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Live System Analytics")
stats = get_stats()
col_a, col_b, col_c = st.sidebar.columns(3)
col_a.metric("Total", stats["total"])
col_b.metric("AI Fixed", stats["resolved"])
col_c.metric("Escalated", stats["escalated"])

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **How A.I.R.S. works:**\n"
    "1. Searches official company FAQs.\n"
    "2. Gives instant step-by-step fixes.\n"
    "3. Escalates to verified human contacts if unresolved."
)

# 5. Main Header
st.title("🤖 A.I.R.S.")
st.caption(f"AI-Powered Issue Resolution & Escalation System — Currently helping with **{selected_company}**")

# 6. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "escalation":
            show_escalation_card(msg["company"], msg["contacts"], msg["query"])
        else:
            st.markdown(msg["content"])

# 7. Chat Input Box with Crash Protection
user_query = st.chat_input(f"Describe your issue with {selected_company}...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing issue and checking company policies..."):
            try:
                result = handle_customer_issue(selected_company, user_query)
            except Exception:
                # If internet drops or API fails, safely fallback to human escalation!
                result = {
                    "status": "ESCALATED",
                    "contacts": get_company_details(selected_company)
                }

        # Save this interaction in our SQLite database
        log_query(selected_company, user_query, result["status"])

        if result["status"] == "RESOLVED":
            reply = f"✅ **Step-by-Step Solution ({selected_company}):**\n\n{result['solution']}"
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

    # Refresh sidebar numbers immediately
    st.rerun()