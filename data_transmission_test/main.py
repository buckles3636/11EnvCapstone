from multiprocessing import Process, Pipe
import random
import csv

import csv_writer
import test_data_generator
from accuracy_check import check_transmission_accuracy


def generate_test_csv(filename="test_data.csv", rows=20000):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CO2 Concentration", "Temperature", "Humidity"])
        for _ in range(rows):
            writer.writerow([
                random.uniform(300, 600),  # CO2
                random.uniform(15, 35),   # Temperature
                random.uniform(30, 70)    # Humidity
            ])

if __name__ == "__main__":
    # Generate test CSV
    generate_test_csv()

    # Set up pipes
    writer_recv_pipe, writer_send_pipe = Pipe()
    generator_recv_pipe, generator_send_pipe = Pipe()

    # Processes
    writer_process = Process(target=csv_writer, args=(writer_recv_pipe,))
    generator_process = Process(target=test_data_generator, args=(writer_send_pipe,))

    # Start processes
    writer_process.start()
    generator_process.start()

    # Wait for completion
    generator_process.join()
    writer_process.join()

    # Check transmission accuracy and plot results
    check_transmission_accuracy()
