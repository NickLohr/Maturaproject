#reparsing
import os
import collections
import json
from tqdm import tqdm
newblacklist = []
path = "onetwoday"
a = collections.defaultdict(int)
for (dirpath, dirnames, filenames) in os.walk(path):

     for j in tqdm(range(len(filenames))):

          m = filenames[j]

          with open(path+"/"+m) as file:
               n = file.readlines()
               for o in n:
                    if o == "\n":
                         continue
                    l = o.split(" ")

                    a[l[0]] +=1
print(len(a))

for m in a:
     if a[m] < 50:
          newblacklist.append(m)
print(len(newblacklist))
with open("blacklist2.txt","w") as fili:
     json.dump(newblacklist,fili)      
               
"""
          with open("onetwoday/"+m+".2","w") as file:
            
               with open("onedaydata/"+m) as file2:
                    n = file2.readlines()
                    for o in n:
                         if o=="\n":
                              continue
                         l = o.split(" ")
                         if not (l[0] in blacklistofmac):
                              file.write(l[0]+" "+l[1]+"\n")
                         else:
                              print(l[0])

"""
