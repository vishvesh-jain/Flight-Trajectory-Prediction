import pymongo
import gmplot
import webbrowser
import csv
import time
from time import mktime
import webbrowser
import os
from datetime import datetime
from pymongo import MongoClient


def map_plot():
	#os.chdir("..")
	base_dir = os.getcwd()
	    #print(base_dir+"")
	dataset_dir = base_dir+'\\Dataset\\'
	 
	


	client = MongoClient("mongodb://localhost:27017/")
	db = client.air_traj_proj
	collection = db.airsigmet_v2
	count = 0
	sdt = "2012-12-09 11:45:00"
	dt = "2012-12-09 14:45:00"



	result =  collection.find( {"$and":[{"timevalidfromutc": {"$lte":dt}},{"timevalidtoutc": {"$gte":dt}}]},{"airsigmetid":1,"timevalidfromutc":1,"timevalidtoutc":1,"movementdirdegrees":1,"movementspeedknots":1,"hazardtype":1,"hazardseverity":1,"sigmetarea":1})
	obj = next(result, None)
	#print(obj['sigmetarea'])
	gmap3 = gmplot.GoogleMapPlotter(38.0303, -111, 4)






	datapath = dataset_dir+"prediction.csv"    
	  
	with open(datapath,'r')as f:
		data = csv.reader(f)
		#print(data)
		lat = []
		lon = []
		for row in data:
			a = str(row[0:1])
			b = a[2:]
			c = b[:-2]
			lat.append(float(c))

			a = str(row[1:2])
			b = a[2:]
			c = b[:-2]
			lon.append(float(c))
			row = next(data)

		#print(lat)
		#print(lon)
		
		lat_list = lat
		lon_list = lon
		avg_lat = sum(lat)/len(lat)
		avg_lon = sum(lon)/len(lon)
		
		#gmap3 = gmplot.GoogleMapPlotter(avg_lat, avg_lon, 5) 
		gmap3.scatter( lat_list, lon_list, '#FFFFFF', size = 40, marker = False ) 
		gmap3.plot(lat_list, lon_list, 'cornflowerblue', edge_width = 2.5) 
		#mappath = base_dir+'\\Map\\'+"output.html"
		#gmap3.draw( mappath )




	for obj in result:
		#print(obj['airsigmetid'])
		count = count+1
		try:
			lat_list = []
			lon_list = []
			
			a = obj['sigmetarea']

			a = a[1:]
			a = a[:-2]
			b = a.split("), ")
			for i in b:
				lat_lon = i[1:].split(", ")
				lat_point = float(lat_lon[0])
				lon_point = float(lat_lon[1])
				lat_list.append(lat_point)
				lon_list.append(lon_point)
			#print(count)
			lat_list.append(lat_list[0])
			lon_list.append(lon_list[0])
			#print(lon_list)
			#print(lat_list)

			if (len(lat_list) > 20):
			
				gmap3.scatter( lat_list, lon_list, '# FF0000', size = 40, marker = False ) 	 
				gmap3.plot(lat_list, lon_list, 'cornflowerblue', edge_width = 2.5)  
			elif (len(lat_list)>6):
				print()
				#gmap3.scatter( lat_list, lon_list, '# 00FF00', size = 40, marker = False ) 	 
				#gmap3.plot(lat_list, lon_list, 'green', edge_width = 2.5)  
				
			else:
				gmap3.scatter( lat_list, lon_list, '# 0000FF', size = 40, marker = False ) 	 
				gmap3.plot(lat_list, lon_list, 'red', edge_width = 2.5)  
		except KeyError:
			continue



	
	mappath = base_dir+'\\Map\\'+"output_sigmet.html"
	gmap3.draw( mappath )

	print()
	print()
	print("--------------------------------------------")
	print("Map for sigmet with Flight Trajectory plotted")
	print("--------------------------------------------")
	print()
	print()
		
	

		
	url = mappath
	webbrowser.open(url, new=2)
 	
	return ("success")



#map_plot()