from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ..schemas.analyze import AnalyzeResponse
from ..services.analyzer import analyze_dataframe, load_dataframe_from_upload
from ..config import settings

router = APIRouter(prefix="/v1/analyze", tags=["analyze"])

_ALLOWED_EXT = {".csv", ".tsv", ".xlsx", ".xls", ".parquet"}
_ALLOWED_CT = {"text/csv","text/tab-separated-values","application/vnd.ms-excel",
               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
               "application/octet-stream","application/x-parquet","application/parquet"}

@router.post("/upload", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_upload(file: UploadFile = File(...)):
    ext = (file.filename or "").lower().rpartition(".")[2]
    ext = f".{ext}" if ext else ""
    if ext not in _ALLOWED_EXT or (file.content_type and file.content_type not in _ALLOWED_CT):
        raise HTTPException(status_code=415, detail="Unsupported file type.")

    raw = await file.read()
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.max_upload_bytes} bytes.")

    try:
        df = load_dataframe_from_upload(file.filename or "upload", raw, use_pyarrow=settings.use_pyarrow)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {e}")

    try:
        return analyze_dataframe(
            df,
            max_preview_rows=settings.max_preview_rows,
            max_corr_cols=settings.max_numeric_cols_for_corr,
            filename=file.filename,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
