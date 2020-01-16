
access_point = "Data/access_points.log"
access_point_l = "Data/access_points2a.log" 

accesspoints={}
##time has to be edited to use descimal (9:30 --> 9.5)
def time_change(time):
        times = time[11:-7]
        timer = times[0:2]+times[3:5]
        return timer
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

def mac_to_other_mac(mac):
        string = mac[9:11]
        
        hex_str=int(string,16)
        
        hex_s=   int('40',16) ^(hex_str)
        i = str(hex(hex_s))[2:]
        if len(i)<=1:
                i = '0' + i
        return mac[:9]+i+mac[11:]
def write_list_to_file(filename, liste):#list is [time,place]
        file = open(filename, "w")
        for k in liste:
                file.write(str(k[0])+" " + str(k[1]))
        file.close()

        
def get_right_file(date):
        return "Data/"+str(date)+"-access.log"

def get_room_from_accesspoint(apmac):
        if '-' in apmac:
                apmac = apmac.replace("-",":")
                #apmac = mac_to_other_mac(apmac)
        if apmac.upper() in accesspoints.keys():
                return accesspoints[apmac.upper()]
        else:
                return apmac

def get_my_data(device_mac, day): ##device_mac like 12-23-42-34-A3-V3
        files = get_right_file(day)
        file = open(files)
        data = file.readlines()
        my_data=[]
        pp = 0
        for o in data:
                m = o.split("][")
                if m[3].upper()==device_mac:
                        pp+=1
                        aa = m[4]
                        b = aa.replace('-',':')
                        #b = mac_to_other_mac(b[0:16])
                        my_data+=[[b[0:16].upper(),time_change(m[0][0:-4])]]
        file.close()
    
        return my_data

def get_rooms(device_mac, day):
        my_data = get_my_data(device_mac, day)
        rooms=[]
        for o in my_data:
               
                rooms+=[[get_room_from_accesspoint(o[0]),o[1]]]
        return rooms
#get the data from the accesspointsfiles to the dictionary
data_to_accesspointsdir2()
data_to_accesspointsdir1()
#test
#print(accesspoints["54:78:1A:5F:D0:7"])

if __name__ == "__main__":
        mac = input("Which Mac?")
        date = input("When?")
        rooms_visited = get_rooms(mac, date)
        for k in rooms_visited:
                print(k)
