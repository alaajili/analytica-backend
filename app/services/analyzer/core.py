"""Core DataFrame analyzer implementation."""

from typing import List, Dict, Any, Optional
import pandas as pd

from .types import AnalysisResults, ColumnInfo, MetadataInfo
from .semantic_inference import SemanticTypeInferencer
from .statistics import StatisticalAnalyzer
from .trends import TrendAnalyzer
from .insights import InsightGenerator
from .utils import preprocess_datetime_columns


class DataFrameAnalyzer:
    """Analyzes pandas DataFrames to extract insights, statistics, and metadata."""

    def __init__(self, df: pd.DataFrame, filename: Optional[str] = None):
        self.df = df.copy()  # Work with a copy to avoid modifying original
        self.filename = filename or ""
        
        # Initialize specialized analyzers
        self.semantic_inferencer = SemanticTypeInferencer()
        self.stats_analyzer = StatisticalAnalyzer(self.df)
        self.trend_analyzer = TrendAnalyzer(self.df)
        self.insight_generator = InsightGenerator(self.df, self.filename)
        
        # Preprocess the data
        self._preprocess_data()

    def _preprocess_data(self) -> None:
        """Preprocess the DataFrame for analysis."""
        preprocess_datetime_columns(self.df)

    def analyze(self, max_preview_rows: int, max_corr_cols: int) -> AnalysisResults:
        """Perform complete analysis of the DataFrame."""
        return {
            "meta": self._get_metadata(),
            "columns": self._analyze_columns(),
            "preview": self._get_preview(max_preview_rows),
            "missing": self.stats_analyzer.get_missing_values(),
            "numeric_stats": self.stats_analyzer.get_numeric_statistics(),
            "correlations": self.stats_analyzer.get_correlations(max_corr_cols),
            "trends": self.trend_analyzer.analyze_trends(),
            "insights": self.insight_generator.generate_insights()
        }

    def _get_metadata(self) -> MetadataInfo:
        """Extract basic metadata about the DataFrame."""
        return {
            "filename": self.filename,
            "rows": int(len(self.df)),
            "cols": int(self.df.shape[1])
        }

    def _analyze_columns(self) -> List[ColumnInfo]:
        """Analyze each column's data type and semantic meaning."""
        return [
            {
                "name": col,
                "dtype": str(self.df[col].dtype),
                "inferred_semantic": self.semantic_inferencer.infer_semantic_dtype(self.df[col])
            }
            for col in self.df.columns
        ]

    def _get_preview(self, max_rows: int) -> List[Dict[str, Any]]:
        """Get a preview of the first few rows as a list of dictionaries."""
        return self.df.head(max_rows).to_dict("records")
