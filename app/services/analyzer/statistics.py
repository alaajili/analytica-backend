"""Statistical analysis for DataFrames."""

from typing import Dict
import pandas as pd
import numpy as np

from .types import NumericStatistics, CorrelationMatrix


class StatisticalAnalyzer:
    """Handles statistical analysis of DataFrame data."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_missing_values(self) -> Dict[str, int]:
        """Calculate missing values count for each column."""
        return self.df.isna().sum().astype(int).to_dict()

    def get_numeric_statistics(self) -> Dict[str, NumericStatistics]:
        """Calculate comprehensive statistics for numeric columns."""
        numeric_df = self.df.select_dtypes(include=np.number)
        if numeric_df.empty:
            return {}

        quantiles = numeric_df.quantile([0.25, 0.5, 0.75])
        descriptions = numeric_df.describe().T

        stats = {}
        for column, row in descriptions.iterrows():
            count = int(row["count"])
            stats[column] = {
                "count": count,
                "mean": float(row["mean"]) if count > 0 else None,
                "std": float(row["std"]) if count > 1 else 0.0,
                "min": float(row["min"]) if count > 0 else None,
                "p25": float(quantiles.loc[0.25, column]) if count > 0 else None,
                "median": float(quantiles.loc[0.5, column]) if count > 0 else None,
                "p75": float(quantiles.loc[0.75, column]) if count > 0 else None,
                "max": float(row["max"]) if count > 0 else None,
            }

        return stats

    def get_correlations(self, max_columns: int) -> CorrelationMatrix:
        """Calculate Pearson correlations for numeric columns with highest variance."""
        numeric_df = self.df.select_dtypes(include=np.number)
        if numeric_df.empty:
            return {}

        # Select columns with highest variance
        variance_sorted = numeric_df.var().sort_values(ascending=False)
        selected_columns = variance_sorted.index[:max_columns]

        # Calculate correlation matrix
        correlation_matrix = numeric_df[selected_columns].corr(method="pearson").fillna(0.0)

        # Convert to nested dictionary format
        return {
            row: {col: float(correlation_matrix.loc[row, col]) for col in correlation_matrix.columns}
            for row in correlation_matrix.index
        }

    def find_strongest_correlation(self, correlations: CorrelationMatrix) -> tuple | None:
        """Find the strongest correlation pair (excluding self-correlations)."""
        strongest = None
        max_abs_correlation = 0.0

        for row_col, row_data in correlations.items():
            for col_col, correlation_value in row_data.items():
                if row_col == col_col:  # Skip self-correlation
                    continue

                abs_correlation = abs(correlation_value)
                if abs_correlation > max_abs_correlation:
                    max_abs_correlation = abs_correlation
                    strongest = (row_col, col_col, correlation_value)

        return strongest
