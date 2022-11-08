import pigpio
from threading import Thread, Lock
from time import sleep

DEFAULT_REQUESTS = [
    # "X_POS","Y_POS","Z_POS",
    # "X_VEL","Y_VEL","Z_VEL",
    "X_ACC_RAW", "Y_ACC_RAW", "Z_ACC_RAW",
    # "X_DEG","Y_DEG","Z_DEG",
    "X_DPS", "Y_DPS", "Z_DPS",
    "X_MAG","Y_MAG","Z_MAG",
]
_2BYTE_MAX = 2**15

_DEFAULT_GYRO_ODR = 104
_DEFAULT_GYRO_RANGE = 1000
_DEFAULT_GYRO_FS_125 = 0
_DEFAULT_ACC_ODR = 104
_DEFAULT_ACC_RANGE = 2
_DEFAULT_ACC_LPF1_BW_SEL = 0
_DEFAULT_ACC_BW0_XL = 0

LSM6_GYRO_RANGE = {245: 0, 500: 1, 1000: 2, 2000: 3}
LSM6_ACC_RANGE = {2: 00, 4: 2, 16: 1, 8: 3}


LSM6_ODR_TABLE = {
    0: 0,
    "off": 0,
    12.5: 1,
    26: 2,
    52: 3,
    104: 4,
    208: 5,
    416: 6,
    833: 7,
    1660: 8,
    3330: 9,
    6660: 10,
    1.6: 11
}


class CorrectedIMU():
    ''' this is the position corrected imu for com of object'''

    def __init__(self, imu_address=0x6A, mag_address=0x1C, offsets=None):
        if offsets is None:
            offsets = {}

        self._offsets = offsets
        self.imu_adr = imu_address
        self.mag_adr = mag_address
        self.pi = pigpio.pi()
        self._CHANNEL = 1
        self.set_acc_config()
        self.set_gyro_config()
        self.REQUESTS_REG = {
            # "X_POS":
            # "Y_POS":
            # "Z_POS":
            # "X_VEL":
            # "Y_VEL":
            # "Z_VEL":
            # "X_ACC":
            # "Y_ACC":
            # "Z_ACC":
            "X_ACC_RAW": [self._bin2real, {"range": self._acc_range, "req": "X_ACC_BIN"}],
            "Y_ACC_RAW": [self._bin2real, {"range": self._acc_range, "req": "Y_ACC_BIN"}],
            "Z_ACC_RAW": [self._bin2real, {"range": self._acc_range, "req": "Z_ACC_BIN"}],
            "X_ACC_BIN": [self._req_N_from_dev, {"registers": [0x29, 0x28], "addr":imu_address}],
            "Y_ACC_BIN": [self._req_N_from_dev, {"registers": [0x2B, 0x2A], "addr":imu_address}],
            "Z_ACC_BIN": [self._req_N_from_dev, {"registers": [0x2D, 0x2C], "addr":imu_address}],
            # "X_DEG":
            # "Y_DEG":
            # "Z_DEG":
            "X_DPS": [self._bin2real, {"range": self._dps_range, "req": "X_DPS_BIN"}],
            "Y_DPS": [self._bin2real, {"range": self._dps_range, "req": "Y_DPS_BIN"}],
            "Z_DPS": [self._bin2real, {"range": self._dps_range, "req": "Z_DPS_BIN"}],
            "X_DPS_BIN": [self._req_N_from_dev, {"registers": [0x23, 0x22], "addr":imu_address}],
            "Y_DPS_BIN": [self._req_N_from_dev, {"registers": [0x25, 0x24], "addr":imu_address}],
            "Z_DPS_BIN": [self._req_N_from_dev, {"registers": [0x27, 0x26], "addr":imu_address}],
            # "X_MAG":[self._bin2real,{"req":"X_ACC_BIN"}],
            # "Y_MAG":[self._bin2real,{"req":"Y_ACC_BIN"}],
            # "Z_MAG":[self._bin2real,{"req":"Z_ACC_BIN"}],
            "X_MAG_BIN": [self._req_N_from_dev, {"registers": [0x29, 0x28], "addr":mag_address}],
            "Y_MAG_BIN": [self._req_N_from_dev, {"registers": [0x2B, 0x2A], "addr":mag_address}],
            "Z_MAG_BIN": [self._req_N_from_dev, {"registers": [0X2D, 0X2C], "addr":mag_address}],
        }
        self.auto_cal_gyro()

    def auto_cal_gyro(self):
        '''auto cals the gyro part of the imu
            returns 0 if failed 1 if success'''
        count = 0
        x_data = []
        y_data = []
        z_data = []
        while (count <= 5000):
            aqudata = self.get_data(["X_DPS_BIN", "Y_DPS_BIN", "Z_DPS_BIN"])
            x_data.append(aqudata["X_DPS_BIN"])
            y_data.append(aqudata["Y_DPS_BIN"])
            z_data.append(aqudata["Z_DPS_BIN"])
            count += 1
            if count > 50:
                xsample = x_data[-50:-1]
                ysample = y_data[-50:-1]
                zsample = z_data[-50:-1]
                if (abs(max(xsample)-min(xsample)) <= 15) and (abs(max(ysample)-min(ysample)) <= 15) and (abs(max(zsample)-min(zsample)) <= 15):
                    self._offsets["X_DPS_BIN"] = -round(sum(xsample)/len(xsample))
                    self._offsets["Y_DPS_BIN"] = -round(sum(ysample)/len(ysample))
                    self._offsets["Z_DPS_BIN"] = -round(sum(zsample)/len(zsample))
                    return 1
            sleep(.02)
        return 0

    def set_acc_config(self,
                       output_data_rate=_DEFAULT_ACC_ODR,
                       range=_DEFAULT_ACC_RANGE,
                       reg_LPF_BW_SEL=_DEFAULT_ACC_LPF1_BW_SEL,
                       reg_BW0_XL=_DEFAULT_ACC_BW0_XL,
                       ):
        odr_bits = LSM6_ODR_TABLE[output_data_rate]
        range_bits = LSM6_ACC_RANGE[range]
        reg_LPF_BW_SEL = reg_LPF_BW_SEL % 2
        if output_data_rate in LSM6_ODR_TABLE.keys():
            self._acc_odr = output_data_rate
        if range in LSM6_ACC_RANGE.keys():
            self._acc_range = range
        # print(hex((odr_bits*16)+(range_bits*4)+(reg_LPF_BW_SEL*2)+reg_BW0_XL))
        self._send8_to_dev((odr_bits*16)+(range_bits*4) +
                           (reg_LPF_BW_SEL*2)+reg_BW0_XL, 0x10, self.imu_adr)  # CTRL1_XL
        self._send8_to_dev(0x09, 0x17, self.imu_adr)  # CTRL8_XL
        pass

    def set_gyro_config(self,
                        output_data_rate=_DEFAULT_GYRO_ODR,
                        range=_DEFAULT_GYRO_RANGE,
                        reg_125=_DEFAULT_GYRO_FS_125
                        ):
        odr_bits = LSM6_ODR_TABLE[output_data_rate]
        if (odr_bits == 13):
            raise ValueError("odr cannot be set to that value")
        range_bits = LSM6_GYRO_RANGE[range]
        reg_125 = reg_125 % 2
        if output_data_rate in LSM6_ODR_TABLE.keys():
            self._dps_odr = output_data_rate
        if range in LSM6_GYRO_RANGE.keys():
            self._dps_range = range
        self._send8_to_dev(odr_bits*16+range_bits*4+reg_125 *
                           2, 0x11, self.imu_adr)  # CTRL2_G
        self._send8_to_dev(0x00, 0x16, self.imu_adr)  # CTRL7_G
        pass

    def get_data(self, data_req=DEFAULT_REQUESTS):
        if not isinstance(data_req, list):
            data_req = [data_req]
        out = dict((req, self.REQUESTS_REG[req][0](
            **(self.REQUESTS_REG[req][1]))) for req in data_req)
        return out

    def _bin2real(self, range, req):  # this goes down the rabbit hole and calls the other functions
        raw = self.REQUESTS_REG[req][0](**(self.REQUESTS_REG[req][1]))
        if req in self._offsets.keys():
            raw = raw + self._offsets[req]
        out = (raw/_2BYTE_MAX)*range
        # print(self.)
        return (out)

    def _req_N_from_dev(self, registers, addr, channel=None, *args):
        data = 0
        count = len(registers)
        for reg in registers:
            data = data * 256
            data = data + self._req8_from_dev(reg, addr, channel)
        # end for
        if data > 2**((count*8)-1)-1:
            data = data - 2**(count*8)
        # end if
        # print(data)
        return data

    def _req8_from_dev(self, register, addr, channel=None, *args):
        '''requests the packet from the device SHOULD NOT BE CALLED
            except through _req_N_from_dev'''
        if channel is None:
            channel = self._CHANNEL
        handle = self.pi.i2c_open(channel, addr)
        data = self.pi.i2c_read_byte_data(handle, register)
        self.pi.i2c_close(handle)
        return data

    def _send8_to_dev(self, data, register, addr, channel=None, *args):
        '''sends the packet from the device'''
        if channel is None:
            channel = self._CHANNEL
        handle = self.pi.i2c_open(channel, addr)
        self.pi.i2c_write_byte_data(handle, register, data)
        self.pi.i2c_close(handle)
        return data


if __name__ == "__main__":
    d = CorrectedIMU()
    #last  = d.get_data()
    while 1:
        print(d.get_data())
        sleep(.25)
