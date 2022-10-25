from time import sleep

from gpiozero import Servo

from hoverbotpy.drivers.driver_abc import HovercraftDriver
from hoverbotpy.drivers.pin_defs import *


class SimplePWM(HovercraftDriver):
    ''''''

    def __init__(self, is_fan=False):
        self.pwm_freq = 1/25000
        if min(HOVERPIN, FORWARDPIN, SERVOPIN) < 2 or \
           max(HOVERPIN, FORWARDPIN, SERVOPIN) > 27:
            raise Exception(
                "All pin definitions must match pins on the raspberry pi")
        if is_fan:
            self.hover_motor = Servo(
                HOVERPIN, min_pulse_width=0, max_pulse_width=.5*self.pwm_freq, frame_width=self.pwm_freq)
            self.forward_motor = Servo(
                FORWARDPIN, min_pulse_width=0, max_pulse_width=.5*self.pwm_freq, frame_width=self.pwm_freq)
        else:
            self.hover_motor = Servo(HOVERPIN)
            self.forward_motor = Servo(FORWARDPIN)
        self.steer_motor = Servo(SERVOPIN)
        self.hover = 0
        self.forward = 0
        self.steering = 0
        sleep(0.1)
        self.steer_motor.min()  # wig wag the servo to show its been started up
        sleep(0.2)
        self.steer_motor.max()
        sleep(0.2)
        self.steer_motor.min()
        sleep(0.2)
        self.steer_motor.max()
        sleep(0.2)
        self.steer_motor.mid()
        pass

    def set_hover_speed(self, speed):
        '''sets the speed of the hover motor
        args: 
            speed: a number of the speed of the motor(0 to 100)'''
        self.hover = (speed/50)-1  # this takes a 1 to -1
        self.hover_motor.value = self.hover
        pass

    def set_forward_speed(self, speed):
        '''sets the speed of the forward motor
        args: 
            speed: a number of the speed of the motor(0 to 100)'''
        self.forward = (speed/50)-1
        self.forward_motor.value = self.forward
        pass

    def set_steering_angle(self, angle):
        '''sets the angle of the steering servo motor
        args: 
            speed: a number of the angle to (-1 to 1)'''
        self.steering = angle
        self.steer_motor.value = self.steering
        pass

    def stop(self):
        '''turn off all motors and return steer to mid'''
        self.forward_motor.detach()
        self.hover_motor.detach()
        self.steer_motor.mid()
        self.hover = 0
        self.forward = 0
        self.steering = 0
        pass
