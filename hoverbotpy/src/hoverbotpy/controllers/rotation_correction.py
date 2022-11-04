"""
Correct rotational inertia in steering.

Implements PD controll for turning the hovercraft.
"""

# Constants representing default values to use for generating correction signal.
# TODO: Find good values with calibration and testing
DEFAULT_PROPORTION_ERR = 1
DEFAULT_PROPORTION_DDT = 1


# Feel free to modify the parameters if this does not work the way you were
# expecting.
def get_imu_data(ser, params=None):
    """
    Get sensor data from IMU unit.

    Args:
        ser: A serial device, representing the Pi Pico to talk to.
        params: A list of strings requesting which parameters to querry for.

    Returns:
        A dictionary where keys are the requested parameters with matching values.
    """
    pass


def calculate_rudder_angle(angle_ref, angle_cur, angle_vel,
                           proportion_err=DEFAULT_PROPORTION_ERR,
                           proportion_ddt=DEFAULT_PROPORTION_DDT):
    """
    Calculate the rudder angle signal based on PD control loop.

    Used to maintain angle when steering commands are not being sent.

    Error is the difference between the `angle_ref` and `angle_cur`. The
    derivative of the error is given as gyroscope data as `angle_vel`.

    Args:
        angle_ref: Reference angle relative to magnetic north in (UNITS). This
            is the direction we want to steer.
        angle_cur: Current angle relative to magnetic north in (UNITS).
        angle_vel: Current angular velocity in (UNITS/s).
        proportaion_err: Proportion of error signal (Δangle) to include in
            rudder angle signal.
        proportion_ddt: Proportion of angular velocity to include in rudder
            angle.

    Returns:
        A float between -1 and 1 representing the signal to send to the rudder.
    """
    error = angle_ref - angle_cur
    rudder_angle = (proportion_err * error) + (proportion_ddt * angle_vel)
    # Ensure signal lies between bounds of -1 and 1
    return max(-1, min(1, rudder_angle))
