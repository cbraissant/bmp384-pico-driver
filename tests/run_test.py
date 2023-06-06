import unittest
import utime
import urandom
from machine import SPI, Pin
from bmp384 import BMP384


class TestSanity(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(1,1)


class TestMicropythonLibraries(unittest.TestCase):
    def test_utime(self):
        utime.sleep_ms(100)

    def test_urandom(self):
        self.assertNotEqual(urandom.randint(1,10), 0)


class TestBMP384(unittest.TestCase):

    # The code was tested on a Raspberry Pi Pico.
    # Change values according to your own device
    def setUp(self):
        cs_pin = Pin(1, Pin.OUT)
        cs_pin.value(1)
        spi = SPI(0, baudrate=1_000_000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))
        utime.sleep_ms(50)
        self.sensor = BMP384(spi, cs_pin)        


    def test_read_register(self):
        self.assertEqual(self.sensor.device_id, 0x50)


    def test_write_then_read_register(self):
        # The register is read first as some old values might still be there
        old_value = self.sensor.fifo_watermark
        new_value = urandom.randint(0, 255)
        # Regenerate the random value until it's different from the old one
        while (old_value == new_value):
            new_value = urandom.randint(0, 255)     
        # Write and read the register
        self.sensor.fifo_watermark = new_value
        self.assertEqual(self.sensor.fifo_watermark, new_value, "FIFO watermark not set")


    def test_reset(self):
        # The FIFO register is set to act as a control value
        self.sensor.fifo_watermark = 0x23
        self.sensor.reset()
        self.assertEqual(self.sensor.fifo_watermark, 1, "FIFO not reset properly")



if __name__ == "__main__":
   unittest.main()