import os
import get_fid_list_1
import cluster_fid_2
import get_cluster_3
import get_typical_traj_4
import predict_path_5
import map_plot_6
import airsigmet_area_load_7
import test_map_mongo_8

def run(arr,dest,inputpath):
	
	airsigmet_area_load_7.airsigmet_load()
	print("--------------------------------------------------------------")
	print()
	print("Database updated with sigmet area co-ordinates")
	print()
	print("--------------------------------------------------------------")
	org = arr
	print("Origin : ",org)
	
	des = dest
	print("Destination : ",dest)
	#print(inputpath)
	a = get_fid_list_1.run_get_fid_list(org,des)
	#print("file1")

	
	#print(str(a))

	b = cluster_fid_2.run_cluster_fid(a)
	#print(b)
	

			
	c = get_cluster_3.run_getcluster(inputpath)
	
	if c=="false":
		print("not in cluster")
		return ("fail")
			
	d = get_typical_traj_4.run_get_typical_traj()
	#print(d)
	
	e = predict_path_5.run_intent(inputpath,'2012-12-09 01:45:00','2012-12-09 23:55:00')
	#print(e)
	
	f = map_plot_6.map_plot()
	#print(f)

	g = test_map_mongo_8.map_plot()
	#print(g)
	return ("success")

