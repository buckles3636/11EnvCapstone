import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

TEST_NAME = "./data/11.6.24_100_pi_test.npy" # name of file that data is saved to
data = np.load(TEST_NAME)
USL = 10

mu = np.mean(data/1000000)
min = np.min(data/1000000)
max = np.max(data/1000000)
sigma = np.sqrt(np.var(data/1000000))
Cpk = (USL - mu) / (3*sigma)
print("mu: %f s\nsigma: %f s\nCpk: %.2f" % (mu, sigma, Cpk))

# plot the data
plt.figure("11.6.24_100_pi_test.npy", (10, 7))

plt.subplot(6,1,(1,2))
plt.title("Distribution of transmission times (n=100): Cpk = %.2f" % Cpk)
plt.boxplot(data/1000000, vert=False)
plt.xlabel("Time (seconds)")
plt.text(min, 1.1, "Min: %0.2f" % min)
plt.text(max-.05, 1.1, "Max: %0.2f" % max)
plt.text(mu-.05, 1.15, "Mean: %0.2f" % mu)
plt.text(mu-.05, .8, "Sigma: %0.2f" % sigma)

plt.subplot(6,1,(4,6))
plt.hist(data/1000000, bins=50)
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency")

plt.savefig("./data/11.6.24_100_pi_test.png")
plt.show()