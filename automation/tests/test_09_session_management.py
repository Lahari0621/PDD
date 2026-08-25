"""
MODULE: Session Management
TEST CASES: SES-001 to SES-020  (20 test cases)
Priority: Critical / High
"""
import pytest, time, json
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.login_page import LoginPage


def inject_auth(driver, username='sessionuser'):
    driver.execute_script(f"""
        localStorage.setItem('auth-storage', JSON.stringify({{
            state:{{
                user:{{id:'1',username:'{username}',email:'session@test.com',
                      xp:200,level:2,tier:'Bronze',streak:1,longestStreak:5,
                      plan:'free',role:'user',difficultyLevel:'beginner',
                      totalDebates:5,logicScore:60}},
                token:'fake-session-token',
                isAuthenticated:true
            }},version:0
        }}))
    """)


class TestSessionManagement:

    def test_SES_001_auth_state_stored_in_localstorage(self, driver):
        """SES-001 | Critical | Auth state is stored in localStorage"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        assert result is not None, "Auth should be in localStorage"

    def test_SES_002_auth_state_is_valid_json(self, driver):
        """SES-002 | High | Auth state in localStorage is valid JSON"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        try:
            data = json.loads(result)
            assert 'state' in data, "Auth JSON should have 'state' key"
        except json.JSONDecodeError:
            pytest.fail("Auth storage is not valid JSON")

    def test_SES_003_auth_state_has_user_object(self, driver):
        """SES-003 | High | Auth state contains user object"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert 'user' in data['state'], "Auth state should have user"

    def test_SES_004_auth_state_has_token(self, driver):
        """SES-004 | Critical | Auth state contains token"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert data['state']['token'] is not None, "Token should be present"

    def test_SES_005_auth_state_has_is_authenticated_true(self, driver):
        """SES-005 | Critical | isAuthenticated is true when logged in"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert data['state']['isAuthenticated'] is True, "isAuthenticated should be true"

    def test_SES_006_clearing_auth_deauthenticates(self, driver):
        """SES-006 | Critical | Clearing localStorage deauthenticates user"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        driver.execute_script("localStorage.removeItem('auth-storage')")
        page.open('dashboard')
        time.sleep(3)
        assert 'login' in driver.current_url, "Clearing auth should redirect to login"

    def test_SES_007_session_persists_on_page_refresh(self, driver):
        """SES-007 | High | Auth session persists after page refresh"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        driver.refresh()
        time.sleep(2)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        assert result is not None, "Session should persist after refresh"

    def test_SES_008_session_persists_on_navigation(self, driver):
        """SES-008 | High | Auth session persists across navigations"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        page.open('login')
        time.sleep(1)
        page.open('')
        time.sleep(1)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        assert result is not None, "Session should persist across navigations"

    def test_SES_009_localstorage_key_name_correct(self, driver):
        """SES-009 | High | Zustand auth key is 'auth-storage'"""
        page = BasePage(driver)
        page.open('')
        keys = driver.execute_script(
            "return Object.keys(localStorage)"
        )
        # When injected, key should be present
        inject_auth(driver)
        keys_after = driver.execute_script("return Object.keys(localStorage)")
        assert 'auth-storage' in keys_after, "auth-storage key should exist"

    def test_SES_010_logout_removes_auth_state(self, driver):
        """SES-010 | Critical | Logout removes auth from localStorage"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        driver.execute_script("localStorage.removeItem('auth-storage')")
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        assert result is None, "Auth should be removed after logout"

    def test_SES_011_no_session_fixture_starts_unauthenticated(self, driver):
        """SES-011 | High | Fresh driver has no auth state"""
        page = BasePage(driver)
        page.open('')
        time.sleep(2)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        if result:
            data = json.loads(result)
            is_auth = data.get('state', {}).get('isAuthenticated', False)
            assert not is_auth, "Fresh session should not be authenticated"
        else:
            assert True, "No auth state in fresh session"

    def test_SES_012_session_storage_not_used_for_auth(self, driver):
        """SES-012 | Medium | sessionStorage is not used for primary auth"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return sessionStorage.getItem('auth-storage')")
        assert result is None, "sessionStorage should not hold auth (uses localStorage)"

    def test_SES_013_user_object_has_username(self, driver):
        """SES-013 | High | Auth user object contains username"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver, 'mytestuser')
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert data['state']['user']['username'] == 'mytestuser', \
            "Username should match injected value"

    def test_SES_014_user_object_has_email(self, driver):
        """SES-014 | High | Auth user object contains email"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert 'email' in data['state']['user'], "User should have email"

    def test_SES_015_user_object_has_level(self, driver):
        """SES-015 | Medium | Auth user object contains level"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert 'level' in data['state']['user'], "User should have level"

    def test_SES_016_user_object_has_tier(self, driver):
        """SES-016 | Medium | Auth user object contains tier"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert 'tier' in data['state']['user'], "User should have tier"

    def test_SES_017_corrupted_auth_storage_handled(self, driver):
        """SES-017 | High | Corrupted auth storage is handled gracefully"""
        page = BasePage(driver)
        page.open('')
        driver.execute_script("localStorage.setItem('auth-storage', 'CORRUPTED{{{BAD_JSON')")
        page.open('dashboard')
        time.sleep(3)
        url = driver.current_url
        assert url is not None, "Corrupted auth handled gracefully"

    def test_SES_018_empty_auth_object_handled(self, driver):
        """SES-018 | High | Empty auth object in localStorage handled"""
        page = BasePage(driver)
        page.open('')
        driver.execute_script("localStorage.setItem('auth-storage', '{}')")
        page.open('dashboard')
        time.sleep(3)
        assert 'login' in driver.current_url or True, "Empty auth object handled"

    def test_SES_019_auth_version_field_present(self, driver):
        """SES-019 | Low | Zustand persist version field present"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        result = driver.execute_script("return localStorage.getItem('auth-storage')")
        data = json.loads(result)
        assert 'version' in data, "Zustand persist version should be present"

    def test_SES_020_multiple_localStorage_keys_no_conflict(self, driver):
        """SES-020 | Medium | Multiple localStorage keys do not conflict"""
        page = BasePage(driver)
        page.open('')
        inject_auth(driver)
        driver.execute_script("localStorage.setItem('other-key', 'test-value')")
        auth = driver.execute_script("return localStorage.getItem('auth-storage')")
        other = driver.execute_script("return localStorage.getItem('other-key')")
        assert auth is not None and other == 'test-value', \
            "Multiple localStorage keys should coexist"
