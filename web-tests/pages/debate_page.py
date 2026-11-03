"""Page Object — Debate Page (/debate)"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class DebatePage(BasePage):
    # Setup mode
    SETUP_HEADING       = (By.XPATH, "//h1[contains(text(),'Start') or contains(text(),'Debate') or contains(text(),'Configure')]")
    TOPIC_TEXTAREA      = (By.XPATH, "//textarea[@placeholder or @name='topic'] | //textarea[1]")
    POSITION_INPUT      = (By.XPATH, "//input[@placeholder[contains(.,'Position') or contains(.,'position') or contains(.,'argue')]]")
    DIFFICULTY_BEGINNER = (By.XPATH, "//button[contains(text(),'beginner') or contains(text(),'Beginner')]")
    DIFFICULTY_INTER    = (By.XPATH, "//button[contains(text(),'intermediate') or contains(text(),'Intermediate')]")
    DIFFICULTY_ADVANCED = (By.XPATH, "//button[contains(text(),'advanced') or contains(text(),'Advanced')]")
    DIFFICULTY_EXPERT   = (By.XPATH, "//button[contains(text(),'expert') or contains(text(),'Expert')]")
    AI_PERSONALITY_OPTS = (By.XPATH, "//button[.//div[@class]]")
    BEGIN_BTN           = (By.XPATH, "//button[contains(text(),'Begin') or contains(text(),'Start Debate') or contains(text(),'begin')]")
    LOADING_SPINNER     = (By.XPATH, "//*[contains(@class,'animate-spin')]")

    # Active debate
    BACK_BTN            = (By.XPATH, "//button[.//*[contains(@class,'lucide-arrow-left')] or contains(@class,'back')]")
    PAUSE_BTN           = (By.XPATH, "//button[.//*[contains(@class,'lucide-pause')]]")
    PLAY_BTN            = (By.XPATH, "//button[.//*[contains(@class,'lucide-play')]]")
    END_BTN             = (By.XPATH, "//button[contains(text(),'End') or .//*[contains(@class,'lucide-square')]]")
    MESSAGE_INPUT       = (By.XPATH, "//textarea[@placeholder[contains(.,'argument') or contains(.,'Argument') or contains(.,'message')]]")
    SEND_BTN            = (By.XPATH, "//button[.//*[contains(@class,'lucide-send')]]")
    MESSAGES_LIST       = (By.XPATH, "//*[contains(@class,'justify-end') or contains(@class,'justify-start')]")
    AI_BADGE            = (By.XPATH, "//*[contains(text(),'Aria') or contains(text(),'AI Coach')]")
    FALLACY_BADGE       = (By.XPATH, "//*[contains(@class,'fallacy') or .//*[contains(@class,'lucide-alert-triangle')]]")
    TURN_COUNT          = (By.XPATH, "//*[contains(text(),'Turn')]")
    PAUSED_INDICATOR    = (By.XPATH, "//*[contains(text(),'Paused') or contains(text(),'paused')]")
    LIVE_INDICATOR      = (By.XPATH, "//*[contains(text(),'Live') or contains(text(),'live')]")
    CHAR_COUNTER        = (By.XPATH, "//*[contains(text(),'/1000')]")

    # Summary
    SUMMARY_HEADING     = (By.XPATH, "//h2[contains(text(),'Debate Complete') or contains(text(),'Complete')]")
    NEW_DEBATE_BTN      = (By.XPATH, "//button[contains(text(),'New Debate')]")
    GO_DASHBOARD_BTN    = (By.XPATH, "//button[contains(text(),'Dashboard')]")
    FINAL_SCORE         = (By.XPATH, "//*[contains(text(),'Final Score')]")
    XP_EARNED           = (By.XPATH, "//*[contains(text(),'XP')]")
    TOPIC_DISPLAY       = (By.XPATH, "//*[contains(@class,'topic') or contains(@class,'truncate')]")

    def open_debate(self):
        return self.open('debate')

    def is_setup_loaded(self) -> bool:
        return self.is_present(*self.SETUP_HEADING, timeout=15)

    def enter_topic(self, topic: str):
        el = self.find(*self.TOPIC_TEXTAREA)
        el.clear()
        el.send_keys(topic)
        return self

    def enter_position(self, position: str):
        if self.is_present(*self.POSITION_INPUT, timeout=5):
            el = self.find(*self.POSITION_INPUT)
            el.clear()
            el.send_keys(position)
        return self

    def select_difficulty(self, level: str = 'intermediate'):
        locs = {
            'beginner':     self.DIFFICULTY_BEGINNER,
            'intermediate': self.DIFFICULTY_INTER,
            'advanced':     self.DIFFICULTY_ADVANCED,
            'expert':       self.DIFFICULTY_EXPERT,
        }
        loc = locs.get(level.lower(), self.DIFFICULTY_INTER)
        if self.is_present(*loc, timeout=5):
            self.click(*loc)
        return self

    def click_begin(self):
        self.click(*self.BEGIN_BTN)
        return self

    def start_debate(self, topic: str, difficulty: str = 'intermediate'):
        self.enter_topic(topic)
        self.select_difficulty(difficulty)
        self.click_begin()
        return self

    def type_message(self, text: str):
        el = self.find(*self.MESSAGE_INPUT)
        el.clear()
        el.send_keys(text)
        return self

    def send_message(self):
        self.click(*self.SEND_BTN)
        return self

    def send_message_with_enter(self):
        el = self.find(*self.MESSAGE_INPUT)
        el.send_keys(Keys.RETURN)
        return self

    def click_pause(self):
        if self.is_present(*self.PAUSE_BTN, timeout=5):
            self.click(*self.PAUSE_BTN)
        return self

    def click_play(self):
        if self.is_present(*self.PLAY_BTN, timeout=5):
            self.click(*self.PLAY_BTN)
        return self

    def click_end(self):
        self.click(*self.END_BTN)
        return self

    def click_back(self):
        self.click(*self.BACK_BTN)
        return self

    def is_debate_active(self) -> bool:
        return self.is_present(*self.MESSAGE_INPUT, timeout=12)

    def is_paused(self) -> bool:
        return self.is_present(*self.PAUSED_INDICATOR, timeout=5)

    def has_ai_response(self) -> bool:
        return self.is_present(*self.AI_BADGE, timeout=15)

    def has_fallacy_detected(self) -> bool:
        return self.is_present(*self.FALLACY_BADGE, timeout=8)

    def is_summary_shown(self) -> bool:
        return self.is_present(*self.SUMMARY_HEADING, timeout=30)

    def click_new_debate(self):
        self.click(*self.NEW_DEBATE_BTN)
        return self

    def click_go_dashboard(self):
        self.click(*self.GO_DASHBOARD_BTN)
        return self

    def get_char_count(self) -> str:
        return self.get_text(*self.CHAR_COUNTER)

    def begin_btn_is_disabled(self) -> bool:
        try:
            btn = self.find(*self.BEGIN_BTN)
            return not btn.is_enabled()
        except Exception:
            return True

    def begin_btn_is_enabled(self) -> bool:
        try:
            btn = self.find(*self.BEGIN_BTN)
            return btn.is_enabled()
        except Exception:
            return False
