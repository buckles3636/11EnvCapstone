import pandas as pd
import matplotlib.pyplot as plt

def accuracy_check(input_csv="test_data.csv", output_csv="sensor_data.csv"):
    # Read the input and output CSV files
    input_data = pd.read_csv(input_csv)
    output_data = pd.read_csv(output_csv)

    # Check for discrepancies
    mismatches = (input_data != output_data).sum().to_dict()

    # Plot the results
    plt.bar(mismatches.keys(), mismatches.values())
    plt.title("Transmission Accuracy")
    plt.ylabel("Number of Mismatches")
    plt.xlabel("Sensor Data Fields")
    plt.show()
