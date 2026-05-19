"""
Customers page - Customer analysis and segmentation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DuckDBManager
from src.analytics import CRMAnalytics
import config

st.set_page_config(page_title="Customers", page_icon="👥", layout="wide")

st.title("👥 Customer Analysis")
st.markdown("Analyze customer data and segments")

# Check if database exists
if config.DB_PATH.exists():
    try:
        db_manager = DuckDBManager(str(config.DB_PATH))
        tables = db_manager.get_table_names()
        
        if "customers" not in tables and "orders" not in tables:
            st.warning("No customer or order data found. Please upload a file from the Overview page.")
        else:
            analytics = CRMAnalytics(db_manager)
            
            # Customer overview
            if "customers" in tables:
                st.markdown("### 📊 Customer Overview")
                info = db_manager.get_table_info("customers")
                st.metric("Total Customers", info.get('row_count', 0))
                
                # Display customer data
                st.markdown("### 📋 Customer List")
                try:
                    customers = db_manager.execute_query("SELECT * FROM customers LIMIT 100")
                    st.dataframe(customers, use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading customers: {str(e)}")
            
            # Customer segmentation
            if "orders" in tables:
                st.markdown("### 🎯 Customer Segmentation")
                try:
                    segmentation = analytics.get_customer_segmentation("orders")
                    if not segmentation.empty:
                        # Segment distribution
                        segment_counts = segmentation['segment'].value_counts()
                        fig = px.pie(
                            segment_counts,
                            values=segment_counts.values,
                            names=segment_counts.index,
                            title="Customer Segments Distribution"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Segmentation table
                        st.dataframe(segmentation.head(20), use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating segmentation: {str(e)}")
        
        db_manager.close()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("No data loaded yet. Please upload a file from the Overview page.")
