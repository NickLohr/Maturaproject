from sklearn.cluster import MeanShift
import numpy as np
import matplotlib.pyplot as plt
import json

X = np.load("datatouseaa.npy")
print(len(X))

a = {}
clustering = MeanShift(bandwidth=2).fit(X)
print(max(clustering.labels_))
delta = 1
step = 100
n = 100
"""
while delta>0 or step >1:
    print(n)
    if delta <=0:
        n-=2*step
        step = step // 2
        
    
    clustering = MeanShift(bandwidth=n).fit(X)
    labels1 = clustering.labels_
    a[str(n)] = str(max(labels1))
    if str(n-step) in a:
        delta =(int(a[str(n-step)])-70)**2-(int(a[str(n)])-70)**2
    else:
        delta = 1
    n+=step
    with open("2hi"+str(n)+".txt","w") as file:
        json.dump(a,file)


with open("2hi.txt","w") as file:
    json.dump(a,file)
    
"""
    
#creates to much groups
#check for same labels from same class

