log_file= "Data/2018-Dec-14-access.log"
access_point = "Data/access_points.log"
accesspoints={}
def data_to_accesspointsdir():
        ap = open(access_point)
        datapoints = ap.readlines()
        for k in datapoints:
                m = k.split(",")
                for o in range(0,len(m)):
                        if "w" in m[o]:
                                accesspoints[m[o-1][1:17].upper()]=m[o].upper()
        ap.close()

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

        
def get_right_file(date): #still TO-DO
        return str(date)+".log"

def get_room_from_accesspoint(apmac):
        if '-' in apmac:
                apmac = apmac.replace("-",":")
                apmac = mac_to_other_mac(apmac)
        if apmac in accesspoints.keys():
                return accesspoints[apmac]
        else:
                return apmac
        
def get_my_data(device_mac, day): ##device_mac like 12-23-42-34-A3-V3
        files = get_right_file(day)
        file = open(files)
        data = file.readlines()
        my_data=[]
        for o in data:
                m = o.split("][")
                if m[3].upper()==device_mac:
                        aa = m[4]
                        b = aa.replace('-',':')
                        b = mac_to_other_mac(b[0:16])
                        my_data+=[[b,m[0][0:-4]]]
        file.close()
        return my_data

def get_rooms(device_mac, day):
        my_data = get_my_data(device_mac, day)
        rooms=[]
        for o in my_data:
                rooms+=[[get_room_from_accesspoint(o[0]),o[1]]]
        return rooms
data_to_accesspointsdir()
rooms_visited = get_rooms("88-E9-FE-B2-7B-46", "Data/2019-Jan-10-access")

for k in rooms_visited:
	print(k)
for k in accesspoints.keys():
	if "5c:".upper() in  k.upper():
		print(k)
