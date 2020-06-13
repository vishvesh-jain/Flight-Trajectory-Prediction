import sys,os
import pandas as pd 
import time  
import get_fid_list_1




def run_cluster_fid(fid_list):
	pd.set_option('precision', 15)
	start_time = time.time()
	
	print("----------------------------------------------------------------")
	print("List of Flights between Origin and Destination : ")
	print(fid_list)
	print("----------------------------------------------------------------")
	print()
	print()
	#os.chdir("..")
	base_dir = os.getcwd()
	#print(base_dir+"")
	dataset_dir = base_dir+'\\Dataset\\'
	#print(dataset_dir)
	data=pd.read_csv((dataset_dir+'asdifpwaypoint.csv'))

	ids = fid_list
	data2 = (data.loc[data['asdiflightplanid'].isin(ids)])
	data2.sort_values(["asdiflightplanid", "ordinal"], axis=0, ascending=True, inplace=True) 
			
	data2.drop('ordinal', axis=1, inplace=True)
	
	print("----------------------------------------------------------------")
	print(data2)
	print("----------------------------------------------------------------")
	print()
	print()
	#print(len(data))
	#print("done")
	#ids = fid_list
	#print(ids)
			
	#data2 =(data.loc[data['asdiflightplanid'].isin(ids)])
	#print(data2)
			
	data3 = data2.groupby(['asdiflightplanid']).mean()
			
			
	data3.to_csv((dataset_dir+'avgcluster.csv'), sep=',')
	
	return ("file 2 yes")

	 

	