
##code so far programmed nicely changed and listed
import os
import datetime
import collections
import json
import unicodedata

#All code is bad: Read in https://gizmodo.com/programming-sucks-why-a-job-in-coding-is-absolute-hell-1570227192
"""
All the tools one need to track one or several macs with the log-rfvbnhztrdata from the IT department
"""
user_mac = ""

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
    months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Mai":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    year = int(time[4])
    month = months[time[1]]
    day = int(time[2])
    hour = int(time[3][0:2])
    minute = int(time[3][3:5])
    sec = int(time[3][6:8])
    #print(year,month,day,hour,minute,sec)
    a = datetime.datetime(year,month,day,hour,minute,sec)
    return a



def parse_line(line):
    
    """
    #the line of the log file
    #e.g.
    #Mon Dec 10 08:48:55 2018 [OK][OUT][lohr.nico.2013@ksz.edu-zg.ch][88-e9-fe-b2-7b-46][00-3a-99-7b-c1-f0:eduroam][172.18.0.32]
    #get the data, the users_mac (first mac) and the
    #aps is a defaultdictionary
    """
    if "FAIL" in line:
        return ("unkown","wrong name")
    if not "OK" in line:
        print(line)
        return ("wierd parsing","wrong username")
    line_segments = line.split("][")
    if "kamb.jani.2016@ksz.edu-z" in line_segments[0][0:-4]:
        print(line)
    time = get_time(line_segments[0][0:-4])
    #ap_mac = line_segments[4].replace("-",":")[:16].upper()
    if len(line_segments)<4:
        print(line_segments)
    users_mac = line_segments[3].replace("-",":").upper()
    #print(line_segments)
    username = line_segments[2].split("@")[0]
    username = unicodedata.normalize('NFD', username).encode('ascii', 'ignore').decode("utf-8")
    return (users_mac, username)

def parse_all_data(filenames):
    """
    Iter function which returns one datapoint after the another from all files
    It goes through every file and every line of the file and creates for every line one tuplin
    e.g.
    (88-e9-fe-b2-7b-46, 347, datetime.datetime(2019,4,2,23,32))
    it puts a dummy tuplin each time the file changes to restart the lessons
    """
    for i in filenames:
        print(i)
        with open(i, encoding="utf-8") as f:

            for line in f.readlines():
                yield parse_line(line)



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





if __name__ == "__main__":
    user_mac = "88:E9:FE:B2:7B:46"
    o = list(parse_all_data(get_files("../../Data/Data from the IT-Department(Nov-Dec)/")))
    print(len(o))
    oo = collections.defaultdict(lambda:collections.defaultdict(list))
    oq = {}
    for m in o:
        oq[m[0].upper()] = m[1]
    
    print(oq["88:E9:FE:B2:7B:46"])
    with open("./usernames2.txt","w") as f:
        json.dump(oq,f)
    
    print("DOne")
