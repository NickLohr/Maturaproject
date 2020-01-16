from os import walk
f = []
for (dirpath, dirnames, filenames) in walk("Data3"):
    for k in filenames:
        if "points" in k:
            continue
        if not "201" in k:
            continue
        f.append(k)
    break


for m in f:
    file = open("Data3/"+str(m), "r")
    file2 = open("Data/"+str(m),"w")
    ff = file.readlines()
    for o in ff:
        if not "ksz" in o:
            continue
        file2.write(o)
    
                 
