"""Touch gesture helpers built on the W3C Actions protocol.

Appium 2 / uiautomator2 dropped the legacy TouchAction API, so gestures are
performed through a W3C pointer input (``ActionBuilder`` + ``PointerInput``).
"""
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def swipe(driver, start_x, start_y, end_x, end_y, duration_ms=600):
    """Swipe with a single finger from (start_x, start_y) to (end_x, end_y).

    The finger is pressed down, held in place for ``duration_ms`` (to make it
    a real drag rather than a fling) and released at the end point.
    """
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    actions = ActionBuilder(driver, mouse=finger)
    actions.pointer_action.move_to_location(int(start_x), int(start_y))
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration_ms / 1000)
    actions.pointer_action.move_to_location(int(end_x), int(end_y))
    actions.pointer_action.pointer_up()
    actions.perform()
