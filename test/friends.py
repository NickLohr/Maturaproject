import os
import collections
import numpy as np
data = []
d= collections.defaultdict(lambda: collections.defaultdict(int))
path = "KNNdata/"
def readin():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for k in filenames:
            f.append(k[:])
        else:
            break
    for o in f:
        with open(path+"/"+o) as file:
            datas = file.readlines()
        for pp in datas:
            if  "\x00" in pp:
                continue
            if pp == "\n":
                continue
          
            mac = pp.split(" ")[0]
            time = float(pp.split(" ")[1])
            data.append((mac,time))
            
def add(l,p):
    for i in p:
        for k in l:
            d[k][i]+=1
            d[i][k]+=1
        for k in p:
            d[k][i]+=1
            d[i][k]+=1
i = 0
def main():
    global data
    global i
    readin()

    data = sorted(data,key=lambda x:x[1])
    print("data")
    l = [data[0]]
    p = []

    while i<len(data):
        print(i)
        if l == []:
            l = [data[i]]
        while len(l)!= 0 and data[i][1]-l[0][1]>=15:
            l.pop(0)
        while data[i][1]-l[-1][1]<=15:
            p+=[data[i]]
            
            i+=1
        add(l,p)
        l+=p
        p = []


main()
