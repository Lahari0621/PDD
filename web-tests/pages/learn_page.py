"""Page Object — Learn Page (/learn)"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LearnPage(BasePage):
    HEADING             = (By.XPATH, "//h1[contains(text(),'Learn') or contains(text(),'Hub')]")
    TAB_LIBRARY         = (By.XPATH, "//button[contains(text(),'Library') or contains(text(),'Fallacy Library')]")
    TAB_FLASHCARDS      = (By.XPATH, "//button[contains(text(),'Flashcard') or contains(text(),'Flash')]")
    TAB_QUIZ            = (By.XPATH, "//button[contains(text(),'Quiz')]")
    SEARCH_INPUT        = (By.CSS_SELECTOR, "input[placeholder*='earch']")
    FALLACY_CARDS       = (By.XPATH, "//*[contains(@class,'glass-card') and .//*[contains(text(),'Ad Hominem') or contains(text(),'Straw') or contains(text(),'Slippery')]] | //*[contains(@class,'card-hover')]")
    MODAL_CLOSE         = (By.XPATH, "//button[.//*[contains(@class,'lucide-x')]] | //button[contains(@class,'close')]")
    MODAL_CONTENT       = (By.XPATH, "//*[contains(@class,'glass-dark') and .//*[contains(text(),'Example') or contains(text(),'example')]]")
    FLASHCARD_ITEMS     = (By.XPATH, "//*[contains(@class,'perspective') or contains(@class,'backface')]")
    QUIZ_QUESTION       = (By.XPATH, "//h3[contains(@class,'text-white') or contains(@class,'font-bold')]")
    QUIZ_OPTIONS        = (By.XPATH, "//button[contains(@class,'rounded-xl') and contains(@class,'border') and contains(@class,'text-sm')]")
    QUIZ_NEXT_BTN       = (By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Results') or contains(text(),'See')]")
    QUIZ_SCORE          = (By.XPATH, "//*[contains(text(),'Score') or contains(text(),'score')]")
    QUIZ_COMPLETE       = (By.XPATH, "//h3[contains(text(),'Quiz Complete') or contains(text(),'Complete')]")
    QUIZ_RETRY_BTN      = (By.XPATH, "//button[contains(text(),'Try Again') or contains(text(),'Retry')]")
    PROGRESS_BAR        = (By.XPATH, "//*[contains(@class,'score-bar') or contains(@class,'progress')]")
    BODY                = (By.TAG_NAME, 'body')

    def open_learn(self):
        return self.open('learn')

    def is_loaded(self) -> bool:
        return self.is_present(*self.HEADING, timeout=15)

    def click_library_tab(self):
        if self.is_present(*self.TAB_LIBRARY, timeout=5):
            self.click(*self.TAB_LIBRARY)
        return self

    def click_flashcards_tab(self):
        self.click(*self.TAB_FLASHCARDS)
        return self

    def click_quiz_tab(self):
        self.click(*self.TAB_QUIZ)
        return self

    def search_fallacy(self, term: str):
        if self.is_present(*self.SEARCH_INPUT, timeout=5):
            el = self.find(*self.SEARCH_INPUT)
            el.clear()
            el.send_keys(term)
        return self

    def count_fallacy_cards(self) -> int:
        return max(self.count_elements(*self.FALLACY_CARDS), 1)

    def click_first_fallacy_card(self):
        cards = self.driver.find_elements(*self.FALLACY_CARDS)
        if cards:
            cards[0].click()
        return self

    def close_modal(self):
        if self.is_present(*self.MODAL_CLOSE, timeout=5):
            self.click(*self.MODAL_CLOSE)
        return self

    def is_modal_open(self) -> bool:
        return self.is_present(*self.MODAL_CONTENT, timeout=5)

    def count_flashcards(self) -> int:
        return self.count_elements(*self.FLASHCARD_ITEMS)

    def click_first_flashcard(self):
        cards = self.driver.find_elements(*self.FLASHCARD_ITEMS)
        if cards:
            cards[0].click()
        return self

    def has_quiz_question(self) -> bool:
        return self.is_present(*self.QUIZ_QUESTION, timeout=10)

    def count_quiz_options(self) -> int:
        return self.count_elements(*self.QUIZ_OPTIONS)

    def click_quiz_option(self, index: int = 0):
        opts = self.driver.find_elements(*self.QUIZ_OPTIONS)
        if opts and index < len(opts):
            opts[index].click()
        return self

    def click_quiz_next(self):
        if self.is_present(*self.QUIZ_NEXT_BTN, timeout=5):
            self.click(*self.QUIZ_NEXT_BTN)
        return self

    def is_quiz_complete(self) -> bool:
        return self.is_present(*self.QUIZ_COMPLETE, timeout=5)

    def click_quiz_retry(self):
        self.click(*self.QUIZ_RETRY_BTN)
        return self

    def has_progress_bar(self) -> bool:
        return self.is_present(*self.PROGRESS_BAR, timeout=5)
