import os
import re
import sqlite3
import requests
import pandas as pd

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def nl_to_sql(question: str, api_key: str) -> str:
    """Convert natural language question to SQL using Gemini."""
    system_prompt = load_system_prompt()

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{system_prompt}\n\nQuestion: {question}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 512,
        }
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={api_key}",
        json=payload,
        timeout=15
    )

    if response.status_code != 200:
        raise ValueError(f"Gemini API error {response.status_code}: {response.text}")

    result = response.json()
    sql = result["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Clean up any accidental markdown fences
    sql = re.sub(r"```sql|```", "", sql).strip()
    return sql

def run_query(sql: str, db_path: str) -> pd.DataFrame:
    """Execute SQL and return results as DataFrame."""
    # Safety check — block write operations
    forbidden = ["drop", "delete", "insert", "update", "alter", "create"]
    if any(word in sql.lower() for word in forbidden):
        raise ValueError("Write operations are not allowed.")

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df

def generate_sql_and_run(question: str, api_key: str, db_path: str):
    """Full pipeline: NL → SQL → DataFrame."""
    sql = nl_to_sql(question, api_key)
    df = run_query(sql, db_path)
    return sql, df
