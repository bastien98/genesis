from fastapi import APIRouter
from ._file import router as file
from ._chat import router as chat

router: APIRouter = APIRouter(prefix="/v2")
router.include_router(file)
router.include_router(chat)

__all__ = ["router"]
