"""Type definitions for DataFrame analysis."""

from typing import Dict, List, Any, Optional, Union
from typing_extensions import TypedDict

# Type aliases
AnalysisResult = Dict[str, Any]
ColumnStats = Dict[str, Union[int, float, None]]
CorrelationMatrix = Dict[str, Dict[str, float]]


class ColumnInfo(TypedDict):
    """Information about a DataFrame column."""
    name: str
    dtype: str
    inferred_semantic: Optional[str]


class TrendInfo(TypedDict):
    """Information about a trend in data."""
    column: str
    slope: float
    r2: float
    direction: Optional[str]


class MetadataInfo(TypedDict):
    """Basic metadata about a DataFrame."""
    filename: str
    rows: int
    cols: int


class NumericStatistics(TypedDict):
    """Statistical information for numeric columns."""
    count: int
    mean: Optional[float]
    std: float
    min: Optional[float]
    p25: Optional[float]
    median: Optional[float]
    p75: Optional[float]
    max: Optional[float]


class AnalysisResults(TypedDict):
    """Complete analysis results for a DataFrame."""
    meta: MetadataInfo
    columns: List[ColumnInfo]
    preview: List[Dict[str, Any]]
    missing: Dict[str, int]
    numeric_stats: Dict[str, NumericStatistics]
    correlations: CorrelationMatrix
    trends: List[TrendInfo]
    insights: List[str]
