import json
import collections
from argon2 import PasswordHasher
ph2 = PasswordHasher()


with open("knn.txt", "r") as f:
    a = json.load(f)
with open("result_poc.txt", "r") as f:
    b = json.load(f)

o = 0
t = 0
for m in b:
    if m in a:
        #print(b[m])
        
        if len(b[m.upper()][0].upper())!=2 or "." in b[m.upper()][0].upper():
            continue
        
        if a[m.upper()].upper() == b[m.upper()][0].upper():
            o+=1
        t+=1

            
    
