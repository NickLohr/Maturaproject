import json
import collections
from argon2 import PasswordHasher
ph2 = PasswordHasher()

#Ankunft und Geht Zeit:
#Klasse/Lehrer 0
#Essen 1
#Wohnort 2
#Alle Daten (Username):
#Name/Inizialen 3
#Namenlänge 4
#ehemalige Klasse 5
#Wohnort 6
#Erstes Jahr an der Kanti 7
#Schwerpunktfach 8
#Ausbildung 9
#Fach 10
results = collections.defaultdict(lambda:["Unknown",0,"Zug_+","NAL.","namelength","class","habitat","ersterjahr","major","kanti","mathi"])
print("KLasse")
#Classe
with open("knn.txt", "r") as file:
    g = json.load(file)

for m in g:
    results[m][0] = g[m]
print("Essen")
#Lunch
with open("lunch_2010.txt", "r") as f:
    c = json.load(f)
for m in c:
    
    if c[m]>10000:
        results[m.upper().replace(",","")][1] = "often"
    elif c[m]>1000:
        results[m.upper().replace(",","")][1] = "regularly"
    else:
        results[m.upper().replace(",","")][1] = "rarely"
print("Ort1")
#Wohnort
with open("sol_minutes_f.txt", "r") as f:
    d = json.load(f)
with open("KNN_SBB_1.txt", "r") as f:
    e = json.load(f)

bb = {}
for m in range(len(d)):
    bb[d[m]] = e[str(m)][0][0]


for m in bb:
    results[m.upper().replace(",","")][2] = bb[m]

print("Jahr")
#initials
#erste Jahr
with open("usernames2.txt", "r") as f:
    a = json.load(f)
    
with open("lehrpersonen_info.txt", "r") as f:
    b = json.load(f)
for m in a:

    i = a[m].split("@")[0]
    if i.count(".") == 2:
        k = i.split(".")
        results[m.upper().replace(",","")][3] = (k[1][0]+k[0][0]).upper()
        results[m.upper().replace(",","")][7] = k[2]
    elif m in b:
        results[m.upper().replace(",","")][0] = "Teacher or Staff"        
        results[m.upper().replace(",","")][3] = (b[m][1][0]+b[m][0][0]).upper()

        results[m.upper().replace(",","")][4] = len(b[m][1]+b[m][0])
        results[m.upper().replace(",","")][9] = b[m][3]
        if len(b[m])==5:
            results[m.upper().replace(",","")][10] = " ".join(b[m][4])
        else:
            print(b[m])
    else:
        results[m.upper().replace(",","")][0] = "Staff or External"
        
                                                 


print("Ort2")
#ehemalige Klasse
#wohnort
with open("nameplace.txt", "r") as f:
    a = json.load(f)
for m in a:
    results[m.upper().replace(",","")][5] = a[m][0]
    results[m.upper().replace(",","")][6] = a[m][2]
    results[m.upper().replace(",","")][4] = len(a[m][1].replace(" ",""))
    
 
with open("results.txt","w") as file:
    json.dump(results,file)

"""
fin = {}
for k in results:
    fin[ph2.hash(k.replace(",","").upper())] = results[k]
with open("results2.txt","w") as file:
    json.dump(fin,file)
>>>>>>> fd160ca53be28c053c59a0a2961542cb0c26b3b7
    
"""
