from sklearn.cluster import DBSCAN 
import numpy as np


X = np.load("datatouseaa6.npy")
print(len(X))



db = DBSCAN(eps = 0.0075, min_samples = 1).fit(X) 

labels1 = db.labels_ 

print(max(labels1))
#check for same labels from same class

