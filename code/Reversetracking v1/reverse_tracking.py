from ddd import *
from time import *
tim = time()
print(tim)
time2 = tim
def look_for_mac(name):
    global time2
    liste=[]
    f = ["2019-Jan-10-access.log"]

    for k in f:
        
        file = open("Data/"+k)
        data = file.readlines()
        pp = 0
        for ooo in range(0,len(data)):
            b = data[ooo]
            c=b.split("][")
            if c[-3] in liste:
                continue
            if not "ksz" in c[-4]:
                continue
            if "anony" in c[-3]:
                continue
            pp+=1
            if pp <100:
                continue
            print(c[-4])
            print(start(c[-3]))
            
            liste+=[c[-3]]
            print(time2-time())
            time2= time()
    print(len(liste))
    #return liste

print(look_for_mac("5H"))
print(time()-tim)
