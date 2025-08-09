from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    allowed_origins: List[str] = []
    max_upload_bytes: int = 25 * 1024 * 1024
    max_preview_rows: int = 20
    max_numeric_cols_for_corr: int = 12
    use_pyarrow: bool = True

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

settings = Settings()
