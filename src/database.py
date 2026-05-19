"""
DuckDB database module for CRM data
"""

import duckdb
import pandas as pd
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class DuckDBManager:
    """Manage DuckDB database connections and operations"""
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize DuckDB manager
        
        Args:
            db_path: Path to database file (default: in-memory)
        """
        self.db_path = db_path
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Create connection to DuckDB"""
        try:
            self.conn = duckdb.connect(self.db_path)
            logger.info(f"Connected to DuckDB: {self.db_path}")
        except Exception as e:
            logger.error(f"Error connecting to DuckDB: {str(e)}")
            raise
    
    def create_table_from_dataframe(self, table_name: str, df: pd.DataFrame) -> bool:
        """
        Create table from DataFrame
        
        Args:
            table_name: Name of the table to create
            df: Pandas DataFrame
            
        Returns:
            True if successful
        """
        try:
            self.conn.register(table_name, df)
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}")
            logger.info(f"Created table: {table_name} ({len(df)} rows)")
            return True
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {str(e)}")
            return False
    
    def create_table_from_csv(self, table_name: str, csv_path: str) -> bool:
        """
        Create table from CSV file
        
        Args:
            table_name: Name of the table
            csv_path: Path to CSV file
            
        Returns:
            True if successful
        """
        try:
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')")
            logger.info(f"Created table from CSV: {table_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating table from CSV: {str(e)}")
            return False
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            Results as DataFrame
        """
        try:
            result = self.conn.execute(query).fetch_df()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def get_table_names(self) -> List[str]:
        """Get list of all tables in database"""
        try:
            result = self.conn.execute("SELECT table_name FROM information_schema.tables").fetch_all()
            return [row[0] for row in result]
        except Exception as e:
            logger.error(f"Error getting table names: {str(e)}")
            return []
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        return table_name in self.get_table_names()
    
    def drop_table(self, table_name: str) -> bool:
        """Drop table from database"""
        try:
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            logger.info(f"Dropped table: {table_name}")
            return True
        except Exception as e:
            logger.error(f"Error dropping table: {str(e)}")
            return False
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about table"""
        try:
            info = self.conn.execute(f"DESCRIBE {table_name}").fetch_all()
            return {
                "columns": [row[0] for row in info],
                "types": [row[1] for row in info],
                "row_count": self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetch_all()[0][0]
            }
        except Exception as e:
            logger.error(f"Error getting table info: {str(e)}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
