"""Utility functions for DataFrame analysis."""

import os
from typing import Optional
import pandas as pd
import numpy as np

from .constants import DATETIME_KEYWORDS, ID_KEYWORDS, CURRENCY_KEYWORDS


def get_file_extension(filename: str) -> str:
    """Extract and normalize file extension from filename."""
    return os.path.splitext(filename or "")[1].lower()


def is_datetime_column_name(column_name: str) -> bool:
    """Check if column name suggests datetime content."""
    if not isinstance(column_name, str):
        return False
    name_lower = column_name.lower()
    return name_lower.endswith(DATETIME_KEYWORDS)


def try_datetime_conversion(series: pd.Series) -> bool:
    """Attempt to convert series to datetime and return success status."""
    try:
        pd.to_datetime(series, errors="raise")
        return True
    except Exception:
        return False


def infer_numeric_semantic_type(column_name: str) -> str:
    """Infer semantic type for numeric columns based on column name."""
    if any(keyword in column_name for keyword in ID_KEYWORDS):
        return "identifier"
    if any(keyword in column_name for keyword in CURRENCY_KEYWORDS):
        return "currency_like"
    return "numeric"


def calculate_r_squared(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Calculate R-squared value for regression quality."""
    residual_sum_squares = float(np.sum((actual - predicted) ** 2))
    total_sum_squares = float(np.sum((actual - np.mean(actual)) ** 2))
    
    if total_sum_squares == 0:
        return 0.0
    
    return 1.0 - (residual_sum_squares / total_sum_squares)


def get_trend_direction(slope: float) -> Optional[str]:
    """Determine trend direction from slope."""
    if slope > 0:
        return "up"
    elif slope < 0:
        return "down"
    return None


def preprocess_datetime_columns(df: pd.DataFrame) -> None:
    """Convert columns with datetime-like names to datetime dtype in-place."""
    for col in df.columns:
        if is_datetime_column_name(col):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass  # Silently continue if conversion fails
