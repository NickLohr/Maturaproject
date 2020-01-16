import sys
import collections
sys.path.insert(1,"../../test/")
import tools_with_fast_tt as tools
import numpy as np
import tqdm

Y = np.load("datatouseaa_mean2.npy")
X = np.array([])
for o in tqdm.tqdm(range(len(Y))):
    m = Y[o]
    for i in m:
        X = np.append(X,i%3600)
X.reshape((len(Y)),len(Y[0]))
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

c = {"Baar":36,"Zug":45,"Rotkreuz,Cham":32,"Rotkreuz":39,"Steinhausen":43}

def KNN(Y):
    p = []
    for m in c:
        l = m[1]
        d = 0
        for i in range(len(l)):
            d+=(Y[i]-l[i])**2
        p += [(m[0],d)]
            
    return sorted(p,key=lambda x: x[1])

o = {}

for macindex in range(len(X)):
    a = KNN(X[macindex])
    o[macindex] = a[:5]


