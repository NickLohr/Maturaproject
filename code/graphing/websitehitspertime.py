import matplotlib.pyplot as plt
import matplotlib
import collections
font = {'size'   : 12}

matplotlib.rc('font', **font)
with open("error.log","r",encoding="utf8") as file:
    n = file.readlines()
m =[]
o = 0
for i in n:
    if "inks" in i:
        o+=1
    if "Dont" in i:
        m.append(i)
print(len(m))


mt = collections.defaultdict(lambda : 0)

for i in m:
    time = i.split("[")[1].split("]")[0].split(" ")[0]
    mt[time]+=1

a = mt.items()
b = [x[0] for x in a]
d = []
for i in b:
    d.append(i.replace("/",".").replace("Dec","12").replace("Jan","01").replace("2020","").replace("2019",""))


    
plt.title("Websites hits per day")
plt.xlabel("Date")
plt.ylabel("Number of hits")
c = [x[1] for x in a]
plt.plot(d,c)
plt.show()
