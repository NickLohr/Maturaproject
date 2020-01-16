from sklearn.cluster import MeanShift
import numpy as np


X = np.load("datatouseaa.npy")
print(len(X))



clustering = MeanShift(bandwidth=1000).fit(X)
labels1 = clustering.labels_ 

#Hat 3600 gruppen generiert (keine ahnung warum)
#check for same labels from same class

