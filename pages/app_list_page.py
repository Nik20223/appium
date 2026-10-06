"""Page Object for the scrollable application list of the PNW app."""
from appium.webdriver.common.appiumby import AppiumBy

from config import APP_PACKAGE
from gestures import swipe


class ListItemNotFoundError(Exception):
    """Raised when a list item cannot be found by swiping."""


class AppListPage:
    """The main list of PNW (a scrolling RecyclerView of application titles)."""

    RECYCLER_ID = f"{APP_PACKAGE}:id/recycler"
    TITLE_ID = f"{APP_PACKAGE}:id/tv_title"

    def __init__(self, driver):
        self.driver = driver

    def visible_titles(self) -> list:
        """Return the text of every title currently rendered on screen."""
        elements = self.driver.find_elements(AppiumBy.ID, self.TITLE_ID)
        return [element.text for element in elements]

    def swipe_up(self):
        """Scroll the list one screen down (finger moves from bottom to top)."""
        recycler = self.driver.find_element(AppiumBy.ID, self.RECYCLER_ID)
        rect = recycler.rect
        center_x = rect["x"] + rect["width"] / 2
        start_y = rect["y"] + rect["height"] * 0.8
        end_y = rect["y"] + rect["height"] * 0.2
        swipe(self.driver, center_x, start_y, center_x, end_y)

    def tap_title(self, text):
        """Tap the list item whose title equals ``text``."""
        locator = (
            AppiumBy.XPATH,
            f'//*[@resource-id="{self.TITLE_ID}" and @text="{text}"]',
        )
        self.driver.find_element(*locator).click()

    def find_by_swiping(self, text: str, max_swipes: int = 20) -> bool:
        """Scroll the list until ``text`` is visible, then tap it.

        The loop stops as soon as the item is found (returns True) or as soon
        as a swipe reveals nothing new, which means the end of the list has
        been reached. In the latter case - and when ``max_swipes`` is
        exhausted - a :class:`ListItemNotFoundError` with a readable message
        is raised.
        """
        previous_titles = None
        for _ in range(max_swipes):
            titles = self.visible_titles()
            if text in titles:
                self.tap_title(text)
                return True
            if titles == previous_titles:
                break  # the swipe did not reveal anything new -> end of list
            previous_titles = titles
            self.swipe_up()

        raise ListItemNotFoundError(
            f"Пункт '{text}' не найден в списке после {max_swipes} свайпов: "
            f"достигнут конец списка."
        )
