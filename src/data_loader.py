"""
Data loader module for reading Excel files
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and process data from Excel files"""
    
    def __init__(self, file_path: str):
        """
        Initialize data loader
        
        Args:
            file_path: Path to Excel file (XLSB or XLSX)
        """
        self.file_path = Path(file_path)
        self.file_type = self.file_path.suffix.lower()
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if self.file_type not in ['.xlsb', '.xlsx']:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        logger.info(f"Initialized DataLoader for: {self.file_path}")
    
    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Load all sheets from Excel file
        
        Returns:
            Dictionary with sheet names as keys and DataFrames as values
        """
        try:
            if self.file_type == '.xlsb':
                return self._load_xlsb()
            else:
                return self._load_xlsx()
        except Exception as e:
            logger.error(f"Error loading sheets: {str(e)}")
            raise
    
    def _load_xlsb(self) -> Dict[str, pd.DataFrame]:
        """Load XLSB file"""
        try:
            import pyxlsb
            
            sheets = {}
            with pyxlsb.open_workbook(str(self.file_path)) as wb:
                for sheet in wb.sheets:
                    logger.info(f"Loading sheet: {sheet.name}")
                    with wb.get_sheet(sheet.name) as ws:
                        data = []
                        for row in ws.rows:
                            data.append([cell.value for cell in row])
                        
                        if data:
                            df = pd.DataFrame(data[1:], columns=data[0])
                            sheets[sheet.name] = df
                            logger.info(f"Loaded {len(df)} rows from {sheet.name}")
            
            return sheets
        except Exception as e:
            logger.error(f"Error loading XLSB: {str(e)}")
            raise
    
    def _load_xlsx(self) -> Dict[str, pd.DataFrame]:
        """Load XLSX file"""
        try:
            xls = pd.ExcelFile(str(self.file_path))
            sheets = {}
            
            for sheet_name in xls.sheet_names:
                logger.info(f"Loading sheet: {sheet_name}")
                df = pd.read_excel(str(self.file_path), sheet_name=sheet_name)
                sheets[sheet_name] = df
                logger.info(f"Loaded {len(df)} rows from {sheet_name}")
            
            return sheets
        except Exception as e:
            logger.error(f"Error loading XLSX: {str(e)}")
            raise
    
    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        """
        Load specific sheet
        
        Args:
            sheet_name: Name of sheet to load
            
        Returns:
            DataFrame
        """
        try:
            sheets = self.load_all_sheets()
            if sheet_name not in sheets:
                raise ValueError(f"Sheet '{sheet_name}' not found")
            
            return sheets[sheet_name]
        except Exception as e:
            logger.error(f"Error loading sheet {sheet_name}: {str(e)}")
            raise
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Remove empty rows and columns
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Convert column names to lowercase with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        return df
    
    @staticmethod
    def infer_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Infer and convert data types
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with inferred types
        """
        for col in df.columns:
            # Try to convert to numeric
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                # Try to convert to datetime
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    # Keep as string
                    pass
        
        return df
