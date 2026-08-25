"""Page Object — Navbar (shared component)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class Navbar(BasePage):
    NAV                 = (By.TAG_NAME, 'nav')
    LOGO                = (By.XPATH, "//nav//a[1] | //header//a[contains(@href,'/')]")
    DASHBOARD_LINK      = (By.XPATH, "//nav//a[contains(@href,'/dashboard')]")
    LEARN_LINK          = (By.XPATH, "//nav//a[contains(@href,'/learn')]")
    ANALYTICS_LINK      = (By.XPATH, "//nav//a[contains(@href,'/analytics')]")
    PROFILE_LINK        = (By.XPATH, "//nav//a[contains(@href,'/profile')]")
    LOGOUT_BTN          = (By.XPATH, "//button[contains(text(),'Logout') or contains(text(),'Sign Out') or contains(text(),'Log out')]")
    DEBATE_BTN          = (By.XPATH, "//nav//a[contains(@href,'/debate')] | //nav//button[contains(text(),'Debate')]")
    MOBILE_MENU_BTN     = (By.XPATH, "//button[contains(@aria-label,'menu') or .//*[contains(@class,'lucide-menu')]]")
    MOBILE_MENU         = (By.XPATH, "//*[contains(@class,'mobile-menu') or contains(@class,'dropdown')]")
    NEW_DEBATE_NAV      = (By.XPATH, "//nav//*[contains(text(),'New Debate') or contains(text(),'Start')]")
    LANDING_LOGIN       = (By.XPATH, "//a[contains(@href,'/login')] | //button[contains(text(),'Sign')]")

    def is_visible(self) -> bool:
        return self.is_present(*self.NAV, timeout=8)

    def click_logo(self):
        self.click(*self.LOGO)
        return self

    def click_dashboard(self):
        self.click(*self.DASHBOARD_LINK)
        return self

    def click_learn(self):
        self.click(*self.LEARN_LINK)
        return self

    def click_analytics(self):
        self.click(*self.ANALYTICS_LINK)
        return self

    def click_profile(self):
        self.click(*self.PROFILE_LINK)
        return self

    def click_logout(self):
        if self.is_present(*self.LOGOUT_BTN, timeout=5):
            self.click(*self.LOGOUT_BTN)
        return self

    def has_dashboard_link(self) -> bool:
        return self.is_present(*self.DASHBOARD_LINK, timeout=8)

    def has_learn_link(self) -> bool:
        return self.is_present(*self.LEARN_LINK, timeout=8)

    def has_analytics_link(self) -> bool:
        return self.is_present(*self.ANALYTICS_LINK, timeout=8)

    def has_profile_link(self) -> bool:
        return self.is_present(*self.PROFILE_LINK, timeout=8)

    def click_mobile_menu(self):
        if self.is_present(*self.MOBILE_MENU_BTN, timeout=5):
            self.click(*self.MOBILE_MENU_BTN)
        return self

    def is_logout_present(self) -> bool:
        return self.is_present(*self.LOGOUT_BTN, timeout=5)
