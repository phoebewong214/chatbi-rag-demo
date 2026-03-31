import os
import streamlit as st
import pandas as pd

from nl2sql import generate_sql_and_run
from visualizer import render_chart
from data.create_db import create_sample_database

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatBI — Natural Language Analytics",
    page_icon="💬",
    layout="wide",
)

# ── DB setup ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_bi.db")
if not os.path.exists(DB_PATH):
    create_sample_database()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔑 API Key")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get a free key at https://aistudio.google.com/app/apikey",
    )
    st.caption("[Get a free Gemini API key →](https://aistudio.google.com/app/apikey)")

    st.markdown("---")
    st.markdown("## 📊 Database tables")
    st.markdown("""
| Table | Description |
|---|---|
| `sales` | Revenue & profit by region, product, channel |
| `users` | Subscription plans, MRR, churn |
| `marketing` | Campaign spend, leads, conversions, CAC |
""")

    st.markdown("---")
    st.markdown("## 💡 Try asking")
    example_questions = [
        "What are the top 5 products by total revenue?",
        "Show monthly revenue trend for 2024",
        "Which region has the highest profit margin?",
        "Compare CAC across marketing channels",
        "How many users churned vs stayed active?",
        "What is the MRR breakdown by subscription plan?",
        "Show revenue vs cost by product",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True, key=q):
            st.session_state["question_input"] = q

# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown("# 💬 ChatBI")
st.markdown("Ask your business data anything in plain English — powered by Gemini + SQLite.")
st.markdown("---")

# Question input
question = st.text_input(
    "Your question",
    placeholder="e.g. What is the monthly revenue trend for the North region?",
    key="question_input",
    label_visibility="collapsed",
)

run_btn = st.button("Ask →", type="primary", disabled=not api_key)

if not api_key:
    st.info("👈 Enter your Gemini API key in the sidebar to get started. It's free!", icon="🔑")

# ── Query execution ───────────────────────────────────────────────────────────
if run_btn and question and api_key:
    with st.spinner("Thinking..."):
        try:
            sql, df = generate_sql_and_run(question, api_key, DB_PATH)

            # Results
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("#### 📈 Visualization")
                fig = render_chart(df, question)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No chart generated — showing raw data below.")

            with col2:
                st.markdown("#### 🔢 Data")
                st.dataframe(df, use_container_width=True, height=300)
                st.caption(f"{len(df)} rows returned")

            # SQL expander
            with st.expander("🧠 Generated SQL", expanded=False):
                st.code(sql, language="sql")

        except ValueError as e:
            st.error(f"Query error: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.caption("Check your API key and try again.")

# ── Query history ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state["history"] = []

if run_btn and question and api_key:
    st.session_state["history"].insert(0, question)
    st.session_state["history"] = st.session_state["history"][:5]

if st.session_state.get("history"):
    st.markdown("---")
    st.markdown("#### 🕒 Recent queries")
    for past_q in st.session_state["history"]:
        st.caption(f"• {past_q}")
