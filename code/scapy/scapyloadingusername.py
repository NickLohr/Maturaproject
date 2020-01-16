import scapy.all as sa
import os as os
import tqdm as tq

filenames = [ ]
path = "H:\\nicol\\Documents\\Maturaarbeit\\test\\scapy_testing\\lan"
for (dirpath, dirnames, filename) in os.walk(path):
    if dirpath == path:
        filenames.extend(filename)
print(filenames) 
for j in tq.tqdm(range(len(filenames))):
    
    i = filenames[j]
    if not ".pcap" in i:
        continue
    
    packets = sa.rdpcap("lan/"+i)
    with open("usernames"+i+".txt","w") as file:
        for m in packets:
                if "Identity" in str(m.summary()):
                    if "Response" in str(m.summary()):
                        k = m.summary().split("'")
                        if len(k)>=1:
                            file.write(str(k[1])+ " " +m.addr1)
                            file.write("\n")
                            file.write(str(k[1])+ " " +m.addr2)
                            file.write("\n")
                        else:
                            print(k)




