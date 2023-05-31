# Micropython library for the Bosch BMP384 pressure sensor
#
# Author: Chris Braissant
# License: MIT


from machine import SPI, Pin
from register import Register, Bits


_CHIP_ID = 0x00
_ERR_REG = 0x02
_STATUS = 0x03
_PRESS_XLSB = 0x04
_PRESS_LSB = 0x05
_PRESS_MSB = 0x06
_TEMP_XLSB = 0x07
_TEMP_LSB = 0x08
_TEMP_MSB = 0x09
_SENSOR_TIME_XLSB = 0x0C
_SENSOR_TIME_LSB = 0x0D
_SENSOR_TIME_MSB = 0x0E
_SENSOR_TIME_XMSB = 0x0F
_EVENT = 0x10
_INT_STATUS = 0x11
_FIFO_LENGTH_0 = 0x12
_FIFO_LENGTH_1 = 0x13
_FIFO_DATA = 0x14
_FIFO_WTM_0 = 0x15
_FIFO_WTM_1 = 0x16
_FIFO_CONFIG_1 = 0x17
_FIFO_CONFIG_2 = 0x18
_INT_CTRL = 0x19
_IF_CONF = 0x1A
_PWR_CTRL = 0x1B
_OSR = 0x1C
_ODR = 0x1D
_CONFIG = 0x1F
_CMD = 0x7E


class BMP384:
    
    # REGISTERS
    _chip_id = Register(_CHIP_ID)
    _press = Register(_PRESS_XLSB, 3)
    _temp = Register(_TEMP_XLSB, 3)
    _sensor_time = Register(_SENSOR_TIME_XLSB, 4)
    _fifo_length = Register(_FIFO_LENGTH_0, 2)
    _fifo_data = Register(_FIFO_DATA)
    _fifo_wtm = Register(_FIFO_WTM_0, 2)
    _cmd = Register(_CMD)

    # ERR_REG
    _fatal_eff = Bits(_ERR_REG, 0)
    _cmd_err = Bits(_ERR_REG, 1)
    _conf_eff = Bits(_ERR_REG, 2)

    # STATUS
    _cmd_rdy = Bits(_STATUS, 5)
    _drdy_press = Bits(_STATUS, 6)
    _drdy_temp = Bits(_STATUS, 7)

    # EVENT
    _por_detected = Bits(_EVENT, 0)

    # INT_STATUS
    _fwm_int = Bits(_INT_STATUS, 0)
    _ffull_int = Bits(_INT_STATUS, 1)
    _drdy = Bits(_INT_STATUS, 3)

    # FIFO_CONFIG_1
    _fifo_mode = Bits(_FIFO_CONFIG_1, 0)
    _fifo_stop_on_full = Bits(_FIFO_CONFIG_1, 1)
    _fifo_time_en = Bits(_FIFO_CONFIG_1, 2)
    _fifo_press_en = Bits(_FIFO_CONFIG_1, 3)
    _fifo_temp_en = Bits(_FIFO_CONFIG_1, 4)

    # FIFO_CONFIG_2
    _fifo_subsampling = Bits(_FIFO_CONFIG_2, 0, 3)
    _data_select = Bits(_FIFO_CONFIG_2, 3, 2)

    # INT_CTRL
    _int_od = Bits(_INT_CTRL, 0)
    _int_level = Bits(_INT_CTRL, 1)
    _int_latch = Bits(_INT_CTRL, 2)
    _fwtm_en = Bits(_INT_CTRL, 3)
    _ffull_en = Bits(_INT_CTRL, 4)
    _drdy_en = Bits(_INT_CTRL, 6)

    # IF_CONF
    _spi3 = Bits(_IF_CONF, 0)
    _i2c_wdt_en = Bits(_IF_CONF, 1)
    _i2c_wdt_sel = Bits(_IF_CONF, 2)

    # PWR_CTRL
    _press_en = Bits(_PWR_CTRL, 0)
    _temp_en = Bits(_PWR_CTRL, 1)
    _mode = Bits(_PWR_CTRL, 4, 2)

    # OSR
    _osr_p = Bits(_OSR, 0, 3)
    _osr_t = Bits(_OSR, 3, 3)

    # ODR
    _odr_sel = Bits(_ODR, 0, 5)

    # CONFIG
    _iir_filter = Bits(_CONFIG, 1, 3)
