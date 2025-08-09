from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled(_: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        return JSONResponse(status_code=500, content={"detail": "Internal server error."})
