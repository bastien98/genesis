from fastapi import APIRouter
from ._kb import router as kb
from ._chat import router as chat

router: APIRouter = APIRouter(prefix="/v2")
router.include_router(kb)
router.include_router(chat)

__all__ = ["router"]
