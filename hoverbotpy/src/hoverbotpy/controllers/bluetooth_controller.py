"""
Module implementing control with a bluetooth gamepad.
"""

from evdev import list_devices, InputDevice, ecodes

from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver

FAN_INCREMENT = 5

def find_controller():
    """
    Finds device of first recognized controller.

    If no controller is found, exits.

    Returns:
        An evdev InputDevice.
    """
    known_devices = ["Nintendo Wii Remote Pro Controller"]
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.name in known_devices:
            return device
    import sys
    print("No recognized game controller found.")
    print("Goodbye")
    sys.exit(-1)


def axis_moved(event, axis, driver):
    """
    Function to call when axis moved event.

    Args:
        event: Evdev event.
        kwargs: Dictionary of kwargs.
    """
    axis["value"] = event.value
    # Turn the reading from 0 to STICK_MAX from -1 to 1.
    axis_relative = axis["value"] - axis["center"]
    if (axis["center"]-axis["deadzone"]
        <= axis_relative
        <= axis["center"]+axis["deadzone"]):
        axis_relative = 0
    driver.set_steering_angle(axis_relative)


def recenter(axis):
    """
    Takes last reading of joystick and sets it as the center.
    """
    axis["center"] = axis["value"]
    print(axis["center"])


def hover_plus(driver):
    """
    Change speed of hover by FAN_INCREMENT.
    """
    speed = min(100, driver.hover+FAN_INCREMENT)
    driver.set_hover_speed(speed)


def hover_minus(driver):
    """
    Change speed of hover by FAN_INCREMENT.
    """
    speed = max(0, driver.hover-FAN_INCREMENT)
    driver.set_hover_speed(speed)


def throttle_plus(driver):
    """
    Change speed of fan by FAN_INCREMENT.
    """
    speed = min(100, driver.forward+FAN_INCREMENT)
    driver.set_forward_speed(speed)


def throttle_minus(driver):
    """
    Change speed of fan by FAN_INCREMENT.
    """
    speed = max(0, driver.forward-FAN_INCREMENT)
    driver.set_forward_speed(speed)


def estop(driver):
    """
    Run estop
    """
    driver.stop()


def main():
    # Global state
    driver = DummyHovercraftDriver()
    device = find_controller()
    axis = {
        "center"   : 0,
        "value"    : 0,
        "deadzone" : 100, # Hardcoded for now
    }

    # Button map
    button_map = {
        ecodes.BTN_SELECT : (recenter, axis),
        ecodes.BTN_EAST   : (estop, driver),
        ecodes.BTN_TL2    : (hover_plus, driver),
        ecodes.BTN_TL     : (hover_minus, driver),
        ecodes.BTN_TR2    : (throttle_plus, driver),
        ecodes.BTN_TR     : (throttle_minus, driver),
    }

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            action = button_map.get(event.code)
            if action and event.value == 1:
                action[0](action[1])

        # Hardcode the joystick axis because it needs to be done by tomorrow
        if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
            axis_moved(event, axis, driver)
