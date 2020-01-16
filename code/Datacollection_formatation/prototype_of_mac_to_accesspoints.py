"""
  GNU nano 3.1                                                tracking_v1.py                                                           

log_file= "log_file.log"
access_point = "access_points.log"

accesspoints={}
ap = open(access_point)
datapoints = ap.readlines()
for k in datapoints:
        m = k.split(",")
        for o in range(0,len(m)):
                if "w-ksz" in m[o]:
                        accesspoints[m[o-1][1:18]]=m[o]



ap.close()


#for later use! Don't have to access the original data afterwards.
mda = open("access_points.lst", "w")
for k in accesspoints.keys():
        mda.write(k,",",accesspoints[k], "\n")
mda.close()

#print(accesspoints)
log = open(log_file)
data= log.readlines()
rooms_visited= []
for op in data:
        t = op.split("][")

        if t[3].upper() == "88-E9-FE-B2-7B-46":
                print(t[4])
                aa = t[4]
                b = aa.replace("-",":")
                if b[0:17] in accesspoints.keys():
                        #have to figure out how all the access points work
                        rooms_visited+=[accesspoints[b[0:17]]]

                        #print(accesspoints[b[0:17]])

log.close()
"""
def mac_to_other_mac(mac):
        string = mac[9:11]
        print(string)
        
        hex_str=int(string,16)
        print(hex_str)
        hex_s=   int('40',16) ^(hex_str)
        print (hex_s)
        i = str(hex(hex_s))[2:]
        if len(i)<=1:
                i = '0' + i
        return mac[:9]+i+mac[11:]
def get_right_file(day): #still TO-DO
        return "day.log"
def get_room_from_accesspoint(apmac):
        apmac = apmac.replace("-",":")
        return accesspoints[apmac]
def get_my_data(device_mac, day): ##device_mac like 12-23-42-34-A3-V3
        files = get_right_file(day)
        file = open(files)
        data = file.readlines()
        my_data=[]
        for o in data:
                m = k.split(",")
                if m[3][0:17]==device_mac:
                        my_data+=[[m[3][0:17],m[4][0:17],m[0][0:-4]]]
        return my_data

def get_rooms(device_mac, day):
        my_data = get_my_data(device_mac, day)
        rooms=[]
        for o in my_data:
                rooms+=[[accesspoints(o[1]),o[2]]]

        return rooms

#get_rooms("12-23-42-34-A3-V3", "10.1.2019")
        
print(mac_to_other_mac("0C:F4:D5:44:4B:08"))
