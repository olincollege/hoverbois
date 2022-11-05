import pigpio
from threading import Thread, Lock


class corrected_imu():
    ''' this is the position corrected imu for com of object'''
    
    def __init__(self, imu_address=0x1c, mag_address=0x6a):
        self.ima_adr = imu_address
        self.mag_adr = mag_address
        self.pi = pigpio.pi()
        self._CHANNEL = 1
        self.DEFAULT_REQUESTS = [
            #"X_POS","Y_POS","Z_POS",
            #"X_VEL","Y_VEL","Z_VEL",
            "X_ACC","Y_ACC","Z_ACC",
            #"X_DEG","Y_DEG","Z_DEG",
            "X_DPS","Y_DPS","Z_DPS",
            "X_MAG","Y_MAG","Z_MAG"
            ]

        self.REQUESTS_REG = {
            #"X_POS":
            #"Y_POS":
            #"Z_POS":
            #"X_VEL":
            #"Y_VEL":
            #"Z_VEL":
            "X_ACC":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            #"Y_ACC":
            #"Z_ACC":
            #"X_DEG":
            #"Y_DEG":
            #"Z_DEG":
            "X_DPS":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            "Y_DPS":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            "Z_DPS":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            "X_MAG":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            "Y_MAG":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
            "Z_MAG":[self._req_N_from_dev,{"registers":[],"addr":imu_address}],
        }
    
    def get_data(data_req = []):
        if  not isinstance(data_req,list):
            data_req = [data_req]
        out = dict((req, req[0](**(req[1]))) for req in data_req)
        return out

    def _req_N_from_dev(self,registers,addr,channel=None):
        data = 0
        for reg in registers:
            data *= 8
            data = self._req8_from_dev(self,reg,addr,channel)
        return data

    def _req8_from_dev(self,register,addr,channel=None):
        '''requests the packet from the device'''
        if channel == None:
            channel=self._CHANNEL
        handle = self.pi.i2c_open(channel,addr)
        data = self.pi.i2c_read_byte_data(handle,register)
        self.pi.i2c_close(handle)
        return data



