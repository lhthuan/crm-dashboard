"""
Configuration file for CRM Dashboard
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "crm_database.duckdb"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)

# Dashboard configuration
DASHBOARD_CONFIG = {
    "theme": "light",
    "page_size": 20,
    "max_rows_display": 1000,
}

# Analytics configuration
ANALYTICS_CONFIG = {
    "vip_threshold": 1000000,
    "premium_threshold": 500000,
    "regular_threshold": 100000,
}

# API Configuration
JOKE_API_URLS = [
    "https://official-joke-api.appspot.com/random_joke",
    "https://jokeapi.dev/random?type=single",
]

# Database configuration
DB_CONFIG = {
    "read_only": False,
    "threads": 4,
    "memory_limit": "2GB",
}
