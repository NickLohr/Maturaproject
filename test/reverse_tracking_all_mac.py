from ddd import *
from time import *
tim = time()
print(tim)
time2 = tim
mmmm={}
def look_for_mac():
    global time2
    liste=[]
    f = ["2019-Mar-12-access.log"]
    global mmmm
    for k in f:
        
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

            per = ooo/2877*100.
            

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
file = open("dic.data","w")
file.write(str(mmmm))
file.close()

print(time()-tim)
