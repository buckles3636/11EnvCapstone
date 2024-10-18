#--------------------------------------------------------------------------------#
# Peter Buckley
# 10/18/2024
# This file serves as a placeholder to recive setpoints from the gui
#--------------------------------------------------------------------------------#
import time
from multiprocessing import Pipe

# Simulate environmental control system
def control_system(pipe_recv):
    while True:
        if pipe_recv.poll():
            co2_setpoint, temp_setpoint, humidity_setpoint = pipe_recv.recv()
            print(f"Received Setpoints - CO2: {co2_setpoint}, Temp: {temp_setpoint}, Humidity: {humidity_setpoint}")
            # Adjust your control system based on the setpoints
            # (e.g., turn on fans, adjust heating, etc.)
        time.sleep(1)  # Simulate control system operations
