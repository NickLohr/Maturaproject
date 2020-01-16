#create list with parsed data for advanced algorithm
#To create a system which is able to be used for multidimensional graphs and its algorithms
#To the same amount of data per mac, I shorten it to a two (arrival and leaving time) a day
#same amounts of days for everyone.
#If it is not found, then use 0
from sklearn.cluster import KMeans
import json
import os
import collections
import datetime
from tqdm import tqdm

macatlunch = collections.defaultdict(int)

#macdatedic["somemac"]["day"] = [datetime.datetime(morning),datetime.datetime(evening)]


path = "parsed201020192"
files = []
days = {}
for (dirpath, dirnames, filenames) in os.walk(path):
    files+=filenames


for i in tqdm(range(len(files))):
    o = files[i]
    with open(path+"/"+o) as file:
        lines = file.readlines()

        
        for k in lines:
            if k=="\n" or "\x00" in k:
                continue

            
            mac = k.split(" ")
            #print(mac)
            secs = float(mac[1][:-2])
            mac = mac[0]
            a = datetime.datetime(1970,1,1)+datetime.timedelta(seconds=secs)
            if a.hour in [11,12,13]:
                macatlunch[mac]+=1





with open("lunch_2010.txt","w") as file:
    json.dump(macatlunch,file)
    
