import os
import json
import tqdm

path2 = "./"

files2= []
macuserdic ={}

for (di,de,filenames) in os.walk(path2):
    files2+=filenames

for i in tqdm.tqdm(range(len(files2))):
    
    o = files2[i]
    if ".py" in o:
        continue
    #print(o)
    with open(path2+"/"+o,"r") as file:
        lines = file.readlines()
	
        for k in lines:
            if k=="\n" or "\x00" in k:
                continue

            
            mac = k.split(" ")
            #print(mac)
            user = mac[0]
            mac1 = mac[1].upper()
            mac2 = mac[2].replace("\n","").upper()
            
            macuserdic[mac1]= user
            macuserdic[mac2]= user

with open("usernames.txt", "w") as f:
    json.dump(macuserdic,f)
