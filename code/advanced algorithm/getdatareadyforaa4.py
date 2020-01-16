#create list with parsed data for advanced algorithm
#To create a system which is able to be used for multidimensional graphs and its algorithms
#To the same amount of data per mac, I shorten it to a two (arrival and leaving time) a day
#same amounts of days for everyone.
#If it is not found, then use 0
from sklearn.cluster import KMeans
import numpy as np
import os
import collections
import datetime
from tqdm import tqdm
import json

macdatedic = collections.defaultdict(lambda:collections.defaultdict(list))

#macdatedic["somemac"]["day"] = [datetime.datetime(morning),datetime.datetime(evening)]
##take minutes

##mean

path = "../../../data10111217/parsed/lol/"
files = []
files2= []
days = {}
for (dirpath, dirnames, filenames) in os.walk(path):
    files+=filenames
for (di,de,filenames) in os.walk("../../test/parsed201020192"):
    files2+=filenames

for i in tqdm(range(len(files))):
    o = files[i]
    #print(o)
    with open(path+"/"+o,"r") as file:
        lines = file.readlines()
	
        for k in lines:
            if k=="\n" or "\x00" in k:
                continue

            
            mac = k.split(" ")
            #print(mac)
            secs = float(mac[1][:-2])
            mac = mac[0]
            a = datetime.datetime(1970,1,1)+datetime.timedelta(seconds=secs)
            #wrong time from the pineapple, changed too late
            if a.month<9:
                #print("i")
                a = a + datetime.timedelta(seconds=3124442)
            b = datetime.datetime(a.year,a.month,a.day)
            days[b.weekday()] = 0
            macdatedic[mac][b.weekday()].append(a)

for i in tqdm(range(len(files2))):
    o = files2[i]
    #print(o)
    with open("../../test/parsed201020192/"+o,"r") as file:
        lines = file.readlines()

        for k in lines:
            if k=="\n" or "\x00" in k:
                continue


            mac = k.split(" ")
            #print(mac)
            secs = float(mac[1][:-2])
            mac = mac[0]
            a = datetime.datetime(1970,1,1)+datetime.timedelta(seconds=secs)
            #wrong time from the pineapple, changed too late
            if a.month<9:
                #print("i")
                a = a + datetime.timedelta(seconds=3124442)
            b = datetime.datetime(a.year,a.month,a.day)
            days[b] = 0
            macdatedic[mac][b].append(a)


da = sorted(days.keys())

##rewrite to mean instead of max/min

mac10D = {}
olo = list(macdatedic.keys())
for lol in tqdm(range(len(olo))):
    k = olo[lol]
    lis = list()
    
    for m in da:
        if macdatedic[k][m] == []:
            lis.append(0)
            lis.append(0)
        else:
            mini = min(macdatedic[k][m])
            maxi = max(macdatedic[k][m])
            lis.append((mini.hour*60+mini.minute))
            lis.append((maxi.hour*60+maxi.minute))
    mac10D[k] = lis
print("lis, ", lis)



for mac in mac10D:
    print(mac10D[mac])
    newlist= []
    for time in range(len(mac10D[mac])):
        newlist.append(mac10D[mac][time])
    mac10D[mac] = newlist



X = np.array([])
for po in mac10D:
    X =np.append(X,[mac10D[po]])
print("saving")
X =X.reshape(len(macdatedic),len(da)*2)

print(len(mac10D))
print(len(mac10D["88:e9:fe:b2:7b:46"]))
print(mac10D["88:e9:fe:b2:7b:46"])

np.save("datatouseaa6.npy",X)
with open("sol5.txt","w") as file:
    json.dump(mac10D,file)
