##I am having all the data [arival and leaving time] in an array
##This ten dimensional data cloud can be seperated by class
##By this I take the distance from the average classmember
##I get the "centroids" from the time table.


##The squard of something small get smaller -> not use the varianz method
##Use the default data

import numpy as np
X = np.load("datatouseaa_mean2.npy")
print(len(X))

##Centroid
##Has to be every class once
##I get this data later from the time-table


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

Centroids = [('6L', '141924291a'), ('6G', '1518252818'), ('6H', '1519252a17'), ('6J', '1529152818'), ('3B', '1529291a19'), ('6E', '1818242915'), ('6B', '1818251815'), ('6A', '1818352915'), ('2j', '181915192a'), ('4J', '1819181918'), ('5H', '18191a193a'), ('3H', '182a151918'), ('1f', '182a15191a'), ('4B', '191818182a'), ('4E', '19182a2a39'), ('1a', '1919151819'), ('1h', '1919151819'), ('2d', '1919151919'), ('3C', '1919151919'), ('3E', '1919151919'), ('1j', '1919151919'), ('2e', '191915192a'), ('2h', '191915292a'), ('1b', '1919152a18'), ('5D', '191918182a'), ('4D', '1919181a29'), ('5K', '19191a1829'), ('4K', '19191a2939'), ('5C', '19193a1a29'), ('2n', '191a151a18'), ('2c', '1929151919'), ('3F', '1929151919'), ('3A', '1929152a18'), ('3G', '19292a151a'), ('2g', '192a151919'), ('2m', '192a152a19'), ('1e', '192a152a19'), ('1m', '192a152a19'), ('4C', '192a192a29'), ('5E', '1a19182919'), ('5B', '1a191a1819'), ('6C', '1a19zy1918'), ('1k', '1a2a15192a'), ('5T', '1a2a182a18'), ('6F', '2818151419'), ('6K', '2829251519'), ('6S', '28292b2918'), ('3D', '2919151929'), ('4A', '2919181818'), ('4G', '2919182a18'), ('5L', '29292a181a'), ('4H', '29292a2a19'), ('2a', '2a1815192a'), ('5G', '2a18181a19'), ('1c', '2a1915182a'), ('1d', '2a19151919'), ('1n', '2a19151919'), ('3J', '2a19152a18'), ('2k', '2a19152a19'), ('5J', '2a19191818'), ('5A', '2a192a1a2a'), ('2b', '2a1a151819'), ('5F', '2a29181a19'), ('5S', '2a291a1818'), ('4S', '2a291a1a29'), ('4T', '2a29281819'), ('1g', '2a2a15182a'), ('2f', '2a2a151919'), ('4F', '3a282a2a19'), ('6D', '3a39251419')]
for Y in Centroids:
    so = KNN(timetonumber(Y))
    classing[Y[0]] = so
