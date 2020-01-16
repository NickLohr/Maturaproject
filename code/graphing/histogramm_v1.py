from matplotlib import pyplot as plt
import collections
filename="../../test/Data/2018-Dec-04-access.log"

data= []
with open(filename, "r") as file:
    for m in file.readlines():
        line = m
        words = line.split(" ")
        data.append(words)

x = []
y = collections.defaultdict(lambda:0)
print(data[0])
for m in data:
    time = m[-3]
    #print(time)
    time = (int(float(time[-5:-3])))+(int(float(time[:2])))*60
    if not(time>7*60 and time < 8*60): #timeframe
        continue
    if time in x:
        y[time]+=1
    else:
        x+=[time]
        y[time]+=1
    
y = [y[t] for t in x]
print(y)

plt.bar(x,y)
plt.xlabel("Time in seconds")
plt.ylabel("Number of new macs")
plt.title("Passing mac-addresses")
plt.show()
