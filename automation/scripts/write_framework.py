"""
Bootstrap script — writes all framework Python source files to disk.
Run before setup_framework.py.
"""
import os, textwrap

ROOT = os.path.join(os.path.dirname(__file__), '..')

def write(rel_path, content):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(content).lstrip('\n'))
    print(f'  ✅ {rel_path}')

print('Writing framework files...')

# ── config/settings.py ────────────────────────────────────────
write('config/settings.py', '''
import os

BASE_URL               = os.environ.get('BASE_URL', 'https://Lahari0621.github.io/PDD/')
HEADLESS               = os.environ.get('HEADLESS', 'true').lower() == 'true'
IMPLICIT_WAIT          = int(os.environ.get('IMPLICIT_WAIT', '10'))
EXPLICIT_WAIT          = int(os.environ.get('EXPLICIT_WAIT', '20'))
PAGE_LOAD_TIMEOUT      = int(os.environ.get('PAGE_LOAD_TIMEOUT', '30'))
RETRY_COUNT            = int(os.environ.get('RETRY_COUNT', '2'))
SCREENSHOT_ON_FAILURE  = os.environ.get('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
REPORT_DIR             = os.environ.get('REPORT_DIR', 'reports')
SCREENSHOT_DIR         = os.environ.get('SCREENSHOT_DIR', 'screenshots')
LOG_DIR                = os.environ.get('LOG_DIR', 'logs')
TEST_SUITE             = os.environ.get('TEST_SUITE', 'all')

# Test user credentials (demo / expected-to-fail on live)
TEST_EMAIL             = os.environ.get('TEST_EMAIL', 'testuser@aidebate.test')
TEST_PASSWORD          = os.environ.get('TEST_PASSWORD', 'Test@123456')
TEST_USERNAME          = os.environ.get('TEST_USERNAME', 'testdebater')
INVALID_EMAIL          = 'invalid@notexist.xyz'
INVALID_PASSWORD       = 'WrongPass999'
''')

# ── utils/driver_factory.py ───────────────────────────────────
write('utils/driver_factory.py', '''
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


def create_driver(headless=None):
    """Factory that returns a configured Chrome WebDriver."""
    use_headless = headless if headless is not None else HEADLESS
    opts = Options()
    if use_headless:
        opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1920,1080')
    opts.add_argument('--disable-extensions')
    opts.add_argument('--disable-web-security')
    opts.add_argument('--allow-running-insecure-content')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.set_window_size(1920, 1080)
    return driver
''')

# ── utils/screenshot_utils.py ─────────────────────────────────
write('utils/screenshot_utils.py', '''
import os, time
from datetime import datetime
from config.settings import SCREENSHOT_DIR


def take_screenshot(driver, name: str, subfolder: str = '') -> str:
    """Capture a screenshot and return the file path."""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:21]
    safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
    folder = os.path.join(SCREENSHOT_DIR, subfolder) if subfolder else SCREENSHOT_DIR
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{safe_name}_{ts}.png')
    try:
        driver.save_screenshot(path)
        return path
    except Exception as e:
        return f'screenshot_failed:{e}'


def take_failure_screenshot(driver, test_id: str) -> str:
    return take_screenshot(driver, f'FAIL_{test_id}', 'failures')
''')

# ── utils/logger.py ───────────────────────────────────────────
write('utils/logger.py', '''
import logging, os
from datetime import datetime
from config.settings import LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    ts = datetime.now().strftime('%Y%m%d')
    fh = logging.FileHandler(os.path.join(LOG_DIR, f'test_run_{ts}.log'), encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter('[%(asctime)s] [%(levelname)-7s] [%(name)s] %(message)s',
                            datefmt='%H:%M:%S')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
''')

# ── utils/wait_utils.py ───────────────────────────────────────
write('utils/wait_utils.py', '''
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import EXPLICIT_WAIT


def wait_for_element(driver, locator, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def wait_for_clickable(driver, locator, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

def wait_for_visible(driver, locator, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def wait_for_url_contains(driver, text, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.url_contains(text))

def wait_for_title_contains(driver, text, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.title_contains(text))

def wait_for_text_in_element(driver, locator, text, timeout=EXPLICIT_WAIT):
    return WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element(locator, text))

def element_exists(driver, by, value, timeout=5) -> bool:
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False

def safe_find(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None
''')

# ── utils/test_data.py ────────────────────────────────────────
write('utils/test_data.py', '''
import random, string, time

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    return f"test_{random_string(6)}_{int(time.time())}@debate.test"

def random_username():
    return f"user_{random_string(5)}"

def random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$"
    pwd = (random.choice(string.ascii_uppercase) +
           random.choice(string.digits) +
           random.choice("!@#$") +
           ''.join(random.choices(chars, k=length-3)))
    return ''.join(random.sample(pwd, len(pwd)))

DEBATE_TOPICS = [
    "Social media does more harm than good",
    "AI will replace most jobs by 2040",
    "Universal Basic Income should be implemented",
    "Climate change requires immediate government action",
    "Privacy is more important than security",
    "Remote work is better than office work",
    "Nuclear energy should be expanded globally",
]

VALID_EMAILS = [
    "alice@example.com",
    "bob.smith@domain.org",
    "test+label@mail.com",
]

INVALID_EMAILS = [
    "notanemail",
    "@missinglocal.com",
    "missing@",
    "spaces in@email.com",
    "",
]

WEAK_PASSWORDS = ["123", "pass", "abc", "12345678"]

SHORT_TEXT = "a"
LONG_TEXT = "x" * 1001
SQL_INJECTION = "'; DROP TABLE users; --"
XSS_PAYLOAD = "<script>alert('xss')</script>"
SPECIAL_CHARS = "!@#$%^&*()_+{}|:<>?"
''')

# ── utils/result_collector.py ─────────────────────────────────
write('utils/result_collector.py', '''
import json, os, time
from datetime import datetime
from config.settings import REPORT_DIR

_results = []

def add_result(test_id, module, test_name, status, execution_time=0,
               priority="Medium", failure_reason="", screenshot_path="",
               preconditions="", test_steps="", expected_result=""):
    _results.append({
        "test_id": test_id,
        "module": module,
        "test_name": test_name,
        "status": status,
        "execution_time": round(execution_time, 2),
        "priority": priority,
        "failure_reason": failure_reason,
        "screenshot_path": screenshot_path,
        "preconditions": preconditions,
        "test_steps": test_steps,
        "expected_result": expected_result,
        "actual_result": status,
        "timestamp": datetime.now().isoformat(),
    })

def get_results():
    return list(_results)

def save_json():
    os.makedirs(os.path.join(REPORT_DIR, 'JSON'), exist_ok=True)
    path = os.path.join(REPORT_DIR, 'JSON', 'execution-results.json')
    summary = {
        "execution_date": datetime.now().isoformat(),
        "total": len(_results),
        "passed": sum(1 for r in _results if r["status"] == "PASSED"),
        "failed": sum(1 for r in _results if r["status"] == "FAILED"),
        "skipped": sum(1 for r in _results if r["status"] == "SKIPPED"),
        "blocked": sum(1 for r in _results if r["status"] == "BLOCKED"),
        "results": _results,
    }
    with open(path, 'w') as f:
        json.dump(summary, f, indent=2)
    return path
''')

print('✅ All framework utils written')
