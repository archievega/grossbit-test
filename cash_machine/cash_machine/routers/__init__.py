from fastapi import APIRouter

from .items import router as items_router
from .cash_machine import router as cash_machine_router
from .media import router as media_router

router = APIRouter()
router.include_router(items_router)
router.include_router(cash_machine_router)
router.include_router(media_router)
