"""Page Object — Analytics Page (/analytics)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class AnalyticsPage(BasePage):
    HEADING             = (By.XPATH, "//h1[contains(text(),'Analytics') or contains(text(),'analytic')]")
    OVERVIEW_CARDS      = (By.XPATH, "//*[contains(@class,'glass-card') or contains(@class,'card-hover')]")
    WIN_RATE_CARD       = (By.XPATH, "//*[contains(text(),'Win Rate')]")
    LOGIC_SCORE_CARD    = (By.XPATH, "//*[contains(text(),'Logic Score')]")
    STREAK_CARD         = (By.XPATH, "//*[contains(text(),'Streak')]")
    XP_CARD             = (By.XPATH, "//*[contains(text(),'XP') or contains(text(),'Experience')]")
    TIER_BADGE          = (By.XPATH, "//*[contains(text(),'Tier') or contains(text(),'tier')]")
    SKILL_RADAR         = (By.XPATH, "//*[contains(text(),'Skill') or contains(text(),'Assessment')]")
    LOGIC_TREND_CHART   = (By.XPATH, "//*[contains(text(),'Logic Score Trend') or contains(text(),'Trend')]")
    FALLACY_CHART       = (By.XPATH, "//*[contains(text(),'Fallacy Breakdown') or contains(text(),'Breakdown')]")
    RECENT_DEBATES      = (By.XPATH, "//*[contains(text(),'Recent Debates')]")
    RECHARTS            = (By.XPATH, "//*[contains(@class,'recharts')]")
    LOADING_SPINNER     = (By.XPATH, "//*[contains(@class,'animate-spin')]")
    XP_BAR              = (By.XPATH, "//*[contains(@class,'score-bar') or contains(@class,'score-fill')]")
    BODY                = (By.TAG_NAME, 'body')

    def open_analytics(self):
        return self.open('analytics')

    def is_loaded(self) -> bool:
        self.wait_for_element_disappear(*self.LOADING_SPINNER, timeout=15)
        return self.is_present(*self.HEADING, timeout=15)

    def has_overview_cards(self) -> bool:
        return self.count_elements(*self.OVERVIEW_CARDS) > 0

    def has_win_rate(self) -> bool:
        return self.is_present(*self.WIN_RATE_CARD, timeout=8)

    def has_logic_score(self) -> bool:
        return self.is_present(*self.LOGIC_SCORE_CARD, timeout=8)

    def has_streak(self) -> bool:
        return self.is_present(*self.STREAK_CARD, timeout=8)

    def has_tier_badge(self) -> bool:
        return self.is_present(*self.TIER_BADGE, timeout=8)

    def has_charts(self) -> bool:
        return self.is_present(*self.RECHARTS, timeout=10)

    def has_skill_section(self) -> bool:
        return self.is_present(*self.SKILL_RADAR, timeout=8)

    def has_logic_trend(self) -> bool:
        return self.is_present(*self.LOGIC_TREND_CHART, timeout=8)

    def has_xp_bar(self) -> bool:
        return self.is_present(*self.XP_BAR, timeout=8)

    def count_overview_cards(self) -> int:
        return self.count_elements(*self.OVERVIEW_CARDS)
