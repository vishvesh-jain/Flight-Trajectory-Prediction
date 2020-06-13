import csv
import gmplot
import os
import webbrowser



def map_plot():
	
	base_dir = os.getcwd()
	    #print(base_dir+"")
	    

	dataset_dir = base_dir+'\\Dataset\\'
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
		
		gmap3 = gmplot.GoogleMapPlotter(avg_lat, avg_lon, 5) 
		gmap3.scatter( lat_list, lon_list, '# FFFFFF', size = 40, marker = False ) 
		gmap3.plot(lat_list, lon_list, 'cornflowerblue', edge_width = 2.5) 
		mappath = base_dir+'\\Map\\'+"output.html"
		gmap3.draw( mappath )

		print()
		print()
		print("--------------------------------------------")
		print("Flight Traj Map Plotted")
		print("--------------------------------------------")
		print()
		print()
		
		
		
		url = mappath
		webbrowser.open(url, new=2)
 	
	return ("success")

