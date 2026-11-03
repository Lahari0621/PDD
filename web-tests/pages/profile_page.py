"""Page Object — Profile Page (/profile)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProfilePage(BasePage):
    AVATAR              = (By.XPATH, "//*[contains(@class,'rounded-3xl') and contains(@class,'bg-gradient')]")
    USERNAME_DISPLAY    = (By.XPATH, "//h1[contains(@class,'font-display') or contains(@class,'font-black')]")
    EMAIL_DISPLAY       = (By.XPATH, "//*[contains(@class,'text-slate-400') and contains(text(),'@')]")
    EDIT_BTN            = (By.XPATH, "//button[.//*[contains(@class,'lucide-edit')]] | //button[contains(@title,'Edit')]")
    USERNAME_INPUT      = (By.XPATH, "//input[contains(@class,'text-lg') or contains(@class,'font-bold')]")
    BIO_TEXTAREA        = (By.XPATH, "//textarea[@placeholder]")
    SAVE_BTN            = (By.XPATH, "//button[contains(text(),'Save')]")
    CANCEL_BTN          = (By.XPATH, "//button[contains(text(),'Cancel')]")
    STATS_SECTION       = (By.XPATH, "//*[contains(@class,'glass-card') and .//*[contains(text(),'Debates') or contains(text(),'Wins')]]")
    DEBATES_STAT        = (By.XPATH, "//*[contains(text(),'Debates')]")
    WINS_STAT           = (By.XPATH, "//*[contains(text(),'Wins')]")
    LOGIC_STAT          = (By.XPATH, "//*[contains(text(),'Logic Score')]")
    STREAK_STAT         = (By.XPATH, "//*[contains(text(),'Streak')]")
    XP_PROGRESS         = (By.XPATH, "//*[contains(@class,'score-bar') or contains(@class,'score-fill')]")
    ACHIEVEMENTS_SECTION= (By.XPATH, "//*[contains(text(),'Achievement')]")
    ACHIEVEMENT_CARDS   = (By.XPATH, "//*[contains(@class,'rounded-xl') and .//*[contains(text(),'Unlocked') or contains(@class,'border-warning')]]")
    TIER_DISPLAY        = (By.XPATH, "//*[contains(text(),'Tier') or contains(text(),'Bronze') or contains(text(),'Silver') or contains(text(),'Gold')]")
    PLAN_DISPLAY        = (By.XPATH, "//*[contains(text(),'plan') or contains(text(),'free') or contains(text(),'pro')]")
    TOAST_SUCCESS       = (By.XPATH, "//*[contains(@class,'toast') or contains(text(),'updated')]")
    TOAST_ERROR         = (By.XPATH, "//*[contains(@class,'toast') and contains(@class,'error')]")
    LEVEL_DISPLAY       = (By.XPATH, "//*[contains(text(),'Level')]")

    def open_profile(self):
        return self.open('profile')

    def is_loaded(self) -> bool:
        return self.is_present(*self.AVATAR, timeout=15)

    def click_edit(self):
        if self.is_present(*self.EDIT_BTN, timeout=5):
            self.click(*self.EDIT_BTN)
        return self

    def update_username(self, username: str):
        if self.is_present(*self.USERNAME_INPUT, timeout=5):
            el = self.find(*self.USERNAME_INPUT)
            el.clear()
            el.send_keys(username)
        return self

    def update_bio(self, bio: str):
        if self.is_present(*self.BIO_TEXTAREA, timeout=5):
            el = self.find(*self.BIO_TEXTAREA)
            el.clear()
            el.send_keys(bio)
        return self

    def click_save(self):
        self.click(*self.SAVE_BTN)
        return self

    def click_cancel(self):
        self.click(*self.CANCEL_BTN)
        return self

    def has_stats(self) -> bool:
        return self.is_present(*self.DEBATES_STAT, timeout=8)

    def has_achievements(self) -> bool:
        return self.is_present(*self.ACHIEVEMENTS_SECTION, timeout=8)

    def has_xp_progress(self) -> bool:
        return self.is_present(*self.XP_PROGRESS, timeout=8)

    def has_tier(self) -> bool:
        return self.is_present(*self.TIER_DISPLAY, timeout=8)

    def has_level(self) -> bool:
        return self.is_present(*self.LEVEL_DISPLAY, timeout=8)

    def count_unlocked_achievements(self) -> int:
        return self.count_elements(*self.ACHIEVEMENT_CARDS)

    def save_successful(self) -> bool:
        return self.is_present(*self.TOAST_SUCCESS, timeout=8)
