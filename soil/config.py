"""
Project configuration for the soil data module.
"""

from pathlib import Path


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA = PROJECT_DIR / "data" / "processed"
CACHE = PROJECT_DIR / "data" / "cache"


# Create directories if they do not already exist
RAW_DATA.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
CACHE.mkdir(parents=True, exist_ok=True)


# ============================================================
# SOILGRIDS API
# ============================================================

SOILGRIDS_URL = (
    "https://rest.isric.org/soilgrids/v2.0/properties/query"
)


# ============================================================
# SOIL PROPERTIES
# ============================================================

SOIL_PROPERTIES = [
    "bdod",       # Bulk density
    "cec",        # Cation exchange capacity
    "clay",       # Clay content
    "nitrogen",   # Total nitrogen
    "phh2o",      # Soil pH
    "sand",       # Sand content
    "silt",       # Silt content
    "soc"         # Soil organic carbon
]