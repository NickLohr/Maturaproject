import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


from sklearn.cluster import DBSCAN 
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import OPTICS


#three classes with three or four student each
#total 11 students
#we look at one day [two datapoints]

s1= [7*60+36,15*60-3,7*60+43]
s2= [7*60+33,15*60+3,7*60+23]
s3= [7*60+31,15*60+10,7*60+31]


s4= [7*60+40,16*60-6,8*60+14]
s5= [7*60+23,16*60-7,8*60+30]
s6= [7*60+34,16*60-1,8*60+24]
s7= [7*60+30,16*60+12,8*60+4]


s8= [8*60+21,15*60+13,7*60+21]
s9= [8*60+26,15*60-6,7*60+40]
s10= [8*60+6,15*60+1,7*60+34]
s11= [8*60+18,15*60-2,7*60+13]

ws =[random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)]
ws2 = [random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)]
ws3 = [random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)]

k = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,ws,ws2,ws3]
random.shuffle(k)
X = np.array(k)
#model = KMeans(n_clusters=3, random_state=0).fit(X)
model = DBSCAN(eps = 31, min_samples = 1).fit(X)
#model = MeanShift().fit(X)
#model = OPTICS().fit(X)

labels=model.labels_
cmap = { 0:'k',1:'b',2:'y',3:'g',4:'r' ,5:'w',6:"g"}
# Fixing random state for reproducibility
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for a in range(len(k)):
    
    ax.scatter(k[a][0], k[a][1], k[a][2], c=cmap[labels[a]])

ax.set_xlabel('Time of Arrving [Day 1] (minutes after midnight)')
ax.set_ylabel('Time of Leaving (minutes after midnight)')
ax.set_zlabel('Time of Arrving [Day 2] (minutes after midnight)')
plt.title("3D Test Data")
plt.show()
