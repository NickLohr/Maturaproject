from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

import json
print("imported")
X = np.load("datatouseaa.npy")
o=[]
print("Got Data")
for m in range(1,100):
    model = KMeans(n_clusters=m, random_state=0).fit(X)
    o.append(model.inertia_ )
print(model.cluster_centers_)

plt.plot(range(100),o)
plt.ylabel("Error Squared")
plt.xlabel("K - Amount of Clusters/Groups")

