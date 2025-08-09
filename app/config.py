from pydantic import BaseModel
import os

class Settings(BaseModel):
    allowed_origins: list[str] = []

def get_settings() -> Settings:
    origins = os.getenv("ALLOWED_ORIGINS", "")
    allowed = [o.strip() for o in origins.split(",") if o.strip()]
    return Settings(allowed_origins=allowed)

settings = get_settings()
