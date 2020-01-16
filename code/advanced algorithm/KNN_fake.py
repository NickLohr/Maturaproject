##I am having all the data [arival and leaving time] in an array
##This ten dimensional data cloud can be seperated by class
##By this I take the distance from the average classmember
##I get the "centroids" from the time table.


##The squard of something small get smaller -> not use the varianz method
##Use the default data

#import numpy as np
#X = np.load("datatouseaa6.npy")
#print(len(X))

##Centroid
##Has to be every class once
##I get this data later from the time-table
import random
import matplotlib.pyplot as plt
s1= [7*60+36,15*60-3]
s2= [7*60+33,15*60+3]
s3= [7*60+31,15*60+10]


s4= [7*60+40,16*60-6]
s5= [7*60+23,16*60-7]
s6= [7*60+34,16*60-1]
s7= [7*60+30,16*60+12]


s8= [8*60+21,15*60+13]
s9= [8*60+26,15*60-6]
s10= [8*60+6,15*60+1]
s11= [8*60+18,15*60-2]

ws =[random.randint(100,400),random.randint(300,900)]
ws2 = [random.randint(100,400),random.randint(300,900)]
ws3 = [random.randint(100,400),random.randint(300,900)]

X = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,ws,ws2,ws3]






def timetonumber(time):
    
    a = time[1]
    timer= []
    for o in range(len(a)):
        if o == 5 and "6" in time[0]:
            m = 9
        elif a[o] == "a":
            m = 10
        elif a[o] == "b":
            m =11
        elif a[o] == "z":
            m = 5
        elif a[o] == "y":
            m = 9
        else:
            m = int(a[o])
        if o%2 ==0:
            m+=1
        ini = 7*60+36
        for p in range(m): ##Always a lesson and ten minutes later
            ini+=55
        timer.append(ini)
    return timer+[0,0,0,0] #Samstag und Sonntag

def KNN(Y):
    indextodistance={}

    #KNN
    for m in range(len(X)):

        array = X[m]
        distance = 0
        #calculates the sum of delta Y squared
        #Which is equals to the distance squared (multidimensional pytogaras)
        for i in range(len(array)):
            value = array[i]
            distance+= (value-Y[i])**2
        #save the distance 
        indextodistance[m] = distance

    items = indextodistance.items()
    so = sorted(items, key=lambda x: x[1])
    return so



classing = {}

#Centroids = [('6L', '141924293a'), ('6G', '1518252838'), ('6H', '1519252a37'), ('6J', '1529152838'), ('3B', '1529291a19'), ('6E', '1818242935'), ('6B', '1818251835'), ('6A', '1818352935'), ('2j', '181915192a'), ('4J', '1819181918'), ('5H', '18191a193a'), ('3H', '182a151918'), ('1f', '182a15191a'), ('4B', '191818182a'), ('4E', '19182a2a39'), ('1a', '1919151819'), ('1h', '1919151819'), ('2d', '1919151919'), ('3C', '1919151919'), ('3E', '1919151919'), ('1j', '1919151919'), ('2e', '191915192a'), ('2h', '191915292a'), ('1b', '1919152a18'), ('5D', '191918182a'), ('4D', '1919181a29'), ('5K', '19191a1829'), ('4K', '19191a2939'), ('5C', '19193a1a29'), ('2n', '191a151a18'), ('2c', '1929151919'), ('3F', '1929151919'), ('3A', '1929152a18'), ('3G', '19292a151a'), ('2g', '192a151919'), ('2m', '192a152a19'), ('1e', '192a152a19'), ('1m', '192a152a19'), ('4C', '192a192a29'), ('5E', '1a19182919'), ('5B', '1a191a1819'), ('6C', '1a19zy1938'), ('1k', '1a2a15192a'), ('5T', '1a2a182a18'), ('6F', '2818151439'), ('6K', '2829251539'), ('6S', '28292b2918'), ('3D', '2919151929'), ('4A', '2919181818'), ('4G', '2919182a18'), ('5L', '29292a181a'), ('4H', '29292a2a19'), ('2a', '2a1815192a'), ('5G', '2a18181a19'), ('1c', '2a1915182a'), ('1d', '2a19151919'), ('1n', '2a19151919'), ('3J', '2a19152a18'), ('2k', '2a19152a19'), ('5J', '2a19191818'), ('5A', '2a192a1a2a'), ('2b', '2a1a151819'), ('5F', '2a29181a19'), ('5S', '2a291a1818'), ('4S', '2a291a1a29'), ('4T', '2a29281819'), ('1g', '2a2a15182a'), ('2f', '2a2a151919'), ('4F', '3a282a2a19'), ('6D', '3a39251439')]
Centroids = [("Klasse 1",[450,900])]
for Y in Centroids:
    so = KNN(Y[1])
    classing[Y[0]] = so



for a in range(len(X)):
    x = X[a][0]
    y = X[a][1]
    plt.scatter(x,y)
    plt.text(x+0.3, y+0.3, a+1, fontsize=9)
    
plt.xlabel("Time of Arrival (minutes after midnight)")
plt.ylabel("Time of Leaving (minutes after midnight)")
plt.show()
