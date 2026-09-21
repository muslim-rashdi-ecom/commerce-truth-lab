import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from security import get_current_user, verify_workspace_access
from schemas.workspace_schemas import StageUploadResponse, CommitUploadResponse
from services.merchant_upload_service import stage_csv_upload, commit_csv_import

router = APIRouter(prefix="/api/workspaces/{workspace_id}/upload", tags=["Merchant Upload"])

@router.post("/stage", response_model=StageUploadResponse)
async def stage_upload(
    workspace_id: str,
    source_type: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Stage a CSV file, analyze headers, preview data with masked PII, and generate mapping suggestions."""
    await verify_workspace_access(workspace_id, user, db)
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    contents = await file.read()
    try:
        res = await stage_csv_upload(workspace_id, source_type, file.filename, contents, db)
        return StageUploadResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/commit", response_model=CommitUploadResponse)
async def commit_upload(
    workspace_id: str,
    upload_id: str = Form(...),
    mappings: str = Form(...),  # JSON-encoded dictionary
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Commit verified and mapped CSV records into the merchant workspace database."""
    await verify_workspace_access(workspace_id, user, db)
    
    try:
        confirmed_mappings = json.loads(mappings)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON column mapping dictionary")
        
    contents = await file.read()
    try:
        res = await commit_csv_import(
            workspace_id=workspace_id,
            upload_id=upload_id,
            contents=contents,
            confirmed_mappings=confirmed_mappings,
            user_id=user.id,
            db=db
        )
        return CommitUploadResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
