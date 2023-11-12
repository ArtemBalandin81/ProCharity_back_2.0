from fastapi import APIRouter
from src.authentication import auth_backend, fastapi_users

admin_user_router = APIRouter()


admin_user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix='/auth', tags=['AdminUser']
)
