from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from file_api.core.domain.ex_document import ExDocument
from file_api.core.services.file_service import FileService
from file_api.dependencies import get_file_service

router = APIRouter()


async def ex_document_mapper(file: UploadFile) -> ExDocument:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF.")

    return ExDocument(file.filename, await file.read())


@router.post("/upload")
async def upload(
        file: UploadFile = File(...),
        file_service: FileService = Depends(get_file_service)
):
    try:
        document = await ex_document_mapper(file)
        name = await file_service.save_ex_document(document)
        return {"file_name": name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
