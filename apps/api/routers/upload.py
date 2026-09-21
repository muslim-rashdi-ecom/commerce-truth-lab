from fastapi import APIRouter, UploadFile, File, HTTPException
from services.upload_service import process_upload
from schemas.responses import UploadResponse

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    contents = await file.read()
    return await process_upload(file.filename, contents)
