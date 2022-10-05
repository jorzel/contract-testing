import pytest
from api import RegisteredUserEvent
from pact import MessageProvider

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"


@pytest.fixture
def default_opts():
    return {
        "broker_username": PACT_BROKER_USERNAME,
        "broker_password": PACT_BROKER_PASSWORD,
        "broker_url": PACT_BROKER_URL,
        "publish_version": "3",
        "publish_verification_results": False,
    }


def test_verify_from_broker(default_opts):
    # key in provider should meet `given` section provided by consumer pact
    provider = MessageProvider(
        message_providers={
            "Registration handled": RegisteredUserEvent(
                user_id=1, username="test"
            ).as_dict
        },
        provider="RegistrationService",
        consumer="AnalyticsService",
    )

    with provider:
        provider.verify_with_broker(**default_opts)
