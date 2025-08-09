"""DataFrame loading from various file formats."""

import io
from typing import Dict, Any
import pandas as pd

from .constants import EXCEL_EXTENSIONS, DELIMITED_EXTENSIONS, PARQUET_EXTENSIONS
from .utils import get_file_extension


class DataFrameLoader:
    """Handles loading DataFrames from various file formats."""

    def load_from_upload(self, filename: str, raw_bytes: bytes, use_pyarrow: bool = True) -> pd.DataFrame:
        """Load DataFrame from uploaded file bytes."""
        file_extension = get_file_extension(filename)
        buffer = io.BytesIO(raw_bytes)

        if file_extension in EXCEL_EXTENSIONS:
            return self._load_excel_file(buffer)

        if file_extension in PARQUET_EXTENSIONS:
            return self._load_parquet_file(buffer)

        if file_extension in DELIMITED_EXTENSIONS:
            return self._load_delimited_file(buffer, file_extension, use_pyarrow)

        raise ValueError(f"Unsupported file extension: {file_extension}")

    def _load_excel_file(self, buffer: io.BytesIO) -> pd.DataFrame:
        """Load Excel file (.xlsx, .xls)."""
        return pd.read_excel(buffer)

    def _load_parquet_file(self, buffer: io.BytesIO) -> pd.DataFrame:
        """Load Parquet file."""
        return pd.read_parquet(buffer)

    def _load_delimited_file(self, buffer: io.BytesIO, extension: str, use_pyarrow: bool) -> pd.DataFrame:
        """Load CSV or TSV file with appropriate separator."""
        read_kwargs: Dict[str, Any] = {"low_memory": False}

        if use_pyarrow:
            read_kwargs["dtype_backend"] = "pyarrow"  # Requires pandas >= 2.0

        separator = "\t" if extension == ".tsv" else ","
        return pd.read_csv(buffer, sep=separator, **read_kwargs)
