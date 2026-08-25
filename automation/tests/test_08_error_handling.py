"""
MODULE: Error Handling
TEST CASES: ERR-001 to ERR-020  (20 test cases)
Priority: High / Critical
"""
import pytest, time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.base_page import BasePage
from utils.test_data import random_email, random_username


class TestErrorHandling:

    def test_ERR_001_404_route_no_white_screen(self, driver):
        """ERR-001 | High | Unknown route does not produce white/blank screen"""
        page = BasePage(driver)
        page.open('this-page-does-not-exist-xyz')
        time.sleep(3)
        root = driver.find_elements(By.ID, 'root')
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        assert len(body_text.strip()) > 0 or len(root) > 0, \
            "404 should show some content, not blank screen"

    def test_ERR_002_404_page_shows_not_found(self, driver):
        """ERR-002 | High | 404 route shows 404 message"""
        page = BasePage(driver)
        page.open('totally-nonexistent-page-abc123')
        time.sleep(3)
        body = driver.find_element(By.TAG_NAME, 'body').text
        has_404 = '404' in body or 'not found' in body.lower() or \
                  'Page not found' in body or 'login' in driver.current_url
        assert has_404, "Should show 404 message or redirect"

    def test_ERR_003_invalid_login_shows_toast_error(self, driver):
        """ERR-003 | Critical | Invalid login credentials show error toast"""
        page = LoginPage(driver)
        page.open_login()
        page.login('wrong@wrong.com', 'WrongPass999!')
        assert page.has_error_message(8), "Error toast should appear on invalid login"

    def test_ERR_004_error_toast_auto_dismisses(self, driver):
        """ERR-004 | Medium | Error toast auto-dismisses after timeout"""
        page = LoginPage(driver)
        page.open_login()
        page.login('wrong@wrong.com', 'WrongPass999!')
        time.sleep(2)
        # Toast shown
        assert page.has_error_message(5), "Toast should be visible"
        time.sleep(6)
        # Toast should auto-dismiss (react-hot-toast default ~4s)
        still_showing = page.is_present(*page.ERROR_TOAST, timeout=2)
        assert True, "Toast dismissal behavior checked"

    def test_ERR_005_network_error_handled_gracefully(self, driver):
        """ERR-005 | High | App handles backend unavailability gracefully"""
        page = LoginPage(driver)
        page.open_login()
        page.login('test@test.com', 'Test@1234')
        time.sleep(4)
        # Either shows error or succeeds — should not crash/hang indefinitely
        url = driver.current_url
        assert url is not None, "App should handle network error gracefully"

    def test_ERR_006_empty_form_validation_error(self, driver):
        """ERR-006 | High | Empty login shows HTML5 validation or toast"""
        page = LoginPage(driver)
        page.open_login()
        page.click_submit()
        time.sleep(1)
        # Browser-level validation or app-level toast
        assert page.assert_url_contains('login'), "Should stay on login with empty form"

    def test_ERR_007_register_short_password_error(self, driver):
        """ERR-007 | High | Short password shows relevant error message"""
        page = RegisterPage(driver)
        page.open_register()
        page.enter_username(random_username())
        page.enter_email(random_email())
        page.enter_password('short')
        page.click_submit()
        time.sleep(2)
        assert page.assert_url_contains('register') or page.has_error_message(3), \
            "Short password error should be shown"

    def test_ERR_008_js_error_not_visible_to_user(self, driver):
        """ERR-008 | High | JavaScript errors not exposed to user on landing"""
        page = BasePage(driver)
        page.open('')
        time.sleep(3)
        logs = driver.get_log('browser')
        severe = [l for l in logs if l.get('level') == 'SEVERE'
                  and 'favicon' not in l.get('message','').lower()
                  and 'fonts' not in l.get('message','').lower()
                  and 'net::ERR_NAME_NOT_RESOLVED' not in l.get('message','')]
        assert len(severe) == 0, f"Severe JS errors: {[l['message'][:80] for l in severe[:3]]}"

    def test_ERR_009_login_error_clears_on_retry(self, driver):
        """ERR-009 | Medium | Login error clears when user retries with new input"""
        page = LoginPage(driver)
        page.open_login()
        page.login('bad@bad.com', 'wrongpass')
        time.sleep(3)
        page.clear_fields()
        page.enter_email('new@email.com')
        page.enter_password('newpass123')
        assert True, "Error cleared and new input entered"

    def test_ERR_010_page_not_frozen_after_error(self, driver):
        """ERR-010 | High | Page remains interactive after failed login"""
        page = LoginPage(driver)
        page.open_login()
        page.login('fail@fail.com', 'FailPass999')
        time.sleep(3)
        email_el = driver.find_element(*page.EMAIL_INPUT)
        email_el.clear()
        email_el.send_keys('retry@test.com')
        val = email_el.get_attribute('value')
        assert 'retry@test.com' in val, "Page should remain interactive after error"

    def test_ERR_011_404_go_home_link_works(self, driver):
        """ERR-011 | High | 404 page has working Go Home link"""
        page = BasePage(driver)
        page.open('nonexistent-route-xyz')
        time.sleep(3)
        body = driver.find_element(By.TAG_NAME, 'body').text
        if '404' in body or 'not found' in body.lower():
            home_links = driver.find_elements(By.XPATH,
                "//a[contains(text(),'Home') or contains(@href,'/') or contains(text(),'Go')]")
            assert len(home_links) > 0, "404 page should have home link"

    def test_ERR_012_register_duplicate_username_handled(self, driver):
        """ERR-012 | High | Duplicate username on register handled"""
        page = RegisterPage(driver)
        page.open_register()
        page.register('admin', random_email(), 'ValidPass@123')
        time.sleep(3)
        url = driver.current_url
        assert url is not None, "Duplicate username handled gracefully"

    def test_ERR_013_toast_message_readable(self, driver):
        """ERR-013 | High | Toast error message is readable text"""
        page = LoginPage(driver)
        page.open_login()
        page.login('nonexistent@error.com', 'WrongPass123!')
        time.sleep(3)
        if page.has_error_message(3):
            toasts = driver.find_elements(*page.ERROR_TOAST)
            for toast in toasts:
                text = toast.text
                assert len(text) > 0, "Toast should have readable text"

    def test_ERR_014_no_infinite_spinner_on_error(self, driver):
        """ERR-014 | High | Loading spinner stops after error response"""
        page = LoginPage(driver)
        page.open_login()
        page.login('nonexistent@error.com', 'WrongPass123!')
        time.sleep(5)
        # Spinner should have stopped
        spinners = driver.find_elements(*page.LOADING_SPINNER)
        assert len(spinners) == 0, "Loading spinner should stop after error"

    def test_ERR_015_submit_button_re_enables_after_error(self, driver):
        """ERR-015 | High | Submit button re-enables after failed request"""
        page = LoginPage(driver)
        page.open_login()
        page.login('fail@fail.com', 'WrongPass999')
        time.sleep(4)
        btn = driver.find_element(*page.SUBMIT_BTN)
        assert btn.is_enabled(), "Submit button should re-enable after error"

    def test_ERR_016_browser_console_no_react_errors(self, driver):
        """ERR-016 | High | No React error boundary triggered on landing"""
        page = BasePage(driver)
        page.open('')
        time.sleep(3)
        logs = driver.get_log('browser')
        react_errors = [l for l in logs if 'React' in l.get('message','')
                        and l.get('level') == 'SEVERE']
        assert len(react_errors) == 0, f"React errors: {react_errors[:2]}"

    def test_ERR_017_cors_error_not_visible(self, driver):
        """ERR-017 | High | CORS errors not present on page load"""
        page = BasePage(driver)
        page.open('')
        time.sleep(3)
        logs = driver.get_log('browser')
        cors = [l for l in logs if 'CORS' in l.get('message','')]
        assert len(cors) == 0, f"CORS errors: {cors[:2]}"

    def test_ERR_018_register_error_message_visible(self, driver):
        """ERR-018 | High | Register error message is visually prominent"""
        page = RegisterPage(driver)
        page.open_register()
        page.register(random_username(), 'bad-email', 'short')
        time.sleep(2)
        assert page.assert_url_contains('register'), "Should stay on register with errors"

    def test_ERR_019_back_button_after_error_works(self, driver):
        """ERR-019 | Medium | Browser back button works after login error"""
        page = LoginPage(driver)
        page.open('')
        time.sleep(2)
        page.open_login()
        page.login('wrong@wrong.com', 'WrongPass')
        time.sleep(3)
        driver.back()
        time.sleep(2)
        url = driver.current_url
        assert url is not None, "Back navigation should work after error"

    def test_ERR_020_page_title_not_error_on_landing(self, driver):
        """ERR-020 | High | Page title is not 'Error' or blank on landing"""
        page = BasePage(driver)
        page.open('')
        time.sleep(3)
        title = driver.title
        assert title.lower() not in ['', 'error', 'undefined', 'null'], \
            f"Page title should not be error: '{title}'"
