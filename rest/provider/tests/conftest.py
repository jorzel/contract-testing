def pytest_addoption(parser):
    parser.addoption(
        "--publish-version",
        type=str,
        action="store",
    )
    parser.addoption(
        "--env",
        type=str,
        action="store",
    )
