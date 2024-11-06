from notify import Flag, TeleBot

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import norm

TEST_NAME = "./data/11.5.24_100_test.npy" # name of file that data is saved to
SAMPLE_N = 100 # number of data points in the sample
USL = 10 # upper limit for time in seconds

# create bot and flag to be sent
# these will both be instantiated prior
# to sending the notification, and execution
# time is irrelevant
my_bot = TeleBot("ChamberStatusBot",
                 "@chamber_status_bot",
                 "8188655307:AAE841Hk_NdVtJs6f1xglu2On7k63vQVoR4",
                 "@incubatorstatus"
                 )
flag = Flag("Humidity", 90, 5.0, datetime.now(), "deviated", 10.0)

# array to hold transmission times
data = np.zeros(SAMPLE_N)

# record and save data
for i in range(SAMPLE_N):
    now = datetime.now()
    report_string = flag.to_report()
    my_bot.send_message(report_string)
    delta = datetime.now() - now
    data[i] = delta.microseconds
    time.sleep(7)

np.save(TEST_NAME, data)

# calculate the Process Control Index (Cpk)
# it is the upper specification limit minus the mean, divided by the three times the standard deviation
mu = np.mean(data)
sigma = np.sqrt(np.var(data))
Cpk = (USL - mu) / (3*sigma)
print("mu: %f s\nsigma: %f s\nCpk: %.2f" % (mu, sigma, Cpk))
