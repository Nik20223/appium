"""Desired Capabilities and settings for the PNW Appium session.

Every value can be overridden through environment variables, so the same
tests run against an emulator, a real device or a CI grid without code
changes. See README.md for the full list of supported variables.
"""
import os


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# URL of the running Appium server (appium --port 4723).
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

# Application under test (PNW).
APP_PACKAGE = os.getenv("PNW_APP_PACKAGE", "com.csdroid.pkg")
# Optional: leave empty to let Appium resolve the launcher activity of the
# package automatically.
APP_ACTIVITY = os.getenv("PNW_APP_ACTIVITY", "")

# The item we are looking for inside the application list.
TARGET_ITEM = os.getenv("PNW_TARGET_ITEM", "Calendar")

# Safety guard for the swipe loop.
MAX_SWIPES = int(os.getenv("PNW_MAX_SWIPES", "20"))


def get_capabilities() -> dict:
    """Build the Desired Capabilities dictionary for the PNW session."""
    capabilities = {
        "platformName": os.getenv("ANDROID_PLATFORM_NAME", "Android"),
        "appium:automationName": "uiautomator2",
        "appium:deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
        "appium:appPackage": APP_PACKAGE,
        "appium:noReset": _env_bool("PNW_NO_RESET", True),
        "appium:autoGrantPermissions": True,
        "appium:newCommandTimeout": int(os.getenv("APPIUM_NEW_COMMAND_TIMEOUT", "180")),
    }
    if APP_ACTIVITY:
        capabilities["appium:appActivity"] = APP_ACTIVITY
    udid = os.getenv("ANDROID_UDID")
    if udid:
        capabilities["appium:udid"] = udid
    return capabilities
