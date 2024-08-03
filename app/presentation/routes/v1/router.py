from fastapi import APIRouter

from app.presentation.routes.v1.account import router as account_router
from app.presentation.routes.v1.auth import router as auth_router


v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(account_router)
v1_router.include_router(auth_router)
