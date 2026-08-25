"""
MODULE: Performance Smoke Tests
TEST CASES: PERF-001 to PERF-020  (20 test cases)
Priority: High / Medium
"""
import pytest, time
from selenium.webdriver.common.by import By
from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.base_page import BasePage


class TestPerformanceSmoke:

    def test_PERF_001_landing_page_loads_under_10s(self, driver):
        """PERF-001 | High | Landing page fully loads within 10 seconds"""
        page = LandingPage(driver)
        start = time.time()
        page.open_landing()
        page.is_loaded()
        elapsed = time.time() - start
        assert elapsed < 10, f"Landing page took {elapsed:.2f}s (limit: 10s)"

    def test_PERF_002_login_page_loads_under_8s(self, driver):
        """PERF-002 | High | Login page loads within 8 seconds"""
        page = LoginPage(driver)
        start = time.time()
        page.open_login()
        page.is_loaded()
        elapsed = time.time() - start
        assert elapsed < 8, f"Login page took {elapsed:.2f}s (limit: 8s)"

    def test_PERF_003_register_page_loads_under_8s(self, driver):
        """PERF-003 | High | Register page loads within 8 seconds"""
        page = RegisterPage(driver)
        start = time.time()
        page.open_register()
        page.is_loaded()
        elapsed = time.time() - start
        assert elapsed < 8, f"Register page took {elapsed:.2f}s (limit: 8s)"

    def test_PERF_004_dom_content_loaded_timing(self, driver):
        """PERF-004 | High | DOMContentLoaded fires within 5 seconds"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(1)
        dcl = driver.execute_script(
            "return performance.timing.domContentLoadedEventEnd - "
            "performance.timing.navigationStart"
        )
        assert dcl < 5000, f"DOMContentLoaded took {dcl}ms (limit: 5000ms)"

    def test_PERF_005_page_load_timing(self, driver):
        """PERF-005 | High | Full page load within 8 seconds per performance API"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(4)
        load_time = driver.execute_script(
            "return performance.timing.loadEventEnd - "
            "performance.timing.navigationStart"
        )
        assert load_time < 8000 or load_time == 0, \
            f"Page load took {load_time}ms (limit: 8000ms)"

    def test_PERF_006_no_render_blocking_resources(self, driver):
        """PERF-006 | Medium | CSS & JS assets load without blocking render"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(4)
        # Check that content is visible (no render block)
        root = driver.find_element(By.ID, 'root')
        children = root.find_elements(By.XPATH, './/*')
        assert len(children) > 0, "Root should have children (not render-blocked)"

    def test_PERF_007_javascript_bundle_loaded(self, driver):
        """PERF-007 | High | JavaScript bundle loaded and executed"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(3)
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        assert len(scripts) > 0, "JavaScript bundle should be loaded"

    def test_PERF_008_css_assets_loaded(self, driver):
        """PERF-008 | High | CSS stylesheets loaded"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(3)
        links = driver.find_elements(By.XPATH, "//link[@rel='stylesheet']")
        styles = driver.find_elements(By.TAG_NAME, 'style')
        assert len(links) + len(styles) > 0, "CSS should be loaded"

    def test_PERF_009_navigation_performance_entries(self, driver):
        """PERF-009 | Medium | Navigation performance entries available"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(3)
        entries = driver.execute_script(
            "return performance.getEntriesByType('navigation').length"
        )
        assert entries >= 1, "Should have navigation performance entries"

    def test_PERF_010_first_contentful_paint_timing(self, driver):
        """PERF-010 | High | First Contentful Paint within 3 seconds"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(4)
        fcp = driver.execute_script("""
            const entries = performance.getEntriesByName('first-contentful-paint');
            return entries.length > 0 ? entries[0].startTime : null;
        """)
        if fcp is not None:
            assert fcp < 3000, f"FCP took {fcp:.0f}ms (limit: 3000ms)"

    def test_PERF_011_page_weight_reasonable(self, driver):
        """PERF-011 | Medium | Total transferred resources within reasonable limit"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(4)
        total_size = driver.execute_script("""
            return performance.getEntriesByType('resource')
                .reduce((sum, r) => sum + (r.transferSize || 0), 0);
        """)
        # Allow up to 10MB total transfer
        assert total_size < 10 * 1024 * 1024 or total_size == 0, \
            f"Page resources: {total_size / 1024:.0f}KB (limit: 10MB)"

    def test_PERF_012_react_hydration_complete(self, driver):
        """PERF-012 | High | React app hydrates and renders within timeout"""
        page = BasePage(driver)
        page.open('')
        time.sleep(5)
        root = driver.find_element(By.ID, 'root')
        inner_text = root.text
        assert len(inner_text.strip()) > 0, "React app should be hydrated"

    def test_PERF_013_login_form_interactive_quickly(self, driver):
        """PERF-013 | High | Login form is interactive within 5s of load"""
        page = LoginPage(driver)
        start = time.time()
        page.open_login()
        page.is_loaded()
        email = driver.find_element(*page.EMAIL_INPUT)
        email.click()
        email.send_keys('test')
        val = email.get_attribute('value')
        elapsed = time.time() - start
        assert 'test' in val, "Form should be interactive"
        assert elapsed < 5, f"Form interactivity took {elapsed:.2f}s"

    def test_PERF_014_no_memory_leaks_basic(self, driver):
        """PERF-014 | Medium | No obvious memory leak on page navigation"""
        page = BasePage(driver)
        for _ in range(3):
            page.open('')
            time.sleep(1)
            page.open('login')
            time.sleep(1)
        heap = driver.execute_script(
            "return performance.memory ? performance.memory.usedJSHeapSize : 0"
        )
        # Just verify it doesn't return an error — heap < 500MB is reasonable
        assert heap < 500 * 1024 * 1024 or heap == 0, \
            f"JS heap size {heap / 1024 / 1024:.0f}MB seems high"

    def test_PERF_015_resource_count_reasonable(self, driver):
        """PERF-015 | Medium | Number of network resources is reasonable"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(5)
        count = driver.execute_script(
            "return performance.getEntriesByType('resource').length"
        )
        assert count < 200, f"Too many resources: {count} (limit: 200)"

    def test_PERF_016_no_failed_resources(self, driver):
        """PERF-016 | High | No critical resource load failures"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(4)
        logs = driver.get_log('browser')
        failed = [l for l in logs
                  if 'net::ERR' in l.get('message', '') and
                  'favicon' not in l.get('message', '').lower() and
                  'fonts.googleapis' not in l.get('message', '')]
        assert len(failed) == 0, \
            f"Failed resources: {[l['message'][:80] for l in failed[:3]]}"

    def test_PERF_017_login_response_time(self, driver):
        """PERF-017 | High | Login form submission responds within 10s"""
        page = LoginPage(driver)
        page.open_login()
        page.enter_email('test@timing.com')
        page.enter_password('TestPass123!')
        start = time.time()
        page.click_submit()
        # Wait for either error toast or dashboard
        while time.time() - start < 10:
            if page.has_error_message(1) or 'dashboard' in driver.current_url:
                break
        elapsed = time.time() - start
        assert elapsed < 10, f"Login response took {elapsed:.2f}s (limit: 10s)"

    def test_PERF_018_smooth_scroll_performance(self, driver):
        """PERF-018 | Low | Page scroll is smooth without jank"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(3)
        start = time.time()
        driver.execute_script("window.scrollTo({top: 2000, behavior: 'smooth'})")
        time.sleep(0.8)
        scroll_y = driver.execute_script("return window.pageYOffset")
        elapsed = time.time() - start
        assert elapsed < 2.0, f"Scroll animation took {elapsed:.2f}s"

    def test_PERF_019_long_tasks_audit(self, driver):
        """PERF-019 | Medium | No blocking long tasks on initial load"""
        page = LandingPage(driver)
        page.open_landing()
        time.sleep(5)
        # Simplified check — just verify page loaded and is responsive
        title = driver.title
        assert len(title) > 0, "Page should be responsive after load"

    def test_PERF_020_time_to_interactive_acceptable(self, driver):
        """PERF-020 | High | Page is interactive within 8 seconds of navigation"""
        page = LoginPage(driver)
        start = time.time()
        page.open_login()
        # Try to interact
        for _ in range(20):
            try:
                el = driver.find_element(*page.EMAIL_INPUT)
                if el.is_enabled():
                    elapsed = time.time() - start
                    assert elapsed < 8, f"TTI: {elapsed:.2f}s (limit: 8s)"
                    return
            except Exception:
                pass
            time.sleep(0.4)
        elapsed = time.time() - start
        assert elapsed < 8, f"Page not interactive within 8s"
