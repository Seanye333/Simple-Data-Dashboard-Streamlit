from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

app = FastAPI(title="Sales Dashboard API")

# Allow Streamlit (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load our sample data once at startup
df = pd.read_csv("data/sales.csv")
df["date"] = pd.to_datetime(df["date"])


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Sales Dashboard API is running"}


@app.get("/summary")
def get_summary():
    """Returns high-level KPIs"""
    return {
        "total_revenue": round(df["revenue"].sum(), 2),
        "total_orders": len(df),
        "avg_order_value": round(df["revenue"].mean(), 2),
        "top_category": df.groupby("category")["revenue"].sum().idxmax(),
    }


@app.get("/sales-by-category")
def sales_by_category():
    """Returns revenue grouped by product category"""
    result = (
        df.groupby("category")["revenue"]
        .sum()
        .round(2)
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
    )
    return result.to_dict(orient="records")


@app.get("/sales-over-time")
def sales_over_time():
    """Returns daily revenue over time"""
    result = (
        df.groupby("date")["revenue"]
        .sum()
        .round(2)
        .reset_index()
    )
    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    return result.to_dict(orient="records")


@app.get("/top-products")
def top_products(limit: int = 5):
    """Returns top N products by revenue"""
    result = (
        df.groupby("product")["revenue"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
    )
    return result.to_dict(orient="records")
