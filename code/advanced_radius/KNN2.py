import sys
import collections
import numpy as np
import json
with open("radius.txt","r") as file:
    X = json.load(file)

print(len(X))
"""
AP_FILE_PATH_TYPE1 = "../../test/Data/access_points.log"
AP_FILE_PATH_TYPE2 = "../../test/Data/access_points2a.log"
DATA_DIRECTORY_PATH = "../../test/Data/"


tools.aps=collections.defaultdict(lambda: None)
tools.aps.update(tools.read_ap_database_type1(AP_FILE_PATH_TYPE1))
tools.aps.update(tools.read_ap_database_type2(AP_FILE_PATH_TYPE2))
tools.files = tools.get_files(DATA_DIRECTORY_PATH)
tools.time_table_dic = tools.parse_time_table("../../test/save9.gpn")

sol = tools.reverse_tracking(tools.files,tools.aps,tools.time_table_dic,filename_tt="../../test/save9.gpn")
print(len(sol),"ool")

"""
def timetonumber(time):
    
    a = time[1]
    timer= []
    for o in range(len(a)):
        if o == 5 and "6" in time[0]:
            m = 9
        elif a[o] == "a":
            m = 10
        elif a[o] == "b":
            m =11
        elif a[o] == "z":
            m = 5
        elif a[o] == "y":
            m = 9
        else:
            m = int(a[o])
        if o%2 ==1:
            m+=1
        ini = 7*3600+36*60

        for p in range(m-1): ##Always a lesson and ten minutes later
            ini+=55*60
        timer.append(ini)
    return (timer+[0,0,0,0])*10 #Samstag und Sonntag


def KNN(Y):
    p = []
    for m in c:
        l = m[1]
        d = 0
        for i in range(0,len(l)):
            if not i<len(Y):
                #print(i)
                continue

            
            d+=((Y[i]-l[i])**(2))**(1/6)

        p += [(m[0],d)]
            
    return sorted(p,key=lambda x: x[1])


Centroids = [('6L', '141924291a'), ('6G', '1518252818'), ('6H', '1519252a17'), ('6J', '1529152818'), ('3B', '1529291a19'), ('6E', '1818242915'), ('6B', '1818251815'), ('6A', '1818352915'), ('2j', '181915192a'), ('4J', '1819181918'), ('5H', '18191a193a'), ('3H', '182a151918'), ('1f', '182a15191a'), ('4B', '191818182a'), ('4E', '19182a2a39'), ('1a', '1919151819'), ('1h', '1919151819'), ('2d', '1919151919'), ('3C', '1919151919'), ('3E', '1919151919'), ('1j', '1919151919'), ('2e', '191915192a'), ('2h', '191915292a'), ('1b', '1919152a18'), ('5D', '191918182a'), ('4D', '1919181a29'), ('5K', '19191a1829'), ('4K', '19191a2939'), ('5C', '19193a1a29'), ('2n', '191a151a18'), ('2c', '1929151919'), ('3F', '1929151919'), ('3A', '1929152a18'), ('3G', '19292a151a'), ('2g', '192a151919'), ('2m', '192a152a19'), ('1e', '192a152a19'), ('1m', '192a152a19'), ('4C', '192a192a29'), ('5E', '1a19182919'), ('5B', '1a191a1819'), ('6C', '1a19zy1918'), ('1k', '1a2a15192a'), ('5T', '1a2a182a18'), ('6F', '2818151419'), ('6K', '2829251519'), ('6S', '28292b2918'), ('3D', '2919151929'), ('4A', '2919181818'), ('4G', '2919182a18'), ('5L', '29292a181a'), ('4H', '29292a2a19'), ('2a', '2a1815192a'), ('5G', '2a18181a19'), ('1c', '2a1915182a'), ('1d', '2a19151919'), ('1n', '2a19151919'), ('3J', '2a19152a18'), ('2k', '2a19152a19'), ('5J', '2a19191818'), ('5A', '2a192a1a2a'), ('2b', '2a1a151819'), ('5F', '2a29181a19'), ('5S', '2a291a1818'), ('4S', '2a291a1a29'), ('4T', '2a29281819'), ('1g', '2a2a15182a'), ('2f', '2a2a151919'), ('4F', '3a282a2a19'), ('6D', '3a39251419')]

c = []
for m in Centroids:
    c+=[(m[0],timetonumber(m))]


o = {}
n = '88:E9:FE:B2:7B:46'.replace("-",":").upper()
#X = {n:X[n]}

for macindex in X:
    a = KNN(X[macindex])
    if a[0][1]>2000:
        o[macindex] = a[0:5]#"Teacher or Staff"
    else:
        o[macindex] = a[0:5]

b = "24:92:0E:16:C4:30"
w = "30-07-4d-dd-fe-25".replace("-",":")

with open("knn.txt","w") as f:
    json.dump(o,f)
