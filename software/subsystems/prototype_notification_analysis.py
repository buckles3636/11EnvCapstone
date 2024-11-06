import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

TEST_NAME = "./data/11.5.24_500_test.npy" # name of file that data is saved to
data = np.load(TEST_NAME)
USL = 10

mu = np.mean(data)
sigma = np.sqrt(np.var(data))
Cpk = (USL - mu) / (3*sigma)
print("mu: %f s\nsigma: %f s\nCpk: %.2f" % (mu, sigma, Cpk))

# plot the data
plt.hist(data, bins=100)
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency")
plt.title("Distribution of transmission times")
plt.show()