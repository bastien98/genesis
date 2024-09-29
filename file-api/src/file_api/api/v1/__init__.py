from fastapi import APIRouter
from ._file import router as file


router: APIRouter = APIRouter(prefix="/v1")
router.include_router(file)

__all__ = ["router"]