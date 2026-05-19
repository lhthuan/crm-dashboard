"""
CRM Dashboard Source Package
"""

from .data_loader import DataLoader
from .database import DuckDBManager
from .analytics import CRMAnalytics

__all__ = [
    'DataLoader',
    'DuckDBManager',
    'CRMAnalytics',
]
