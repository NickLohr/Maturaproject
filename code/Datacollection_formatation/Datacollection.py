log_file= "Data/2018-Dec-14-access.log"
access_point = "Data/access_points.log"

accesspoints={}
ap = open(access_point)
datapoints = ap.readlines()
for k in datapoints:
	m = k.split(",")
	for o in range(0,len(m)):
		if "w-ksz" in m[o]:
			accesspoints[m[o-1][1:10]]=m[o]



ap.close()

#print(accesspoints)
log = open(log_file)
data= log.readlines()
for op in data:
	t = op.split("][")
	
	if t[3].upper() == "88-E9-FE-B2-7B-46":
		print(t[4])
		aa = t[4]
		b = aa.replace("-",":")
		if b[0:9] in accesspoints.keys():
			#have to figure out how all the access points work
			print(accesspoints[b[0:9]])
