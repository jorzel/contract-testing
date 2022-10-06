def pytest_addoption(parser):
    parser.addoption(
        "--publish-version",
        type=str,
        action="store",
    )
