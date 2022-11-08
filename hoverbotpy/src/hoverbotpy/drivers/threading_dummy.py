"""
Dummy driver to make sure thread can work in tornado.
"""

from time import sleep

from threading import Thread

from hoverbotpy.drivers.driver_abc import HovercraftDriver


class ThreadingDummy():
    """
    Dummy threaded driver
    """

    def __init__(self):
        # Hovercraft params
        self.hover = 0
        self.forward = 0
        self.steering = 0

        # PID params
        self.prop_err = 1
        self.prop_ddt = 1

        # Loop on another thread
        self.running = False
        self.process = Thread(target=self._pid_loop,
                              daemon=True)

    # Standard interface as determined by ABC
    def set_hover_speed(self, speed):
        """
        Set speed of hover motor.

        Args:
            speed: Float representing speed of motor from 0 to 100.
        """
        self.hover = speed

    def set_forward_speed(self, speed):
        """
        Set speed of forward motor.

        Args:
            speed: Float representing speed of motor from 0 to 100.
        """
        self.forward = speed

    def set_steering_angle(self, speed):
        """
        Set servo motor angle.

        Note: If set to 0, the PID controller takes over and tries to maintain
        current direction.

        Args:
            speed: Float representing angle from -1 to 1.
        """
        self.steering = speed

    def stop(self):
        """Stop all motors except hover motor."""
        self.hover = 0
        self.steering = 0
        self.forward = 0

    # Additional public methods to set PID params in real time.
    def set_prop_err(self, proportion):
        """
        Set proportion of error to use for PID.

        Args:
            proportion: Float to set proportion to.
        """
        self.prop_err = proportion

    def set_prop_ddt(self, proportion):
        """
        Set proportion of ddt to use for PID.

        Args:
            proportion: Float to set proportion to.
        """
        self.prop_ddt = proportion

    # PID loop on its own thread
    def _pid_loop(self):
        """
        Runs the PID control loop.

        If the rudder angle is 0, try to maintain current direction. Else, set
        the rudder angle to its specified value.
        """
        while self.running:
            print("Driver thread is running.")
            sleep(1)


    def _get_north_vector(self):
        """Return list representing vector pointing to magnetic north."""
        data = self.imu.get_data(["X_MAG_BIN", "Y_MAG_BIN"])
        # 0 is for cross product later
        return [data["X_MAG_BIN"], data["Y_MAG_BIN"], 0]

    def run_loop(self):
        """Start PID loop."""
        self.running = True
        self.process.start()

    def stop_loop(self):
        """Stop PID loop."""
        self.running = False
        self.process.join()
