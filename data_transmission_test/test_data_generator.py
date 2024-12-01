#--------------------------------------------------------------------------------#
# Peter Buckley
# 11/24/2024
# This function generates 20,000 fake sensordata values and sends them to the 
# csv writer process. It also records the data as a csv for error checking.
#--------------------------------------------------------------------------------#

def test_data_generator(pipe_send, input_csv="test_data.csv"):
    with open(input_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            # Convert data to float for consistency
            data = tuple(map(float, row))
            pipe_send.send(data)
        # Send a signal to stop the writer process
        pipe_send.send("STOP")
