"""
Module implementing control with a bluetooth gamepad.
"""

from threading import Thread
from time import sleep
from evdev import list_devices, InputDevice, ecodes

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


def axis_moved(event, robot_state):
    """
    Function to call when axis moved event.

    Args:
        event: Evdev event.
        kwargs: Dictionary of kwargs.
    """
    robot_state["value"] = event.value
    # Turn the reading from 0 to STICK_MAX from -1 to 1.
    axis_relative = robot_state["value"] - robot_state["center"]
    if (robot_state["center"]-robot_state["deadzone"]
        <= axis_relative
            <= robot_state["center"]+robot_state["deadzone"]):
        axis_relative = 0
    rudder = -min(1, max(-1, axis_relative/1024))
    robot_state["rudder"] = rudder


def recenter(robot_state):
    """
    Takes last reading of joystick and sets it as the center.
    """
    robot_state["center"] = robot_state["value"]
    print(robot_state["center"])


def hover_plus(robot_state):
    """
    Change speed of hover by FAN_INCREMENT.
    """
    speed = min(80, robot_state["hover"]+FAN_INCREMENT)
    robot_state["hover"] = speed


def hover_minus(robot_state):
    """
    Change speed of hover by FAN_INCREMENT.
    """
    speed = max(0, robot_state["hover"]-FAN_INCREMENT)
    robot_state["hover"] = speed


def throttle_plus(robot_state):
    """
    Change speed of fan by FAN_INCREMENT.
    """
    speed = min(60, robot_state["throttle"]+FAN_INCREMENT)
    robot_state["throttle"] = speed


def throttle_minus(robot_state):
    """
    Change speed of fan by FAN_INCREMENT.
    """
    speed = max(0, robot_state["throttle"]-FAN_INCREMENT)
    robot_state["throttle"] = speed


def estop_water(robot_state):
    """
    Stop throttle fan.
    """
    robot_state["throttle"] = 0


def estop_land(robot_state):
    """
    Stop all fans
    """
    robot_state["throttle"] = 0
    robot_state["hover"]    = 0


def driver_loop(robot_state, driver):
    """
    Thread to send robot state to driver.

    Args:
        robot_state: Dictionary representing state of robot.
        driver: Robot driver.
    """
    while robot_state["running"]:
        driver.set_steering_angle (robot_state["rudder"])
        driver.set_forward_speed  (robot_state["throttle"])
        driver.set_hover_speed    (robot_state["hover"])
        sleep(0.05)
    driver.stop()


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="BluetoothController",
        description="Hovercraft controller using bluetooth gamepad.",
        epilog="Written by Devlin Ih",
    )
    parser.add_argument(
        "driver_type",
        help=("Type of driver to use. Legal values:\n"
              "  dummy, dummy_threading, pico, pico_pid"),
    )
    args = parser.parse_args()
    # Wish we were using Python 3.10 for pattern matching.
    driver_type = args.driver_type
    if driver_type == "dummy":
        from hoverbotpy.drivers.driver_dummy import DummyHovercraftDriver
        driver = DummyHovercraftDriver()
    elif driver_type == "threading_dummy":
        from hoverbotpy.drivers.threading_dummy import ThreadingDummy
        driver = ThreadingDummy()
        driver.run_loop()
    elif driver_type == "pico":
        from hoverbotpy.drivers.pi_pico_simple import SimpleFan
        driver = SimpleFan()
    elif driver_type == "pico_pid":
        from hoverbotpy.drivers.pi_pico_pid import PIDCorrectedFan
        driver = PIDCorrectedFan()
        driver.run_loop()
    else:
        import sys
        print(f"Error: {driver_type} is not a valid driver type.")
        sys.exit(-1)

    # Global state
    device = find_controller()
    robot_state = {
        "running"  : True,
        "center"   : 0,
        "value"    : 0,
        "deadzone" : 100,  # Hardcoded for now
        "hover"    : 0,
        "throttle" : 0,
        "rudder"   : 0,
    }

    # Button map
    button_map = {
        ecodes.BTN_SELECT : (recenter,       robot_state),
        ecodes.BTN_EAST   : (estop_water,    robot_state),
        ecodes.BTN_SOUTH  : (estop_land,     robot_state),
        ecodes.BTN_TL2    : (hover_plus,     robot_state),
        ecodes.BTN_TL     : (hover_minus,    robot_state),
        ecodes.BTN_TR2    : (throttle_plus,  robot_state),
        ecodes.BTN_TR     : (throttle_minus, robot_state),
    }

    # Start driver thread
    driver_thread = Thread(target = driver_loop,
                           args   = [robot_state, driver],
                           daemon = True, )
    driver_thread.start()

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            # Hardcode exit as start button
            if event.code == ecodes.BTN_START:
                robot_state["running"] = False
                driver_thread.join()
                import sys
                print("Goodbye")
                sys.exit()

            action = button_map.get(event.code)
            if action and event.value == 1:
                action[0](action[1])

        # Hardcode the joystick axis because it needs to be done by tomorrow
        if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
            axis_moved(event, robot_state)


if __name__ == "__main__":
    main()
