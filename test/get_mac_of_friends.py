#Friendship is how often a person changes the AP at the same time then another person
#threshold is 10 sec
from os import walk
fdict={}
data={}
dicw={"Mon":1, "Tue":2,"Wed":3,"Thu":4,"Fri":5,"Sat":6,"Sun":7}
#time as dhhmmss as string
#t1<t2
def same_time(t1,t2):

    o=0
    return ((int(t2[0+o])-int(t1[0+o]))*60*60*24+(int(t2[1+o:3+o])-int(t1[1+o:3+o]))*60*60+(int(t2[3+o:5+o])-int(t1[3+o:5+o]))*60+int(t2[5+o:])-int(t1[5+o:]))<=1

def changetime(a):
    a = a.replace("  ", " ")
    b = a.split(" ")
    c = b[-3].replace(":","")
    d = b[0]
    e = dicw[d]


    return str(e)+str(c)
#check if accesspoint is the same in data example then mac
def apmac(m):
    b = m.split("][")
    return b[-2][:17]


def usermac(i):
    b = i.split("][")
    return b[-3]
def get_time(u):
    b = u.split("][")
    return changetime(b[0])
def add_eachother(l):
    global fdict
    for m in range(len(l)):
        if not l[m] in fdict.keys():
            fdict[l[m]]={}
        for oo in l:
           
            if oo == l[m]:
                continue
            if oo in fdict[l[m]].keys():
              fdict[l[m]][oo]+=1
            else:
                fdict[l[m]][oo]=1
def add_onemac(l,m):
    global fdict
    if not m in l:
        return
    if not m in fdict:
        fdict[m]={}
    for oo in l:

        if oo in fdict[m].keys():
            fdict[m][oo]+=1
        else:
            fdict[m][oo]=1
  
def readin():
    global data
    f = []
    m=0
    for (dirpath, dirnames, filenames) in walk("Data"):
        for k in filenames:
            if "points" in k: ##accesspoints file in the same folder
                continue
            if not "Jan" in k:
                continue
            if m>12 and m<18:
                f.append(k[:])
            m+=1
        break
    for o in f:
        print(o)
        datan = open("Data/"+o)
        datas = datan.readlines()
        for pp in datas:
            if not "ksz" in pp:
                continue
            macap=apmac(pp)
            macdv=usermac(pp)
            time = get_time(pp)
            if macap in data:
                data[macap]+=[[time,macdv]]
            else:
                data[macap] = [[time,macdv]]
#data ={"macap": ["1235959",macdv]}
ppop = "88-e9-fe-b2-7b-46"
def main():
    global data
    readin()
    ddf=0
    for o in data.keys():
        ddf+=1
        print(ddf)
        m = data[o]  #o is a mac address
        for i in range(len(m)):
            k = i
            liste=[]
            while k<len(m) and same_time(m[i][0],m[k][0]):
                liste+=[m[k][1]]
                k+=1
            
            add_onemac(liste,ppop)
    
main()

"""
for opo in fdict[ppop]:
	if fdict[ppop][opo]>2000:
	    print(opo,fdict[ppop][opo])
			       """





