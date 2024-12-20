import multiprocessing as mp

from subsystem import Subsystem

class Logger(Subsystem):

     def __init__(self, sensor_data_in: mp.connection.PipeConnection = None,
                 sensor_data_out: mp.connection.PipeConnection = None,
                 set_points_in: mp.connection.PipeConnection = None,
                 set_points_out: mp.connection.PipeConnection = None,
                 status_in: mp.connection.PipeConnection = None,
                 status_out: mp.connection.PipeConnection = None) -> 'Logger':
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

          # create any necessary custom classes for functionality
          self.datalogger = DataLogger()

     def start(self) -> None:
          # override the parent start() function
          # this is where you begin looping your process for implmenting functionality
          # pipes can be assessed like the following: self.pipe_sensor_data_in.send(<data_here>)
          # data packets can be created like the following: data_dict = {"CO2": 5.1, "temperature": 37.0, "humidity": 90.0}
          pass

# custom class
class DataLogger:
    def __init__(self) -> None:
        self.current_file = None
        self.start_timestamp = None

    def update_file_status(self, running: bool) -> None:
        """
        Handle file creation and renaming based on the system's running status.

        @param running: Boolean indicating whether the system is running.
        """
        if running and not self.current_file:
            # System started running, create a new file
            self.start_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_file = f"{self.start_timestamp}.csv"
            with open(self.current_file, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Temperature", "Humidity", "CO2 Concentration"])
        
        elif not running and self.current_file:
            # System stopped running, rename the file
            end_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"{self.start_timestamp}-done_{end_timestamp}.csv"
            os.rename(self.current_file, new_file_name)
            self.current_file = None
            self.start_timestamp = None

    def log_sensor_data(self, data: dict) -> None:
        """
        Log sensor data to the current file if it exists.

        @param data: Dictionary containing sensor data.
        """
        if self.current_file:
            with open(self.current_file, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data.get("temperature", ""), 
                                 data.get("humidity", ""), 
                                 data.get("CO2", "")])
