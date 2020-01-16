import time
tt = time.time()
##code so far programmed nicely changed and listed
from os import walk
import datetime
import re

#All code is bad: Read in https://gizmodo.com/programming-sucks-why-a-job-in-coding-is-absolute-hell-1570227192
reg_mac = '([a-fA-F0-9]{2}[:|\-]?){6}'
reg_time  ='([0-9]{2}[:]?){2}'
reg_room = 'w-ksz-\w\w\w'

rrr = 0
#read in basic data
class ReadInBasicData():
    def __init__(self):
        #where the access_points data is stored
        self.access_point_position_1 = "Data/access_points.log"
        self.access_point_position_2 = "Data/access_points2a.log"
        self.accesspoints={}
        self.get_data_ap1()
        self.get_data_ap2()

    def get_mac(self,line):
        #extract the mac from the data
        c = re.compile(reg_mac).finditer(line)
        m = []
        for y in c:
            m+=[line[y.start():y.end()].replace("-",":").upper()[:17]]
        return m

    #mac can be in the format 34.4.16.2.123.32 which is equal to 22:04:10:02:7b:20. I use always the second one, but the data comes with both
    def change_mactype(self,mac):
        new_mac = ""
        for i in mac.split("."):
            #change i from hex to dec and remove the "0x" from the beginning
            part_mac = str(hex(int(i)))[2:]
            #adding a 0 to prevent ...:45:8:78:...
            if len(part_mac)<=1:
                part_mac = "0" + part_mac
            #add the part of the mac together with a ":" in the middle
            new_mac = new_mac + part_mac + ":"
        #remove the extra ":" at the end
        return new_mac[:-1]
    #the mac of the accesspoint in the ap files have not the right value. It is offset by a certain value which is change here
    def change_mac_value(self,old_mac):
        wrong_value = old_mac[9:11]
        #this is a Binary XOR function to change the value to the one in the datasets (the forth bit on the 4th number
        new_value = str(hex(int('40',16)^(int(wrong_value,16))))[2:]
        #add if needed a "0"
        if len(new_value)<=1:
            new_value = "0" + new_value
        #replace old value with new one
        new_mac = old_mac[:9]+new_value+old_mac[11:]
        return new_mac
    def get_room(self,line):
        match = re.search(reg_room, line)
        if not match:
            return 0
        return match.group()[6:].upper()
    #add the data from the first access point file
    def get_data_ap1(self):
        #read in the file
        ap_file = open(self.access_point_position_1)
        ap_data = ap_file.readlines()
        for ap in ap_data:
            ap_mac = self.get_mac(ap)[0]
            #change the mac to the right value and form
            ap_mac = self.change_mac_value(ap_mac)[:-1]
            #add accesspoint to dictionary
            self.accesspoints[ap_mac.upper()] = self.get_room(ap)
        ap_file.close()

    def get_data_ap2(self):
        #read in the file
        ap_file = open(self.access_point_position_2)
        ap_data = ap_file.readlines()
        for ap in ap_data:
            if len(ap)<10:
                continue
            if ap[38] == '3':
                #change the mac to the right vlaue and form
                ap_mac = self.change_mactype(ap.split(" ")[0][40:])
                #add accesspoint to dictionary
                self.accesspoints[ap_mac.upper()[:-1]] = ap.split(" ")[3][2:5].upper()
        ap_file.close()


#track a mac address during one day
class Track_one_room():
    def __init__(self):
        #Readin the data from the accespoint
        self.APs= ReadInBasicData()
        self.test=[]
    #get time from data
    def get_time(self,dataline):
        k = re.compile(reg_time).finditer(dataline)
        ###########################DO with reg and whole line
        m = []


        for y in k:

            m+=[dataline[y.start():y.end()].replace(":","")]
        return m[0]
    #check if apmac is in the ap dictionary and returns the saved room from the dic
    def get_room_from_ap(self,apmac):
        apmac = apmac[:-1]
        if apmac.upper() in self.APs.accesspoints:
            return self.APs.accesspoints[apmac.upper()]
        if not apmac in self.test:
            self.test+=[apmac]
        return apmac
    #read in user data
    def get_dataset_one_p(self,device_mac, filename):
        #read in file
        data_file = open(filename)
        data = data_file.readlines()
        device_data = []
        # go through file
        for datapoint in data:
            macs = self.APs.get_mac(datapoint)
            if len(macs)!=2:
                continue
            mac_device = macs[0]

            mac_ap = macs[1]

            #check if file matches to the devices_mac
            if mac_device == device_mac:
                #reformating the mac and of AP and adding the time of the access-point
                device_data+=[[mac_ap,self.get_time(datapoint)]]
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
        for (dirpath, dirnames, filenames) in walk("Data"):
            for k in filenames:
                #checks if it is a log file or another file
                if not "201" in k:
                    continue
                #add the filepath to self.files
                self.files.append("Data/"+k)
            break

    #get the day of the week (0-6) knowing what the date
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

        roomnumber=0

        while roomnumber < len(self.rooms_visited):
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
            roomnumber+=1
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
    def reverse(self):
        i = 0
        #for every file search for new mac-addresses
        for file in self.Class.files:
            data = open(file)
            lines = data.readlines()
            for line in lines:

                mac = self.Class.Tracker.APs.get_mac(line)[0]
                #check if the mac is already found
                if mac in self.reverse_dic:
                    continue
                print(i, mac)
                i+=1
                #track mac and get class and hits
                classs, amount = self.Class.track_mac(mac.upper())
                print(classs,amount)
                self.reverse_dic[mac] = classs
            data.close()


if __name__ == "__main__":
    c = Get_Class()
    print(c.track_mac("88:e9:fe:b2:7b:46".upper()))


print(time.time()-tt, "reg")
