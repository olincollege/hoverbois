from abc import ABC, abstractmethod

class hovercraftDriver(ABC):


    def __init__(self):
        self.hover = 0
        self.forward = 0
        self.steering = 0
        pass

    @abstractmethod
    def set_hover_speed(self,speed):
        '''sets the speed of the hover motor
        args: 
            speed: the speed of the motor(0 to 100)'''
        pass


    @abstractmethod
    def set_forward_speed(self,speed):
        '''sets the speed of the forward motor
        args: 
            speed: the speed of the motor(0 to 100)'''
        pass

    @abstractmethod
    def set_steering_angle(self,speed):
        '''sets the speed of the steering servo motor
        args: 
            speed: the angle to (-1 to 1)'''
        pass

    @abstractmethod
    def stop(self):
        '''stops all motors'''
        pass


