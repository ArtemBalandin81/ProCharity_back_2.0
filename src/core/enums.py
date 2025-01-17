from enum import StrEnum


class TelegramNotificationUsersGroups(StrEnum):
    """Класс с доступными категориями пользователей,
    которым будет отправлено сообщение"""

    ALL = "all"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"


class UserRoles(StrEnum):
    """Роли пользователя в системе.

    Значения членов перечисления - строки длиной не более
    src.core.db.models.MAX_USER_ROLE_NAME_LENGTH.
    """

    FUND = "fund"
    VOLUNTEER = "volunteer"
