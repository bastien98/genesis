from fastapi import APIRouter
from ._file import router as file
from ._chat import router as chat
from ._list_knowledgebases import router as list_kb

router: APIRouter = APIRouter(prefix="/v2")
router.include_router(file)
router.include_router(chat)
router.include_router(list_kb)

__all__ = ["router"]
