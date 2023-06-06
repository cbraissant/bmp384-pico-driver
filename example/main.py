import utime
from machine import SPI, Pin
from bmp384 import BMP384

# Create a new SPI device, and assign the pins corresponding to your device
cs_pin = Pin(1, Pin.OUT)
cs_pin.value(1)
spi = SPI(0, baudrate=1_000_000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

# The pico startfaster than the sensor, so a delay must be introduced
utime.sleep_ms(50)

# Create a new instance of the sensor
sensor = BMP384(spi, cs_pin)

# By default, the pressure and temperature sensors are disabled
sensor.enable_pressure_sensor = 1
sensor.enable_temperature_sensor = 1


# By default, the device is in power-down mode and the mode need to be changed
# for the device to take continuous measurements
sensor.mode = 3

# If necessary, filter the data by adjusting the IIR filter coefficient
# sensor.iir_filter_coefficient = 3

# Change the resolution of the signal by chaning the oversampling
# sensor.pressure_oversampling = 0

sensor.temperature
