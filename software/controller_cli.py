"""
Module for CLI interface.
"""

import cmd

# Use dummy for now, can be changed
from driver_dummy import DummyHovercraftDriver

class HovercraftShell(cmd.Cmd):
    """
    Define CLI interface for hovercraft.
    """
    intro = "Type help or ? to list commands."
    prompt = "hovercraft> "
    driver = None # Will be a driver

    def preloop(self):
        """
        Init before loop starts.
        """
        self.driver = DummyHovercraftDriver()

    def do_motor_speeds(self, arg):
        """
        Display motor speeds.
        """
        hover = self.driver.hover
        forward = self.driver.forward
        steering = self.driver.steering
        message = (f"hover speed   : {hover}\n"
                   f"forward speed : {forward}\n"
                   f"steering angle: {steering}\n")
        print(message)

    def do_set_forward_speed(self, arg):
        """
        Set forward motor speed.
        """
        # Cries in Python < 3.10
        try:
            number = float(arg.strip())
            self.driver.set_forward_speed(number)
        except:
            print("Invalid argument")

    def do_set_hover_speed(self, arg):
        """
        Set hover motor speed.
        """
        # Cries in Python < 3.10
        try:
            number = float(arg.strip())
            self.driver.set_hover_speed(number)
        except:
            print("Invalid argument")

    def do_set_steering_angle(self, arg):
        """
        Set steering angle.
        """
        # Cries in Python < 3.10
        try:
            number = float(arg.strip())
            self.driver.set_steering_angle(number)
        except:
            print("Invalid argument")

    def do_stop(self, arg):
        """
        Stop all motors.
        """
        self.driver.stop()

    def do_exit(self, arg):
        """
        End program.
        """
        self.driver.stop()
        return True


if __name__ == "__main__":
    HovercraftShell().cmdloop()
