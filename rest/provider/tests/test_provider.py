import os

import pytest
from pact import Verifier

PACT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../pacts")

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"


@pytest.fixture(scope="session")
def default_opts(request):
    version = request.config.getoption("--publish-version")
    publish = True if version else False
    env = request.config.getoption("--env")
    return {
        "broker_username": PACT_BROKER_USERNAME,
        "broker_password": PACT_BROKER_PASSWORD,
        "broker_url": PACT_BROKER_URL,
        "publish_version": version,
        "publish_verification_results": publish,
        "provider_tags": [env] if env else None,
    }


PROVIDER_URL = "http://localhost:5000"


def test_user_service_provider_against_pact(default_opts):
    verifier = Verifier(
        provider="UserService",
        provider_base_url=PROVIDER_URL,
    )
    output, _ = verifier.verify_with_broker(verbose=True, **default_opts)

    assert output == 0
