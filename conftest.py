import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--suite", action="store", help="option:input test_suite num"
    )

@pytest.fixture
def s(request):
    return request.config.getoption("--suite")