#! /usr/bin/python
import sys,os
import re
import csv
import datetime
import pandas as pd 
import time  





#from pymongo import MongoClient

## Function to get trajectories from db for all typical trajectory ids
def get_typical_trajectories(typical_trajectories_id_path,db,dataset_dir):

## Getting typical trajectory ids from csv file
	typ_ids=[]
	with open(typical_trajectories_id_path, 'r') as idfile:
		#data = idfile.read().strip().replace('\n','')
		counter = 0
		for row in idfile:
			counter = counter + 1
			row = row.rstrip('\n')
			typ_ids.append(int(row))
			typ_ids.sort()

	print()
	print()
	print("---------------------------------------------------------------------")
	print("Typical Trajectories Extracted for these Flight IDS : ")
	print (typ_ids)

	print("---------------------------------------------------------------------")
	print()
	print()



	pd.set_option('precision', 15)
	data_fplan=pd.read_csv(dataset_dir+"asdiflightplan.csv") 
	data_fplan.sort_values(["asdiflightplanid"], axis=0, ascending=True, inplace=True) 

	data_fplan.drop(['updatetimeutc','flighthistoryid','aircraftid','legacyroute','estimateddepartureutc','estimatedarrivalutc','departureairport','arrivalairport'], axis=1, inplace=True)

	data2 =(data_fplan.loc[data_fplan['asdiflightplanid'].isin(typ_ids)])
	
	data2.to_csv(dataset_dir+"testing.csv", sep=',')

	data_waypoint=pd.read_csv(dataset_dir+"asdifpwaypoint.csv") 

	

	
	data3 =(data_waypoint.loc[data_waypoint['asdiflightplanid'].isin(typ_ids)])
	data3.sort_values(["asdiflightplanid","ordinal"], axis=0, ascending=True, inplace=True) 
	data3.to_csv(dataset_dir+"testing2.csv", sep=',')

	result = data2.merge(data3, on="asdiflightplanid", how = 'inner')
	#print(result)
	result.to_csv(dataset_dir+'typical_trajectories.csv',index=False) 
	
	


def run_get_typical_traj():

	#client = MongoClient('localhost',27017,maxPoolSize=None)
	#db = client.kddproject_v2
	#os.chdir("..")
	base_dir = os.getcwd()
	#print(base_dir+"")
	input_dir = base_dir+'\\Input\\'

	dataset_dir = base_dir+'\\Dataset\\'
	#print(dataset_dir)
	#print(dataset_dir)
	db = 0			
	typical_trajectories_id_path = dataset_dir+'typicaltrajectory-flightid.csv'
	get_typical_trajectories(typical_trajectories_id_path,db,dataset_dir)
	#predictpath.run_intent()

	return ("yes")


#run_get_typical_traj()