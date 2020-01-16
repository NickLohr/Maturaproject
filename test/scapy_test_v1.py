import time
import tqdm
import os

import scapy.all as sa
for (dirpath, dirnames, filenames) in os.walk("/mnt/"):
    for i in tqdm.tqdm(range(len(filenames))):

        filename = filenames[i]
        time1 = time.time()
        #filename="mon11561761749.pcap"
        #print("hi-0")
        #print(time.time()-time1)
        packets = sa.rdpcap("/mnt/"+filename)
        #print("hi-1")
        #print(time.time()-time1)
        data=[]
        for k in tqdm.tqdm(range(len(packets))):
            reveivermac = packets[k].addr1
            aendermac = packets[k].addr2
            times = packets[k].time
            data+=[(reveivermac,aendermac,times)]
        #print(time.time()-time1)
        #print(len(data))
        #print(time.time()-time1)

        with open("/mnt/parsed/"+filename+".parsed","w+") as file:
            for x,y,z in data:
                
                file.write(str(x)+", "+str(y)+", "+str(z)+"\n")
