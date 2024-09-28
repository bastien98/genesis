from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from file_api.core.services.file_service import FileStorageService
from file_api.dependencies import get_file_service

router = APIRouter()


@router.post("/upload")
async def upload(
        file: UploadFile = File(...),
        file_service: FileStorageService = Depends(get_file_service)
):
    try:
        file_content = await file.read()
        chunks = await file_service.process(file_content, file.filename)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
