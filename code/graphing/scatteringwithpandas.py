import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
print("Imported")
X = np.load("../../Data/parsed/data101111217/datatouseaa.npy")
print("loaded")
data = pd.DataFrame(X)
print("got data")
scatter_matrix(data,alpha=0.2, figsize=(6,6), diagonal="kde")
print("scattered")
plt.show()
