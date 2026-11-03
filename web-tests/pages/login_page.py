"""Page Object — Login Page (/login)"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT         = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT      = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BTN          = (By.CSS_SELECTOR, "button[type='submit']")
    SHOW_PASS_BTN       = (By.XPATH, "//button[@type='button'][.//svg]")
    FORGOT_PASS_LINK    = (By.XPATH, "//a[contains(@href,'forgot') or contains(text(),'Forgot')]")
    REGISTER_LINK       = (By.XPATH, "//a[contains(@href,'register') or contains(text(),'Create') or contains(text(),'Register')]")
    LOGO_LINK           = (By.XPATH, "//a[contains(@href,'/') and not(contains(@href,'login'))]")
    ERROR_TOAST         = (By.XPATH, "//*[contains(@class,'toast') or contains(@role,'alert') or contains(@class,'error')]")
    SUCCESS_TOAST       = (By.XPATH, "//*[contains(@class,'toast-success') or contains(text(),'Welcome')]")
    HEADING             = (By.XPATH, "//h1[contains(text(),'Welcome') or contains(text(),'Sign')]")
    EMAIL_ICON          = (By.XPATH, "//*[contains(@class,'lucide-mail') or contains(@data-lucide,'mail')]")
    BODY                = (By.TAG_NAME, 'body')
    FORM                = (By.TAG_NAME, 'form')
    LOADING_SPINNER     = (By.XPATH, "//*[contains(@class,'animate-spin') or contains(@class,'loading')]")

    def open_login(self):
        return self.open('login')

    def is_loaded(self) -> bool:
        return self.is_present(*self.EMAIL_INPUT, timeout=15)

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

    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        return self

    def toggle_password_visibility(self):
        self.click(*self.SHOW_PASS_BTN)
        return self

    def get_password_input_type(self) -> str:
        return self.get_attribute(*self.PASSWORD_INPUT, 'type')

    def click_forgot_password(self):
        self.click(*self.FORGOT_PASS_LINK)
        return self

    def click_register_link(self):
        self.click(*self.REGISTER_LINK)
        return self

    def click_logo(self):
        self.click(*self.LOGO_LINK)
        return self

    def has_error_message(self, timeout: int = 5) -> bool:
        return self.is_present(*self.ERROR_TOAST, timeout=timeout)

    def has_success_message(self, timeout: int = 5) -> bool:
        return self.is_present(*self.SUCCESS_TOAST, timeout=timeout)

    def is_redirected_to_dashboard(self, timeout: int = 15) -> bool:
        return self.wait_for_url_contains('dashboard', timeout)

    def submit_with_enter(self):
        el = self.find(*self.PASSWORD_INPUT)
        el.send_keys(Keys.RETURN)
        return self

    def email_field_is_required(self) -> bool:
        attr = self.get_attribute(*self.EMAIL_INPUT, 'required')
        return attr is not None and attr != 'false'

    def password_field_is_required(self) -> bool:
        attr = self.get_attribute(*self.PASSWORD_INPUT, 'required')
        return attr is not None and attr != 'false'

    def clear_fields(self):
        self.find(*self.EMAIL_INPUT).clear()
        self.find(*self.PASSWORD_INPUT).clear()
        return self

    def has_heading(self) -> bool:
        return self.is_present(*self.HEADING, timeout=8)

    def has_form(self) -> bool:
        return self.is_present(*self.FORM, timeout=8)

    def get_submit_btn_text(self) -> str:
        return self.get_text(*self.SUBMIT_BTN)

    def is_submit_disabled(self) -> bool:
        try:
            btn = self.find(*self.SUBMIT_BTN)
            return not btn.is_enabled()
        except Exception:
            return False
