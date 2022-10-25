from time import sleep

from gpiozero import Servo
import RPi.GPIO as gp
import lgpio as sbc

from hoverbotpy.drivers.driver_abc import HovercraftDriver
from hoverbotpy.drivers.pin_defs import *

PWM_FREQ = 15000


class SimpleFan(HovercraftDriver):
    ''''''

    def __init__(self):
        if min(FORWARDPIN, SERVOPIN) < 2 or \
           max(FORWARDPIN, SERVOPIN) > 27:
            raise Exception(
                "All pin definitions must match pins on the raspberry pi")

        self.forward_motor = sbc.gpiochip_open(0)
        sbc.gpio_claim_output(self.forward_motor, FORWARDPIN)
        self.steer_motor = Servo(SERVOPIN)
        #self.hover = 0
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
        # self.hover = (speed/50)-1  # this takes a 1 to -1
        # self.hover_motor.value(self.hover)
        pass

    def set_forward_speed(self, speed):
        '''sets the speed of the forward motor
        args: 
            speed: a number of the speed of the motor(0 to 100)'''
        self.forward = (speed/50)-1
        sbc.tx_pwm(self.forward_motor, FORWARDPIN, PWM_FREQ,
                   speed, pulse_offset=0, pulse_cycles=0)
        pass

    def set_steering_angle(self, angle):
        '''sets the angle of the steering servo motor
        args: 
            speed: a number of the angle to (-1 to 1)'''
        self.steering = angle
        self.steer_motor.value(angle)
        pass

    def stop(self):
        '''turn off all motors and return steer to mid'''
        # self.forward_motor.detach()
        # self.hover_motor.detach()
        self.steer_motor.mid()
        self.forward_motor.start(0)
        #self.hover = 0
        self.forward = 0
        self.steering = 0
        # gp.cleanup()
        pass
