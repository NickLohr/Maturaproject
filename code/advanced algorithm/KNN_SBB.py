import sys
import collections
sys.path.insert(1,"../../test/")
import tools_with_fast_tt as tools
import numpy as np

X = np.load("datatouseaa_minutes.npy")
print(len(X))

#remove ageri und menzingen wenn noch keine daten (separat)
c = ["Menzingen":[42,53]"Ägeri":[36,52],"Baar":[32,44],"Zug":[50,43],"Rotkreuz,Cham":[29,44],"Rotkreuz":[35,35],"Steinhausen":[36,46]]

def KNN(Y):
    p = {}
    for m in c.items():
        
        i = m[1]
        
        
        
        d = 0
        for i in range(len(Y),2): #only mornings
                o = []
                for l in i:
                    o+=[(Y[i]-l)**2]
                d+=min(o)
 
        p.append([m[0],d])
            
            
    return sorted(p,key=lambda x: x[1])

o = {}

for macindex in range(len(X)):
    a = KNN(X[macindex])
    o[macindex] = a[:5]


