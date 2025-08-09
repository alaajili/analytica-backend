from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import analyze
from .utils.errors import install_exception_handlers

app = FastAPI(title="Analytica API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

install_exception_handlers(app)
app.include_router(analyze.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
