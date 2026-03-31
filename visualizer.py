import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLORS = ["#5B8FF9", "#5AD8A6", "#F6BD16", "#E86452", "#6DC8EC", "#945FB9"]

def detect_chart_type(df: pd.DataFrame, question: str) -> str:
    """Heuristic to pick the best chart type based on data shape and question."""
    q = question.lower()
    cols = list(df.columns)
    n_rows = len(df)

    # Time series keywords
    time_keywords = ["month", "year", "trend", "over time", "quarterly", "weekly", "daily"]
    if any(k in q for k in time_keywords):
        return "line"

    # Comparison / ranking keywords
    rank_keywords = ["top", "best", "worst", "compare", "vs", "versus", "rank", "highest", "lowest"]
    if any(k in q for k in rank_keywords):
        return "bar"

    # Distribution keywords
    dist_keywords = ["distribution", "breakdown", "share", "proportion", "percentage", "split"]
    if any(k in q for k in dist_keywords):
        return "pie" if n_rows <= 8 else "bar"

    # Shape-based fallback
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    if len(numeric_cols) >= 2 and len(text_cols) == 0:
        return "scatter"
    if len(text_cols) >= 1 and len(numeric_cols) >= 1:
        return "bar" if n_rows > 8 else "bar"

    return "table"

def render_chart(df: pd.DataFrame, question: str):
    """Return a Plotly figure based on df content and the original question."""
    if df.empty:
        return None

    chart_type = detect_chart_type(df, question)
    cols = list(df.columns)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    # Identify x and y
    x_col = text_cols[0] if text_cols else cols[0]
    y_col = numeric_cols[0] if numeric_cols else cols[-1]

    # If date-like column exists, sort by it
    date_col = next((c for c in cols if "date" in c.lower() or "month" in c.lower() or "year" in c.lower()), None)
    if date_col:
        df = df.sort_values(date_col)
        x_col = date_col

    try:
        if chart_type == "line":
            if len(numeric_cols) > 1:
                fig = px.line(df, x=x_col, y=numeric_cols,
                              color_discrete_sequence=COLORS,
                              markers=True)
            else:
                fig = px.line(df, x=x_col, y=y_col,
                              color_discrete_sequence=COLORS,
                              markers=True)

        elif chart_type == "bar":
            color_col = text_cols[1] if len(text_cols) > 1 else None
            fig = px.bar(df, x=x_col, y=y_col,
                         color=color_col,
                         color_discrete_sequence=COLORS,
                         text_auto=".2s")
            fig.update_traces(textposition="outside")

        elif chart_type == "pie":
            fig = px.pie(df, names=x_col, values=y_col,
                         color_discrete_sequence=COLORS,
                         hole=0.35)

        elif chart_type == "scatter":
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                             color_discrete_sequence=COLORS,
                             trendline="ols" if len(df) > 5 else None)
        else:
            return None

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Inter, sans-serif", size=13),
            margin=dict(l=40, r=20, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")

        return fig

    except Exception:
        return None
