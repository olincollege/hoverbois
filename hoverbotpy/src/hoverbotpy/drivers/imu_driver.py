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

_DEFAULT_GYRO_ODR = 104
_DEFAULT_GYRO_RANGE = 1000
_DEFAULT_GYRO_FS_125 = 0
_DEFAULT_ACC_ODR = 104
_DEFAULT_ACC_RANGE = 2
_DEFAULT_ACC_LPF1_BW_SEL = 0
_DEFAULT_ACC_BW0_XL = 0

LSM6_GYRO_RANGE = {245:0,500:1,1000:2,2000:3}
LSM6_ACC_RANGE = {2:00,4:2,16:1,8:3}


LSM6_ODR_TABLE ={
    0:0,
    "off":0,
    12.5:1,
    26:2,
    52:3,
    104:4,
    208:5,
    416:6,
    833:7,
    1660:8,
    3330:9,
    6660:10,
    1.6:11
    }

class correctedIMU():
    ''' this is the position corrected imu for com of object'''
    
    def __init__(self, imu_address=0x1c, mag_address=0x6a):
        self.imu_adr = imu_address
        self.mag_adr = mag_address
        self.pi = pigpio.pi()
        self._CHANNEL = 1
        self.set_acc_config()
        self.set_gyro_config()

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
            "X_ACC_RAW":[self.acc_bin2real,{"req":"X_ACC_BIN"}],
            "Y_ACC_RAW":[self.acc_bin2real,{"req":"Y_ACC_BIN"}],
            "Z_ACC_RAW":[self.acc_bin2real,{"req":"Z_ACC_BIN"}],
            "X_ACC_BIN":[self._req_N_from_dev,{"registers":[0x29,0x28],"addr":imu_address}],
            "Y_ACC_BIN":[self._req_N_from_dev,{"registers":[0x2B,0x2A],"addr":imu_address}],
            "Z_ACC_BIN":[self._req_N_from_dev,{"registers":[0x2D,0x2C],"addr":imu_address}],
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

    def set_acc_config(self,
        output_data_rate=_DEFAULT_ACC_ODR,
        range=_DEFAULT_ACC_RANGE,
        reg_LPF_BW_SEL=_DEFAULT_ACC_LPF1_BW_SEL,
        reg_BW0_XL = _DEFAULT_ACC_BW0_XL,
        ):
        odr_bits = LSM6_ODR_TABLE[output_data_rate]
        range_bits = LSM6_ACC_RANGE[range]
        reg_LPF_BW_SEL = reg_LPF_BW_SEL%2
        if output_data_rate in LSM6_ODR_TABLE.keys():
            self._acc_odr = output_data_rate
        if range in LSM6_ACC_RANGE.keys():
            self._acc_range = range
        self._send8_to_dev(odr_bits*16+range_bits*4+reg_LPF_BW_SEL*2+reg_BW0_XL,0x10,self.imu_adr)#CTRL1_XL
        self._send8_to_dev(0x09,0x17,self.imu_adr)#CTRL8_XL
        pass


    def set_gyro_config(self,
        output_data_rate=_DEFAULT_GYRO_ODR,
        range=_DEFAULT_GYRO_RANGE,
        reg_125=_DEFAULT_GYRO_FS_125
        ):
        odr_bits = LSM6_ODR_TABLE[output_data_rate]
        if(odr_bits == 13):
            raise ValueError("odr cannot be set to that value")
        range_bits = LSM6_GYRO_RANGE[range]
        reg_125 = reg_125%2
        if output_data_rate in LSM6_ODR_TABLE.keys():
            self._acc_odr = output_data_rate
        if range in LSM6_ACC_RANGE.keys():
            self._acc_range = range
        self._send8_to_dev(odr_bits*16+range_bits*4+reg_125*2,0x11,self.imu_adr)#CTRL2_G
        self._send8_to_dev(0x00,0x16,self.imu_adr)#CTRL7_G
        pass
    
    def get_data(self,data_req = DEFAULT_REQUESTS):
        if  not isinstance(data_req,list):
            data_req = [data_req]
        out = dict((req, self.REQUESTS_REG[req][0](
            **(self.REQUESTS_REG[req][1]))) for req in data_req)
        return out

    def acc_bin2real(self,req):
        raw = self.REQUESTS_REG[req][0](**(self.REQUESTS_REG[req][1]))
        out = raw * self._acc_range/_2BYTE_MAX
        return(out)

    def _req_N_from_dev(self,registers,addr,channel=None,*args):
        data = 0
        count =  len(registers)
        for i, reg in enumerate(registers):
            print(i)
            data = data * 256
            data = data + self._req8_from_dev(reg,addr,channel)
            print(data)
        #end for
        if i == 0 and data > 2^(count-1)-1:
            data = data - 2^count
            print(data)
        #end if
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

    def _send8_to_dev(self,data,register,addr,channel=None,*args):
        '''sends the packet from the device '''
        if channel is None:
            channel=self._CHANNEL
        handle = self.pi.i2c_open(channel,addr)
        self.pi.i2c_write_byte_data(handle,register,data)
        self.pi.i2c_close(handle)
        return data

    

if __name__ == "__main__":
    from time import sleep
    d = correctedIMU()
    while 1:
        print(d.get_data(["X_ACC_RAW"]))
        sleep(1)



