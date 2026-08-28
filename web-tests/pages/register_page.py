"""Page Object — Register Page (/register)"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class RegisterPage(BasePage):
    USERNAME_INPUT      = (By.CSS_SELECTOR, "input[type='text']")
    EMAIL_INPUT         = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT      = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BTN          = (By.CSS_SELECTOR, "button[type='submit']")
    SHOW_PASS_BTN       = (By.XPATH, "//button[@type='button'][.//svg][1]")
    LOGIN_LINK          = (By.XPATH, "//a[contains(@href,'login') or contains(text(),'Sign in')]")
    LOGO_LINK           = (By.XPATH, "//a[contains(@href,'/') and not(contains(@href,'register'))]")
    HEADING             = (By.XPATH, "//h1[contains(text(),'Create') or contains(text(),'Register') or contains(text(),'Account')]")
    ERROR_TOAST         = (By.XPATH, "//*[contains(@class,'toast') or contains(@role,'alert')]")
    PASS_STRENGTH_BAR   = (By.XPATH, "//div[contains(@class,'h-1') and contains(@class,'flex-1')]")
    DIFF_BEGINNER       = (By.XPATH, "//button[contains(text(),'Beginner')]")
    DIFF_INTERMEDIATE   = (By.XPATH, "//button[contains(text(),'Intermediate')]")
    DIFF_ADVANCED       = (By.XPATH, "//button[contains(text(),'Advanced')]")
    DIFF_EXPERT         = (By.XPATH, "//button[contains(text(),'Expert')]")
    TERMS_TEXT          = (By.XPATH, "//*[contains(text(),'Terms') or contains(text(),'terms')]")
    FORM                = (By.TAG_NAME, 'form')
    LOADING_SPINNER     = (By.XPATH, "//*[contains(@class,'animate-spin')]")

    def open_register(self):
        return self.open('register')

    def is_loaded(self) -> bool:
        return self.is_present(*self.SUBMIT_BTN, timeout=15)

    def enter_username(self, username: str):
        el = self.find(*self.USERNAME_INPUT)
        el.clear()
        el.send_keys(username)
        return self

    def enter_email(self, email: str):
        el = self.find(*self.EMAIL_INPUT)
        el.clear()
        el.send_keys(email)
        return self

    def enter_password(self, password: str):
        el = self.find(*self.PASSWORD_INPUT)
        el.clear()
        el.send_keys(password)
        return self

    def click_submit(self):
        self.click(*self.SUBMIT_BTN)
        return self

    def register(self, username: str, email: str, password: str, difficulty: str = 'beginner'):
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password(password)
        self.select_difficulty(difficulty)
        self.click_submit()
        return self

    def select_difficulty(self, level: str):
        locators = {
            'beginner':     self.DIFF_BEGINNER,
            'intermediate': self.DIFF_INTERMEDIATE,
            'advanced':     self.DIFF_ADVANCED,
            'expert':       self.DIFF_EXPERT,
        }
        loc = locators.get(level.lower(), self.DIFF_BEGINNER)
        if self.is_present(*loc, timeout=5):
            self.click(*loc)
        return self

    def toggle_password_visibility(self):
        if self.is_present(*self.SHOW_PASS_BTN, timeout=5):
            self.click(*self.SHOW_PASS_BTN)
        return self

    def get_password_input_type(self) -> str:
        return self.get_attribute(*self.PASSWORD_INPUT, 'type')

    def has_error_message(self, timeout: int = 5) -> bool:
        return self.is_present(*self.ERROR_TOAST, timeout=timeout)

    def is_redirected_to_dashboard(self, timeout: int = 15) -> bool:
        return self.wait_for_url_contains('dashboard', timeout)

    def click_login_link(self):
        self.click(*self.LOGIN_LINK)
        return self

    def click_logo(self):
        self.click(*self.LOGO_LINK)
        return self

    def password_strength_visible(self) -> bool:
        return self.is_present(*self.PASS_STRENGTH_BAR, timeout=5)

    def has_terms_text(self) -> bool:
        return self.is_present(*self.TERMS_TEXT, timeout=5)

    def has_difficulty_options(self) -> bool:
        return self.is_present(*self.DIFF_BEGINNER, timeout=8)

    def get_username_max_length(self) -> int:
        attr = self.get_attribute(*self.USERNAME_INPUT, 'maxlength')
        return int(attr) if attr else 999
