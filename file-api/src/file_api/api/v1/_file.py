from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from file_api.core.services.file_service import FileService
from file_api.dependencies import get_file_service

router = APIRouter()


@router.post("/upload")
async def upload(
        file: UploadFile = File(...),
        file_service: FileService = Depends(get_file_service)
):
    try:
        file_path = await file_service.save_file(file, file.filename)
        return {"file_path": file_path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
