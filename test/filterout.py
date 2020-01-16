import os
import collections
import json
from tqdm import tqdm
blacklistofmac=['a0:4f:d4:c9:87:a3', '30:23:03:87:65:94', '33:33:00:01:00:02', '33:33:00:00:00:fb', 'ff:ff:ff:ff:ff:ff', 'None', '36:23:03:87:63:06', '58:ef:68:7b:41:15', '2c:30:33:d1:f8:e7', '37:23:03:87:63:06', '08:6a:0a:a2:50:99', '01:80:c2:00:00:00', '01:80:c2:00:00:13', '14:20:5e:04:b9:e8', '01:00:5e:7f:ff:fa', '01:00:5e:00:00:fb', '33:33:00:00:00:01']

a = collections.defaultdict(int)
with open("blacklist.txt","r") as fili:
     blacklist = json.load(fili)
with open("blacklist2.txt","r") as fili:
     blacklist += json.load(fili)

blacklistofmac += blacklist
path = "../../data10111217/parsed/"

deltatime = 5856908 #sec

for (dirpath, dirnames, filenames) in os.walk(path):

     for j in tqdm(range(len(filenames))):

          m = filenames[j]

          with open(path+"lol/"+m,"w") as file:
            
               with open(path+m) as file2:
                    n = file2.readlines()
                    for o in n:
                         if o=="\n":
                              continue
                         l = o.split(" ")
                         if not (l[0][:-1] in blacklistofmac):
                              file.write(l[0][:-1]+" "+str(float(l[1][:-1])+deltatime)+"\n")
                         
