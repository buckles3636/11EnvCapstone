
import time
from multiprocessing import Pipe

# Simulate sensor data
def read_sensors(pipe_send):
    while True:
        # Simulate reading sensor data
        co2_concentration = 400  # Example value, replace with actual sensor code
        temp = 25  # Example value
        humidity = 50  # Example value
        pipe_send.send((co2_concentration, temp, humidity))
        time.sleep(1)  # Simulate a 1-second delay between sensor reads
