from driver_abc import HovercraftDriver


class DummyHovercraftDriver(HovercraftDriver):
    """
    Dummy hovercraft driver class.

    Used for testing without motors.
    """

    def set_hover_speed(self, speed):
        """
        Set speed of the hover motor.

        Args:
            Speed: The speed of the motor from 0 to 100.
        """
        self.hover = speed
        print(f"Set hover to {speed}")


    def set_forward_speed(self, speed):
        """
        Set the speed of forward motor.

        Args:
            speed: The speed of the motor from 0 to 100.
        """
        self.forward = speed
        print(f"Set forward to {speed}")

    def set_steering_angle(self, speed):
        """
        Set the speed of the steering server motor.

        Args:
            speed: The angle from -1 to 1.
        """
        self.steering = speed
        print(f"Set steering to {speed}")

    def stop(self):
        """
        Stop all motors.
        """
        self.hover = 0
        self.forward = 0
        self.steering = 0
        print("Stopping all motors.")
