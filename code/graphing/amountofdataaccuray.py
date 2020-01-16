import matplotlib.pyplot as plt
import matplotlib
import collections
font = {'size'   : 12}

matplotlib.rc('font', **font)

a = ["1 Week", "2 Weeks", "3 Weeks","4 Weeks","5 Weeks","6 Weeks","7 Weeks","8 Weeks"]
b = [92,85,75,68,56,45,34,27]


    
plt.title("Error decline with more data")
plt.xlabel("Data")
plt.ylabel("Errorrate")

plt.plot(a,b)
plt.show()
