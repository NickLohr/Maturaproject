from sklearn.cluster import DBSCAN 
import numpy as np


X = np.load("datatouseaa_mean2.npy")
print(len(X))



db = DBSCAN(eps = 100000, min_samples = 50).fit(X) 

labels1 = db.labels_ 


#check for same labels from same class

