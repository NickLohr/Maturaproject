from sklearn.cluster import KMeans
import numpy as np
import os
import collections
import datetime
from tqdm import tqdm
import json

path = "../../../data10111217/lol"
path2 = "../../test/parsed201020192"
files = []
files2= []
days = {}
macdatedic = collections.defaultdict(lambda:collections.defaultdict(list))


for (dirpath, dirnames, filenames) in os.walk(path):
    files+=filenames
for (di,de,filenames) in os.walk(path2):

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
            if a.month<9:
                #print("i")
                a = a + datetime.timedelta(seconds=3124442)


            b = datetime.datetime(a.year,a.month,a.day)
            macdatedic[mac][b].append(a.hour*3600+a.minute*60+a.second)

for i in tqdm(range(len(files2))):
    
    o = files2[i]
    #print(o)
    with open(path2+"/"+o,"r") as file:
        lines = file.readlines()
	
        for k in lines:
            if k=="\n" or "\x00" in k:
                continue

            
            mac = k.split(" ")
            #print(mac)
            secs = float(mac[1][:-2])
            mac = mac[0]
            a = datetime.datetime(1970,1,1)+datetime.timedelta(seconds=secs)
            if a.month<9:
                #print("i")
                a = a + datetime.timedelta(seconds=3124442)


            b = datetime.datetime(a.year,a.month,a.day)
            macdatedic[mac][b].append(a.hour*3600+a.minute*60+a.second)

macidic = collections.defaultdict(lambda:collections.defaultdict(list))

files=[]
files2=[]
print(macdatedic["88:E9:FE:B2:7B:46".lower()].keys())

for mac in macdatedic:
    
    for day in macdatedic[mac]:
        macidic[mac][day].append(min(macdatedic[mac][day]))
        macidic[mac][day].append(max(macdatedic[mac][day]))
macweekdic = collections.defaultdict(lambda:collections.defaultdict(list))

print(macidic["88:E9:FE:B2:7B:46".lower()])
macdatedic=0
for mac in macidic:
    for time in macidic[mac]:
        if macweekdic[mac][time.weekday()] == []:
            macweekdic[mac][time.weekday()]=[[],[]]
        macweekdic[mac][time.weekday()][0].append(macidic[mac][time][0])
        macweekdic[mac][time.weekday()][1].append(macidic[mac][time][1])
print("Status report")
macdic = {}#collections.defaultdict(list)
macidic=0
for mac in macweekdic:
    times = []
    for time in range(0,7):
        for i in range(2):#morning night
            if macweekdic[mac][time] == []:
                macweekdic[mac][time]=[[0],[0]] 
            so = sorted(macweekdic[mac][time][i])
            if len(so)>=2:
                mean =so[len(so)//2]
            if len(so)==0:
                mean = 0
            if len(so) == 1:
                mean = so[0]
            times.append(mean)

    macdic[mac.upper()] = times
macweekdic=0

print(macdic["88:E9:FE:B2:7B:46"])



X = np.array([])
solution = []
for mac in macdic:
    X = np.append(X,[macdic[mac]])
    solution.append(mac)

X =X.reshape(len(macdic),14)
macdic=0
np.save("datatouseaa_mean2.npy",X)

with open("sol_mean.txt","w") as file:
    json.dump(solution,file)














    
    
