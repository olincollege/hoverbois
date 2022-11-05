import pigpio
from threading import Thread, Lock

DEFAULT_REQUESTS = [
            #"X_POS","Y_POS","Z_POS",
            #"X_VEL","Y_VEL","Z_VEL",
            "X_ACC_RAW","Y_ACC_RAW","Z_ACC_RAW",
            #"X_DEG","Y_DEG","Z_DEG",
            "X_DPS","Y_DPS","Z_DPS",
            "X_MAG","Y_MAG","Z_MAG"
            ]
_2BYTE_MAX  = 2^16

class correctedIMU():
    ''' this is the position corrected imu for com of object'''
    
    def __init__(self, imu_address=0x1c, mag_address=0x6a):
        self.ima_adr = imu_address
        self.mag_adr = mag_address
        self.pi = pigpio.pi()
        self._CHANNEL = 1

        self.REQUESTS_REG = {
            #"X_POS":
            #"Y_POS":
            #"Z_POS":
            #"X_VEL":
            #"Y_VEL":
            #"Z_VEL":
            #"X_ACC":
            #"Y_ACC":
            #"Z_ACC":
            "X_ACC_RAW":[self._req_N_from_dev,{"registers":[0x29,0x28],"addr":imu_address}],
            "Y_ACC_RAW":[self._req_N_from_dev,{"registers":[0x2B,0x2A],"addr":imu_address}],
            "Z_ACC_RAW":[self._req_N_from_dev,{"registers":[0x2D,0x2C],"addr":imu_address}],
            #"X_DEG":
            #"Y_DEG":
            #"Z_DEG":
            "X_DPS":[self._req_N_from_dev,{"registers":[0x23,0x22],"addr":imu_address}],
            "Y_DPS":[self._req_N_from_dev,{"registers":[0x25,0x24],"addr":imu_address}],
            "Z_DPS":[self._req_N_from_dev,{"registers":[0x27,0x26],"addr":imu_address}],
            "X_MAG":[self._req_N_from_dev,{"registers":[0x29,0x28],"addr":mag_address}],
            "Y_MAG":[self._req_N_from_dev,{"registers":[0x2B,0x2A],"addr":mag_address}],
            "Z_MAG":[self._req_N_from_dev,{"registers":[0X2D,0X2C],"addr":mag_address}],
        }
    
    def get_data(self,data_req = DEFAULT_REQUESTS):
        if  not isinstance(data_req,list):
            data_req = [data_req]
        out = dict((req, self.REQUESTS_REG[req][0](
            **(self.REQUESTS_REG[req][1]))) for req in data_req)
        return out

    def _req_N_from_dev(self,registers,addr,channel=None,*args):
        data = 0
        for i, reg in enumerate(registers):
            data *= 256
            data = self._req8_from_dev(reg,addr,channel)
            if i is 0 and data > 127:
                data -= 256
            #end if
        #end for
        return data

    def _req8_from_dev(self,register,addr,channel=None,*args):
        '''requests the packet from the device SHOULD NOT BE CALLED
            except through _req_N_from_dev'''
        if channel is None:
            channel=self._CHANNEL
        handle = self.pi.i2c_open(channel,addr)
        data = self.pi.i2c_read_byte_data(handle,register)
        self.pi.i2c_close(handle)
        return data

if __name__ == "__main__":
    from time import sleep
    d = correctedIMU()
    while 1:
        print(d.get_data())
        sleep(.1)



