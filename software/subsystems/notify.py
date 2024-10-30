import multiprocessing as mp
from datetime import datetime
import requests
from urllib.parse import quote_plus

from subsystem import Subsystem

class Notifier(Subsystem):

    def __init__(self, sensor_data_in: mp.connection.PipeConnection = None,
                    sensor_data_out: mp.connection.PipeConnection = None,
                    set_points_in: mp.connection.PipeConnection = None,
                    set_points_out: mp.connection.PipeConnection = None) -> 'Notifier':
        """
        Initialize the subsystem with one-way Pipes to communicate with the data bus

        @param sensor_data_in: multiprocessing one-way Pipe to receive sensor data
        @param sensor_data_out: multiprocessing one-way Pipe to send sensor data
        @param set_point_in: multiprocessing one-way Pipe to receive set points
        @param set_point_out: multiprocessing one-way Pipe to send set points

        @rtype: Notifier
        @return: Initialized Notifier subsystem with necessary Pipes for communication
        """
        super().__init__(sensor_data_in, sensor_data_out, set_points_in, set_points_out)

        self.flagger = Flagger()
        self.telebot = TeleBot()

    def start(self) -> None:
        pass

class Flagger():

    MSMT: str                               # The environmental variable being monitored ∈ {CO2, Humidity, Temperature}
    SET_PT: float                           # The current set-point for the environmental variable
    FLAG_THRESH: float                      # The threshold in percent deviation from the set point to qualify a measurement as a deviation
    FLAG_PERIOD: int                        # The duration in seconds for a deviation/stability to be flagged
    FLAG_TOL: float                         # The percent of measurements during a flag period that must satisfy the flag threshold
    DATA_FREQ: float                        # The frequency of the data stream in Hz
    _enable: bool                           # Control whether the flagger is active
    _flag_start: datetime                   # The timestamp of the start of a flag period
    _flagged_measurements: list[float]      # The list of measurements during a flag period
    _status: str                            # The status of the flagger ∈ {stable, stabilizing, deviated, deviating}:
                                            #   stable: measurements have been within flag threshold for more than a flag period
                                            #   stabilizing: measurements have been within flag threshold for less than a flag period
                                            #   deviated: measurements have been outside flag threshold for more than a flag period
                                            #   deviating: measurements have been outside flag threshold for less than a flag period

    def __init__(self, msmt: str, set_pt: float, flag_thresh: float, flag_period: int, flag_tol: float, data_freq: float) -> 'Flagger':
        """
        Initialize a Flagger object and set attributes corresponding to the data being monitored and desired flagging characteristics. The flagger is disabled initially.

        @param msmt: The environmental variable being monitored ∈ {CO2, Humidity, Temperature}
        @param set_pt: The current set-point for the environmental variable
        @param flag_thresh: The threshold in percent deviation from the set point to qualify a measurement as a deviation
        @param flag_period: The duration in seconds for a deviation/stability to be flagged
        @param flag_tol: The percent of measurements during a flag period that must satisfy the flag threshold
        @param data_freq: The frequency of the data stream in Hz
        
        @rtype: Flagger
        @return Flagger object that is initially stable and disabled
        """
        self.MSMT = msmt
        self.SET_PT = set_pt
        self.FLAG_THRESH = flag_thresh
        self.FLAG_PERIOD = flag_period
        self.FLAG_TOL = flag_tol
        self.DATA_FREQ = data_freq
        self._enable = False
        self._flagged_measurements = []
        self._status = "stable"

    def new_data_pt(self, pt: float) -> 'Flag':
        """
        Feed a data point to the flagger object.
        A flag is returned if the data stream exhibits a deviation or stabilization.
        Otherwise, None will be returned.

        @param pt: the most recent data point

        @rtype: Flag
        @return: A flag if data exhibits a change in state; otherwise, None
        """
        # TODO logic to flag measurements here
        pass

    def enable(self) -> None:
        """
        Enable the flagger, clearing any flagged measurements and setting the status to stable
        """

        self._flagged_measurements = []
        self._status = "stable"
        self._enable = True

    def disable(self) -> None:
        """
        Disable the flagger
        """

        self._enable = False

class Flag:

    MSMT: str               # The environmental variable being monitored ∈ {CO2, Humidity, Temperature}
    SET_PT: float           # The current set-point for the environmental variable
    FLAG_THRESH: float      # The threshold in percent deviation from the set point to qualify a measurement as a deviation
    FLAG_TIME: datetime     # The timestamp of the start of a flag period
    FLAG_STATUS: str        # The status of the flag ∈ {deviated, stabilized}:
                            #   deviated: the system deviated from the set point 
                            #   stabilized: the system returned to the set point
    AVE: float              # The average value of the environmental value over the flag period

    def __init__(self, msmt: str, set_pt: float, flag_thresh: float, flag_time: datetime, flag_status: str, ave: float) -> 'Flag':
        """
        Initialize a Flag object and set attributes corresponding to the flagged data.

        @param msmt: The environmental variable being monitored ∈ {CO2, Humidity, Temperature}
        @param set_pt: The current set-point for the environmental variable
        @param flag_thresh: The threshold in percent deviation from the set point to qualify a measurement as a deviation
        @param flag_time: The timestamp of the start of a flag period
        @param flag_status: The status of the flag ∈ {deviated, stabilized}:
                                deviated: the system deviated from the set point 
                                stabilized: the system returned to the set point
        @param ave: The average value of the environmental value over the flag period
        """

        self.MSMT = msmt
        self.SET_PT = set_pt
        self.FLAG_THRESH = flag_thresh
        self.FLAG_TIME = flag_time
        self.FLAG_STATUS = flag_status
        self.AVE = ave
    
    def to_report(self) -> str:

        # build date and time strings
        date = "%02d.%02d.%4d" % (self.FLAG_TIME.month, self.FLAG_TIME.day, self.FLAG_TIME.year)
        time = "%02d:%02d" % (self.FLAG_TIME.hour, self.FLAG_TIME.minute)

        # compile markdown message
        report = ""
        if (self.MSMT == "CO2"):
            report = "CO2 %s (%s @ %s):\nSet Point: %.1f%% | Current: %.1f%% | Thresh: %.1f%%" % (
                self.FLAG_STATUS,
                date,
                time,
                self.SET_PT,
                self.AVE,
                self.FLAG_THRESH/100 * self.SET_PT
            )

        elif (self.MSMT == "Humidity"):
            report = "Humidity %s (%s @ %s):\n Set Point: %.0f%% | Current: %.0f%% | Thresh: %.0f%%" % (
                self.FLAG_STATUS,
                date,
                time,
                self.SET_PT,
                self.AVE,
                self.FLAG_THRESH/100 * self.SET_PT
            )
        
        elif (self.MSMT == "Temperature"):
            report = "Temperature %s (%s @ %s):\nSet Point: %.1f degC | Current: %.1f degC | Thresh: %.1f degC" % (
                self.FLAG_STATUS,
                date,
                time,
                self.SET_PT,
                self.AVE,
                self.FLAG_THRESH/100 * self.SET_PT
            )

        return report

class TeleBot():
    
    NAME: str       # The name of the bot - must match name of created Telegram bot​
    USERNAME: str   # The username of the bot - must match username of created Telegram bot​
    TOKEN: str      # The token for the bot - must match the token for the created Telegram bot​
    CHAT_ID: str    # The unique identifier for the target chat to send messages to
    
    def __init__(self, name: str, username: str, token: str, chat_id: str) -> 'TeleBot':
        """
        Initialize a TeleBot object used to send messages to a defined Telegram chat.​

        @param name: The name of the bot - must match name of created Telegram bot​
        @param username: The username of the bot - must match username of created Telegram bot​
        @param token: The token for the bot - must match the token for the created Telegram bot​

        @rtype TeleBot
        @return A initialized bot ready to send messages
        """

        self.NAME = name
        self.USERNAME = username
        self.TOKEN = token
        self.CHAT_ID = chat_id

    def send_message(self, msg: str) -> datetime:
        """
        Send the provided string to the Telegram chat using Python requests library, returning the date and time the message was sent.​

        @param msg: The string in MarkdownV2 format to be sent. Max of 4096 characters.

        @rtype datetime
        @return The date and time the message was sent.
        """

        # build url and make request
        url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (self.TOKEN, self.CHAT_ID, msg)
        response = requests.post(url)

        # convert message timestamp to a datetime object
        if (response.json()["ok"]):
            unix_timestamp = response.json()["result"]["date"]
            return datetime.fromtimestamp(unix_timestamp)
        else:
            print("MESSAGE NOT DELIVERED:\n", response.json())
            return None