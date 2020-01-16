#just read in data
from os import walk
from lxml import objectify

access_point = "Data/access_points.log"
access_point_l = "Data/access_points2a.log" 
timetable = "save9.gpn"

dicw={"Mon":1, "Tue":2,"Wed":3,"Thu":4,"Fri":5,"Sat":6,"Sun":7}

accesspoints={}
tt=[]
data=[]
def mac_to_other_mac(mac):
        string = mac[9:11]
        
        hex_str=int(string,16)
        
        hex_s=   int('40',16) ^(hex_str)
        i = str(hex(hex_s))[2:]
        if len(i)<=1:
                i = '0' + i
        return mac[:9]+i+mac[11:]
def data_to_accesspointsdir1():
        ap = open(access_point)
        datapoints = ap.readlines()
        for k in datapoints:
                m = k.split(",")
                o=1
                x = mac_to_other_mac(m[o-1][1:17].upper())
                accesspoints[x.upper()]=m[o].upper()[7:10]
        ap.close()

def ip_to_mac(ip):
        k = ip.split(".")
        mac = ""
        for h in k:
                i = str(hex(int(h)))[2:]
                if len(i)<=1:
                        i = '0' + i
                mac= mac + i + ":"
        return mac[:-1]      
def data_to_accesspointsdir2():
        ap = open (access_point_l)
        datapoints = ap.readlines()
        for k in datapoints:
                if len(k)<10:
                        continue
                
                if k[38] == '3':
                        o = k.split(" ")
                        ip = o[0][40:]
                        place= o[3][2:5]
                        mac = ip_to_mac(ip)
                        accesspoints[mac.upper()[:-1]]=place.upper()

def change_time(time):
    o = dicw[time[0:3]]
    
    ti = time[11:16]
    ti = ti.replace(":", "")
    time = o*10000+int(ti)
    return time
def data_data():
    global data
    f = []
    for (dirpath, dirnames, filenames) in walk("Data"):
        for k in filenames:
            if "points" in k: ##accesspoints file in the same folder
                continue
            f.append(k[:])
        break
    for o in f:
        datan = open("Data/"+o)
        datas = datan.readlines()
        for pp in datas:
            if not "ksz" in pp:
                continue
            w = pp.split("][")
            #print(w[-2][:-9], o)
            try:
                data+=[[accesspoints[w[-2][:-9].replace("-",":").upper()],w[-3],change_time(w[0])]]
            except KeyError as e:
                #print(e,o)
                continue
        
    data.sort(key=lambda x: x[2])
        

def data_tt():
    for k in range(0,100):
            tt.append([[],[],[]])
    toto = open(timetable)
    dat = toto.readlines()
   
    for op in range(len(dat)):
        if "<lesson " in dat[op]:
                #ausnahmen
                if not "<periods>" in dat[op+1]:
                       continue
                if not "\"" in dat[op+3]:
                        continue
                if not "\"" in dat[op+4]:
                        continue
                periods = int(dat[op+1].replace("/","").split("<periods>")[1])
                teach = dat[op+3].split("\"")[1][3:]
                clas = dat[op+4].split("\"")[1][3:]
                #print(dat[op+4])
                if " " in clas:
                        clas=[clas[:2],clas[-2:]]
                
                q=3
                while not "<times>" in dat[op+q]:
                        q+=1
                #print(q)
                for a in range(periods):
                     
                        per = dat[op+q+3].replace("/","").split("<assigned_period>")[1]
                      
                        day = dat[op+q+2].replace("/","").split("<assigned_day>")[1]
                        if not "room" in dat[op+q+6]:
                                continue
                        room = dat[op+q+6].split("\"")[1][3:]
                     
                        period = (int(day)-1)*11+int(per)+1
                        #print(period)
                        tt[period][0] += [clas]
                        #print(clas)
                        tt[period][1] += [room]
                        tt[period][2] += [teach]
                        q+=1
                        while not "</time>" in dat[op+q]:
                                q+=1
                        
                       
                
                




if __name__ == "__main__":
    data_tt()
    data_to_accesspointsdir2()
    data_to_accesspointsdir1()
    data_data()
























    
