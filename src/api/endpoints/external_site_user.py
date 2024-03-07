from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.auth import check_header_contains_token
from src.api.schemas import ExternalSiteUserRequest
from src.api.services import ExternalSiteUserService
from src.bot.services.user import UserService
from src.core.depends import Container

site_user_router = APIRouter(dependencies=[Depends(check_header_contains_token)])


@site_user_router.post("/external_user_registration", description="Актуализирует пользователя с сайта ProCharity.")
@inject
async def external_user_registration(
    site_user: ExternalSiteUserRequest,
    site_user_service: ExternalSiteUserService = Depends(Provide[Container.api_services_container.site_user_service]),
    user_service: UserService = Depends(Provide[Container.bot_services_container.bot_user_service]),
) -> None:
    await site_user_service.register(site_user)
    user = await user_service.get_by_user_id(site_user.user_id)
    if user:
        await user_service.set_categories_to_user(site_user.user_id, site_user.specializations)
