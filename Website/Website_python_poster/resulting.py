import json
import collections
from argon2 import PasswordHasher
ph2 = PasswordHasher()


results = collections.defaultdict(lambda:["Unknown",0,"Zug_+"])
with open("sol_mean.txt", "r") as f:
    a = json.load(f)
with open("KNN2_final_1.txt", "r") as f:
    b = json.load(f)


aa = {}
for m in range(len(a)):
    aa[a[m]] = b[str(m)]


with open("results_aa.txt","w") as file:
    json.dump(aa,file)

