from readindata import *
dicl={0:"0735",1:"0830",2:"0925",3:"1020",4:"1120",5:"1215",6:"1310",7:"1405",8:"1500",9:"1555",10:"1650",11:"1740"}

d={}
lesson = 0

def setup():
    data_tt()
    data_to_accesspointsdir2()
    data_to_accesspointsdir1()
    data_data()
def newlesson(t):
    global lesson
    if lesson%11> int(t[0]):
        return False
    return int(dicl[lesson%11])<=int(t[1:])

def start():
    global lesson
    for o in data:

        if newlesson(str(o[2])):
            lesson+=1

        for m in range(len(tt[lesson][0])):
            if o[0] == tt[lesson][1][m]:
                if o[1] in d.keys():
                    #print(o[1])
                    d[o[1]]+=[tt[lesson][0][m]]
                else:
                    d[o[1]] = [tt[lesson][0][m]]
  
print("Start preparing")
setup()
print("End preparing")
print("start calculating")
start()
print("Done")
