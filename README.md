# Maturaarbeit

##Idea behind the project
The goal of my project was to capture Wi-Fi metadata and use Big Data algorithms for it to find out information about each student.

##Steps to use it
###Preparation
Install Python
Install the repositories (repositories.txt)
Having a device that supports monitor mode
###Collect data
To be able to collect data, you need a device that you can leave at one place to sniff data and supports monitor mode. I used the WIFI-pineapple tetra, which has two built-in Wi-Fi cards to sniff data on two channels at the same time (2.4GHz and 5GHz).
With the Wi-Fi pineapple, it is recommended to use an external storage device to save all the captured packets.

Depending on the device one uses, there are different scripts in the "Code/collect data" folder. I will go on with the WIFI-pineapple because this is the best way (in my opinion) to do so.
There are also options for the Ngup and the software aircrack-ng.

For the WIFI-pineapple, after the initial setup, one should connect to over SSH. 
If you connect via the Wi-Fi that the pineapple provides, that it is necessary to paste the WiFi-pineapple.txt file content into a run.sh file on the pineapple over the terminal. 
This is necessary because the script turns off the Wi-Fi you use.

Depending on the USB stick, it needs to be first formated. Be aware that this will delete all the data on the external drive.
The code to do that is provided in the same folder with the name "formatdrive.txt".

If you choose not to use an external drive (local storage is available on the Wi-FI pineapple, but it is constrained), there is also a script ("extractdata.txt"), which provides the code to extract the data from the pineapple to the primary device.

If the possibility is there, that the pineapple my be plugged out, it helps to have the sniffing script in autostart. This helps not to lose all the files when the pineapple loses power for a short time, but there will not be a Wi-Fi from the pineapple to connect to the pineapple. One can still connect via cable to the pineapple, but it may be a little harder.

When using a USB, it is possible to unplug the USB-stick as soon as you believe in having enough data.

###First look at the data (optional)
I always took a look at my data before running the code. I used Wireshark to open the .pcap files. 
For me, the most exciting part was to find the usernames, which are sent during the handshake.
The right filter to find these usernames is in the "Code/Filtering own Data" folder under "wireshark_filtering.txt"
In Wireshark, one can filter for other connection types or information sent. For me, it was a control that I used the right channels to capture my data.


###Parse data
Working with the .pcap files takes forever. There is a library that makes it possible to work with python and .pcap files.
The first thing I had to do is to reduce my data only to the MAC address and the time. I also collected usernames. Both files are in the scapy subfolder from the code folder. 
This process takes a long time. I recommend to run it in terminal not in IDLE because it uses TQDM.
After about 100 hours, about two weeks of data should be parsed. The longest part is behind us!

###Use the data
In the folder, an advanced algorithm contains several algorithms and ideas on how to use once data.
I created first a ten-dimensional numpy array to have to data in a uniform standard. "getdatareadyforaa_novarianz_meanvalue.py" creates in my experience the best results. There are other ways to do this. 
With the numpy array applying the advanced algorithm is simple. Be sure to select the right file to test and change the parameters depending on your goal and collected data.
There are several sklearn libraries used for different algorithm (mean shift,dbscan,k-means, and OPTICS)
There is also my own KNN algorithm in different versions. Some are for the classes, and some are for the SBB.

##Proof of concept
For proof of concept, I used the data provided by the school. The code in basic-PoC should be run with the main.py. In this program, the data location can be changed, the time-table can be modified, and the access-point data can be modified. There should be no reason to open the tools.py except to see how it is done. The help function works for every function used in the proof of concept.

##Rest
###Arduino
As in the paper said, I had the idea to create my own WIFI pineapple. I wanted to create it with the Arduino, and in the code/arduino folder, there are a few libraries and code snippets that should make it possible to capture and sniff Wi-Fi metadata from the air.
###Website
In the website folder, there are three different attends to create a website. The website_python_poster is the final one. To start the website, one has to run either flask run in the terminal or python3 app.py
###Test
The test folder exists to test codes. There are a lot of subfolders with individually parsed data. Most programs have path in them which work in the text files (especially the proof of concept data)
###Poster
In the folder poster, one can find all the posters I created, but in the end, I only used the don't scan ones. There are also QR codes to my website.
###Data
In the data folder, I have every data point I have collected or got from the IT-department. One can run the code with this data, but one has to rewrite the code with the right path.
###Graphing
In the graphing folder, it shows a few ideas on how to visualize the code one gathers. There are also testing files in there which use fake data, but for explaining the ideas, it helps a lot.
###More
There are many other programs which helped me to develop the main programs. Some of them work and are helpful, and others were no success at all. 





