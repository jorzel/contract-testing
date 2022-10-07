import atexit
import logging
import os

import pytest
from app import UserClient
from pact import Consumer, Format, Like, Provider, Term

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234

PACT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../pacts")


@pytest.fixture
def consumer() -> UserClient:
    return UserClient(
        "http://{host}:{port}".format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
    )


@pytest.fixture(scope="session")
def pact(request):
    """Setup a Pact Consumer, which provides the Provider mock service. This
    will generate and optionally publish Pacts to the Pact Broker"""

    version = request.config.getoption("--publish-pact")
    publish = True if version else False
    env = request.config.getoption("--env")
    pact = Consumer(
        "UserClient",
        version=version,
        tags=[env] if env else None,
    ).has_pact_with(
        Provider("UserService"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
        publish_to_broker=publish,
        broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
    )
    pact.start_service()
    atexit.register(pact.stop_service)
    yield pact
    pact.stop_service()

    pact.publish_to_broker = False


def test_get_user_non_admin(pact, consumer):
    expected = {
        "name": "UserA",
        "username": "usera",
        "id": Format().uuid,
        "created_on": Term(r"\d+-\d+-\d+T\d+:\d+:\d+", "2016-12-15T20:16:01"),
        "ip_address": Format().ip_address,
        "admin": False,
    }

    (
        pact.given("UserA exists and is not an administrator")
        .upon_receiving("a request for UserA")
        .with_request("get", "/users/UserA")
        .will_respond_with(200, body=Like(expected))
    )

    with pact:
        user = consumer.get_user("UserA")
        assert user.name == "UserA"

        pact.verify()


def _test_get_non_existing_user(pact, consumer):
    (
        pact.given("UserA does not exist")
        .upon_receiving("a request for UserA")
        .with_request("get", "/users/UserA")
        .will_respond_with(404)
    )

    with pact:
        user = consumer.get_user("UserA")
        assert user is None

        pact.verify()
