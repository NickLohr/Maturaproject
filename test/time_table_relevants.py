import time
timer = time.time()
import tools as tools
import datetime
import collections

AP_FILE_PATH_TYPE1 = "Data/access_points.log"
AP_FILE_PATH_TYPE2 = "Data/access_points2a.log"
TIME_TABLE_PATH = "Stundenplan.xml"
DATA_DIRECTORY_PATH = "Data"

mac = "58-48-22-A4-99-86".upper().replace("-",":")


lessontime = [["0740","0825"],["0835","0920"],["0930","1015"],["1030","1115"],["1125","1210"],["1220","1305"],["1315","1400"],["1410","1455"],["1505","1550"],["1600","1645"],["1650","1735"]]
lessontime2 = [["0755","0840"],["0850","0935"],["0945","1030"],["1045","1130"],["1140","1225"],["1235","1320"],["1330","1415"],["1425","1510"],["1520","1605"],["1615","1700"],["1700","1745"]]


tools.files = tools.get_files(DATA_DIRECTORY_PATH)

# read AP database containing AP MAC and location
tools.aps=collections.defaultdict(lambda: None)
tools.aps.update(tools.read_ap_database_type1(AP_FILE_PATH_TYPE1))
tools.aps.update(tools.read_ap_database_type2(AP_FILE_PATH_TYPE2))

tools.time_table_dic = tools.parse_time_table(TIME_TABLE_PATH)

time_table = collections.defaultdict(lambda: collections.defaultdict(lambda: []))

for day in tools.time_table_dic:
    for lesson in tools.time_table_dic[day]:
        for room in tools.time_table_dic[day][lesson]:
            classes = tools.time_table_dic[day][lesson][room]
            for class_ in set(classes):
                
                if room is None or room == "div.":
                    continue
                if len(class_) != 2 or class_ in ["v."]:
                    continue
                time_table[class_][day] += [int(lesson)]

first = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
last = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
for class_ in time_table:
    for day in time_table[class_]:
        a = sorted(time_table[class_][day])
        if a[0] == 7:
            print(class_,day,a)
        first[day][a[0]]+=1
        last[day][a[-1]]+=1


for m in first:
    for k in first[m]:
        print(m,k,first[m][k])

print()
        
for m in last:
    for k in last[m]:
        print(m,k,last[m][k])
                                

                                
                   
                

