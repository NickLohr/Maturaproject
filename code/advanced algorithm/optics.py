
from sklearn.cluster import OPTICS
import numpy as np

print("imported")
X = np.load("datatouseaa6.npy")
print("Got Data",len(X))

clust = OPTICS(min_samples=20, xi=.05, min_cluster_size=.05)
print("hi")
# Run the fit
clust.fit(X)
