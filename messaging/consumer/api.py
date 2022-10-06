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


def handle_registered_user_event(
    serialized_event: dict[str, Any]
) -> RegisteredUserEvent:
    if not serialized_event.get("user_id") or not serialized_event.get("username"):
        raise RegisteredUserEventError
    event = RegisteredUserEvent(
        user_id=serialized_event["user_id"], username=serialized_event["username"]
    )
    # do something interesting here
    return event


class AnalyticsService:
    """Event listening service."""

    name = "analytics_service"

    @event_handler("registration_service", "registered_user")
    def handle_registered_user(self, payload: dict[str, Any]):
        handle_registered_user_event(payload)
