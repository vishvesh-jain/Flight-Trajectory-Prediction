import sys,os
import re
import csv
import gmplot
import datetime
from pymongo import MongoClient


def airsigmet_load():
	client = MongoClient("mongodb://localhost:27017/")
	db = client.air_traj_proj
	#print(client)
	#print(db)
	traj = []
	#print(type(traj))
	counter = 11
	a =[]
	b = []

	airsigmentarea_path = 'C:/Users/vishv/OneDrive/Desktop/final_major_proj/Dataset/flightstats_airsigmetarea.csv'
	with open(airsigmentarea_path, 'r') as asfile:
		rows = csv.reader(asfile, delimiter=',')
		next(rows, None)
		for row in rows:
		#	print(rows)
			ordinal = int(row[3])
			if (ordinal == 0):
				if traj:

					result = db.airsigmet_v2.update_one(
							{"airsigmetid": str(airsigmetid)},
							{
								"$set":{
										"sigmetarea": str(traj)
										},
							}
							)
					#print(result)
					#print(traj)
					#print(airsigmetid)
					#print()
					#print()
					
				traj = []
				airsigmetid = int(row[0])
				#print(type(airsigmetid))
				loc = ()
			
			else:
				latitude = float(row[1])
				longitude = float(row[2])
				loc = (latitude,longitude)
				traj.append(loc)

				"""
				wa.append(float(latitude))
				b.append(float(longitude))

							
				lat_list = a
				lon_list = b
				avg_lat = sum(a)/len(a)
				avg_lon = sum(b)/len(b)
				
				gmap3 = gmplot.GoogleMapPlotter(avg_lat, avg_lon, 5) 
				gmap3.scatter( lat_list, lon_list, '# FF0000', size = 40, marker = False ) 
				gmap3.plot(lat_list, lon_list, 'cornflowerblue', edge_width = 2.5) 
				gmap3.draw( "C:/Users/vishv/OneDrive/Desktop/mdd final review/datasets/flightplan/map13.html" )
				"""

					
			#print(airsigmetid)
			#print(traj)
	#print(traj)
	#print(airsigmetid)
	db.airsigmet_v2.update_one(
							{"airsigmetid": str(airsigmetid)},
							{
								"$set":{
										"sigmetarea": str(traj)
										},
							}
							)

	print("Successfully updated Mongo Database with AIR SIGMET AREA")

				



				