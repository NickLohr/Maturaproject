##https://stackabuse.com/k-nearest-neighbors-algorithm-in-python-and-scikit-learn/

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


X_train  = [] ##Time table data
y_train = [] ##coresponding class name

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)



