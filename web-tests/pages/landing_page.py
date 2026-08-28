"""Page Object — Landing Page (/)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LandingPage(BasePage):
    # Locators
    TITLE_HEADING       = (By.TAG_NAME, 'h1')
    NAV_BAR             = (By.TAG_NAME, 'nav')
    GET_STARTED_BTN     = (By.XPATH, "//a[contains(@href,'/register') or contains(text(),'Get Started') or contains(text(),'Start')]")
    SIGN_IN_LINK        = (By.XPATH, "//a[contains(@href,'/login') or contains(text(),'Sign In') or contains(text(),'Log in')]")
    HERO_SECTION        = (By.XPATH, "//*[contains(@class,'hero') or contains(@id,'hero')]")
    FEATURES_SECTION    = (By.XPATH, "//*[contains(@id,'features') or contains(@class,'features')]")
    PRICING_SECTION     = (By.XPATH, "//*[contains(@id,'pricing') or contains(@class,'pricing')]")
    CTA_SECTION         = (By.XPATH, "//*[contains(@class,'cta') or contains(@id,'cta')]")
    FOOTER              = (By.TAG_NAME, 'footer')
    BODY                = (By.TAG_NAME, 'body')
    ANY_HEADING         = (By.XPATH, "//h1|//h2|//h3")
    ROOT_DIV            = (By.ID, 'root')
    LOGO_LINK           = (By.XPATH, "//a[contains(@href,'/')] | //a[contains(@class,'logo')]")
    DEBATE_TEXT         = (By.XPATH, "//*[contains(text(),'Debate') or contains(text(),'debate')]")
    AI_TEXT             = (By.XPATH, "//*[contains(text(),'AI') or contains(text(),'Artificial')]")
    FALLACY_TEXT        = (By.XPATH, "//*[contains(text(),'Fallac') or contains(text(),'fallac')]")
    FREE_PLAN_BTN       = (By.XPATH, "//*[contains(text(),'Free') or contains(text(),'free')]")
    PRO_PLAN_BTN        = (By.XPATH, "//*[contains(text(),'Pro') or contains(text(),'pro')]")

    def open_landing(self):
        return self.open('')

    def is_loaded(self) -> bool:
        self.wait_for_title_contains('Debate')
        return self.is_present(*self.ROOT_DIV, timeout=15)

    def has_navbar(self) -> bool:
        return self.is_present(*self.NAV_BAR, timeout=8)

    def has_hero_content(self) -> bool:
        return self.is_present(*self.TITLE_HEADING, timeout=10)

    def has_footer(self) -> bool:
        self.scroll_to_bottom()
        return self.is_present(*self.FOOTER, timeout=8)

    def click_get_started(self):
        self.click(*self.GET_STARTED_BTN)
        return self

    def click_sign_in(self):
        self.click(*self.SIGN_IN_LINK)
        return self

    def has_page_text(self, text: str) -> bool:
        return self.assert_text_present(text)

    def get_heading_text(self) -> str:
        return self.get_text(*self.TITLE_HEADING)

    def page_title_is_set(self) -> bool:
        return len(self.get_title()) > 0

    def scroll_to_features(self):
        self.execute_script("document.querySelector('[id*=features],[class*=features]')?.scrollIntoView()")
        self.sleep(0.5)

    def scroll_to_pricing(self):
        self.execute_script("document.querySelector('[id*=pricing],[class*=pricing]')?.scrollIntoView()")
        self.sleep(0.5)

    def count_headings(self) -> int:
        return self.count_elements(*self.ANY_HEADING)

    def has_debate_content(self) -> bool:
        return self.is_present(*self.DEBATE_TEXT, timeout=10)

    def no_js_errors(self) -> bool:
        logs = self.get_console_logs()
        errors = [l for l in logs if l.get('level') == 'SEVERE']
        return len(errors) == 0
