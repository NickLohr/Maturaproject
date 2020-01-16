#                                tracking_v2.py
log_file= "Data/2018-Dec-14-access.log"
access_point = "Data/access_points.log"
def mac_to_other_mac(mac):
        string = mac[9:11]
        hex_str=int(string,16)
        hex_s=   int('40',16) ^(hex_str)
        i = str(hex(hex_s))[2:]
        if len(i)<=1:
                i = '0' + i
        return mac[:9]+i+mac[11:]

accesspoints={}
ap = open(access_point)
datapoints = ap.readlines()
for k in datapoints:
        m = k.split(",")
        for o in range(0,len(m)):
                if "w-ksz" in m[o]:
			#			print(m[o-1][1:18])
                        accesspoints[m[o-1][1:17].upper()]=m[o].upper()



ap.close()
"""

#for later use! Don't have to access the original data afterwards.
mda = open("access_points.lst", "w")
for k in accesspoints.keys():
        mda.write(str(k+" , "+accesspoints[k]+ " \n"))
mda.close()
"""
#print(accesspoints)
log = open(log_file)
data= log.readlines()
rooms_visited= []
for op in data:
        t = op.split("][")
        if t[3].upper() == "88-E9-FE-B2-7B-46":
                aa = t[4]
                b = aa.replace("-",":")
                b = mac_to_other_mac(b[0:16])
                if b.upper() in accesspoints.keys():
                        #have to figure out how all the access points work
                        rooms_visited+=[accesspoints[b]]
                else:
                        print(b.upper(), t[4])                        #print(accesspoints[b[0:17]])

log.close()
#print(rooms_visited)
def mac_to_other_mac(mac):
        string = mac[9:11]
        hex_str=int(string,16)
        hex_s=   int('40',16) ^(hex_str)
        i = str(hex(hex_s))[2:]
        if len(i)<=1:
                i = '0' + i
        return mac[:9]+i+mac[11:]
def get_right_file(day): #still TO-DO
        return "day.log"
def get_room_from_accesspoint(apmac):
        apmac = apmac.replace("-",":")
        apmac = mac_to_other_mac(apmac)
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
#print(accesspoints["00:3A:99:44:70:5"])


for k in rooms_visited:
	print(k)
for k in accesspoints.keys():
	if "54:" in  k:
		print(k)
