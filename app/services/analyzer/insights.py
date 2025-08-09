"""Insight generation for DataFrame analysis."""

from typing import List, Optional
import pandas as pd

from .statistics import StatisticalAnalyzer
from .trends import TrendAnalyzer
from .types import MetadataInfo


class InsightGenerator:
    """Generates human-readable insights about datasets."""

    def __init__(self, df: pd.DataFrame, filename: str = ""):
        self.df = df
        self.filename = filename
        self.stats_analyzer = StatisticalAnalyzer(df)
        self.trend_analyzer = TrendAnalyzer(df)

    def generate_insights(self) -> List[str]:
        """Generate human-readable insights about the dataset."""
        insights = []
        meta = self._get_metadata()

        # Basic dataset info
        insights.append(f"Loaded {meta['rows']} rows × {meta['cols']} columns.")

        # Variability insight
        variability_insight = self._get_variability_insight()
        if variability_insight:
            insights.append(variability_insight)

        # Trend insight
        trend_insight = self._get_trend_insight()
        if trend_insight:
            insights.append(trend_insight)

        # Correlation insight
        correlation_insight = self._get_correlation_insight()
        if correlation_insight:
            insights.append(correlation_insight)

        return insights

    def _get_metadata(self) -> MetadataInfo:
        """Extract basic metadata about the DataFrame."""
        return {
            "filename": self.filename,
            "rows": int(len(self.df)),
            "cols": int(self.df.shape[1])
        }

    def _get_variability_insight(self) -> Optional[str]:
        """Generate insight about the column with highest variability."""
        numeric_stats = self.stats_analyzer.get_numeric_statistics()
        if not numeric_stats:
            return None

        # Find column with highest variance
        highest_variance_col = None
        highest_variance = 0.0

        for column, stats in numeric_stats.items():
            if stats["count"] and stats["count"] > 1:
                variance = (stats["std"] or 0.0) ** 2
                if variance > highest_variance:
                    highest_variance = variance
                    highest_variance_col = column

        if highest_variance_col:
            return f"High variability in '{highest_variance_col}'."

        return None

    def _get_trend_insight(self) -> Optional[str]:
        """Generate insight about the strongest trend."""
        trends = self.trend_analyzer.analyze_trends()
        if not trends:
            return None

        strongest_trend = trends[0]
        direction = "Increasing" if strongest_trend["direction"] == "up" else "Decreasing"
        return f"{direction} trend in '{strongest_trend['column']}' (R²={strongest_trend['r2']:.2f})."

    def _get_correlation_insight(self) -> Optional[str]:
        """Generate insight about the strongest correlation."""
        correlations = self.stats_analyzer.get_correlations(max_columns=10)
        if not correlations:
            return None

        strongest_correlation = self.stats_analyzer.find_strongest_correlation(correlations)
        if not strongest_correlation:
            return None

        col1, col2, correlation_value = strongest_correlation
        return f"Strongest Pearson correlation: {col1} ↔ {col2} (ρ={correlation_value:.2f})."
