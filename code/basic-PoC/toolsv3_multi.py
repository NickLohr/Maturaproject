
##code so far programmed nicely changed and listed
import os
import datetime
import collections
from multiprocessing import Pool
#All code is bad: Read in https://gizmodo.com/programming-sucks-why-a-job-in-coding-is-absolute-hell-1570227192
"""
All the tools one need to track one or several macs with the log-rfvbnhztrdata from the IT department
"""
user_mac = ""
files = []
time_table_dic={}
aps={}

def hex_byte(number):
    """
    Takes a 2 byte dec number and returns a 2 byte hex number (upper case)
    e.g. 123 to 7B, 15 to 0F
    return: (string)
    """
    #hex gives one "0x3a" back
    #but we need just 3A. So remove the first two digits and upper all
    hex_number = hex(number)[2:].upper()

    #ensure two digits, e.g (0x)3 to (0x)03
    if len(hex_number)<=1:
        hex_number = "0" + hex_number

    assert len(hex_number)==2, "unexpected length of hex byte"

    return hex_number

def mac_dec_to_hex(dec_mac):
    """
    mac_dec_to_hex
    It takes the make from the OID system and converts it to the standard hex
    converts "34.4.15." to common "22:04:0f:.." (upper case)
    return: (string)
    """
    hex_mac = ""
    #THi
    for i in dec_mac.split("."):
        #change i from hex to dec and remove the "0x" from the beginning
        # converts a single byte to hex, removes '0x' added by hex(...)
        part_mac = hex_byte(int(i))


        assert len(part_mac)==2, "unexpected length of hex byte"
        #assert len(a)==1, f"len: {len(a)}, a: {a}"
        #add the part of the mac together with a ":" in the middle
        hex_mac = hex_mac + part_mac + ":"

    #remove the extra ":" at the end
    return hex_mac[:-1]

def radio_mac(file_mac):
    """
    radio_mac invertes 4th bit in 4th byte of the mac to get the mac used in the logfiles
    input: mac from the accesspoints files as STRING
    output: radio mac used in the log files (STRING)
    e.g 88:E9:FE:B2:7B:4 --> 88:E9:FE:F2:7B:4
    last digit of mac is removed because of unimportance
    """
    assert len(file_mac)==16, f"unexpected length of mac: {file_mac}"

    #this is a Binary XOR function to change the value to the one in the datasets (the forth bit on the 4th number
    new_value = hex_byte(int('40',16)^(int(file_mac[9:11],16))) # The [9:11] takes the 4th byte and the rest gets inverted
    # new_value = hex(0x40 ^ ) ...  # [9:11] is 4th byte


    #replace old value with new one
    new_mac = file_mac[:9]+new_value+file_mac[11:]
    return new_mac

#add the data from the first access point file
def read_ap_database_type1(filename):
    """
    read_ap_database_type1
    input: The filename of the accesspoint with the type1
    output: it returns a dictionary with mac of ap and room of ap of all aps
    e.g. {"34:54:23:1A:0F:3":"424",...}
    Last digit varies depending on the frequence --> gets removed
    """
    aps = {}
    with open(filename, encoding='utf-8') as f:
        for ap in f.readlines():
            ap_info = ap.split(",")
            #change the mac to the right value and form
            ap_mac = radio_mac(ap_info[0][1:17].upper())
            ap_room = ap_info[1].upper()[7:10]
            #add accesspoint to dictionary

            aps[ap_mac.upper()] = ap_room

    return aps

def read_ap_database_type2(filename):
    """
    read_ap_database_type2
    input: The filename of the accesspoint with the type2
    output: it returns a dictionary with mac of ap and room of ap of all aps
    e.g. {"34:54:23:1A:0F:2":"424",...}
    Last digit varies depending on the frequence --> gets removed
    """
    aps = {}
    with open(filename, encoding = 'utf-8') as f:
        for ap in f.readlines():

            if len(ap)<10:
                # ignore comments, first few lines, other strange stuff
                continue

            # typical line looks like this:
            #  SNMPv2-SMI::enterprises.14179.2.2.1.1.3.244.207.226.203.53.240 = STRING: "W945-0"
            # oid contains "3" just before decimal mac. File contains other lines with "1", we do NOT use these lines
            # ap[38] is that "1" or "3"
            if ap[38] == '3':

                #oid contains the mac in dec after "3." until the first space in the file
                #change mac from dec to hex
                ap_mac = mac_dec_to_hex(ap.split(" ")[0][40:])

                # [3][2:5] is describing the rooms
                # SNMPv2-SMI::enterprises.14179.2.2.1.1.3.244.207.226.203.53.240 = STRING: "W945-0"
                # the [3] filters out "W945-0"
                # with the "W" gets removed and everything after the 3 digit room hex_number
                # The last digit of the mac of the ap changes depending on 2.4 or 5 MHz
                # so it gets removed
                aps[ap_mac.upper()[:-1]] = ap.split(" ")[3][2:5].upper()
    return aps

def get_time(time):
    """
    read the time out of the data line and put it in the format of datetime.datetime
    use year to second
    """
    #input is a time from the file
    #e.g. Sun Dec  9 04:34:01 2018
    time = time.replace("  "," ").split(" ")
    assert len(time) in [5,6,7], f"unexpected length/format of time: {time}"
    assert len(time[4])==4, f"unexpected length/format of year: {time}"
    months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    year = int(time[4])
    month = months[time[1]]
    day = int(time[2])
    hour = int(time[3][0:2])
    minute = int(time[3][3:5])
    sec = int(time[3][6:8])
    #print(year,month,day,hour,minute,sec)
    a = datetime.datetime(year,month,day,hour,minute,sec)
    return a

def parse_time_table(filename):
    time_table_dic=collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [])))
    #time_table_dic[0]["0740"]["304"]="4H"
    """
    <lesson id="LS_1718300">
      <periods>3</periods>
      <lesson_subject id="SU_SPD"/>
      <lesson_teacher id="TR_WICK"/>
      <lesson_classes id="CL_2d CL_2g"/>
      <teacher_value>300000</teacher_value>
      <effectivebegindate>20180820</effectivebegindate>
      <effectiveenddate>20190705</effectiveenddate>
      <block>2</block>
      <occurence>11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111FF11111</occurence>
      <text>SPD-2dg-WICK</text>
      <text1>SPD-2dg-WICK</text1>
      <text2>Sport Damen</text2>
      <foreignkey>Sport Damen</foreignkey>
      <times>
        <time>
          <assigned_day>1</assigned_day>
          <assigned_period>4</assigned_period>
          <assigned_starttime>1030</assigned_starttime>
          <assigned_endtime>1115</assigned_endtime>
          <assigned_room id="RM_803"/>
        </time>
        <time>
          <assigned_day>4</assigned_day>
          <assigned_period>4</assigned_period>
          <assigned_starttime>1030</assigned_starttime>
          <assigned_endtime>1115</assigned_endtime>
          <assigned_room id="RM_803"/>
        </time>
        <time>
          <assigned_day>4</assigned_day>
          <assigned_period>5</assigned_period>
          <assigned_starttime>1125</assigned_starttime>
          <assigned_endtime>1210</assigned_endtime>
          <assigned_room id="RM_803"/>
        </time>
      </times>
    </lesson>
    """

    f = open(filename)
    lines = f.readlines()
    f.close()
    for line_number in range(len(lines)):
        #<lesson id="LS_XXXXXXXX"> is alway at the beginning of a lesson
        if "<lesson id=\"" in lines[line_number]:

            #<periods>3</periods> --> 3
            #needed later (in times)
            amount = lines[line_number+1].replace("/","").split("<periods>")[1]
            try:
                amount = int(amount)
            except ValueError as e:
                print(e)

            assert type(amount)==int, "wrong amount"

            #next step is to get this informations parsed
            #<lesson_subject id="SU_SPD"/>
            #<lesson_teacher id="TR_WICK"/>
            #<lesson_classes id="CL_2d CL_2g"/>

            #if there is no subject there is not teacher or classes so that it makes no sense to save it-->skip this "lesson"
            if not "subject" in lines[line_number+2]:
                continue
            subject = lines[line_number+2].split("\"")[1][3:]
            #subject which make not much sense --> skip this class
            if subject in ["AGICT"]:
                continue
            #exceptions by teachers
            #<lesson_teacher id="TR_stvFLUE"/>
            #<lesson_teacher id="TR_WICK TR_GERB"/>
            potential_teachers = lines[line_number+3].split("\"")[1].split(" ")
            teachers = []
            for k in potential_teachers:
                teachers.append(k[-4:])

            #<lesson_classes id="CL_2d CL_2g"/>
            potential_classes = lines[line_number+4].split("\"")[1].split(" ")
            classes = []
            for k in potential_classes:
                classes.append(k[-2:])

            moment_line = line_number+4
            while not "times" in lines[moment_line]:
                moment_line +=1

            moment_line+=1

            for k in range(amount):
                #<time>
                #<assigned_day>4</assigned_day>
                #<assigned_period>5</assigned_period>
                #<assigned_starttime>1125</assigned_starttime>
                #<assigned_endtime>1210</assigned_endtime>
                #<assigned_room id="RM_803"/>
                #</time>


                #<assigned_day>4</assigned_day>
                assert "day" in lines[moment_line+1], "something went wrong with the day"
                day =lines[moment_line+1].replace("/","").split("<assigned_day>")[1]

                #<assigned_period>5</assigned_period>
                assert "period" in lines[moment_line+2], "something went wrong with the period"

                period = lines[moment_line+2].replace("/","").split("<assigned_period>")[1]

                #<assigned_starttime>1125</assigned_starttime>
                assert "starttime" in lines[moment_line+3], "something went wrong with the starttime"
                starttime= lines[moment_line+3].replace("/","").split("<assigned_starttime>")[1]

                #<assigned_room id="RM_803"/>
                #in case there is not room (possible, dont know why)
                if not "time" in lines[moment_line+5]:

                    assert "room" in lines[moment_line+5], "something went wrong with the room"
                    #print(lines[moment_line+5],moment_line+5)
                    room = lines[moment_line+5].split("\"")[1][3:]
                else:
                    room = (None)


                for classi in classes:
                    time_table_dic[day][starttime][room].append(classi)
                for teacher in teachers:
                    time_table_dic[day][starttime][room].append(teacher)





                while not "</time>" in lines[moment_line]:
                    moment_line+=1
                moment_line+=1





    return time_table_dic

def parse_line(line, aps):

    """
    #the line of the log file
    #e.g.
    #Mon Dec 10 08:48:55 2018 [OK][OUT][lohr.nico.2013@ksz.edu-zg.ch][88-e9-fe-b2-7b-46][00-3a-99-7b-c1-f0:eduroam][172.18.0.32]
    #get the data, the users_mac (first mac) and the
    #aps is a defaultdictionary
    """
    if "FAIL" in line:
        return ("unkown","None",datetime.datetime(1970,1,1))
    if not "OK" in line:
        print(line)
        return ("wierd parsing","None",datetime.datetime(1970,1,1))
    #print(line)
    line_segments = line.split("][")
    time = get_time(line_segments[0][0:-4])

    ap_mac = line_segments[4].replace("-",":")[:16].upper()
    ap_room = aps[ap_mac]
    users_mac = line_segments[3].replace("-",":").upper()

    return (users_mac, ap_room, time)

def parse_all_data(filenames, aps):
    """
    Iter function which returns one datapoint after the another from all files
    It goes through every file and every line of the file and creates for every line one tuplin
    e.g.
    (88-e9-fe-b2-7b-46, 347, datetime.datetime(2019,4,2,23,32))
    it puts a dummy tuplin each time the file changes to restart the lessons
    """

    for i in filenames:

        with open(i, encoding="utf-8") as f:

            for line in f.readlines():

                yield parse_line(line,aps)

def get_files(folder):
    """
    get a list of all the files in a folder
    e.g get_files("Data")
    returns a list [2019-Dec-23-access.log, ...]
    """
    files=[]
    for (dirpath, dirnames, filenames) in os.walk(folder):

        for k in filenames:
            #checks if it is a log file or another file (e.g. accespoint)
            if not "201" in k:
                continue
            #add the filepath to self.files
            files.append(folder+"/"+k)
        return files

def filter_mac(t):
    """
    basic filter
    compares user_mac (global, string) to first (0) elemtent of input

    """
    global user_mac
    #it uses dummy when the day changes
    return t[0]==user_mac

def filter_mac_all(t):
    """
    a filter which doesnt give a false back
    """
    return True

def fit_to_lesson(filenames,aps,time_table_dic,filter_function=filter_mac):
    """
    This class goes through every lesson on every day and collects the classes that maybe visited
    Input: filenames of the datapoints(list), dictionary of the aps (dictionary),optional the filename of the timetable (standard is save9.gpn), optional filter_function (standard is filter_mac)
    Output: A list with n elements (n = 8 (lessons per day) * amount of days), Every element in the list contains the class most fitting at this time
    It goes through every datapoint and checks if it is in a certain lesson and then checks if the data and fits to a certain class
    """

    last = collections.defaultdict(lambda:(1230,123,(datetime.datetime(2020,2,3))))
    lessons = [["0740","0825"],["0835","0920"],["0930","1015"],["1030","1115"],["1125","1210"],["1220","1305"],["1315","1400"],["1410","1455"],["1505","1550"],["1600","1645"]]
    lessons = [["0755","0840"],["0850","0935"],["0945","1030"],["1045","1130"],["1140","1225"],["1235","1320"],["1330","1415"],["1425","1510"],["1520","1605"],["1615","1700"],["1700","1745"]]
    
    classes=collections.defaultdict(lambda: [])

    #m = filter(filter_mac,parse_all_data(filenames,aps)))
    #go through every day
    m = list(filter(filter_function,parse_all_data(filenames,aps)))
    lessons_visited=collections.defaultdict(lambda: [])
    #print("jetzt")
    day = 0
    for roomsystem in m:
        #every lesson on this day
        #changes
        
        if roomsystem[2].day!=day:
            lessons_visited=collections.defaultdict(lambda: [])

        day = roomsystem[2].day
        for  lesson in lessons:
            #go through all the data at this day
            if lesson in lessons_visited[roomsystem[0]]:
                continue
            time = roomsystem[2].hour*100+roomsystem[2].minute
            #for roomnumber in range(len(self.rooms_visited)):

            #check if time is after the start of the lesson but still before the end
            if time >= int(lesson[0]):
                if time<=int(lesson[1]):
                    #check if this room is used during this lesson and by which class

                    #classes[roomsystem[0]].append(check_for_class(roomsystem[1],roomsystem[2].weekday()+1,lesson[0],data_tt))
                    #(room,day,time,data_tt)

                    #print(roomsystem,lesson)
                    if roomsystem[1] == None:
                        continue

                    classes[roomsystem[0]].append(time_table_dic[str(roomsystem[2].weekday()+1)][lesson[0]][roomsystem[1]])
                    lessons_visited[roomsystem[0]].append(lesson)


                elif last[roomsystem[0]][2].hour*100+last[roomsystem[0]][2].minute> int(lesson[0])-10:
                    #check if last room is used during this lesson
                    #ww = check_for_class(last[roomsystem[0]][1],last[roomsystem[0]][2].weekday()+1,lesson[0],data_tt)
                    if last[roomsystem[0]][1] == None:
                        continue
                    ww = time_table_dic[str(last[roomsystem[0]][2].weekday()+1)][lesson[0]][last[roomsystem[0]][1]]

                    classes[roomsystem[0]].append(ww)
                    lessons_visited[roomsystem[0]].append(lesson)

        last[roomsystem[0]] = list(roomsystem)


    return classes

def list_to_percent(classes):
    """
    Input: List of classes e.g. [["5H","GERB"],["5H","EWER"],["3R", "ZINK"],["5H", "KELL"],[],["6A","6B","KELL","ZUER"],["5H","STAJ"]]
    It counts how many of each element exist in the list
    Output: dictionary with every class or teacher as keys and amount as number e.g. {"KELL":2,"6A":1,"6B":1,"5H":4,"STAJ":1,"EWER":1,"ZINK":1,"ZUER":1,"3R":1,"5H":"GERB"}

    """
    dic = collections.defaultdict(lambda: 0)
    #go through all the classes visited
    for classe in classes:
        for person in classe:
            dic[person]+=1
    return dic

def track_mac(mac,filenames,aps,time_table_dic):
    """
    It trackes a certain mac address over the day the filenames go (every day one file)
    It runs "fit_to_lesson" and with this result it runs "list_to_percent"
    It returns the key with the maximume value of the dictionary resultat from "list_to_percent"
    Input: mac of device, filenames of Data, dictionary of aps, optional filename of timetable (filename_tt)
    """
    classes=fit_to_lesson(filenames,aps,time_table_dic)


    dic = list_to_percent(classes[user_mac])
    
    #if the mac descovert a class or a teacher it returns the most likely one
    #that means it returns the class or teche which has the highest value in the dictionary

    if len(dic)!=0:
        return max(dic, key=dic.get), dic[max(dic, key=dic.get)]
    #if there is nothing in the dictionary it returns:
    return "unknown", 0

def reverse_tracking(filenames,aps,time_table_dic,filename_tt="save9.gpn"):
    """
    Reverse tracking tracks every mac addresse. That means there is no filter by the data and all the data are getting searched through
    It runs "fit_to_lesson" without a filter and with this result it runs "list_to_percent"
    It returns a defaultdictionary with every mac and its coresponds class and amount of hits
    """
    classes=fit_to_lesson(filenames,aps,time_table_dic,filter_function=filter_mac_all)

    solution={}
    for k in classes:
        
        dic = list_to_percent(classes[k])
        if len(dic)!=0:
            #print(dic)
            solution[k]=(max(dic, key=dic.get), dic[max(dic, key=dic.get)])
        #if there is nothing in the dictionary it adds unknown
        else:
            solution[k]=( "unknown", 0)
    return solution

def multi_fit_to_lesson(liste):
    global aps, time_table_dic
    solution={}
    classes = fit_to_lesson(liste,aps,time_table_dic,filter_function=filter_mac_all)
    for k in classes:
        dic = list_to_percent(classes[k])
        if len(dic)!=0:
            solution[k]=(max(dic, key=dic.get), dic[max(dic, key=dic.get)])
        #if there is nothing in the dictionary it adds unknown
        else:
            solution[k]=( "unknown", 0)
    return solution

def multi_track(filenames, aps, time_table_dic, pooli):
    processes = []
    fil = len(filenames)
    for k in range(1,1+pooli):
        processes.append(filenames[int((k-1)/pooli*fil):int((k)/pooli*fil)])
    print(len(processes))
    p = Pool(pooli)
    print("HH")
    return p.map(multi_fit_to_lesson,processes)

if __name__ == "__main__":

    user_mac = "88:E9:FE:B2:7B:46"
    print(track_mac(user_mac))
