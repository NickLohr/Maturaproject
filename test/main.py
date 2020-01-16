import time
tt = time.time()

#All code is bad: Read in https://gizmodo.com/programming-sucks-why-a-job-in-coding-is-absolute-hell-1570227192


import collections
import toolsv3_multi as tools
import multiprocessing
#https://www.python.org/dev/peps/pep-0257/

AP_FILE_PATH_TYPE1 = "Data/access_points.log"
AP_FILE_PATH_TYPE2 = "Data/access_points2a.log"
DATA_DIRECTORY_PATH = "Data"

#set the target user mac in the right format e.g '88:E9:FE:B2:7B:46'
tools.user_mac = "64:a2:f9:29:5d:46".replace("-",":").upper()


# read AP database containing AP MAC and location
tools.aps=collections.defaultdict(lambda: None)
tools.aps.update(tools.read_ap_database_type1(AP_FILE_PATH_TYPE1))
tools.aps.update(tools.read_ap_database_type2(AP_FILE_PATH_TYPE2))
# ap now contains {"XX:XX:XX:XX:XX:XX":"102", ...}

#get all the
tools.files = tools.get_files(DATA_DIRECTORY_PATH)
#files now contains ["2018-Dec-01-access.log","2018-Dec-02-access.log"...]

tools.time_table_dic = tools.parse_time_table("save9.gpn")


#trackes the tools.user_mac in the files from DATA_DIRECTORY_PATH with thr APs
#running time ~30 sec

result = tools.reverse_tracking(tools.user_mac,tools.files,tools.aps,tools.time_table_dic)

print(result)
print(time.time()-tt)
tt = time.time()
#result looks like ("3A",124)

#track all mac addresses in the files again with the APs
#it returns a dictionary with all the results {"88:E9:FE:B2:7B:46":(5H,129),...}
#running time is about 12 hours
#solution = tools.reverse_tracking(files,aps,time_table_dic)
#print(solution[tools.user_mac], len(solution))
"""
for multiprocessing
if __name__ == "__main__":
    s = tools.multi_track(tools.files,tools.aps,tools.time_table_dic,5)
    print(len(s))
    print(s[4]["88:E9:FE:B2:7B:46"])

"""
print(time.time()-tt)
