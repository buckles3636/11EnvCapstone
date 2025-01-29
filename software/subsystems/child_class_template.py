import multiprocessing as mp

from subsystem import Subsystem

class Child_Subsystem(Subsystem):

     def __init__(self, sensor_data_in: mp.connection.Connection = None,
                 sensor_data_out: mp.connection.Connection = None,
                 set_points_in: mp.connection.Connection = None,
                 set_points_out: mp.connection.Connection = None,
                 status_in: mp.connection.Connection = None,
                 status_out: mp.connection.Connection = None) -> 'Child_Subsystem':
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
          @rtype: Subsystem
          @return: Initialized subsystem with necessary Pipes for communication
          """

          # initialize the subsystem parent class with data pipes
          super().__init__(sensor_data_in, sensor_data_out, set_points_in, set_points_out, status_in, status_out)

          # initialize the logger
          self.logger = mp.log_to_stderr()

          # create any necessary custom classes for functionality
          self.class_1 = Class1()
          self.class_2 = Class2()

     def start(self) -> None:
          # override the parent start() function
          # this is where you begin looping your process for implmenting functionality
          # pipes can be assessed like the following: self.pipe_sensor_data_in.send(<data_here>)
          # data packets can be created like the following: data_dict = {"CO2": 5.1, "temperature": 37.0, "humidity": 90.0}
          pass

# custom class
class Class1():
     pass

# custom class
class Class2():
     pass
