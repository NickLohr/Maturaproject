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
            macdatedic[mac][b].append(a.minute*60+a.second)

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
            macdatedic[mac][b].append(a.minute*60+a.second)

macidic = {}

files=[]
files2=[]
print(macdatedic["88:E9:FE:B2:7B:46".lower()].keys())

for mac in macdatedic:
    macidic[mac] = {}
    for day in macdatedic[mac]:
        macidic[mac][day] = []
        macidic[mac][day].append(min(macdatedic[mac][day]))
        macidic[mac][day].append(max(macdatedic[mac][day]))
macweekdic = collections.defaultdict(lambda:collections.defaultdict(list))

print(macidic["88:E9:FE:B2:7B:46".lower()])




X = np.array([])
solution = []
for mac in macidic:
    X = np.append(X,[macidic[mac]])
    solution.append(mac)

print(len(X))
"""
X =X.reshape(len(macidic),14)
macdic=0
np.save("datatouseaa_minutes.npy",X)

with open("sol_minutes.txt","w") as file:
    json.dump(solution,file)





"""








    
    
