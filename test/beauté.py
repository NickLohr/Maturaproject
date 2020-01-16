import time
tt = time.time()
##code so far programmed nicely changed and listed
import os
import datetime
#All code is bad: Read in https://gizmodo.com/programming-sucks-why-a-job-in-coding-is-absolute-hell-1570227192
"""
import tools
#https://www.python.org/dev/peps/pep-0257/

# {"XX:XX:XX:XX:XX:XX":"102", ...}

# read AP database containing AP MAC and location
aps={}
aps+=tools.read_ap_database_type1("filename1")
aps+=tools.read_ap_database_type2("filename2")
"""
# ap now contains {"XX:XX:":"102"}

#read in basic data
class ReadInBasicData():
    def __init__(self):
        #where the access_points data is stored
        self.access_point_position_1 = "Data/access_points.log"
        self.access_point_position_2 = "Data/access_points2a.log"
        self.accesspoints={}
        self.get_data_ap1()
        self.get_data_ap2()

    #mac can be in the format 34.4.16.2.123.32 which is equal to 22:04:10:02:7B:20. I use always the second one, but the data comes with both
    def change_mactype(self,mac):
        # mac_dec_to_hex
        # converts "34.4.16." to common "22:04:10:.." (upper case)
        # return: (string)
        new_mac = ""
        for i in mac.split("."):
            #change i from hex to dec and remove the "0x" from the beginning
            # converts a single byte to hex, removes '0x' added by hex(...)
            part_mac = hex(int(i))[2:]

            # ensure two digits, e.g. (0x)1 to (0x)01
            #adding a 0 to prevent ...:45:8:78:...
            if len(part_mac)<=1:
                part_mac = "0" + part_mac

            assert len(part_mac)==2, "unexpected length of hex byte"
            #assert len(a)==1, f"len: {len(a)}, a: {a}"
            #add the part of the mac together with a ":" in the middle
            new_mac = new_mac + part_mac + ":"

        #remove the extra ":" at the end
        return new_mac[:-1]

    #the mac of the accesspoint in the ap files have not the right value. It is offset by a certain value which is change here
    # 4th bit in the 4th byte has to be inverted to get the radio's MAC from the MAC in the file
    # e.g. 1245 -> 1245
    # radio_mac(...)
    def change_mac_value(self,old_mac):
        assert len(old_mac)==16, f"unexpected length of mac: {old_mac}"
        wrong_value = old_mac[9:11]

        #this is a Binary XOR function to change the value to the one in the datasets (the forth bit on the 4th number
        new_value = hex(int('40',16)^(int(wrong_value,16)))[2:]
        # new_value = hex(0x40 ^ ) ...  # [9:11] is 4th byte
        #add if needed a "0"

        # bullshit hex converter bauen, zweimal identischer code ... ;-) tools.hex_byte()
        if len(new_value)<=1:
            new_value = "0" + new_value

        #replace old value with new one
        new_mac = old_mac[:9]+new_value+old_mac[11:]
        return new_mac

    #add the data from the first access point file
    def get_data_ap1(self):
        #read in the file
        ap_file = open(self.access_point_position_1)
        ap_data = ap_file.readlines() # check utf-8
        # ap_file_lines?
        # with open(...) as f:
        #   for ap in f.readlines()
        #

        for ap in ap_data:
            ap_info = ap.split(",")
            #change the mac to the right value and form
            ap_mac = self.change_mac_value(ap_info[0][1:17].upper())
            #add accesspoint to dictionary
            ap_room = ap_info[1].upper()[7:10]
            if not "ksz" in ap:
                ap_room = 0 # None,
            self.accesspoints[ap_mac.upper()] = ap_room

            # if "ksz" in ap: # only interested in KSZ, not other schools
            #   accesspoint[...]= ...

        ap_file.close()

    def get_data_ap2(self):
        #read in the file

        # use with
        #list(filter(lambda x: (x%2==0), a))
        ap_file = open(self.access_point_position_2)
        ap_data = ap_file.readlines()
        for ap in ap_data:
            if len(ap)<10:
                # ignore comments, first few lines, other strange stuff
                continue

            # typical line looks like this:
            #  SNMPv2-SMI::enterprises.14179.2.2.1.1.3.244.207.226.203.53.240 = STRING: "W945-0"
            # oid contains "3" just before decimal mac. File contains other lines with "1", we do NOT use these lines
            # ap[38] is that "1" or "3"
            if ap[38] == '3':
                #change the mac to the right vlaue and form
                # ... neu schreiben, base mac to radio mac, ....
                ap_mac = self.change_mactype(ap.split(" ")[0][40:])
                #add accesspoint to dictionary

                # explain [3][2:5]
                self.accesspoints[ap_mac.upper()[:-1]] = ap.split(" ")[3][2:5].upper()
        ap_file.close()


# aps als parameter

#track a mac address during one day
class Track_one_room():
    def __init__(self):
        #Readin the data from the accespoint
        self.APs= ReadInBasicData()

    #get time from data
    def get_time(self,datapart):
        return datapart[11:13] + datapart[14:16]
    #check if apmac is in the ap dictionary and returns the saved room from the dic
    def get_room_from_ap(self,apmac):
        apmac = apmac.replace("-",":")
        if apmac.upper() in self.APs.accesspoints:  # defaultdictionary, None; upper vermeiden, beim lesen 1x machen
            return self.APs.accesspoints[apmac.upper()] # wuerde eigentlich in lesefunktionen gehoeren, oder?
        return apmac
    #read in user data
    #ersätzen durch iter returns  (mac_user, room, time)
    def get_dataset_one_p(self,device_mac, filename):
        # gut erklaren
        # in memory
        #read in file
        # allenfalls filter lambda als parameter
        # user_mac, timestamp, ap_mac
        # if (filter(user_mac, timestamp, ap_mac)):
        #    append to result
        # lambda (user_mac, timestamp, ap_mac): user_mac=="1111111"
        data_file = open(filename)
        data = data_file.readlines()
        device_data = []
        # go through file
        for datapoint in data:
            dataset = datapoint.split("][")
            #check if file matches to the devices_mac
            if dataset[3].upper() == device_mac:
                #reformating the mac and of AP and adding the time of the access-point
                device_data+=[[dataset[4].replace("-",":")[:16].upper(),self.get_time(dataset[0][0:-4])]]
        data_file.close()
        return device_data

    #get all the rooms visited from this mac from one day
    def get_rooms(self, device_mac, filename):
        userdata = self.get_dataset_one_p(device_mac,filename)
        #not space time :-)
        roomtime = []
        for data in userdata:
            #add the room and time (both needed later for the track to class
            roomtime +=[[self.get_room_from_ap(data[0]),data[1]]]
        return roomtime


#get the class back from a macaddress
class Get_Class():
    def __init__(self):

        self.Tracker = Track_one_room()
        #set inital values and constants
        self.months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Nov":11,"Dec":12}
        self.rooms_visited=[]
        #need to change
        self.dic = {}
        self.timetablefile = "save9.gpn"
        self.date=0
        self.files=[]
        #find all files
        self.get_files()
        #lesson starts and lesson end of each lesson (has to change for next school year)
        self.lessons = [["0740","0825"],["0835","0920"],["0930","1015"],["1030","1115"],["1125","1210"],["1220","1305"],["1315","1400"],["1410","1455"],["1505","1550"],["1600","1645"]]
        timetable = open(self.timetablefile)
        self.data_tt = timetable.readlines()
        timetable.close()
    #get files in Data direcory
    def get_files(self):
        for (dirpath, dirnames, filenames) in os.walk("Data"):
            for k in filenames:
                #checks if it is a log file or another file
                if not "201" in k:
                    continue
                #add the filepath to self.files
                self.files.append("Data/"+k)
            break

    #get the day of the week (0-6) knowing what the date
    ##class datetime.datetime
    def get_weekday(self,date):
        date = date.split("/")[1]
        year = int(date.split("-")[0])
        month = self.months[date.split("-")[1]]
        day = int(date.split("-")[2])
        #need to replace this somehow
        return str(datetime.date(year,month,day).weekday()+1)
    #looks for a class which happens during this time (time and day) in this room
    def check_for_class(self,room,day,time):

        last_class = ""
        data_tt=list(self.data_tt)
        list_of_classes=[]

        for line_n in range(len(data_tt)):
            if "<text>" in data_tt[line_n]:
                last_class = data_tt[line_n]
            if line_n+3<len(data_tt) and '<assigned_day>'+day+'</assigned_day>' in data_tt[line_n-2] and time in data_tt[line_n] and str(room) in data_tt[line_n+2]:

                if "-" in last_class and last_class.count("-")>1:

                    list_of_classes+=[last_class.split("-")[1],last_class.split("-")[2][:-8]]
                else:
                    list_of_classes+=[last_class]

        return list_of_classes
    def fit_to_lesson(self,lesson):

        for  roomnumber in range( len(self.rooms_visited)):
        #for roomnumber in range(len(self.rooms_visited)):
            roomsystem = self.rooms_visited[roomnumber]
            time = int(roomsystem[1])

            #check if time is after the start of the lesson but still before the end
            if time >= int(lesson[0]):
                if time<=int(lesson[1]):
                    #check if this room is used during this lesson and by which class
                    return self.check_for_class(self.rooms_visited[roomnumber][0],self.get_weekday(self.date),lesson[0])
                elif int(self.rooms_visited[roomnumber-1][1])> int(lesson[0])-10:
                    #check if last room is used during this lesson
                    return self.check_for_class(self.rooms_visited[roomnumber-1][0],self.get_weekday(self.date),lesson[0])
        return []

    #finds out how many how what is visited
    def list_to_percent(self,classes):
        self.dic = {}
        #go through all the classes visited
        for classe in classes:
            if classe == []:
                continue
            if len(classe)==1:

                continue
            #defining all the people infolved in this class
            people = []

            #go through every class
            for j in range(1,len(classe[0])):
                if classe[0][j]=="x":
                    continue
                people+=[classe[0][0]+classe[0][j]]


            #multiple teachers are seperated by a comma
            if "," in classe[1]:
                for m in classe[1].split(","):

                    people+=[m]
            else:
                #if just one teacher teaches
                people+=[classe[1]]

            #add all person to self.dic
            for person in people:
                if person in self.dic:
                    self.dic[person]+=1
                else:
                    self.dic[person]=1


    #track mac with the rooms visited
    def track_mac(self,mac):
        self.classes=[]
        for file in self.files:
            self.date = file
            self.rooms_visited = self.Tracker.get_rooms(mac,self.date)
            #go through every lesson and find if the device visited it
            for lesson in self.lessons:
                self.classes+=[self.fit_to_lesson(lesson)]

        self.list_to_percent(self.classes)
        print(self.dic)
        #if the mac descovert a class or a teacher it returns the most likely one
        if len(self.dic)!=0:
            return max(self.dic, key=self.dic.get), self.dic[max(self.dic, key=self.dic.get)]

        return "unknown", 0

#reverse tracking tracks every mac-addresse from the data

class Reverse_Tracking():
    def __init__(self):
        self.Class = Get_Class()
        #set the dic which get all the macs in it
        self.reverse_dic={}
    def get_mac(self,line):
        #extract the mac from the data
        line = line.split("][")
        return line[3].upper()

    def reverse(self):
        i = 0
        #for every file search for new mac-addresses
        for file in self.Class.files:
            data = open(file)
            lines = data.readlines()
            for line in lines:

                mac = self.get_mac(line)
                #check if the mac is already found
                if mac in self.reverse_dic:
                    continue

                i+=1
                #track mac and get class and hits
                classs, amount = self.Class.track_mac(mac.upper())

                self.reverse_dic[mac] = classs
            data.close()


if __name__ == "__main__":
    c = Get_Class()
    print(c.track_mac("E0-33-8E-74-84-04".upper()))
print(time.time()-tt, "beauté")
