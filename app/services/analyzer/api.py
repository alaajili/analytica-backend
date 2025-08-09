"""Public API functions for DataFrame analysis (backward compatibility)."""

from typing import Optional
import pandas as pd

from .core import DataFrameAnalyzer
from .loader import DataFrameLoader
from .types import AnalysisResults


def analyze_dataframe(
    df: pd.DataFrame, 
    *, 
    max_preview_rows: int, 
    max_corr_cols: int, 
    filename: Optional[str] = None
) -> AnalysisResults:
    """
    Analyze a DataFrame and return comprehensive statistics and insights.
    
    Args:
        df: The pandas DataFrame to analyze
        max_preview_rows: Maximum number of rows to include in preview
        max_corr_cols: Maximum number of columns to include in correlation analysis
        filename: Optional filename for metadata
    
    Returns:
        Dictionary containing analysis results including metadata, statistics, and insights
    """
    analyzer = DataFrameAnalyzer(df, filename)
    return analyzer.analyze(max_preview_rows, max_corr_cols)


def load_dataframe_from_upload(filename: str, raw: bytes, use_pyarrow: bool = True) -> pd.DataFrame:
    """
    Load a DataFrame from uploaded file bytes.
    
    Args:
        filename: Name of the uploaded file
        raw: Raw bytes of the file content
        use_pyarrow: Whether to use pyarrow backend for pandas (requires pandas >= 2.0)
    
    Returns:
        Loaded pandas DataFrame
    
    Raises:
        Exception: If file cannot be parsed or format is unsupported
    """
    loader = DataFrameLoader()
    return loader.load_from_upload(filename, raw, use_pyarrow)
