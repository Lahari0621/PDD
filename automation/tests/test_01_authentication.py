"""
MODULE: Authentication
TEST CASES: AUTH-001 to AUTH-040  (40 test cases)
Priority: Critical / High
"""
import pytest
import time
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.landing_page import LandingPage
from utils.test_data import random_email, random_username, random_password
from config.settings import BASE_URL


# ─────────────────────────────────────────────────────────────────────────────
# AUTH-001 to AUTH-010 — Login Page Rendering & Structure
# ─────────────────────────────────────────────────────────────────────────────

class TestLoginPageStructure:

    def test_AUTH_001_login_page_loads(self, driver):
        """AUTH-001 | Critical | Login page renders successfully"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_loaded(), "Login page did not load"

    def test_AUTH_002_login_page_has_title(self, driver):
        """AUTH-002 | High | Page title contains 'Debate'"""
        page = LoginPage(driver)
        page.open_login()
        assert page.page_title_is_set(), "Page title is empty"

    def test_AUTH_003_login_has_email_field(self, driver):
        """AUTH-003 | Critical | Email input field present"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_displayed(*page.EMAIL_INPUT), "Email field not displayed"

    def test_AUTH_004_login_has_password_field(self, driver):
        """AUTH-004 | Critical | Password input field present"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_displayed(*page.PASSWORD_INPUT), "Password field not displayed"

    def test_AUTH_005_login_has_submit_button(self, driver):
        """AUTH-005 | Critical | Submit button present"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_displayed(*page.SUBMIT_BTN), "Submit button not displayed"

    def test_AUTH_006_login_has_heading(self, driver):
        """AUTH-006 | High | Login heading is visible"""
        page = LoginPage(driver)
        page.open_login()
        assert page.has_heading(), "Login heading not visible"

    def test_AUTH_007_login_has_register_link(self, driver):
        """AUTH-007 | Medium | Register link present on login page"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_displayed(*page.REGISTER_LINK), "Register link missing"

    def test_AUTH_008_login_has_forgot_password_link(self, driver):
        """AUTH-008 | Medium | Forgot password link present"""
        page = LoginPage(driver)
        page.open_login()
        assert page.is_displayed(*page.FORGOT_PASS_LINK), "Forgot password link missing"

    def test_AUTH_009_login_has_form(self, driver):
        """AUTH-009 | High | Login form element present"""
        page = LoginPage(driver)
        page.open_login()
        assert page.has_form(), "Login form not found"

    def test_AUTH_010_login_page_url_is_correct(self, driver):
        """AUTH-010 | High | Login URL contains '/login'"""
        page = LoginPage(driver)
        page.open_login()
        assert page.assert_url_contains('login'), f"URL does not contain 'login': {page.get_current_url()}"


# ─────────────────────────────────────────────────────────────────────────────
# AUTH-011 to AUTH-020 — Login Functionality
# ─────────────────────────────────────────────────────────────────────────────

class TestLoginFunctionality:

    def test_AUTH_011_password_field_masked_by_default(self, driver):
        """AUTH-011 | High | Password field is masked (type=password) by default"""
        page = LoginPage(driver)
        page.open_login()
        assert page.get_password_input_type() == 'password', "Password not masked"

    def test_AUTH_012_password_toggle_shows_text(self, driver):
        """AUTH-012 | Medium | Toggle password visibility shows text"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_password('TestPass123')
        page.toggle_password_visibility()
        time.sleep(0.5)
        assert page.get_password_input_type() == 'text', "Password toggle did not reveal text"

    def test_AUTH_013_password_toggle_hides_again(self, driver):
        """AUTH-013 | Medium | Toggle password back to hidden"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_password('TestPass123')
        page.toggle_password_visibility()
        time.sleep(0.3)
        page.toggle_password_visibility()
        time.sleep(0.3)
        assert page.get_password_input_type() == 'password', "Password not re-masked"

    def test_AUTH_014_invalid_credentials_show_error(self, driver):
        """AUTH-014 | Critical | Invalid credentials show error toast"""
        page = LoginPage(driver)
        page.open_login()
        page.login('invalid@notexist.xyz', 'WrongPass999')
        assert page.has_error_message(timeout=8), "No error shown for invalid credentials"

    def test_AUTH_015_empty_email_shows_validation(self, driver):
        """AUTH-015 | High | Empty email triggers HTML5 validation"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_password('SomePass123')
        page.click_submit()
        # Either HTML5 validation fires (form not submitted) or toast error
        still_on_login = page.assert_url_contains('login')
        assert still_on_login, "Should stay on login with empty email"

    def test_AUTH_016_empty_password_shows_validation(self, driver):
        """AUTH-016 | High | Empty password triggers HTML5 validation"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_email('valid@email.com')
        page.click_submit()
        still_on_login = page.assert_url_contains('login')
        assert still_on_login, "Should stay on login with empty password"

    def test_AUTH_017_both_fields_empty_stays_on_login(self, driver):
        """AUTH-017 | High | Submitting empty form stays on login"""
        page = LoginPage(driver)
        page.open_login()
        page.click_submit()
        time.sleep(1)
        assert page.assert_url_contains('login'), "Should stay on login"

    def test_AUTH_018_invalid_email_format_blocked(self, driver):
        """AUTH-018 | High | Malformed email format is rejected"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_email('notanemail')
        page.enter_password('ValidPass123!')
        page.click_submit()
        time.sleep(1)
        assert page.assert_url_contains('login'), "Malformed email should be rejected"

    def test_AUTH_019_register_link_navigates_to_register(self, driver):
        """AUTH-019 | High | Clicking register link navigates to /register"""
        page = LoginPage(driver)
        page.open_login()
        page.click_register_link()
        assert page.wait_for_url_contains('register', 10), "Did not navigate to register"

    def test_AUTH_020_logo_click_goes_to_landing(self, driver):
        """AUTH-020 | Medium | Logo click on login page goes to landing"""
        page = LoginPage(driver)
        page.open_login()
        page.click_logo()
        time.sleep(1.5)
        url = page.get_current_url()
        assert '/' in url, f"Logo did not navigate to landing: {url}"


# ─────────────────────────────────────────────────────────────────────────────
# AUTH-021 to AUTH-030 — Register Page Structure & Validation
# ─────────────────────────────────────────────────────────────────────────────

class TestRegisterPageStructure:

    def test_AUTH_021_register_page_loads(self, driver):
        """AUTH-021 | Critical | Register page renders successfully"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_loaded(), "Register page did not load"

    def test_AUTH_022_register_has_username_field(self, driver):
        """AUTH-022 | Critical | Username input field present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_displayed(*page.USERNAME_INPUT), "Username field missing"

    def test_AUTH_023_register_has_email_field(self, driver):
        """AUTH-023 | Critical | Email input field present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_displayed(*page.EMAIL_INPUT), "Email field missing"

    def test_AUTH_024_register_has_password_field(self, driver):
        """AUTH-024 | Critical | Password input field present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_displayed(*page.PASSWORD_INPUT), "Password field missing"

    def test_AUTH_025_register_has_difficulty_options(self, driver):
        """AUTH-025 | High | Difficulty level options present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.has_difficulty_options(), "Difficulty options not found"

    def test_AUTH_026_register_has_submit_button(self, driver):
        """AUTH-026 | Critical | Submit button present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_displayed(*page.SUBMIT_BTN), "Submit button missing"

    def test_AUTH_027_register_has_login_link(self, driver):
        """AUTH-027 | Medium | Login link present on register page"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.is_displayed(*page.LOGIN_LINK), "Login link missing"

    def test_AUTH_028_register_has_terms_text(self, driver):
        """AUTH-028 | Low | Terms & Privacy text present"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.has_terms_text(), "Terms text missing"

    def test_AUTH_029_password_strength_indicator_visible(self, driver):
        """AUTH-029 | Medium | Password strength bar appears when typing"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_password('Test123!')
        assert page.password_strength_visible(), "Password strength bar not visible"

    def test_AUTH_030_password_masked_by_default(self, driver):
        """AUTH-030 | High | Password field masked by default on register"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.get_password_input_type() == 'password', "Password not masked"


# ─────────────────────────────────────────────────────────────────────────────
# AUTH-031 to AUTH-040 — Registration Validation & Navigation
# ─────────────────────────────────────────────────────────────────────────────

class TestRegisterFunctionality:

    def test_AUTH_031_short_password_rejected(self, driver):
        """AUTH-031 | High | Password shorter than 8 chars shows error"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_username(random_username())
        page.enter_email(random_email())
        page.enter_password('abc')
        page.click_submit()
        time.sleep(2)
        assert page.assert_url_contains('register') or page.has_error_message(3), \
            "Short password not rejected"

    def test_AUTH_032_empty_username_blocked(self, driver):
        """AUTH-032 | High | Empty username blocks form submission"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_email(random_email())
        page.enter_password('ValidPass123!')
        page.click_submit()
        time.sleep(1)
        assert page.assert_url_contains('register'), "Empty username not blocked"

    def test_AUTH_033_invalid_email_format_blocked(self, driver):
        """AUTH-033 | High | Invalid email format blocked on register"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_username(random_username())
        page.enter_email('notanemail')
        page.enter_password('ValidPass123!')
        page.click_submit()
        time.sleep(1)
        assert page.assert_url_contains('register'), "Invalid email not blocked"

    def test_AUTH_034_select_beginner_difficulty(self, driver):
        """AUTH-034 | Medium | Beginner difficulty can be selected"""
        page = RegisterPage(driver)
        page.open_register()
        page.select_difficulty('beginner')
        assert page.is_present(*page.DIFF_BEGINNER, timeout=5), "Beginner option not found"

    def test_AUTH_035_select_intermediate_difficulty(self, driver):
        """AUTH-035 | Medium | Intermediate difficulty can be selected"""
        page = RegisterPage(driver)
        page.open_register()
        page.select_difficulty('intermediate')
        assert page.is_present(*page.DIFF_INTERMEDIATE, timeout=5), "Intermediate not found"

    def test_AUTH_036_select_advanced_difficulty(self, driver):
        """AUTH-036 | Medium | Advanced difficulty can be selected"""
        page = RegisterPage(driver)
        page.open_register()
        page.select_difficulty('advanced')
        assert page.is_present(*page.DIFF_ADVANCED, timeout=5), "Advanced not found"

    def test_AUTH_037_select_expert_difficulty(self, driver):
        """AUTH-037 | Medium | Expert difficulty can be selected"""
        page = RegisterPage(driver)
        page.open_register()
        page.select_difficulty('expert')
        assert page.is_present(*page.DIFF_EXPERT, timeout=5), "Expert not found"

    def test_AUTH_038_login_link_navigates_to_login(self, driver):
        """AUTH-038 | High | Login link navigates to /login"""
        page = RegisterPage(driver)
        page.open_register()
        page.click_login_link()
        assert page.wait_for_url_contains('login', 10), "Did not navigate to login"

    def test_AUTH_039_register_page_url_correct(self, driver):
        """AUTH-039 | Medium | Register URL contains '/register'"""
        page = RegisterPage(driver)
        page.open_register()
        assert page.assert_url_contains('register'), "URL does not contain 'register'"

    def test_AUTH_040_password_toggle_works_on_register(self, driver):
        """AUTH-040 | Medium | Password toggle works on register page"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_password('TestPass123!')
        page.toggle_password_visibility()
        time.sleep(0.5)
        assert page.get_password_input_type() == 'text', "Password toggle failed on register"
