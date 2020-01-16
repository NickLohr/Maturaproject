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


path = "../../test/parsed201020192"
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
            #wrong time from the pineapple, changed too late
            if a.month<9:
                a = a + datetime.timedelta(seconds=3124442)
            b = datetime.datetime(a.year,a.month,a.day).weekday()
            days[b] = 0
            macdatedic[mac][b].append(datetime.time(a.hour,a.minute,a.second))


da = sorted(days.keys())[:-2] #reduce to weekdays not weekend
print(da)


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
print("my ",mac10D["88:E9:FE:B2:7B:46".lower()])
#calc varianz
v = {}
m = {}
ma = {}
for k in range(len(lis)):
    summe = 0
    maxi = 0
    for o in mac10D:
        summe+=mac10D[o][k]
        maxi = max(mac10D[o][k],maxi)
    mittelwert = summe/len(mac10D)
    m[k] = mittelwert
    varianz = 0
    ma[k] = maxi
    for o in mac10D:
        varianz += (mac10D[o][k]-mittelwert)**2
    varianz/=len(mac10D)
    print(varianz)
    v[k] = varianz

for mac in mac10D:
    newlist= []
    for time in range(len(mac10D[mac])):
        if mac10D[mac][time] == 0:
            #print("japs")
            newlist.append(None)
        else:
            newlist.append(mac10D[mac][time]/(v[time]**(1/2)))
    mac10D[mac] = newlist


o = []
X = np.array([])
for po in mac10D:
    X =np.append(X,[mac10D[po]])
    o.append(po)
print("saving")
X =X.reshape(len(macdatedic),len(da)*2)



np.save("datatouseaa6.npy",X)
with open("sol5.txt","w") as file:
    json.dump(o,file)
