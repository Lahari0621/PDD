"""Page Object — Dashboard Page (/dashboard)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class DashboardPage(BasePage):
    HEADING             = (By.XPATH, "//h1[contains(text(),'Welcome') or contains(text(),'Dashboard')]")
    USERNAME_TEXT       = (By.XPATH, "//*[contains(@class,'gradient-text') or contains(@class,'font-black')]")
    NEW_DEBATE_BTN      = (By.XPATH, "//a[contains(@href,'/debate') or contains(text(),'New Debate') or contains(text(),'Debate')]")
    STAT_CARDS          = (By.XPATH, "//*[contains(@class,'glass-card') or contains(@class,'stat')]")
    TOTAL_DEBATES       = (By.XPATH, "//*[contains(text(),'Total Debates') or contains(text(),'Debates')]")
    WIN_RATE            = (By.XPATH, "//*[contains(text(),'Win Rate') or contains(text(),'Win')]")
    LOGIC_SCORE         = (By.XPATH, "//*[contains(text(),'Logic Score') or contains(text(),'Logic')]")
    FALLACIES_DETECTED  = (By.XPATH, "//*[contains(text(),'Fallacies') or contains(text(),'Detected')]")
    XP_BAR              = (By.XPATH, "//*[contains(@class,'score-bar') or contains(@class,'xp')]")
    SKILL_RADAR         = (By.XPATH, "//*[contains(text(),'Skill') or contains(text(),'Radar')]")
    RECENT_DEBATES      = (By.XPATH, "//*[contains(text(),'Recent Debates') or contains(text(),'Recent')]")
    LEARN_LINK          = (By.XPATH, "//a[contains(@href,'/learn') or contains(text(),'Learn')]")
    ANALYTICS_LINK      = (By.XPATH, "//a[contains(@href,'/analytics') or contains(text(),'Analytics')]")
    NAVBAR              = (By.TAG_NAME, 'nav')
    BODY                = (By.TAG_NAME, 'body')
    CHARTS_AREA         = (By.XPATH, "//*[contains(@class,'recharts') or contains(@class,'chart')]")
    COACHING_TIP        = (By.XPATH, "//*[contains(text(),'Coach') or contains(text(),'coach') or contains(text(),'Tip')]")
    SUGGESTED_TOPICS    = (By.XPATH, "//*[contains(text(),'Suggested') or contains(text(),'Topics')]")
    LEVEL_TEXT          = (By.XPATH, "//*[contains(text(),'Level')]")
    STREAK_TEXT         = (By.XPATH, "//*[contains(text(),'streak') or contains(text(),'Streak')]")
    TIER_TEXT           = (By.XPATH, "//*[contains(text(),'Bronze') or contains(text(),'Silver') or contains(text(),'Gold') or contains(text(),'Platinum') or contains(text(),'Diamond')]")
    ROOT                = (By.ID, 'root')

    def open_dashboard(self):
        return self.open('dashboard')

    def is_loaded(self) -> bool:
        return self.is_present(*self.ROOT, timeout=15) and self.wait_for_url_contains('dashboard', 12)

    def has_welcome_message(self) -> bool:
        return self.assert_text_present('Welcome')

    def has_stats(self) -> bool:
        return self.is_present(*self.STAT_CARDS, timeout=8)

    def click_new_debate(self):
        self.click(*self.NEW_DEBATE_BTN)
        return self

    def click_learn(self):
        self.click(*self.LEARN_LINK)
        return self

    def click_analytics(self):
        self.click(*self.ANALYTICS_LINK)
        return self

    def count_stat_cards(self) -> int:
        return self.count_elements(*self.STAT_CARDS)

    def has_navbar(self) -> bool:
        return self.is_present(*self.NAVBAR, timeout=8)

    def has_xp_bar(self) -> bool:
        return self.is_present(*self.XP_BAR, timeout=8)

    def has_recent_debates_section(self) -> bool:
        return self.is_present(*self.RECENT_DEBATES, timeout=8)

    def has_charts(self) -> bool:
        return self.is_present(*self.CHARTS_AREA, timeout=10)

    def has_level_info(self) -> bool:
        return self.is_present(*self.LEVEL_TEXT, timeout=8)

    def is_not_on_login(self) -> bool:
        return 'login' not in self.get_current_url()

    def get_page_content(self) -> str:
        return self.get_text(*self.BODY)
