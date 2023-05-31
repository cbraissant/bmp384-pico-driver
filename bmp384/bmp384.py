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
    _fatal_err = Bits(_ERR_REG, 0)
    _cmd_err = Bits(_ERR_REG, 1)
    _conf_err = Bits(_ERR_REG, 2)

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


    def __init__(self, spi:SPI, cs:Pin):
        self.spi = spi
        self.cs = cs


    @property
    def spi_device(self) -> SPI:
        '''Serial Peripherical Interface (SPI)'''
        return self.spi
    
    @spi_device.setter
    def spi_device(self, spi:SPI) -> None:
        self.spi = spi

    
    @property
    def cs_pin(self) -> Pin:
        '''Chip Select Pin used to enable/disable the SPI'''
        return self.cs

    @cs_pin.setter
    def cs_pin(self, cs_pin:Pin) -> None:
        self.cs = cs_pin
    

    @property
    def device_id(self) -> int:
        '''
        Device identification
        For the BMP384, the default value is 80 (0x50)
        '''
        return self._chip_id
    

    @property
    def fatal_error(self) -> int:
        '''Sensor fatal error'''
        return self._fatal_err
    

    @property
    def command_error(self) -> int:
        '''Command execution failed. Cleared on read.'''
        return self._cmd_err
    

    @property
    def configuration_error(self) -> int:
        '''Sensor configuration error detected. Cleared on read.'''
        return self._conf_err
    

    @property
    def command_ready(self) -> int:
        '''
        CMD decoder status.
            0: Command in progress
            1: Command decoder is ready to accept a new command
        '''
        return self._cmd_rdy
    

    @property
    def pressure_data_ready(self) -> int:
        '''
        Data ready for pressure.
        It gets reset, when one pressure DATA register is read out
        '''
        return self._drdy_press
    

    @property
    def temperature_data_ready(self) -> int:
        '''
        Data ready for temperature.
        It gets reset, when one temperature DATA register is read out
        '''
        return self._drdy_temp


    @property
    def raw_pressure(self) -> int:
        '''Pressure value as a 24-bit data'''
        return self._press


    @property
    def raw_temperature(self) -> int:
        '''Temperature value as a 24-bit data'''
        return self._temp
    
    
    @property
    def time(self) -> int:
        '''Sensor time value as a 24-bit data'''
        return self._sensor_time
    

    @property
    def power_up_detected(self) -> int:
        '''
        Power up detected.
            1: After device power up or softreset. Clear-on-read
        '''
        return self._por_detected
    

    @property
    def fifo_watermark_interrupt(self) -> int:
        '''FIFO Watermark Interrupt'''
        return self._fwm_int
    

    @property
    def fifo_full_interrupt(self) -> int:
        '''FIFO Full Interrupt'''
        return self._ffull_int
    

    @property
    def data_ready_interrupt(self) -> int:
        '''Data ready interrupt'''
        return self._drdy
    

    @property
    def fifo_length(self) -> int:
        '''Indicates the current fill level of the FIFO buffer.'''
        # The value if over 9 bits and the rest of the MSB register is reserved.
        return (self._fifo_length & 0x01FF)
    

    @property
    def fifo_data(self) -> int:
        '''FIFO data output register'''
        return self._fifo_data
    

    @property
    def fifo_watermark(self) -> int:
        '''FIFO watermark '''
        # The value if over 9 bits and the rest of the MSB register is reserved.
        return (self._fifo_wtm & 0x01FF)
    
    @fifo_watermark.setter
    def fifo_watermark(self, data:int) -> None:
        # The value if over 9 bits and the rest of the MSB register is reserved.
        self._fifo_wtm = data & 0x01FF


    @property
    def fifo_mode(self) -> int:
        '''Enables or disables the FIFO'''
        return self._fifo_mode
    
    @fifo_mode.setter
    def fifo_mode(self, data:int) -> None:
        self._fifo_mode = data


    @property
    def fifo_stop_on_full(self) -> int:
        '''Stop writing samples into FIFO when FIFO is full.'''
        return self._fifo_stop_on_full
    
    @fifo_stop_on_full.setter
    def fifo_stop_on_full(self, data:int) -> None:
        self._fifo_stop_on_full = data


    @property
    def fifo_time_enable(self) -> int:
        '''Return sensortime frame after the last valid data frame'''
        return self._fifo_time_en
    
    @fifo_time_enable.setter
    def fifo_time_enable(self, data:int) -> None:
        self._fifo_time_en = data

    
    @property
    def fifo_press_enable(self) -> int:
        '''Store pressure data in FIFO'''
        return self._fifo_press
    
    @fifo_press_enable.setter
    def fifo_press_enable(self, data:int) -> None:
        self._fifo_press = data

    
    @property
    def fifo_temp_enable(self) -> int:
        '''Store temperature data in FIFO'''
        return self._fifo_temp_en
    
    @fifo_temp_enable.setter
    def fifo_temp_enable(self, data:int) -> None:
        self._fifo_temp_en = data

    
    @property
    def fifo_downsampling(self) -> int:
        '''
        FIFO downsampling selection for pressure and temperature data, 
        factor is 2^fifo_subsampling
        '''
        return self._fifo_subsampling
    
    @fifo_downsampling.setter
    def fifo_downsampling(self, data:int) -> None:
        self._fifo_subsampling = data


    @property
    def data_select(self) -> int:
        '''
        for pressure and temperature, select data source
            00: unfiltered data (compensated or uncompensated)
            01: filtered data (compensated or uncompensated)
            11/10: reserved, same as for "unfilt"
        '''
        return self._data_select
    
    @data_select.setter
    def data_select(self, data:int) -> None:
        self._data_select = data 


    @property
    def interrupt_open_drain(self) -> int:
        '''
        Configure output: open-drain or push-pull
            0: push-pull
            1: open-drain
        '''
        return self._int_od
    
    @interrupt_open_drain.setter
    def interrupt_open_drain(self, data:int) -> None:
        self._int_od = data


    @property
    def interrupt_level(self) -> int:
        '''
        level of INT pin
            0: active_low
            1: active_high
        '''
        return self._int_level
    
    @interrupt_level.setter
    def interrupt_level(self, data:int) -> None:
        self._int_level = data

    
    @property
    def interrupt_latching(self) -> int:
        '''
        Latching of interrupts for INT pin and INT_STATUS register
            0: disabled
            1: enabled
        '''
        return self._int_latch
    
    @interrupt_latching.setter
    def interrupt_latching(self, data:int) -> None:
        self._int_latch = data

    
    @property
    def enable_interrupt_fifo_watermark(self) -> int:
        '''
        Enable FIFO watermark reached interrupt for INT pin and INT_STATUS.
            0: disabled
            1: enabled
        '''
        return self._fwtm_en
    
    @enable_interrupt_fifo_watermark.setter
    def enable_interrupt_fifo_watermark(self, data:int) -> None:
        self._fwtm_en = data


    @property
    def enable_interrupt_fifo_full(self) -> int:
        '''
        Enable Fifo full interrupt for INT pin and INT_STATUS
            0: disabled
            1: enabled
        '''
        return self._ffull_en
    
    @enable_interrupt_fifo_full.setter
    def enable_interrupt_fifo_full(self, data:int) -> None:
        self._ffull_en = data
    

    @property
    def enable_interrupt_data_ready(self) -> int:
        '''
        Enable temperature / pressure data ready interrupt for INT pin and INT_STATUS
            0: disabled
            1: enable
        '''
        return self._drdy_en
    
    @enable_interrupt_data_ready.setter
    def enable_interrupt_data_ready(self, data:int) -> None:
        self._drdy_en = data

    
    @property
    def spi_configuration(self) -> int:
        '''
        Configure SPI Interface Mode for primary interface
            0: spi4 SPI 4-wire mode
            1: spi3 SPI 3-wire mode
        '''
        return self._spi3
    
    @spi_configuration.setter
    def spi_configuration(self, data:int) -> None:
        self._spi3 = data


    @property
    def enable_i2c_watchdog(self) -> int:
        '''Enable for the I2C Watchdog timer, backed by NVM
            0: disabled Watchdog disabled
            1: enabled Watchdog enabled
        '''
        return self._i2c_wdt_en
    
    @enable_i2c_watchdog.setter
    def enable_i2c_watchdog(self, data:int) -> None:
        self._i2c_wdt_en = data

    
    @property
    def i2c_watchdog_timeout(self) -> int:
        '''
        Select timer period for I2C Watchdog , backed by NVM
            0: wdt_short I2C watchdog timeout after 1.25 ms
            1: wdt_long I2C watchdog timeout after 40 ms
        '''
        return self._i2c_wdt_sel
    
    @i2c_watchdog_timeout.setter
    def i2c_watchdog_timeout(self, data:int) -> None:
        self._i2c_wdt_sel = data

    
    @property
    def enable_pressure_sensor(self) -> int:
        '''Enables the pressure sensor'''
        return self._press_en
    
    @enable_pressure_sensor.setter
    def enable_pressure_sensor(self, data:int) -> None:
        self._press_en = data

    
    @property
    def enable_temperature_sensor(self) -> int:
        '''Enable the temperature sensor'''
        return self._temp_en
    
    @enable_temperature_sensor.setter
    def enable_temperature_sensor(self, data:int) -> None:
        self._temp_en = data

    
    @property
    def mode(self) -> int:
        '''
        Mode selection
            00: sleep mode
            01/10: forced mode
            11: normal mode
        '''
        return self._mode
    
    @mode.setter
    def mode(self, data:int) -> None:
        self._mode = data


    @property
    def pressure_oversampling(self) -> int:
        '''
        Oversampling setting pressure measurement
            000: x1     no oversampling.
            001: x2     x2 oversampling.
            010: x4     x4 oversampling.
            011: x8     x8 oversampling.
            100: x16    x16 oversampling.
            101: x32    x32 oversampling.
        '''
        return self._osr_p
    
    @pressure_oversampling.setter
    def pressure_oversampling(self, data:int) -> None:
        self._osr_p = data


    @property
    def temperature_oversampling(self) -> int:
        '''
        Oversampling setting temperature measurement
            000: x1     no oversampling.
            001: x2     x2 oversampling.
            010: x4     x4 oversampling.
            011: x8     x8 oversampling.
            100: x16    x16 oversampling.
            101: x32    x32 oversampling.
        '''
        return self._osr_p
    
    @temperature_oversampling.setter
    def temperature_oversampling(self, data:int) -> None:
        self._osr_p = data


    @property
    def odr_prescaler(self) -> int:
        '''
        Output Data Rate (ODR) prescaler.
        Set the sampling period and frequency divider.
        The final ODR is: 200 Hz / 2^value
        Allowed values are 0 to 17. Other values are saturated at 17.
        '''
        return self._odr_se
    
    @odr_prescaler.setter
    def odr_prescaler(self, data:int) -> None:
        self._odr_se = data