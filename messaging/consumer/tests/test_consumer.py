"""pact test for a message consumer"""

import logging
import os

import pytest
from api import RegisteredUserEventError, handle_registered_user_event
from pact import Format, MessageConsumer, Provider, Term

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"

PACT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../pacts")


@pytest.fixture(scope="session")
def pact(request):
    version = request.config.getoption("--publish-pact")
    publish = True if version else False

    pact = MessageConsumer("AnalyticsService", version=version).has_pact_with(
        Provider("RegistrationService"),
        publish_to_broker=publish,
        broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
        pact_dir=PACT_DIR,
    )

    yield pact


def test_throw_exception_handler(pact):
    wrong_event = {
        "event_name": "registered_user",
        "username": Term("[a-zA-Z]+", "username"),
    }

    (
        pact.given("Registered event not proper")
        .expects_to_receive("user_id field not exist")
        .with_content(wrong_event)
        .with_metadata({"Content-Type": "application/json"})
    )

    with pytest.raises(RegisteredUserEventError):
        with pact:
            handle_registered_user_event(wrong_event)


def test_put_file(pact):
    expected_event = {
        "event_name": "registered_user",
        "username": Term("[a-zA-Z]+", "username"),
        "user_id": Format().integer,
    }
    (
        pact.given("Registration handled")
        .expects_to_receive("user_id(int), username(str), event_name(str)")
        .with_content(expected_event)
        .with_metadata({"Content-Type": "application/json"})
    )

    with pact:
        event = handle_registered_user_event(expected_event)
    assert event.event_name == "registered_user"
