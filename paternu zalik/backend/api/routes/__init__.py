from fastapi import APIRouter
from backend.api.routes.movies import movies_router

router = APIRouter()
router.include_router(movies_router, prefix="/movies", tags=["movies"])
