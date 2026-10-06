"""Unit tests for the swipe-search loop using a fake driver.

These tests do not need Appium or a device - they verify the control flow of
``AppListPage.find_by_swiping`` (scrolling, end-of-list detection and the
readable exception), which is the core logic of the homework.
"""
import re

import pytest

from pages import app_list_page
from pages.app_list_page import AppListPage, ListItemNotFoundError

ITEMS = [
    "Notes",
    "Files",
    "Music",
    "Maps",
    "Clock",
    "Calendar",
    "Camera",
    "Photos",
    "Store",
]


class FakeElement:
    def __init__(self, text=None, rect=None):
        self.text = text
        self.rect = rect
        self.clicked = False

    def click(self):
        self.clicked = True


class FakeListDriver:
    """Emulates a fixed-size viewport over a scrolling list."""

    def __init__(self, items, page_size=4):
        self.items = items
        self.page_size = page_size
        self.offset = 0
        self.tapped = None
        self.recycler_rect = {"x": 0, "y": 0, "width": 1080, "height": 1920}

    def find_elements(self, by, value):
        window = self.items[self.offset : self.offset + self.page_size]
        return [FakeElement(text=text) for text in window]

    def find_element(self, by, value):
        if value == AppListPage.RECYCLER_ID:
            return FakeElement(rect=self.recycler_rect)
        match = re.search(r'@text="([^"]+)"', value)
        if match:
            self.tapped = match.group(1)
        return FakeElement()


@pytest.fixture()
def swipe_advances_viewport(monkeypatch):
    def fake_swipe(driver, *args, **kwargs):
        driver.offset += driver.page_size

    monkeypatch.setattr(app_list_page, "swipe", fake_swipe)


def test_finds_item_on_a_later_screen(swipe_advances_viewport):
    driver = FakeListDriver(ITEMS, page_size=4)
    page = AppListPage(driver)

    assert page.find_by_swiping("Calendar") is True
    assert driver.tapped == "Calendar"
    assert driver.offset > 0, "the list should have been swiped"


def test_finds_item_already_visible_without_swiping(swipe_advances_viewport):
    driver = FakeListDriver(["Calendar"] + ITEMS, page_size=4)
    page = AppListPage(driver)

    assert page.find_by_swiping("Calendar") is True
    assert driver.offset == 0, "no swipe needed when the item is visible"


def test_raises_readable_error_when_end_of_list_reached(swipe_advances_viewport):
    driver = FakeListDriver(ITEMS, page_size=4)
    page = AppListPage(driver)

    with pytest.raises(ListItemNotFoundError) as exc_info:
        page.find_by_swiping("Gallery")

    assert "не найден" in str(exc_info.value)


def test_raises_when_max_swipes_exhausted(swipe_advances_viewport):
    driver = FakeListDriver(ITEMS, page_size=4)
    page = AppListPage(driver)

    with pytest.raises(ListItemNotFoundError):
        page.find_by_swiping("Calendar", max_swipes=1)
