from dic_as_class import *
import argon2
hasher = argon2.PasswordHasher()
Dic = dic()
k2 = Dic.k2
salt = b"somesalt"
dici={}
print(hasher.hash(k2["5H"][0][0],salt))
for o in k2:
    for p in k2[o]:
        if p[0] in dici:
            
            dici[hasher.hash(p[0],salt)]+=[o]
            print(hasher.hash(p[0],salt))
        else:
            dici[hasher.hash(p[0],salt)] = [o]

file = open("dic4.data","w")
file.write("#hashed with salt [somesalt] \n"+str(dici))
file.close()
i = input("Mac")
hashed = hasher.hash(i,salt)
print(dici[hashed])
