"""
Pi Pico driver with PID loop for correcting angular velocity.

If steering angle is 0, attempts to keep current angle. Else, uses the
provided steering angle.
"""

from threading import Thread

import numpy as np

from hoverbotpy.drivers.driver_abc import HovercraftDriver
from hoverbotpy.drivers.pi_pico_simple import SimpleFan
from hoverbotpy.drivers.imu_driver import CorrectedIMU


# Constants representing default values to use for generating correction signal.
# TODO: Find good values with calibration and testing
DEFAULT_PROPORTION_ERR = -.1
DEFAULT_PROPORTION_DDT = -.1
DEFAULT_PROPORTION_ANGLE_TO_DPS = 1


class PIDCorrectedFan():
    """
    Driver with PID control loop to correct angle.

    Attributes:
        hover: Float representing hover motor speed from 0 to 100.
        forward: Float representing forward motor speed from 0 to 100.
        steering: Float representing rudder angle from -1 to 1.
        pico: Instance of SimpleFan hovercraft driver.
        imu: Instance of IMU driver.
        prop_err: Float representing proportion of error to use for PID.
        prop_ddt: Float representing proportion of angular velocity to use
            for PID.
        angle_target: A list of 3 floats representing the vector pointing to
            magnetic north at a given angle. Reference signal for PID control.
        running: Boolean representing whether or not PID loop is running.
        process: Thread containing PID process.
    """

    def __init__(self):
        # Hovercraft params
        self.hover = 0
        self.forward = 0
        self.steering = 0

        # The drivers within the driver
        self.pico = SimpleFan()
        self.imu = CorrectedIMU()

        # PID Loop
        # Proportions
        self.prop_err = DEFAULT_PROPORTION_ERR
        self.prop_ddt = DEFAULT_PROPORTION_DDT

        # Reference signal
        self.angle_target = self._get_north_vector()

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
        self.pico.set_hover_speed(speed)

    def set_forward_speed(self, speed):
        """
        Set speed of forward motor.

        Args:
            speed: Float representing speed of motor from 0 to 100.
        """
        self.forward = speed
        self.pico.set_forward_speed(speed)

    def set_steering_angle(self, speed):
        """
        Set servo motor angle.

        Note: If set to 0, the PID controller takes over and tries to maintain
        current direction.

        Args:
            speed: Float representing angle from -1 to 1.
        """
        if abs(self.steering - speed) > .05 and abs(speed)<.05:
            self.angle_target = self._get_north_vector()
            print(f"New north vector is :{self.angle_target}")
        self.steering = speed

    def stop(self):
        """Stop all motors except hover motor."""
        self.set_forward_speed(0)
        self.set_steering_angle(0)
        self.set_hover_speed(0)

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
            # Fudge it a little in case float errors happen
            if -0.1 < self.steering < 0.1:
                angle_head = self._get_north_vector()
                angle_vel = float(self.imu.get_data(["Z_DPS"])["Z_DPS"])

                rudder_angle = calc_rudder_angle(
                    self.angle_target, angle_head, angle_vel,
                    self.prop_err, self.prop_ddt
                )
                self.pico.set_steering_angle(rudder_angle)
            else:
                self.pico.set_steering_angle(self.steering)

    def _get_north_vector(self):
        """Return list representing vector pointing to magnetic north."""
        data = self.imu.get_data(["X_MAG_RAW", "Y_MAG_RAW"])
        # 0 is for cross product later
        #print(data)
        return [data["X_MAG_RAW"], data["Y_MAG_RAW"], 0]

    def run_loop(self):
        """Start PID loop."""
        self.running = True
        self.process.start()

    def stop_loop(self):
        """Stop PID loop."""
        self.running = False
        self.process.join()


def calc_rudder_angle(target_angle, angle_head, angle_vel,
                      prop_err, prop_ddt):
    """
    Calculate the rudder angle signal based on PD control loop.

    Used to maintain angle when steering commands are not being sent.

    Error is the difference between the `angle_ref` and `angle_cur`. The
    derivative of the error is given as gyroscope data as `angle_vel`.

    Args:
        angle_ref: List of 3 floats representing a vector pointing to magnetic
            north at a reference angle.
        angle_head: List of 3 floats representing a vector pointing to magnetic
            north at current angle.
        angle_vel: Float representing current angular velocity in (UNITS/s).
        prop_err: Float representing proportion of error signal (Δangle) to
            include in rudder angle signal.
        prop_ddt: Float representing proportion of angular velocity to include
            in rudder angle.

    Returns:
        A float between -1 and 1 representing the signal to send to the rudder.
    """
    # Direction from heading to target, sign of cross prod
    direction = np.cross(angle_head, target_angle)[2]
    # Angle between two vectors
    angle = np.arccos(np.dot(angle_head, target_angle) /
                      (np.linalg.norm(angle_head) *
                       np.linalg.norm(target_angle)))
    error = float(direction/np.abs(direction) * angle) # Back to Python float

    # PD control signal
    signal = (
        prop_err * error + 
        prop_ddt * angle_vel)
    # Ensure it lies in legal range
    return max(-1, min(1, signal))
