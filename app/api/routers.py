from fastapi import APIRouter
from app.api.endpoints import cadastral_router


main_router = APIRouter()

main_router.include_router(cadastral_router)
