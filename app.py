import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Dashboard")
st.caption("Data served by FastAPI · Visualized with Streamlit")


def fetch(endpoint):
    """Call the FastAPI backend and return JSON data."""
    try:
        response = requests.get(f"{API}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the FastAPI backend. Make sure it's running on port 8000.")
        st.stop()


# ── KPI Cards ────────────────────────────────────────────────────────────────
summary = fetch("/summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",    f"${summary['total_revenue']:,.2f}")
col2.metric("Total Orders",     summary["total_orders"])
col3.metric("Avg Order Value",  f"${summary['avg_order_value']:,.2f}")
col4.metric("Top Category",     summary["top_category"])

st.divider()

# ── Row 1: Revenue Over Time + Category Breakdown ────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Revenue Over Time")
    time_data = fetch("/sales-over-time")
    df_time = pd.DataFrame(time_data)
    df_time["date"] = pd.to_datetime(df_time["date"])
    df_time = df_time.set_index("date")
    st.line_chart(df_time["revenue"])

with right:
    st.subheader("Revenue by Category")
    cat_data = fetch("/sales-by-category")
    df_cat = pd.DataFrame(cat_data).set_index("category")
    st.bar_chart(df_cat["total_revenue"])

st.divider()

# ── Row 2: Top Products Table ─────────────────────────────────────────────────
st.subheader("Top Products")
limit = st.slider("Number of products to show", min_value=3, max_value=20, value=5)
top_data = fetch(f"/top-products?limit={limit}")
df_top = pd.DataFrame(top_data)
df_top.index += 1  # rank starts at 1
df_top.columns = ["Product", "Total Revenue ($)"]
st.dataframe(df_top, use_container_width=True)
