"""
Insights page - Advanced analytics and insights
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DuckDBManager
import config

st.set_page_config(page_title="Insights", page_icon="💡", layout="wide")

st.title("💡 Advanced Insights")
st.markdown("Deep analysis and SQL queries")

# Check if database exists
if config.DB_PATH.exists():
    try:
        db_manager = DuckDBManager(str(config.DB_PATH))
        tables = db_manager.get_table_names()
        
        if not tables:
            st.warning("No data found. Please upload a file from the Overview page.")
        else:
            # Custom SQL query
            st.markdown("### 🔍 Custom SQL Query")
            st.info("Write your own SQL query to analyze the data")
            
            query = st.text_area(
                "Enter SQL Query",
                value="SELECT * FROM orders LIMIT 10",
                height=150
            )
            
            if st.button("Execute Query", key="execute_query"):
                try:
                    result = db_manager.execute_query(query)
                    st.success("Query executed successfully!")
                    st.dataframe(result, use_container_width=True)
                    
                    # Download results
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
            
            # Table statistics
            st.markdown("### 📋 Data Overview")
            for table in tables:
                with st.expander(f"Table: {table}"):
                    info = db_manager.get_table_info(table)
                    st.write(f"**Rows**: {info.get('row_count', 0):,}")
                    st.write(f"**Columns**: {len(info.get('columns', []))}")
                    
                    # Column info
                    columns_df = pd.DataFrame({
                        "Column": info.get('columns', []),
                        "Type": info.get('types', [])
                    })
                    st.dataframe(columns_df, use_container_width=True)
        
        db_manager.close()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("No data loaded yet. Please upload a file from the Overview page.")
