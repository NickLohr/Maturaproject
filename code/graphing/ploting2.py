import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

X = np.load("datatouseaa6.npy")
X2 = np.load("datatouseaa5.npy")
X = np.append(X,X2)
exi = {}
print(len(X))
print(X[0])


model = KMeans(n_clusters=50, random_state=0).fit(X)

a = [[] for _ in range(len(X[0]))]

for li in X:
    for i in range(len(li)):
        a[i].append(li[i])
color = model.labels_

for i in range(1, 10):
    plt.subplot(2, 5, i)
    plt.scatter(a[i],a[i-1],a[i-2],c=color)

    plt.xlabel(f"Zeit normiert in der {i}te Dimension")

    plt.ylabel(f"Zeit normiert in der {i+1}te Dimension")


"""

print("hi")
op = sorted(exi.items(),key=lambda x: x[1])

ab = [o[0] for o in op]
ac = [o[1] for o in op]
plt.plot(ab,ac)
"""
plt.show()
