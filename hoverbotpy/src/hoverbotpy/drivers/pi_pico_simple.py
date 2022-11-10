from hoverbotpy.drivers.driver_abc import HovercraftDriver
from hoverbotpy.drivers.pin_defs import *
from time import sleep
import serial

PWM_FREQ = 15000
SERVO_DIST = 85
SERVO_MID = 90


class SimpleFan(HovercraftDriver):
    ''''''

    def __init__(self):
        self.pico = serial.Serial(
            port='/dev/ttyACM0', baudrate=115200, timeout=.1)
        #self.steer_motor = Servo(SERVOPIN)
        self.hover = 0
        self.forward = 0
        self.steering = 0
        sleep(0.1)
        self.set_steering_angle(-1)  # wig wag the servo to show its been started up
        sleep(0.3)
        self.set_steering_angle(1)
        sleep(0.3)
        self.set_steering_angle(-1)
        sleep(0.3)
        self.set_steering_angle(1)
        sleep(0.3)
        self.set_steering_angle(0)
        pass

    def set_hover_speed(self, speed):
        '''sets the speed of the hover motor
        args:
            speed: a number of the speed of the motor(0 to 100)'''
        self.hover = speed
        self.pico.write(bytes("h"+str(speed), 'utf-8'))
        pass

    def set_forward_speed(self, speed):
        '''sets the speed of the forward motor
        args:
            speed: a number of the speed of the motor(0 to 100)'''
        self.forward = speed
        self.pico.write(bytes("f"+str(speed), 'utf-8'))
        pass

    def set_steering_angle(self, angle):
        '''sets the angle of the steering servo motor
        args:
            speed: a number of the angle to (-1 to 1)'''
        #self.steering = angle
        # self.steer_motor.value=angle
        self.steering = angle
        self.pico.write(bytes("s"+str(angle*SERVO_DIST+SERVO_MID), 'utf-8'))
        pass

    def stop(self):
        '''turn off all motors and return steer to mid'''
        # self.forward_motor.detach()
        # self.hover_motor.detach()
        self.pico.write(bytes("s"+str(SERVO_MID), 'utf-8'))
        self.pico.write(bytes("f"+str(0), 'utf-8'))
        #self.hover = 0
        self.forward = 0
        self.steering = 0
        # gp.cleanup()
        pass
