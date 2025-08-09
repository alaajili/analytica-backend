"""Trend analysis for DataFrames."""

from typing import List, Optional
import pandas as pd
import numpy as np

from .constants import MIN_TREND_OBSERVATIONS, MIN_TREND_R2, MAX_TRENDS_TO_RETURN
from .types import TrendInfo
from .utils import calculate_r_squared, get_trend_direction


class TrendAnalyzer:
    """Handles trend analysis for DataFrame data."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze_trends(self) -> List[TrendInfo]:
        """Analyze trends in numeric columns over time or row index."""
        x_values = self._get_x_axis_values()
        finite_x_mask = np.isfinite(x_values)
        filtered_x = x_values[finite_x_mask]

        if len(filtered_x) < MIN_TREND_OBSERVATIONS:
            return []

        trends = []
        numeric_df = self.df.select_dtypes(include=np.number)

        for column, series in numeric_df.items():
            trend = self._calculate_column_trend(column, series, filtered_x, finite_x_mask)
            if trend:
                trends.append(trend)

        # Sort by trend strength (absolute slope * R²) and return top trends
        trends.sort(key=lambda t: abs(t["slope"]) * t["r2"], reverse=True)
        return trends[:MAX_TRENDS_TO_RETURN]

    def _get_x_axis_values(self) -> np.ndarray:
        """Get X-axis values for trend analysis (datetime or row index)."""
        datetime_columns = [
            col for col in self.df.columns 
            if pd.api.types.is_datetime64_any_dtype(self.df[col])
        ]

        if datetime_columns:
            # Use first datetime column converted to epoch nanoseconds
            datetime_series = pd.to_datetime(self.df[datetime_columns[0]], errors="coerce")
            return datetime_series.astype("int64").astype("float64").to_numpy()
        else:
            # Use row index
            return pd.Series(range(len(self.df)), dtype="int64", index=self.df.index).astype("float64").to_numpy()

    def _calculate_column_trend(
        self, 
        column: str, 
        series: pd.Series, 
        x_values: np.ndarray, 
        x_mask: np.ndarray
    ) -> Optional[TrendInfo]:
        """Calculate trend statistics for a single numeric column."""
        y_values = series.astype("float64").to_numpy()
        valid_mask = x_mask & np.isfinite(y_values)

        if valid_mask.sum() < MIN_TREND_OBSERVATIONS:
            return None

        # Get valid data points
        valid_x = x_values[:valid_mask.sum()]
        valid_y = y_values[valid_mask]

        # Calculate linear regression
        slope, intercept = np.polyfit(valid_x, valid_y, 1)
        predicted_y = slope * valid_x + intercept

        # Calculate R-squared
        r_squared = calculate_r_squared(valid_y, predicted_y)

        # Check if trend is meaningful
        if self._is_meaningful_trend(slope, r_squared, valid_y):
            return {
                "column": column,
                "slope": float(slope),
                "r2": float(r_squared),
                "direction": get_trend_direction(slope)
            }

        return None

    def _is_meaningful_trend(self, slope: float, r_squared: float, y_values: np.ndarray) -> bool:
        """Determine if a trend is statistically meaningful."""
        has_significant_slope = abs(slope) > 1e-12
        has_good_fit = r_squared >= MIN_TREND_R2
        has_variance = np.nanpercentile(y_values, 75) - np.nanpercentile(y_values, 25) > 0

        return has_significant_slope and has_good_fit and has_variance
