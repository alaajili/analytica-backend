"""
Data analysis service for pandas DataFrames.

This package provides comprehensive DataFrame analysis capabilities including:
- Loading from various file formats
- Statistical analysis and insights generation
- Trend analysis and correlations
- Data type inference and preprocessing
"""

from .core import DataFrameAnalyzer
from .loader import DataFrameLoader
from .api import analyze_dataframe, load_dataframe_from_upload

__all__ = [
    "DataFrameAnalyzer",
    "DataFrameLoader", 
    "analyze_dataframe",
    "load_dataframe_from_upload"
]
