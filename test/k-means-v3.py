from sklearn.cluster import KMeans
import numpy as np

X = np.load("")



model = KMeans(n_clusters=70, random_state=0).fit(X)

print(model.cluster_centers_)

