"""
Base Page Object — all page objects extend this class.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import BASE_URL, EXPLICIT_WAIT
from utils.screenshot_utils import take_screenshot
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)
        self.base_url = BASE_URL.rstrip('/')

    # ── Navigation ───────────────────────────────────────────────
    def open(self, path: str = ''):
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url + '/'
        self.logger.info(f'Navigating to: {url}')
        self.driver.get(url)
        return self

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def go_back(self):
        self.driver.back()

    def refresh(self):
        self.driver.refresh()

    # ── Element Interactions ─────────────────────────────────────
    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_clickable(self, by, value):
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def find_visible(self, by, value):
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def click(self, by, value):
        el = self.find_clickable(by, value)
        el.click()
        return self

    def type_text(self, by, value, text: str, clear: bool = True):
        el = self.find(by, value)
        if clear:
            el.clear()
        el.send_keys(text)
        return self

    def get_text(self, by, value) -> str:
        try:
            return self.find(by, value).text
        except TimeoutException:
            return ''

    def get_attribute(self, by, value, attr: str) -> str:
        try:
            return self.find(by, value).get_attribute(attr) or ''
        except TimeoutException:
            return ''

    def is_displayed(self, by, value, timeout: int = 5) -> bool:
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_present(self, by, value, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def element_exists(self, by, value, timeout: int = 3) -> bool:
        return self.is_present(by, value, timeout)

    def count_elements(self, by, value) -> int:
        try:
            return len(self.driver.find_elements(by, value))
        except Exception:
            return 0

    def scroll_to_element(self, by, value):
        el = self.find(by, value)
        self.driver.execute_script('arguments[0].scrollIntoView({block:"center"})', el)
        time.sleep(0.3)
        return el

    def scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(0.5)

    def scroll_to_top(self):
        self.driver.execute_script('window.scrollTo(0, 0)')
        time.sleep(0.3)

    # ── Waiting ──────────────────────────────────────────────────
    def wait_for_url_contains(self, text: str, timeout: int = EXPLICIT_WAIT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
            return True
        except TimeoutException:
            return False

    def wait_for_title_contains(self, text: str, timeout: int = EXPLICIT_WAIT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.title_contains(text))
            return True
        except TimeoutException:
            return False

    def wait_for_text_in_element(self, by, value, text: str, timeout: int = EXPLICIT_WAIT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_disappear(self, by, value, timeout: int = EXPLICIT_WAIT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def sleep(self, seconds: float = 1.0):
        time.sleep(seconds)
        return self

    # ── JavaScript ───────────────────────────────────────────────
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def get_console_logs(self) -> list:
        try:
            return self.driver.get_log('browser')
        except Exception:
            return []

    def js_click(self, by, value):
        el = self.find(by, value)
        self.driver.execute_script('arguments[0].click()', el)
        return self

    # ── Screenshots ──────────────────────────────────────────────
    def screenshot(self, name: str) -> str:
        return take_screenshot(self.driver, name)

    # ── Assertions ───────────────────────────────────────────────
    def assert_url_contains(self, fragment: str) -> bool:
        current = self.get_current_url()
        result = fragment in current
        if not result:
            self.logger.warning(f'URL assertion failed: "{fragment}" not in "{current}"')
        return result

    def assert_title_contains(self, text: str) -> bool:
        title = self.get_title()
        result = text.lower() in title.lower()
        if not result:
            self.logger.warning(f'Title assertion failed: "{text}" not in "{title}"')
        return result

    def assert_element_visible(self, by, value) -> bool:
        return self.is_displayed(by, value)

    def assert_text_present(self, text: str) -> bool:
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body').text
            return text.lower() in body.lower()
        except Exception:
            return False

    # ── Responsive helpers ───────────────────────────────────────
    def set_viewport(self, width: int, height: int):
        self.driver.set_window_size(width, height)
        time.sleep(0.5)

    def get_viewport_size(self) -> dict:
        return {
            'width': self.driver.execute_script('return window.innerWidth'),
            'height': self.driver.execute_script('return window.innerHeight'),
        }
