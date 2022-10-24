from abc import ABC, abstractmethod

class hovercraftController(ABC):


    def __init__(self):
        pass


    @abstractmethod
    def stop(self):
        '''stops all motors'''
        pass