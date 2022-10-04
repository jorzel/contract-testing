from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class User:
    name: str


class UserClient:
    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    def get_user(self, user_name: str) -> Optional[User]:
        uri = self.base_uri + "/users/" + user_name
        response = requests.get(uri)
        if response.status_code == 404:
            return None
        return User(name=response.json()["name"])
