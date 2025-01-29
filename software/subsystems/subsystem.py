import multiprocessing as mp

class Subsystem():

    # create so interpreter can use PipeConnection for typing
    _garbage = mp.Pipe()

    def __init__(self, sensor_data_in: mp.connection.Connection = None,
                 sensor_data_out: mp.connection.Connection = None,
                 set_points_in: mp.connection.Connection = None,
                 set_points_out: mp.connection.Connection = None,
                 status_in: mp.connection.Connection = None,
                 status_out: mp.connection.Connection = None) -> 'Subsystem':
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

        self.pipe_sensor_data_in = sensor_data_in
        self.pipe_sensor_data_out = sensor_data_out
        self.pipe_set_point_in = set_points_in
        self.pipe_set_point_out = set_points_out
        self.pipe_status_in = status_in
        self.pipe_status_out = status_out
    

    def start(self):
        """
        Start subsystem process that loops continuously, publishing to and polling pipes as needed 

        @return: None
        """
        # TODO override in subsystem implementation
        
