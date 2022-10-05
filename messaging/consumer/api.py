from dataclasses import dataclass
from typing import Any

from nameko.events import event_handler


class RegisteredUserEventError(Exception):
    pass


@dataclass
class RegisteredUserEvent:
    user_id: int
    username: str
    event_name: str = "registered_user"


def handle_registered_user_event(event: dict[str, Any]):
    print(event)
    if not event.get("user_id") or not event.get("username"):
        raise RegisteredUserEventError
    return RegisteredUserEvent(user_id=event["user_id"], username=event["username"])


class AnalyticsService:
    """Event listening service."""

    name = "analytics_service"

    @event_handler("registration_service", "registered_user")
    def handle_registered_user(self, payload: dict[str, Any]):
        handle_registered_user_event(payload)
