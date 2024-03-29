from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.auth import check_header_contains_token
from src.api.schemas import TaskResponse, TasksRequest
from src.api.services import TaskService
from src.api.services.messages import TelegramNotificationService
from src.core.db.models import Task
from src.core.depends import Container
from src.core.utils import display_task

task_router = APIRouter(dependencies=[Depends(check_header_contains_token)])


@task_router.post("", description="Актуализирует список задач.")
@inject
async def actualize_tasks(
    tasks: TasksRequest,
    task_service: TaskService = Depends(Provide[Container.api_services_container.task_service]),
    telegram_notification_service: TelegramNotificationService = Depends(
        Provide[Container.api_services_container.message_service]
    ),
    bonus_info_url: str = Depends(Provide[Container.settings.provided.procharity_bonus_info_url]),
) -> None:
    new_tasks_ids = await task_service.actualize_objects(tasks.root, Task)
    new_category_tasks = await task_service.get_user_tasks_ids(new_tasks_ids)
    for task in new_category_tasks:
        message = display_task(task, bonus_info_url)
        await telegram_notification_service.send_messages_to_subscribed_users(message, task.category_id)


@task_router.get(
    "/{user_id}",
    response_model=list[TaskResponse],
    response_model_exclude_none=True,
    description="Получает список всех задач из категорий на которые подписан юзер.",
)
@inject
async def get_tasks_for_user(
    user_id: int,
    task_service: TaskService = Depends(Provide[Container.api_services_container.task_service]),
) -> list[TaskResponse]:
    return await task_service.get_tasks_for_user(user_id)


@task_router.get(
    "",
    response_model=list[TaskResponse],
    response_model_exclude_none=True,
    description="Получает список всех задач.",
)
@inject
async def get_all_tasks(
    task_service: TaskService = Depends(Provide[Container.api_services_container.task_service]),
) -> list[TaskResponse]:
    return await task_service.get_all()
