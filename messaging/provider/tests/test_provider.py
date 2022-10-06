import pytest
from api import RegisteredUserEvent
from pact import MessageProvider

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"


@pytest.fixture(scope="session")
def default_opts(request):
    version = request.config.getoption("--publish-version")
    publish = True if version else False
    return {
        "broker_username": PACT_BROKER_USERNAME,
        "broker_password": PACT_BROKER_PASSWORD,
        "broker_url": PACT_BROKER_URL,
        "publish_version": version,
        "publish_verification_results": publish,
    }


def test_verify_from_broker(default_opts, request):
    # key in provider should meet `given` section provided by consumer pact
    provider = MessageProvider(
        message_providers={
            "registered_user event": RegisteredUserEvent(
                user_id=1, username="test"
            ).as_dict
        },
        provider="RegistrationService",
        consumer="AnalyticsService",
    )

    with provider:
        provider.verify_with_broker(**default_opts)
