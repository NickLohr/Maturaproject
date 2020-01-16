from sklearn.cluster import KMeans
import numpy as np

import json
print("imported")
X = np.load("datatouseaa6.npy")
print("Got Data")

model = KMeans(n_clusters=71, random_state=0).fit(X)

print(model.cluster_centers_)

