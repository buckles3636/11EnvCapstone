#--------------------------------------------------------------------------------#
# Peter Buckley
# 10/18/2024
# This file serves as a placeholder to randomly change sensor data evey second
#--------------------------------------------------------------------------------#

import time
import random
from multiprocessing import Pipe

# Simulate sensor data with random variation
def read_sensors(pipe_send):
    # Initial sensor values
    co2_concentration = 20
    temp = 30
    humidity = 85

    while True:
        # Randomly vary the sensor values within a reasonable range
        co2_concentration += random.uniform(-5, 5)  # Vary CO2 by +/- 5 %
        temp += random.uniform(-1, 1)            # Vary temperature by +/- 1 °C
        humidity += random.uniform(-10, 10)            # Vary humidity by +/- 10 %

        # Ensure values stay within reasonable limits
        co2_concentration = max(5, min(30, co2_concentration))  # CO2 between 300 and 600 ppm
        temp = max(15, min(35, temp))                              # Temp between 15 and 35 °C
        humidity = max(30, min(70, humidity))                      # Humidity between 30 and 70 %

        # Send the updated sensor data
        pipe_send.send((co2_concentration, temp, humidity))

        time.sleep(1)  # Simulate a 1-second delay between sensor reads
