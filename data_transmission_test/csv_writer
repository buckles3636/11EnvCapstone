import csv
from multiprocessing import Pipe

def csv_writer(pipe_recv, filename="sensor_data.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["CO2 Concentration", "Temperature", "Humidity"])
        
        while True:
            if pipe_recv.poll():
                data = pipe_recv.recv()
                if data == "STOP":
                    break
                writer.writerow(data)
