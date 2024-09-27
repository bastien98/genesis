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
        clean_file_location = await file_service.process(file_content, file.filename)
        return {"clean_source": clean_file_location.source, "clean_filename": clean_file_location.filename}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
