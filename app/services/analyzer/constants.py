"""Constants and configuration for DataFrame analysis."""

from typing import Tuple

# Data type constants
NUMERIC_DTYPES = [
    "int8", "int16", "int32", "int64", 
    "UInt8", "UInt16", "UInt32", "UInt64", 
    "float32", "float64"
]

# Keywords for semantic type inference
DATETIME_KEYWORDS: Tuple[str, ...] = ("date", "time")
CURRENCY_KEYWORDS: Tuple[str, ...] = ("price", "amount", "revenue", "cost", "sales", "salary")
ID_KEYWORDS: Tuple[str, ...] = ("id", "_id")

# Thresholds for analysis
CATEGORICAL_THRESHOLD_RATIO = 0.05
CATEGORICAL_MIN_UNIQUE = 20
MIN_TREND_R2 = 0.2
MIN_TREND_OBSERVATIONS = 5
MAX_TRENDS_TO_RETURN = 5

# File format constants
EXCEL_EXTENSIONS = {".xlsx", ".xls"}
DELIMITED_EXTENSIONS = {".csv", ".tsv"}
PARQUET_EXTENSIONS = {".parquet"}
