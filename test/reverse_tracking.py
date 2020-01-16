from ddd import *
from time import *
tim = time()
print(tim)
time2 = tim
mmmm=[]
def look_for_mac(name):
    global time2
    liste=[]
    f = ["2019-Jan-10-access.log"]
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

            per = ooo/len(data)*100.
            

            print(str(per)+ "%")
            kp = start(c[-3].upper())
            if str(kp).upper() == name.upper():
                mmmm+=[c[-3].upper()]
            
            liste+=[c[-3].upper()]
            #print(time2-time())
            time2= time()

    return mmmm

print(look_for_mac("5H"))
print(time()-tim)
