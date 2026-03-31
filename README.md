# ChatBI — Natural Language Analytics Demo

> Ask your business data anything in plain English. Get SQL. Get charts. No code required.

**Live Demo →** https://chatbi-demo.streamlit.app

---

## The problem this solves

At NetEase, I saw non-technical analysts spending 40% of their time reformulating the same queries — either waiting for engineering bandwidth or wrestling with SQL they half-understood. The questions were simple; the bottleneck was the interface.

This demo replicates the core of the NL→SQL→Visualization pipeline I led in production, where we reduced user re-queries by **17%** and increased prompt accuracy by **23%**.

---

## How it works

```
User question (plain English)
        │
        ▼
  Gemini 2.0 Flash          ← schema-aware system prompt
        │
        ▼
   SQL query
        │
        ▼
   SQLite execution
        │
        ▼
  Auto chart detection      ← heuristic based on data shape + question intent
        │
        ▼
  Plotly visualization
```

**Key design decisions:**

- **Schema injection in system prompt** — the LLM sees full table definitions, so it doesn't hallucinate column names
- **Read-only safety guard** — blocks any write operations (DROP, DELETE, INSERT, UPDATE)
- **Heuristic chart picker** — detects time-series, ranking, distribution, and correlation patterns from question keywords + data shape
- **Stateless architecture** — no vector DB needed; context fits in a single prompt

---

## Database

Three mock enterprise tables (24 months of synthetic data):

| Table | Rows | Description |
|---|---|---|
| `sales` | 480 | Revenue, profit, units by region / product / channel |
| `users` | 500 | Subscription plans, MRR, churn rate |
| `marketing` | 288 | Campaign spend, leads, conversions, CAC |

---

## Run locally

```bash
# 1. Clone
git clone https://github.com/phoebewong214/chatbi-rag-demo.git 
cd chatbi-rag-demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free Gemini API key
# → https://aistudio.google.com/app/apikey

# 4. Run
streamlit run app.py
```

Enter your API key in the sidebar — no `.env` file needed.

---

## Example questions to try

- *"What are the top 5 products by total revenue?"*
- *"Show monthly revenue trend for 2024"*
- *"Which region has the highest profit margin?"*
- *"Compare customer acquisition cost across marketing channels"*
- *"What is the MRR breakdown by subscription plan?"*

---

## Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-free_tier-4285F4?style=flat&logo=google&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=flat&logo=plotly&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-embedded-003B57?style=flat&logo=sqlite&logoColor=white)
![chatbi-rag-demo](https://github.com/phoebewong214/chatbi-rag-demo)
---

## Author

**Phoebe (Tszching) Wang** — PM with AI & data background  
Northwestern MSIS '26 · Previously @ NetEase · Xiaohongshu · NielsenIQ  
[LinkedIn](https://www.linkedin.com/in/phoebewang003214) · [Portfolio](#)
