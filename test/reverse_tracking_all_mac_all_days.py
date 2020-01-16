from ddd import *
from time import *
import dic_as_class as d
Dic = d.dic()
tim = time()
print(tim)
time2 = tim
mmmm = Dic.k
liste = []
mmmm["3x"] = []
for o in mmmm:
    for k in mmmm[o]:
        liste+=[k[0]]
print(len(liste))
def look_for_mac():
    global time2
    global mmmm
    global liste

    f = []

    for (dirpath, dirnames, filenames) in walk("Data"):
        for k in filenames:
            if "points" in k:
                continue
            f.append(k)
        break

    for k in f:
        print(k)
        file = open("Data/"+k)
        data = file.readlines()

        for ooo in range(0,len(data)):

            b = data[ooo]
            c=b.split("][")
            if c[-3].upper() in liste:
                continue
            if not "ksz" in c[-4]:
                continue
            if "anony" in c[-3]:
                continue

            per = ooo/len(data)*100.
            

            print(str(per)+ "%")
            kp = start(c[-3].upper())
            print(kp,c[-3].upper())
            if kp in mmmm.keys():
                mmmm[kp]+=[[c[-3],c[-4]]]
            else:
                mmmm[kp]=[[c[-3],c[-4]]]

            
            liste+=[c[-3].upper()]
            #print(time2-time())
            time2= time()

    return mmmm

print(look_for_mac())
file = open("dic3.data","w")
file.write(str(mmmm))
file.close()

print(time()-tim)
