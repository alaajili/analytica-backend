"""Semantic type inference for DataFrame columns."""

from typing import Optional
import pandas as pd

from .constants import DATETIME_KEYWORDS, CATEGORICAL_THRESHOLD_RATIO, CATEGORICAL_MIN_UNIQUE
from .utils import try_datetime_conversion, infer_numeric_semantic_type


class SemanticTypeInferencer:
    """Handles semantic type inference for DataFrame columns."""

    def infer_semantic_dtype(self, series: pd.Series) -> Optional[str]:
        """Infer the semantic data type of a pandas Series."""
        column_name = (series.name or "").lower()
        
        # Check pandas-detected datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        
        # Check if name suggests datetime and try conversion
        if self._is_potential_datetime_column(column_name, series):
            return "datetime"
        
        # Check for boolean data
        if pd.api.types.is_bool_dtype(series):
            return "boolean"
        
        # Check for numeric data with special semantics
        if pd.api.types.is_numeric_dtype(series):
            return infer_numeric_semantic_type(column_name)
        
        # Check for categorical vs text based on uniqueness
        return self._infer_categorical_or_text(series)

    def _is_potential_datetime_column(self, column_name: str, series: pd.Series) -> bool:
        """Check if column could be datetime based on name and convertibility."""
        if any(keyword in column_name for keyword in DATETIME_KEYWORDS):
            return try_datetime_conversion(series)
        return False

    def _infer_categorical_or_text(self, series: pd.Series) -> str:
        """Determine if a non-numeric series should be treated as categorical or text."""
        unique_count = series.nunique(dropna=True)
        threshold = max(CATEGORICAL_MIN_UNIQUE, len(series) * CATEGORICAL_THRESHOLD_RATIO)
        return "categorical" if unique_count < threshold else "text"
