import multiprocessing as mp
import time
import argparse

# pip install sensirion-i2c-sht4x
# pip install sensirion-i2c-stc3x
# pip install sensirion-driver-adapters
# pip install sensirion-i2c-driver
from subsystems.subsystem import Subsystem
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_i2c_sht4x.device import Sht4xDevice
from sensirion_i2c_stc3x.device import Stc3xDevice

class Sensor(Subsystem):

     def __init__(self, sensor_data_in: mp.connection.Connection = None,
                 sensor_data_out: mp.connection.Connection = None,
                 set_points_in: mp.connection.Connection = None,
                 set_points_out: mp.connection.Connection = None,
                 status_in: mp.connection.Connection = None,
                 status_out: mp.connection.Connection = None,
                 T: int = 1000) -> 'Sensor':
          """
          Initialize the subsystem with one-way Pipes to communicate with the data bus.

          @param sensor_data_in: multiprocessing one-way Pipe to receive sensor data in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param sensor_data_out: multiprocessing one-way Pipe to send sensor data in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param set_points_in: multiprocessing one-way Pipe to receive set points in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param set_points_out: multiprocessing one-way Pipe to send set points in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param status_in: multiprocessing one-way Pipe to receive status in the following format:
               {"status": "on" or "off"}
          @param status_out: multiprocessing one-way Pipe to send status in the following format:
               {"status": "on" or "off"}
          @param T: sampling period in milliseconds (aka data is sent every T ms)
          
          @rtype: Subsystem
          @return: Initialized subsystem with necessary Pipes for communication
          """

          # initialize the subsystem parent class with data pipes
          super().__init__(sensor_data_in, sensor_data_out, set_points_in, set_points_out, status_in, status_out)
          
          self.T = T
          # initialize the logger
          #self.logger = mp.log_to_stderr()

     def start(self) -> None:
          # override the parent start() function
          # this is where you begin looping your process for implmenting functionality
          # pipes can be assessed like the following: self.pipe_sensor_data_in.send(<data_here>)
          # data packets can be created like the following: data_dict = {"CO2": 5.1, "temperature": 37.0, "humidity": 90.0}

                    # Initialize argument parser for I2C bus setup
          parser = argparse.ArgumentParser()
          parser.add_argument('--i2c-port', '-p', default='/dev/i2c-1')
          args = parser.parse_args()

          # Set up I2C bus for the STC31 and SHT40
          with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
               i2c_transceiver = I2cConnection(i2c_transceiver)
               stc31_channel = I2cChannel(i2c_transceiver,
                                             slave_address=0x29,
                                             crc=CrcCalculator(8, 0x31, 0xff, 0x0))
               sht40_channel = I2cChannel(i2c_transceiver,
                                             slave_address=0x44,
                                             crc=CrcCalculator(8, 0x31, 0xff, 0x0))
               self.stc31_sensor = Stc3xDevice(stc31_channel)
               self.sht40_sensor = Sht4xDevice(sht40_channel)
               time.sleep(0.014)

               # Output serial number for SHT40
               sht40_serial_number = self.sht40_sensor.serial_number()
               print(f"SENSE:\t\tSHT4x Serial Number = {sht40_serial_number}")

               # Output the product identifier and serial number for STC31
               (stc31_product_id, stc31_serial_number) = self.stc31_sensor.get_product_id()
               print(f"SENSE:\t\tSTC3x Product id = {stc31_product_id}")
               print(f"SENSE:\t\tSTC3x Serial Number = {stc31_serial_number}")

               # Measure STC31-C CO2 in air in range 0% - 25%
               self.stc31_sensor.set_binary_gas(19)

               while True:
                    # Set the sampling to 1Hz
                    cur_ns = time.monotonic_ns()

                    # Read humidity and temperature from SHT40 sensor and use
                    # it for CO2 measurement compensation.
                    sht40_temperature, sht40_humidity = self.sht40_sensor.measure_high_precision()

                    self.stc31_sensor.set_relative_humidity(sht40_humidity.value)
                    self.stc31_sensor.set_temperature(sht40_temperature.value)

                    # Read CO2 from STC31 sesnor
                    (co2_concentration, stc31_temperature) = self.stc31_sensor.measure_gas_concentration()

                    # Log CO2 concentration in Vol%, temperature in degree celsius,
                    # and humidity in %
                    #print({"CO2": co2_concentration.value, "temperature": sht40_temperature.value, 
                    #                              "humidity": sht40_humidity.value})
                    self.pipe_sensor_data_out.send({"CO2": co2_concentration.value, "temperature": sht40_temperature.value, 
                                                  "humidity": sht40_humidity.value})
                    
                    delta_ns = time.monotonic_ns() - cur_ns
                    print(f"SENSE:\t\tData read and transmitted in {delta_ns/1e6} ms")
                    time.sleep((self.T*1e6 - delta_ns)/1e9)
