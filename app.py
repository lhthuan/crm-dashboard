"""
Main Streamlit application - CRM Dashboard
"""

import streamlit as st
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="CRM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/static/img/streamlit_black.svg", width=100)
st.sidebar.title("CRM Dashboard")
st.sidebar.markdown("---")

# Main content
st.title("📊 CRM Data Analysis Dashboard")
st.markdown("""
    Welcome to the CRM Dashboard! This application helps you analyze customer relationship management data
    using DuckDB and interactive visualizations.
""")

# Overview section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Customers", value="Loading...", delta=None)

with col2:
    st.metric(label="Total Revenue", value="Loading...", delta=None)

with col3:
    st.metric(label="Avg Order Value", value="Loading...", delta=None)

with col4:
    st.metric(label="Conversion Rate", value="Loading...", delta=None)

st.markdown("---")

# How to use section
with st.expander("📖 How to Use This Dashboard", expanded=False):
    st.markdown("""
        ### Getting Started
        
        1. **Upload Data**: Place your Excel XLSB files in the `data/` folder
        2. **Navigate**: Use the sidebar menu to access different analysis pages
        3. **Explore**: View charts, metrics, and detailed insights
        
        ### Available Pages
        
        - **Overview**: Dashboard with key metrics and KPIs
        - **Customers**: Customer analysis and segmentation
        - **Sales**: Sales trends and revenue analysis
        - **Insights**: Advanced analytics and predictions
        
        ### Data Requirements
        
        Your Excel file should contain these sheets:
        - `customers`: Customer information
        - `orders`: Order/transaction data
        - `products`: Product information (optional)
        
        ### Expected Columns
        
        **Customers Sheet**:
        - customer_id, name, email, phone, country, city
        
        **Orders Sheet**:
        - order_id, customer_id, order_date, amount, status
    """)

st.markdown("---")

# Footer
st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 2rem;'>
        <p>CRM Dashboard v1.0.0 | Powered by Streamlit + DuckDB</p>
    </div>
""", unsafe_allow_html=True)
