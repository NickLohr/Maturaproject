from collections import defaultdict
from os import walk
dd = defaultdict(lambda:defaultdict(lambda:0))

data = []
for root, dirs, files in walk("parsed"):
    for m in files:
        if "mon0" in m:
            continue
        with open("parsed/"+m) as file:

            k = file.readlines()
            for p in k:
                a = p.split(" ")
                a[0]=a[0][:-1]
                #print(a[0])
                if "ff:ff:ff:ff:ff:ff" != a[0]:
                    data.append([a[0],float(a[2][:-2])])

                data.append([a[1],float(a[2][:-2])])
                


#data = [["a",1],["b",3],["c",17],["d",340],["a",341],["b",343]]
span = []
p2 = 0
print("parsed")
print(len(data))
for p1 in range(len(data)):
    if p1%1000 == 0:
        print(p2-p1,p1)
    new = []
    while p2 < len(data) and data[p2][1]-data[p1][1]<15:
        new.append(data[p2])
        p2+=1
    #print(new)
    for mini in span:
        for news in new:
            dd[mini[0]][news[0]] += 1
            dd[news[0]][mini[0]] += 1

    for a in new:
        for b in new:
            if a==b:
                continue
            dd[a[0]][b[0]]+=1

    span+=new
    span.pop(0)
    
    
