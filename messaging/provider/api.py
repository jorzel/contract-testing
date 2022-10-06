import random
from dataclasses import asdict, dataclass

from nameko.events import EventDispatcher


@dataclass
class RegisteredUserEvent:
    user_id: int
    username: str
    event_name: str = "registered_user"
    test: int = 1

    def as_dict(self):
        return asdict(self)


class RegistrationService:
    """Event publishing service."""

    name = "registration_service"

    dispatcher = EventDispatcher()

    def register_user(self, username: str) -> None:
        # create user here
        user_id = random.randint(1, 100000)
        event = RegisteredUserEvent(user_id=user_id, username=username)
        self.dispatcher(event.event_name, event.as_dict())
