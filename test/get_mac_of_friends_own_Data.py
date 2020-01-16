from os import walk
from tqdm import tqdm
fdict={}
udic={}
data={}
dicw={"Mon":1, "Tue":2,"Wed":3,"Thu":4,"Fri":5,"Sat":6,"Sun":7}
path = "KNNdata"
def readin():
    global data
    global udic
    f = []
    m=0
    for (dirpath, dirnames, filenames) in walk(path):
        for k in filenames:
            f.append(k[:])
        else:
            break
    for o in f:
        print(o)
        with open(path+"/"+o) as file:
            datas = file.readlines()
        for pp in datas:
            if  "\x00" in pp:
                continue
            if pp == "\n":
                continue
          
            macap="WiFi-Pineapple"
            macdv=pp.split(" ")[0]
            time = float(pp.split(" ")[1])

            if macap in data:
                data[macap]+=[[time,macdv]]
            else:
                data[macap] = [[time,macdv]]

def add_eachother(l):
    print(len(l),"len(l)")
    global fdict
    for m in tqdm(range(len(l))):
        if not l[m] in fdict.keys():
            fdict[l[m]]={}
        for oo in l:
           
            if oo == l[m]:
                continue
            if oo in fdict[l[m]].keys():
              fdict[l[m]][oo]+=1
            else:
                fdict[l[m]][oo]=1

def main():
    global data
    readin()
    ddf=0
    for o in data.keys():
        ddf+=1
        print(ddf)
        m = data[o]  #o is a mac address
        for i in tqdm(range(len(m))):
            k = i
            liste=[]
            while k<len(m) and (m[i][0]-m[k][0])**2<15**2:
                liste+=[m[k][1]]
                k+=1
            print("hiih")
            add_eachother(liste)


if __name__ == "__main__":
    main()
