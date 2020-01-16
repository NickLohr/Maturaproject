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

macdatedic = collections.defaultdict(lambda:collections.defaultdict(list))

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
            b = datetime.datetime(a.year,a.month,a.day)
            days[b] = 0
            macdatedic[mac][b].append(a)

X = np.array([])
olo = list(macdatedic.keys())
for lol in tqdm(range(len(olo))):
    k = olo[lol]
    lis = list()
    da = sorted(days.keys())
    for m in da:
        if macdatedic[k][m] == []:
            lis.append(0)
            lis.append(0)
        else:
            lis.append(min(macdatedic[k][m]).hour*60+min(macdatedic[k][m]).minute)
            lis.append(max(macdatedic[k][m]).hour*60+max(macdatedic[k][m]).minute)
    X =np.append(X,[lis])
print("saving")
X =X.reshape(len(macdatedic),len(da)*2)



np.save("datatouseaa.npy",X)
