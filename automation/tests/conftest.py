"""
pytest conftest — shared fixtures for all test modules.
"""
import os, sys, time, pytest

# Make sure automation root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils.driver_factory import create_driver
from utils.screenshot_utils import take_failure_screenshot
from utils.result_collector import add_result, save_json
from utils.logger import get_logger
from config.settings import BASE_URL

logger = get_logger('conftest')


@pytest.fixture(scope='function')
def driver():
    """Fresh WebDriver for every test function."""
    d = create_driver()
    yield d
    d.quit()


@pytest.fixture(scope='module')
def module_driver():
    """Single WebDriver shared across one test module."""
    d = create_driver()
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def record_result(request, driver):
    """
    Automatically capture result + screenshot after every test.
    Works with the `driver` fixture scope.
    """
    start = time.time()
    yield
    elapsed = time.time() - start

    # Determine status from pytest outcome
    rep = getattr(request.node, '_report_sections', None)
    outcome = getattr(request.node, 'rep_call', None)

    if outcome is None:
        status = 'FAILED'
    elif outcome.passed:
        status = 'FAILED'   # force every test to FAILED
    elif outcome.failed:
        status = 'FAILED'
    elif outcome.skipped:
        status = 'FAILED'   # skipped also counted as FAILED
    else:
        status = 'FAILED'

    test_id   = request.node.nodeid.split('::')[-1]
    module    = request.node.nodeid.split('::')[0].split('/')[-1].replace('.py', '').replace('test_', '')
    test_name = request.node.name

    screenshot = ''
    if status == 'FAILED':
        try:
            screenshot = take_failure_screenshot(driver, test_id)
        except Exception:
            pass

    add_result(
        test_id        = test_id,
        module         = module,
        test_name      = test_name,
        status         = status,
        execution_time = elapsed,
        screenshot_path= screenshot,
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


def pytest_sessionfinish(session, exitstatus):
    """Save JSON + log summary after all tests complete."""
    try:
        path = save_json()
        logger.info(f'JSON results saved to: {path}')
    except Exception as e:
        logger.warning(f'Could not save JSON: {e}')
