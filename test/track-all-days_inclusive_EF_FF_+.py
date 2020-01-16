from tracking_v4b import *
import datetime
from os import walk
from random import *
data_to_accesspointsdir2()
data_to_accesspointsdir1()
f = []
for (dirpath, dirnames, filenames) in walk("Data"):
    for k in filenames:
        if "points" in k:
            continue
        f.append(k[:-11])
    break


#every lesson from 2018-2019
lessons = [["0740","0825"],["0835","0920"],["0930","1015"],["1030","1115"],["1125","1210"],["1220","1305"],["1315","1400"],["1410","1455"],["1505","1550"],["1600","1645"]]
maccc = str(input("Which mac-address to class?")).upper()

#88-e9-fe-b2-7b-46
#C4-9D-ED-AA-8C-29
##<assigned_starttime>1505</assigned_starttime>
##<assigned_endtime>1550</assigned_endtime>
##<assigned_room id="RM_342"/>
#converts the short terms from the month to the number
def sl_to_num(num):
    dictt={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"Nov":11,"Dec":12}
    return dictt[num]
#converts the date to the weekday
def get_weekday(date):
    mmm = date.split("-")
    year = int(mmm[0])
    month = sl_to_num(mmm[1])
    day = int (mmm[2])
    return str(datetime.date(year,month,day).weekday()+1)
#takes the list of the potential lessons visited and returns the class most common
dic = {}
dicte={}
total = 0
def list_to_per(liste):
    global total
    global dic
    global dicte
    #go thourgh every lesson and add the class to the dictionary
    for k in liste:
        if k==[]:
            continue

        total+=1
     
        if len(k[0][0])==2:
            if k[0][0] in dic.keys():
                dic[k[0][0]]+=1
            else:
                dic[k[0][0]]=1
        else:
            if len(k[0][0])==3:
                p1 = k[0][0][0:2]
                p2 = k[0][0][0]+k[0][0][2]
                if p1 in dic.keys():
                    dic[p1]+=1
                else:
                    dic[p1] =1
                if p2 in dic.keys():
                    dic[p2]+=1
                else:
                    dic[p2]=1
            elif "ff" in k[0][0]:
                total-=1
                print("FF", k[0][0])
                continue
            elif "ef" in k[0][0]:
                print("ef", k[0][0])
                total-=1
                continue
            else:
                print(k[0][0])
            if "b" in k[0][0]:
                print("bi")
 

        
        if len(k[0])>=2 and len(k[0][1])==4:
            if k[0][1] in dicte.keys():
                dicte[k[0][1]]+=1
            else:
                dicte[k[0][1]]=1
        else:
            if len(k[0])>=2 and len(k[0][1])>6:
                p1 = k[0][1][0:4]
                p2 = k[0][1][5:9]
                
                if p1 in dicte.keys():
                    dicte[p1]+=1
                else:
                    dicte[p1] =1
                if p2 in dicte.keys():
                    dicte[p2]+=1
                else:
                    dicte[p2]=1
    if total==0:
        return {}

    
    return dic#+ " to " + str(dic[max(dic, key=dic.get)]/total*100)+"%" )
#this def takes the room visited at a certain time at a day and find out to which class it fits on the time table
def check_for_class(room,day,time):
    print(room)
    lll=[]
    #time table
    file = open("save9.gpn")
    data = file.readlines()
    last = 0
    #go through the timetable
    for m in range(len(data)):
        if "<text>" in data[m]:
            
            last = m
        #check if the time day and room fits to the lesson?
        if m+3<len(data) and '<assigned_day>'+day+'</assigned_day>' in data[m-2] and time in data[m] and str(room) in data[m+2]:
            if "-" in data[last]:
                lll+=[[data[last].split("-")[1],data[last].split("-")[2][:-8]]]
            else:
                lll+=[[data[last]]]
    return lll
#which datapoint fits into the lesson
def vis_time(lesson):
    #goes through all the rooms (access-points) visited 
    for p in range(len(rooms_visited)):
        #get the the time and place 
        k=rooms_visited[p]
        time = str(k[1])
        #check if the time is after lesson start
        if int(time)>=int(lesson[0]):
            #check if there is a data-point during the lesson
            if int(time)<=int(lesson[1]):
                #take the data-point during the lesson and check which class it fits to
                return check_for_class(rooms_visited[p][0],get_weekday(ddaattee),lesson[0])
            else:
                #if the datapoint is after the lesson take the one before
                if int(rooms_visited[p-1][1])> int(lesson[0])-10:
                    return check_for_class(rooms_visited[p-1][0],get_weekday(ddaattee),lesson[0])
    #if it doesn't find any during or before the lesson then return []
    return []

mml=[]
dici={}
for k in f:
    

    ddaattee = k

    rooms_visited = get_rooms(maccc, ddaattee)
    if rooms_visited!=[] and 2 == 1:
        print(rooms_visited)
        print("tracking on the " + ddaattee)
    mm = []
    for i in lessons:
        mm+=[vis_time(i)]
    
    
    #mml+=[list_to_per(mm)]
    dici.update(list_to_per(mm))
print(dic)

print(dicte)
print("If student")
print(max(dic, key=dic.get))
print(str(dic[max(dic, key=dic.get)]/total*100)+"%" )

print("If teacher")
print(max(dicte, key=dicte.get))
print(str(dicte[max(dicte, key=dicte.get)]/total*100)+"%" )
