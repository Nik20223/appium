"""Shared pytest fixtures and reporting hooks."""
import allure
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions

import config


@pytest.fixture(scope="session")
def driver():
    """Start a single Appium session for the PNW app and close it at the end."""
    options = AppiumOptions()
    options.load_capabilities(config.get_capabilities())
    session = webdriver.Remote(
        command_executor=config.APPIUM_SERVER_URL, options=options
    )
    yield session
    session.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to Allure when a mobile test fails."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver is not None:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:  # pragma: no cover - best effort reporting
            pass
