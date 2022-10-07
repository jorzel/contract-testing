def pytest_addoption(parser):
    parser.addoption(
        "--publish-pact",
        type=str,
        action="store",
        help="Upload generated pact file to pact broker with version",
    )

    parser.addoption(
        "--run-broker",
        type=bool,
        action="store",
        help="Whether to run broker in this test or not.",
    )
    parser.addoption(
        "--provider-url", type=str, action="store", help="The url to our provider."
    )
    parser.addoption(
        "--env",
        type=str,
        action="store",
    )
