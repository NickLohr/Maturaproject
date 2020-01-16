import matplotlib.pyplot as plt
from collections import defaultdict
from os import walk
dicw={"Mon":1, "Tue":2,"Wed":3,"Thu":4,"Fri":5,"Sat":6,"Sun":7}
timee= 1567189211
x = []
y = []

def time_to_int(s):
    
    sb = s[0]
    
    ss = sb.split(" ")
    time = ss[-1].replace(":","")
    if ss[0].upper()=="88:E9:FE:B2:7B:46" or ss[1].upper() == "88:E9:FE:B2:7B:46":
        print(s)
    #print(ss)
    
    ##print(s[-2])
    if len(ss)<2:
        return ""
    time = float(time[:-3])
    
    return [[time,ss[0]],[time,ss[1]]]
ooi=2
#k = open("Data/2019-Mar-26-access.log")
o = []
p = 0
for (dirpath, dirnames, filenames) in walk("../../Data/parsed/data101111217/parsed"):

    for m in filenames:
        if "scapy" in m or "user" in m:
            continue
        timing = int(m[4:].split(".")[0])
        if not(timing> timee+3600*ooi and timing < (timee+3600+3600*ooi)):
            if p!=0:
                print("lastone",timing)
                p=0
            continue
        if p == 0:
            print("first one",timing)
        #print(timing,m)
        p+=1
        if "point" in m:
            continue
        print("another")
        n = open("../../Data/parsed/data101111217/parsed/"+m)
        ol = n.readlines()
        print(ol[0])
        o += ol
        n.close()

  
for m in o:
    mm = m.split("][")
    oop = time_to_int(mm)
    x +=[oop[0]]
    x+= [oop[1]]

times = []

for m in x:
    if m == "":
        continue

    
    n = m[0]-(timee+3600*ooi)
    times+=[[n,m[1]]]
    #times += [(int(n[:-4])*3600+int(n[-4:-2])*60+int(n[-2:]))]
amountpertime=defaultdict(lambda: list())
times = sorted(times)
k  = 0#min(times)
mms = []
print("hi")
oloo=0
print(len(times))
for m in times:
    oloo+=1
    if oloo%10000==0:
        print(oloo)
    #print(k)
    if k >= 19.2 and k<19.3:
        #print("hi",m)
        pass
    while (k-1)*60<m[0] and k*60<=m[0]:
        
        k+=1
    if m[1] in mms:
        continue
    if m[1] in amountpertime[100*(5+ooi)+k-1.5]:
        #print(len(mms))
        continue

    
    else:
        amountpertime[100*(5+ooi)+k-1.5]+=[m[1]]
    mms.append(m[1])
print("ok")

aa = sorted(list(amountpertime.items()),key=lambda x: x[0])
aa[0] = (aa[0][0],[])
ab = [a[0] for a in aa]
ac = [len(a[1]) for a in aa]
plt.bar(ab, ac)
plt.xlabel("Time")
plt.ylabel("Number of new macs")
plt.title("Arriving mac-addresses")
plt.show()
