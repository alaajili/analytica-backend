from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ColumnInfo(BaseModel):
    name: str
    dtype: str
    inferred_semantic: Optional[str] = None

class NumericStats(BaseModel):
    count: int
    mean: float | None
    std: float | None
    min: float | None
    p25: float | None
    median: float | None
    p75: float | None
    max: float | None

class TrendInfo(BaseModel):
    column: str
    slope: float
    r2: float
    direction: Optional[str]

class AnalyzeResponse(BaseModel):
    meta: Dict[str, Any]
    columns: List[ColumnInfo]
    preview: List[Dict[str, Any]] = Field(default_factory=list)
    missing: Dict[str, int]
    numeric_stats: Dict[str, NumericStats]
    correlations: Dict[str, Dict[str, float]]
    trends: List[TrendInfo]
    insights: List[str]
