import multiprocessing as mp

class Subsystem():

    # create so interpreter can use PipeConnection for typing
    _garbage = mp.Pipe()

    def __init__(self,
                 sensor_data_in: mp.connection.PipeConnection = None,
                 sensor_data_out: mp.connection.PipeConnection = None,
                 set_points_in: mp.connection.PipeConnection = None,
                 set_points_out: mp.connection.PipeConnection = None) -> 'Subsystem':
        """
        Initialize the subsystem with one-way Pipes to communicate with the data bus

        @param sensor_data_in: multiprocessing one-way Pipe to receive sensor data
        @param sensor_data_out: multiprocessing one-way Pipe to send sensor data
        @param set_points_in: multiprocessing one-way Pipe to receive set points
        @param set_points_out: multiprocessing one-way Pipe to send set points

        @rtype: Subsystem
        @return: Initialized subsystem with necessary Pipes for communication
        """

        self.pipe_sensor_data_in = sensor_data_in
        self.pipe_sensor_data_out = sensor_data_out
        self.pipe_set_point_in = set_points_in
        self.pipe_set_point_out = set_points_out

    def start(self):
        """
        Start subsystem process that loops continuously, publishing to and polling pipes as needed 

        @return: None
        """
        # TODO override in subsystem implementation
        
