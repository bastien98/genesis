from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api.core.services.file_service import FileStorageService
from file_api.core.services.kb_service import KBService
from file_api.dependencies import get_file_service, get_kb_service

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        file: UploadFile = File(...),
        kb_id: str = Query(..., description="Knowledge Base ID"),
        file_service: FileStorageService = Depends(get_file_service),
        kb_service: KBService = Depends(get_kb_service),
):
    try:
        filename = file.filename
        file_content = await file.read()
        md_chunks, text_chunks  = await file_service.process(file_content, filename, kb_id)
        await kb_service.update(filename, md_chunks, text_chunks, kb_id)
        return {"message": "File uploaded and processed successfully.", "filename": file.filename}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
