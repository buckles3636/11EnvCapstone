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
