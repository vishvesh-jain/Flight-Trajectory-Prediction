import sys,os
import re
import csv
import datetime
from pymongo import MongoClient



def run_get_fid_list(org,dest):
	#part to get current working directory
	
	os.chdir("..")
	base_dir = os.getcwd()
	
	
	#print(base_dir)
	dataset_dir = base_dir+'\\Dataset\\'
	
	
	#print(dataset_dir)
	f_id = []
	csv_file = csv.reader(open((dataset_dir+'asdiflightplan.csv'),'r'),delimiter = ",")

	for row in csv_file:
		if org==row[3] and dest ==row[4]:
			f_id.append(int(row[0]))

	#print(f_id)		
			
	count = 0		
	count = len(f_id)
	return (f_id)
	#print(count)


#run_get_fid_list("LAX","JFK")