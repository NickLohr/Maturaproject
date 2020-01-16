from collections import defaultdict
from os import walk
import tqdm
import matplotlib.pyplot as plt
import math
plt.rcParams.update({'font.size': 22})
dd = defaultdict(lambda:defaultdict(lambda:0))
amountcounter = defaultdict(int)
data = []
for root, dirs, files in walk("pasred20102019"):
    for oop in tqdm.tqdm(range(len(files))):
        #print(m)

        m = files[oop]

        with open("pasred20102019/"+m) as file:

            k = file.readlines()
            for p in k:
                a = p.split(" ")
                a[0]=a[0][:-1]
                a[1] = a[1][:-1]
                #print(a[0])

                amountcounter[a[0].upper()]+=1

                amountcounter[a[1].upper()]+=1

print(amountcounter["88:E9:FE:B2:7B:46"])          
                
print("DOne")
print(len(amountcounter))
a = sorted(list(amountcounter.items()),key=lambda x:x[1])
aver = sum(list(amountcounter.values()))/len(list(amountcounter.values()))
print("average", aver)
print("median", sorted(list(amountcounter.values()))[len(amountcounter.values())//2])
b = sorted(list(amountcounter.values()))
x,y = 0,0
for m in b:
    if m>5 and m<1000000:
        x,y = x+1,y+m
print("durchschnitt schüler", y/x)
print("hoechste anzahl", a[-20:])
stand = 0

for m in amountcounter:
    stand += (amountcounter[m]-aver)**2

print("stand",stand)

counting = defaultdict(lambda:0)

for m in amountcounter:
    counting[amountcounter[m]]+=1
c = sorted(list(counting.items()))
o = [(math.log(v[0])) for v in c]
p = [v[1] for v in c]


fig,ax = plt.subplots()
data_line = ax.plot(o,p)
average = ax.plot([math.log(aver)]*len(p),p,label="Average total",linestyle='--')
average_student = ax.plot([math.log(y/x)]*len(p),p,label="Average of student",linestyle='--',color="green")
median = ax.plot([math.log(sorted(list(amountcounter.values()))[len(amountcounter.values())//2])]*len(p),p,label="Median",linestyle='--',color="red")
legend = ax.legend(loc='upper right')
plt.title("Frequency")
plt.ylabel("The occurence of the MAC occurrences")
plt.xlabel("MAC occurrences (ln)")
plt.show()

                 
