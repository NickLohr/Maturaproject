import numpy as np
import random
import matplotlib.pyplot as plt


from sklearn.cluster import DBSCAN 
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import OPTICS


#three classes with three or four student each
#total 11 students
#we look at one day [two datapoints]

s1= [7*60+36,15*60-3]
s2= [7*60+33,15*60+3]
s3= [7*60+31,15*60+10]


s4= [7*60+40,16*60-6]
s5= [7*60+23,16*60-7]
s6= [7*60+34,16*60-1]
s7= [7*60+30,16*60+12]


s8= [8*60+21,15*60+13]
s9= [8*60+26,15*60-6]
s10= [8*60+6,15*60+1]
s11= [8*60+18,15*60-2]

ws =[random.randint(0,1000),random.randint(0,1000)]
ws2 = [random.randint(0,1000),random.randint(0,1000)]
ws3 = [random.randint(0,1000),random.randint(0,1000)]

k = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,ws,ws2,ws3]
random.shuffle(k)
X = np.array(k)

ac = [a[0] for a in k]
ab = [a[1] for a in k]
#model = KMeans(n_clusters=3, random_state=0).fit(X)
model = DBSCAN(eps = 20, min_samples = 1).fit(X)
#model = MeanShift().fit(X)
#model = OPTICS().fit(X)

labels=model.labels_
plt.scatter(ac,ab,c=labels)
plt.xlabel("Time of Arrival (minutes after midnight)")
plt.ylabel("Time of Leaving (minutes after midnight)")
plt.show()



