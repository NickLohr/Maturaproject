import time
timer = time.time()
import tools as tools
import datetime
import collections
import tqdm

AP_FILE_PATH_TYPE1 = "Data/access_points.log"
AP_FILE_PATH_TYPE2 = "Data/access_points2a.log"
TIME_TABLE_PATH = "save9.gpn"
DATA_DIRECTORY_PATH = "Data"

mac = "58-48-22-A4-99-86".upper().replace("-",":")


lessontime = [["0740","0825"],["0835","0920"],["0930","1015"],["1030","1115"],["1125","1210"],["1220","1305"],["1315","1400"],["1410","1455"],["1505","1550"],["1600","1645"],["1650","1735"]]


tools.files = tools.get_files(DATA_DIRECTORY_PATH)

# read AP database containing AP MAC and location
tools.aps=collections.defaultdict(lambda: None)
tools.aps.update(tools.read_ap_database_type1(AP_FILE_PATH_TYPE1))
tools.aps.update(tools.read_ap_database_type2(AP_FILE_PATH_TYPE2))

tools.time_table_dic = tools.parse_time_table(TIME_TABLE_PATH)

time_table_knn = collections.defaultdict(lambda: collections.defaultdict(lambda: []))

for day in tools.time_table_dic:
    for lesson in tools.time_table_dic[day]:
        for room in tools.time_table_dic[day][lesson]:
            classes = tools.time_table_dic[day][lesson][room]
            for class_ in set(classes):
                
                if room is None or room == "div.":
                    continue
                if len(class_) != 2 or class_ in ["v."]:
                    continue
                time_table_knn[class_][day] += [int(lesson)]

assert time_table_knn["5H"]["1"]

def datetimetostring(time):

    return time.hour*100+time.minute
def stringtodatetime(time,timing):
    return datetime.datetime(timing.year,timing.month,timing.day,int(time[:2]),int(time[2:]))
                                       



def timeduringlesson(time,lessons, delta = datetime.timedelta(minutes= 0)):
    for lesson in lessons:
        startend = lessontime[int(lesson)-1]
        start = stringtodatetime(startend[0],time)
        end = stringtodatetime(startend[1],time)
        if time-delta>start and time+delta<end:
            return True
                                       
    return False

def check(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day])):
        return -100
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)

                                       
                                       
    if time+datetime.timedelta(minutes=15)>timestart:
        return -1
    if time-datetime.timedelta(minutes=15)<timeend:
        return -1

    return 0

def reparse_data():
    DataDic = collections.defaultdict(lambda: [])
    print("start parsing")
    data = list(filter(lambda x: x[1] == "5XX" and x[0] == mac, tools.parse_all_data(tools.files,tools.aps)))
    print("start reparsing")
    for m in data:
        user_mac = m[0]
        time = m[2]
        DataDic[user_mac]+=[time]
    print("Done reparsing")
    return DataDic
DataDic = reparse_data()


#takes every datapoint
def KNN1(check = check):
    counter = 0
    CM = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    pbar = tqdm.tqdm(total=len(time_table_knn))
    for class_ in time_table_knn:
        for mac in DataDic:
            for time in DataDic[mac]:
               
                error = check(time,class_)
                CM[class_][mac] +=error
                counter+=1
                
        pbar.update(1)

    print(counter)
    pbar.close()
    return CM, counter





#takes first datapoint of the day
def KNN2(check = check):
    counter = 0
    CM = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    pbar = tqdm.tqdm(total=len(time_table_knn))
    for class_ in time_table_knn:
        
        for mac in DataDic:
            day = datetime.datetime(2017,1,1)
            for time in sorted(DataDic[mac]):
                if day.day!=time.day:
                    day = time
                    counter+=1
                
                    error = check(time,class_)
                    CM[class_][mac] +=error
        pbar.update(1)
        
    print(counter)
    pbar.close()
                
    return CM,counter

#last one 
def KNN3(check = check):
    counter = 0
    CM = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    pbar = tqdm.tqdm(total=len(time_table_knn))
    for class_ in time_table_knn:
        
        for mac in DataDic:
            #print(min(DataDic[mac]),max(DataDic[mac])
            day = datetime.datetime(2017,1,1)
            prevtime = datetime.datetime(2017,1,1)
            for time in sorted(DataDic[mac]):
                if day.day!=time.day:
                    if prevtime == datetime.datetime(2017,1,1):
                        prevtime = time
                        continue
                    day = time
                    counter+=1

                    error = check(prevtime,class_)
                    CM[class_][mac] +=error
                prevtime = time
            #for the last day:
            counter+=1
            error = check(prevtime,class_)
            CM[class_][mac] +=error
        pbar.update(1)
    print(counter)
    pbar.close()
                
    return CM, counter

def check2(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day])):
        return -5
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)
    if time+datetime.timedelta(minutes=15)>timestart:
        return -1
    if time-datetime.timedelta(minutes=15)<timeend:
        return -1
    
    return 0

def check3(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day])):
        return -1
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)
    if time+datetime.timedelta(minutes=15)>timestart:
        return 0
    if time-datetime.timedelta(minutes=15)<timeend:
        return 0
    
    return 0


def check4(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day]),delta = datetime.timedelta(minutes= 5)):
        return -1
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)
    if time+datetime.timedelta(minutes=15)>timestart:
        return 0
    if time-datetime.timedelta(minutes=15)<timeend:
        return 0
    
    return 0
def check5(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day]),delta = datetime.timedelta(minutes= 5)):
        return -5
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)
    if time+datetime.timedelta(minutes=15)>timestart:
        return -1
    if time-datetime.timedelta(minutes=15)<timeend:
        return -1
    
    return 0
def check6(time,class_):

    day = str(time.weekday()+1)

    if day == "0":
        print("reverse the +1")
    if int(day)>5:
        return 0        
    if time_table_knn[class_][day]==[]:#possible for 6C because they have the wednesday morning off and in the afternoon just EF
        return 0
    firstlesson = int(sorted(time_table_knn[class_][day])[0])
    lastlesson = int(sorted(time_table_knn[class_][day])[-1])
                   
    if timeduringlesson(time,set(time_table_knn[class_][day]),delta = datetime.timedelta(minutes= 5)):
        return -1
    if firstlesson == 0:
        print("reverse -1")
    timestart = stringtodatetime(lessontime[firstlesson-1][0],time)
    timeend = stringtodatetime(lessontime[lastlesson-1][1],time)
    if time-datetime.timedelta(minutes=15)>timestart:
        return 0
    if time-datetime.timedelta(minutes=15)<timeend:
        return 0
    
    return 0


#takes every datapoint
def KNN4(check = check):
    counter = 0
    CM = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    pbar = tqdm.tqdm(total=len(time_table_knn))
    for class_ in time_table_knn:
        for mac in DataDic:
            for time in DataDic[mac]:
                if time.weekday()==4:
                    error = check(time,class_)
                    CM[class_][mac] +=error
                    counter+=1
                
        pbar.update(1)

    print(counter)
    pbar.close()
    return CM, counter
KNNS = [KNN1,KNN2,KNN3,KNN4]
checks = [check,check2,check3,check4,check5,check6]
results = [[0 for __ in checks] for _ in KNNS]
print(results)
for knnN in range(len(KNNS)):
    knn = KNNS[knnN]
    for checkN in range(len(checks)):
        checki = checks[checkN]
        m,c = knn(check = checki)
        print(c)
        results[knnN][checkN]= [(m[xx][mac],xx) for xx in m]
for n in range(len(results)):
    for o in range(len(checks)):
        mini = min(results[n][o])
        if mini[0]==0:
            mini = (1,)
        results[n][o] = sorted([(results[n][o][xx][0]/mini[0],results[n][o][xx][1]) for xx in range(len(results[n][o]))])
               
delta = collections.defaultdict(lambda: 0)
for n in results:
    for o in n:
        for m in o:
            delta[m[1]] += m[0]**2


print(time.time()-timer)
a = sorted([(delta[m],m) for m in delta])
for n in results:
    for o in n:
        q = sorted(o)
        for p in range(len(o)):
            if q[p][1]=="5H":
                print(p,q[p][0])
for m in range(len(a)):
    if a[m][1]=="5H":
        print(m, a[m][0])



##T3st 3x4mpl35
#m["5H"]["88:E9:FE:B2:7B:46"]
#a = [(m[xx]["88:E9:FE:B2:7B:46"],xx) for xx in m]
"""
qq = [a,b,c,d,e,f]
for r in qq:
    p = sorted(r)
    print(p[:4])

0.4772 5H 0.378


for m in results:
    for i in m:
	print(i[0:4])


a = sorted([(delta[m],m) for m in delta])
"""
