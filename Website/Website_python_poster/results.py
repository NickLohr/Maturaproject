import json
import collections

results = collections.defaultdict(lambda:[[],[],[]])
with open("sol_mean.txt", "r") as f:
    a = json.load(f)
with open("KNN2_final_1.txt", "r") as f:
    b = json.load(f)
with open("lunch_2010.txt", "r") as f:
    c = json.load(f)
with open("sol_minutes_f.txt", "r") as f:
    d = json.load(f)
with open("KNN_SBB_1.txt", "r") as f:
    e = json.load(f)

p = list(set(a+d+list(c.keys())))
for m in range(len(p)):
    
    if  m >=len(a):
        results[o][0].append("Unknown")
        continue
    o = a[m]
    results[o][0].append(b[str(m)])
for m in c:
    m1 = m.replace(",","")
    results[m1.upper()][1].append(c[m])


for m in range(len(d)):
    results[d[m]][2].append(e[str(m)])

#results

classi = {} #result from KNN2.py


sbb = {} #results from KNN_SBB.py

lunch = {} #results from lunch (over all data and look out for time)

username = {} #reverse lookup from known usernames




