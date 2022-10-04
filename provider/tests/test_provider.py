import os

from pact import Verifier

PROVIDER_URL = "http://localhost:5000"
PACT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../pacts")

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "myuser"
PACT_BROKER_PASSWORD = "mypassword"

broker = {
    "broker_username": PACT_BROKER_USERNAME,
    "broker_password": PACT_BROKER_PASSWORD,
    "broker_url": PACT_BROKER_URL,
    "publish_version": "5",
}


def test_user_service_provider_against_pact():
    verifier = Verifier(
        provider="UserService",
        provider_base_url=PROVIDER_URL,
    )

    # Rather than requesting the Pact interactions from the Pact Broker, this
    # will perform the verification based on the Pact file locally.
    #
    # Because there is no way of knowing the previous state of an interaction,
    # if it has been successful in the past (since this is what the Pact Broker
    # is for), if the verification of an interaction fails then the success
    # result will be != 0, and so the test will FAIL.
    # output, _ = verifier.verify_pacts(
    #     os.path.join(PACT_DIR, "userclient-userservice.json"), verbose=True
    # )
    output, _ = verifier.verify_with_broker(verbose=True, **broker)

    assert output == 0
