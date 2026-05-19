"""
Overview page - Main dashboard with KPIs
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.database import DuckDBManager
from src.analytics import CRMAnalytics
import config

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Dashboard Overview")
st.markdown("Key metrics and performance indicators")

# Sidebar - Data loading
st.sidebar.markdown("### 📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload Excel file (XLSB/XLSX)", type=['xlsb', 'xlsx'])

if uploaded_file is not None:
    try:
        # Save uploaded file
        data_path = config.DATA_DIR / uploaded_file.name
        with open(data_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Load data
        loader = DataLoader(str(data_path))
        sheets = loader.load_all_sheets()
        
        st.sidebar.markdown(f"**Sheets found**: {len(sheets)}")
        for sheet_name in sheets.keys():
            st.sidebar.text(f"  • {sheet_name}")
        
        # Initialize database
        db_manager = DuckDBManager(str(config.DB_PATH))
        
        # Load sheets into database
        for sheet_name, df in sheets.items():
            df = loader.clean_dataframe(df)
            table_name = sheet_name.lower().replace(' ', '_')
            db_manager.create_table_from_dataframe(table_name, df)
        
        # Get analytics
        analytics = CRMAnalytics(db_manager)
        tables = db_manager.get_table_names()
        
        # Display KPI metrics
        st.markdown("### 📈 Key Metrics")
        
        # Create columns for metrics
        metrics_data = {}
        
        try:
            if "customers" in tables:
                customer_metrics = analytics.get_customer_metrics("customers")
                metrics_data.update(customer_metrics)
        except Exception as e:
            st.warning(f"Could not load customer metrics: {str(e)}")
        
        try:
            if "orders" in tables:
                revenue_metrics = analytics.get_revenue_metrics("orders")
                metrics_data.update(revenue_metrics)
        except Exception as e:
            st.warning(f"Could not load revenue metrics: {str(e)}")
        
        # Display metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Customers",
                f"{metrics_data.get('total_customers', 0):,}",
                delta=None
            )
        
        with col2:
            total_revenue = metrics_data.get('total_revenue', 0)
            st.metric(
                "Total Revenue",
                f"${total_revenue:,.0f}",
                delta=None
            )
        
        with col3:
            avg_value = metrics_data.get('avg_order_value', 0)
            st.metric(
                "Avg Order Value",
                f"${avg_value:,.0f}",
                delta=None
            )
        
        with col4:
            active = metrics_data.get('active_customers', 0)
            total = metrics_data.get('total_customers', 1)
            rate = (active / total * 100) if total > 0 else 0
            st.metric(
                "Active Customers",
                f"{active:,}",
                f"{rate:.1f}%"
            )
        
        st.markdown("---")
        
        # Sales trend
        if "orders" in tables:
            st.markdown("### 📈 Sales Trend")
            try:
                sales_data = analytics.get_sales_by_period("orders", period="month")
                if not sales_data.empty:
                    fig = px.line(
                        sales_data,
                        x="period",
                        y="total_sales",
                        markers=True,
                        title="Monthly Sales Trend"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not generate sales trend: {str(e)}")
        
        # Top customers
        if "orders" in tables:
            st.markdown("### ⭐ Top Customers")
            try:
                top_customers = analytics.get_top_customers("orders", limit=10)
                if not top_customers.empty:
                    fig = px.bar(
                        top_customers,
                        x="customer",
                        y="total_spent",
                        title="Top 10 Customers by Revenue"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(top_customers, use_container_width=True)
            except Exception as e:
                st.error(f"Could not generate top customers: {str(e)}")
        
        # Table info
        st.markdown("### 📋 Loaded Tables")
        for table in tables:
            info = db_manager.get_table_info(table)
            st.write(f"**{table}**: {info.get('row_count', 0)} rows, {len(info.get('columns', []))} columns")
        
        db_manager.close()
        
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
else:
    st.info("👈 Please upload an Excel file to get started!")
    
    st.markdown("""
        ### How to use:
        1. Click on the file uploader in the sidebar
        2. Select your Excel XLSB or XLSX file
        3. The data will be loaded into DuckDB
        4. Dashboard metrics will appear automatically
    """)
