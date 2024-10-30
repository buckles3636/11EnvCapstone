import multiprocessing as mp
from typing import override

from subsystem import Subsystem

class Notifier(Subsystem):

    def __init__(self, sensor_data_in: mp.connection.Connection = None,
                 sensor_data_out: mp.connection.Connection = None,
                 set_point_in: mp.connection.Connection = None,
                 set_point_out: mp.connection.Connection = None):
        """
        Initialize the subsystem with one-way Pipes to communicate with the data bus

        @param sensor_data_in: multiprocessing one-way Pipe to receive sensor data
        @param sensor_data_out: multiprocessing one-way Pipe to send sensor data
        @param set_point_in: multiprocessing one-way Pipe to receive set points
        @param set_point_out: multiprocessing one-way Pipe to send set points

        @rtype: Notifier
        @return: Initialized Notifier subsystem with necessary Pipes for communication
        """
        super().__init__(sensor_data_in, sensor_data_out, set_point_in, set_point_out)

        self.flagger = Flagger()
        self.telebot = TeleBot()

    @override
    def start(self) -> None:
        pass

class Flagger():
    pass

class TeleBot():
    pass




