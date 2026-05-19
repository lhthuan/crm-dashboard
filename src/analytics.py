"""
Analytics module for CRM data analysis
"""

import pandas as pd
import logging
from typing import Dict, Any, List
from src.database import DuckDBManager

logger = logging.getLogger(__name__)


class CRMAnalytics:
    """Perform analytics on CRM data"""
    
    def __init__(self, db_manager: DuckDBManager):
        """
        Initialize analytics
        
        Args:
            db_manager: DuckDBManager instance
        """
        self.db = db_manager
    
    def get_customer_metrics(self, customers_table: str = "customers") -> Dict[str, Any]:
        """Get customer metrics"""
        try:
            metrics = {}
            
            # Total customers
            total = self.db.execute_query(f"SELECT COUNT(*) as count FROM {customers_table}").iloc[0, 0]
            metrics['total_customers'] = int(total) if total else 0
            
            # Active customers (if status column exists)
            try:
                active = self.db.execute_query(
                    f"SELECT COUNT(*) as count FROM {customers_table} WHERE status = 'Active' OR status = 'active'"
                ).iloc[0, 0]
                metrics['active_customers'] = int(active) if active else 0
            except:
                metrics['active_customers'] = 0
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting customer metrics: {str(e)}")
            return {}
    
    def get_revenue_metrics(self, orders_table: str = "orders", amount_column: str = "amount") -> Dict[str, Any]:
        """Get revenue metrics"""
        try:
            metrics = {}
            
            # Total revenue
            query = f"SELECT SUM({amount_column}) as total_revenue FROM {orders_table}"
            result = self.db.execute_query(query)
            metrics['total_revenue'] = float(result.iloc[0, 0]) if result.iloc[0, 0] else 0
            
            # Average order value
            query = f"SELECT AVG({amount_column}) as avg_value FROM {orders_table}"
            result = self.db.execute_query(query)
            metrics['avg_order_value'] = float(result.iloc[0, 0]) if result.iloc[0, 0] else 0
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting revenue metrics: {str(e)}")
            return {}
    
    def get_sales_by_period(self, orders_table: str = "orders", 
                           date_column: str = "order_date", 
                           amount_column: str = "amount",
                           period: str = "month") -> pd.DataFrame:
        """Get sales by time period"""
        try:
            if period == "month":
                query = f"""
                    SELECT 
                        DATE_TRUNC('month', {date_column})::date as period,
                        SUM({amount_column}) as total_sales,
                        COUNT(*) as order_count
                    FROM {orders_table}
                    GROUP BY DATE_TRUNC('month', {date_column})
                    ORDER BY period
                """
            elif period == "day":
                query = f"""
                    SELECT 
                        {date_column} as period,
                        SUM({amount_column}) as total_sales,
                        COUNT(*) as order_count
                    FROM {orders_table}
                    GROUP BY {date_column}
                    ORDER BY period
                """
            else:
                raise ValueError(f"Unknown period: {period}")
            
            return self.db.execute_query(query)
        except Exception as e:
            logger.error(f"Error getting sales by period: {str(e)}")
            return pd.DataFrame()
    
    def get_top_customers(self, orders_table: str = "orders", 
                         customer_column: str = "customer_id",
                         amount_column: str = "amount",
                         limit: int = 10) -> pd.DataFrame:
        """Get top customers by revenue"""
        try:
            query = f"""
                SELECT 
                    {customer_column} as customer,
                    SUM({amount_column}) as total_spent,
                    COUNT(*) as order_count
                FROM {orders_table}
                GROUP BY {customer_column}
                ORDER BY total_spent DESC
                LIMIT {limit}
            """
            return self.db.execute_query(query)
        except Exception as e:
            logger.error(f"Error getting top customers: {str(e)}")
            return pd.DataFrame()
    
    def get_customer_segmentation(self, orders_table: str = "orders",
                                 customer_column: str = "customer_id",
                                 amount_column: str = "amount") -> pd.DataFrame:
        """Segment customers by spending"""
        try:
            query = f"""
                WITH customer_summary AS (
                    SELECT 
                        {customer_column} as customer,
                        SUM({amount_column}) as total_spent,
                        COUNT(*) as order_count,
                        AVG({amount_column}) as avg_order_value
                    FROM {orders_table}
                    GROUP BY {customer_column}
                )
                SELECT 
                    customer,
                    total_spent,
                    order_count,
                    avg_order_value,
                    CASE 
                        WHEN total_spent >= 10000000 THEN 'VIP'
                        WHEN total_spent >= 5000000 THEN 'Premium'
                        WHEN total_spent >= 1000000 THEN 'Regular'
                        ELSE 'Bronze'
                    END as segment
                FROM customer_summary
                ORDER BY total_spent DESC
            """
            return self.db.execute_query(query)
        except Exception as e:
            logger.error(f"Error getting customer segmentation: {str(e)}")
            return pd.DataFrame()
    
    def get_summary_stats(self, table_name: str) -> Dict[str, Any]:
        """Get summary statistics for table"""
        try:
            info = self.db.get_table_info(table_name)
            return {
                "table_name": table_name,
                "columns": info.get("columns", []),
                "types": info.get("types", []),
                "row_count": info.get("row_count", 0)
            }
        except Exception as e:
            logger.error(f"Error getting summary stats: {str(e)}")
            return {}
