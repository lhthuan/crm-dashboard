"""
Sales page - Sales analysis and trends
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DuckDBManager
from src.analytics import CRMAnalytics
import config

st.set_page_config(page_title="Sales", page_icon="💰", layout="wide")

st.title("💰 Sales Analysis")
st.markdown("Sales trends and revenue analysis")

# Check if database exists
if config.DB_PATH.exists():
    try:
        db_manager = DuckDBManager(str(config.DB_PATH))
        tables = db_manager.get_table_names()
        
        if "orders" not in tables:
            st.warning("No order data found. Please upload a file from the Overview page.")
        else:
            analytics = CRMAnalytics(db_manager)
            
            # Revenue metrics
            st.markdown("### 📊 Revenue Metrics")
            revenue_metrics = analytics.get_revenue_metrics("orders")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Revenue", f"${revenue_metrics.get('total_revenue', 0):,.0f}")
            with col2:
                st.metric("Avg Order Value", f"${revenue_metrics.get('avg_order_value', 0):,.0f}")
            
            # Sales trend - Daily
            st.markdown("### 📈 Daily Sales Trend")
            try:
                daily_sales = analytics.get_sales_by_period("orders", period="day")
                if not daily_sales.empty and len(daily_sales) > 0:
                    fig = px.line(
                        daily_sales,
                        x="period",
                        y="total_sales",
                        markers=True,
                        title="Daily Sales"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate daily sales trend: {str(e)}")
            
            # Sales trend - Monthly
            st.markdown("### 📊 Monthly Sales Trend")
            try:
                monthly_sales = analytics.get_sales_by_period("orders", period="month")
                if not monthly_sales.empty and len(monthly_sales) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig1 = px.bar(
                            monthly_sales,
                            x="period",
                            y="total_sales",
                            title="Monthly Revenue"
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = px.bar(
                            monthly_sales,
                            x="period",
                            y="order_count",
                            title="Monthly Order Count"
                        )
                        st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate monthly sales trend: {str(e)}")
            
            # Top customers
            st.markdown("### ⭐ Top Customers")
            try:
                top_customers = analytics.get_top_customers("orders", limit=20)
                if not top_customers.empty:
                    fig = px.bar(
                        top_customers,
                        x="customer",
                        y="total_spent",
                        title="Top 20 Customers by Revenue"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate top customers: {str(e)}")
        
        db_manager.close()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("No data loaded yet. Please upload a file from the Overview page.")
