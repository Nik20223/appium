"""End-to-end test: find the 'Calendar' app in PNW by swiping the list.

Requires a running Appium server, an Android emulator/device with the PNW
app installed. See README.md.
"""
import allure
import pytest

import config
from pages.app_list_page import AppListPage


@allure.feature("PNW")
@allure.story("Поиск приложения в главном списке свайпами")
@allure.title("Найти 'Календарь' через свайпы и открыть его")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.mobile
def test_find_calendar_by_swiping(driver):
    page = AppListPage(driver)

    allure.attach(
        str(driver.capabilities),
        name="Desired Capabilities",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step(
        f"Свайпаем список вниз, пока не найдём '{config.TARGET_ITEM}'"
    ):
        found = page.find_by_swiping(config.TARGET_ITEM, config.MAX_SWIPES)

    assert found is True, f"Пункт '{config.TARGET_ITEM}' не найден в списке"


@allure.feature("PNW")
@allure.story("Поиск приложения в главном списке свайпами")
@allure.title("Понятная ошибка, если пункт отсутствует в списке")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.mobile
def test_missing_item_raises_readable_error(driver):
    page = AppListPage(driver)
    missing = "НесуществующееПриложение"

    with allure.step(f"Ищем заведомо отсутствующий пункт '{missing}'"):
        with pytest.raises(Exception) as exc_info:
            page.find_by_swiping(missing, config.MAX_SWIPES)

    message = str(exc_info.value)
    assert missing in message
    allure.attach(message, name="exception", attachment_type=allure.attachment_type.TEXT)
