

file = "testfile.log"
database_of_my_logs=[]
with open(file) as x:
    line = x.readline()
    line.split(" ")
    element=[0,"",""]  # [time, mac_of_device, mac_of_access_point]
    if line[3]=="[my_mac-address]": #change index
        element[0]=line[0] #change index
        element[1]=line[3] #change index
        element[2]=line[4] #change index
        database_of_my_logs+=[element]
        

