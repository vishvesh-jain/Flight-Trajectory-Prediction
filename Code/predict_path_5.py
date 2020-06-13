import csv
import numpy as np
import pandas as pd
import os
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import time
from time import mktime
from datetime import datetime
from pymongo import MongoClient


def resample_trajectory(data, final_length):
    #print(data[len(data)-1])
    new_data = []
    current_length = len(data)
    new_data.append(data[0])
    for j_dash in range(1, final_length):
        j = round((j_dash*current_length)/final_length) 
        #print(j)
        new_data.append(data[int(j)-1]);
    
    new_data[final_length-1] = data[len(data)-1]
    #print(new_data)
    #print(len(data))
    #print(len(new_data))
    return new_data


def resample_time(starttime, endtime, n):

    #print(starttime)
    #print(endtime)
    #print(n)
    index = pd.date_range(starttime, endtime, freq='min')
    df = pd.DataFrame(index=index)
    first = df.index.min()
    last = df.index.max()
    secs = int((last-first).total_seconds()//n)
    #print(index)
    #print(df)

    final_list = []
    periodsize = '{:d}S'.format(secs)
    result = df.resample(periodsize).sum()
    #print(periodsize)
    #print(result)
    final_list = []
    for i in range (0,len(result.index)):
        final_list.append(str(result.index[i]))
    return final_list



def getairsigmetareas(time):


    client = MongoClient("mongodb://localhost:27017/")
    db = client.air_traj_proj
    collection = db.airsigmet_v2

    #print(collection)
    dt = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
    
    dt = str(dt)
    #print(dt)
    
    airsigmet_cursor = collection.find( {"$and":[{"timevalidfromutc": {"$lt":dt}},{"timevalidtoutc": {"$gte":dt}}]},{"airsigmetid":1,"timevalidfromutc":1,"timevalidtoutc":1,"movementdirdegrees":1,"movementspeedknots":1,"hazardtype":1,"hazardseverity":1,"sigmetarea":1})
    airsigmet_res = list(airsigmet_cursor)
    

    #print(airsigmet_res)
    airsigmet = {}
    
    for entries in airsigmet_res:
        key = entries['airsigmetid']
        #print(entries)
        if key not in airsigmet.keys():
            airsigmet[key] = {}
            airsigmet[key]['validfrom'] = ''
            airsigmet[key]['validto'] = ''
            airsigmet[key]['movementdirdegrees'] = ''
            airsigmet[key]['movementspeedknots'] = ''
            airsigmet[key]['hazardtype'] = ''
            airsigmet[key]['hazardseverity'] = ''
            airsigmet[key]['area'] = []
            #print entries['timevalidfromutc']
        airsigmet[key]['validfrom'] = entries['timevalidfromutc']
        airsigmet[key]['validto'] = entries['timevalidtoutc']
        airsigmet[key]['movementdirdegrees'] = entries['movementdirdegrees']
        airsigmet[key]['movementspeedknots'] = entries['movementspeedknots']
        airsigmet[key]['hazardtype'] = entries['hazardtype']
        airsigmet[key]['hazardseverity'] = entries['hazardseverity']
        airsigmet[key]['area'] = entries['sigmetarea']
        
        #print()
        #print(key)
        #print(airsigmet[key])
        #print()

    #print()
    #print()
    #print(airsigmet)
    #print()
    #print()
    return airsigmet

def is_point_in_polygon(x,y,poly):
    #print(x)
    #print(y)

    #print(poly)
    n = len(poly)
    #print()
    #print(n)

    lat_list = []
    lon_list = []
    b=[]
    a = poly
    a = a[1:]
    a = a[:-2]
    #print(a)
    b = a.split("), ")
    #print(len(a))
    #print(a)

    for i in b:
        i = i[1:]
        #print(i)
        lat_lon = i.split(", ")
        #print(lat_lon)
        lat_list.append(float(lat_lon[0]))
        lon_list.append(float(lat_lon[1]))
    
    #print(lat_list)
    #print(lon_list)
    inside = False
    
    final_poly_list = []
    len_lat = len(lat_list)
    for k in range(len_lat):
        temp = (lat_list[k],lon_list[k])
        final_poly_list.append(temp)

    #print(final_poly_list)
    p1x,p1y = final_poly_list[0]
    len_poly_list = len(final_poly_list)
    for i in range(len_poly_list+1):
        p2x,p2y = final_poly_list[i % len_poly_list]
        #print(str(p1x)+"   "+str(p1y))
        #print(str(p2x)+"   "+str(p2y))
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y
            #print(inside)

    #print(inside)
    #print()
    #print()
    
    return inside
'''
    for i in range(n+1):
        p2x,p2y = poly[i % n]
#        print "p2x, p2y: ", p2x, p2y
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
'''
    
def is_point_in_polygon2(x,y,poly):
    #print(x)
    #print(y)

    #print(poly)
    n = len(poly)
    #print()
    #print(n)

    lat_list = []
    lon_list = []
    b=[]
    #print("-----------------------------------------------------------------------------")
    #print(poly)
    
    a = poly
    a = a[1:]
    a = a[:-2]

    b = a.split("), ")
    #print(len(a))
    #print(a)

    for i in b:
        i = i[1:]
        #print(i)
        lat_lon = i.split(", ")
        #print(lat_lon)
        lat_list.append(float(lat_lon[0]))
        lon_list.append(float(lat_lon[1]))
        #print(lat_list)
        #print(lon_list)
    
    inside = False
    
    final_poly_list = []
    len_lat = len(lat_list)
    for k in range(len_lat):
        temp = (lat_list[k],lon_list[k])
        final_poly_list.append(temp)

    #print(final_poly_list)
    point = Point(x,y)
    polygon = Polygon(final_poly_list)
    #print("------------------------------------------------------------------------------------")
    #print(x)
    #print(y)
    #print(polygon.contains(point))
    #print("------------------------------------------------------------------------------------")
    if (polygon.contains(point))==True:
        #print(x)
        #print(y)
        #print(polygon.contains(point))
        print()
    return polygon.contains(point)
    

def check_typical_trajectory(datasets, sigmet, index):
    #print(datasets)
    modifiedtuple = []
    #print(index)
    for key in datasets:
        #print(key)
        dataset_time = datetime.strptime(datasets[key]['time'][index], "%Y-%m-%d %H:%M:%S")
        amn = sigmet['validfrom'][:-6]
        validfrom_time = datetime.strptime(amn,"%Y-%m-%d %H:%M:%S")
        amy = sigmet['validto'][:-6]
        validto_time = datetime.strptime(amy,"%Y-%m-%d %H:%M:%S")
        #print()
        #print(dataset_time)
        #print(validfrom_time)
        #print(validto_time)
        #print()
        #print(dataset_time - validfrom_time)
        #print(dataset_time < validto_time)
        if(dataset_time > validfrom_time and dataset_time < validto_time):
            #print(dataset_time)
            #print(validfrom_time)
            #print(validto_time)
            within_polygon = is_point_in_polygon2(datasets[key]['trajectory'][index][0], datasets[key]['trajectory'][index][1], sigmet['area'])
            if within_polygon:
                modifiedtuple.append(datasets[key]['trajectory'][i])

    return modifiedtuple
    
'''
                                dataset_time = datetime.strptime(datasets[key]['time'][index], "%Y-%m-%d %H:%M:%S").time()
                                validfrom_time = sigmet['validfrom'].time()
                                validto_time = sigmet['validto'].time()
                             
                                if(dataset_time > validfrom_time and dataset_time < validto_time):
                                    within_polygon = is_point_in_polygon(datasets[key]['trajectory'][i][0], datasets[key]['trajectory'][i][1], sigmet['area'])
                                    if within_polygon:
                                        modifiedtuple.append(datasets[key]['trajectory'][i])
                            return modifiedtuple
                        '''




def run_intent(inputPath_main,starttime,endtime):

    #os.chdir("..")
    base_dir = os.getcwd()
    #print(base_dir+"")
    

    dataset_dir = base_dir+'\\Dataset\\'
    
  

    dataPath = dataset_dir+'typical_trajectories.csv'
    inputPath = inputPath_main
    data = []
    data_dict = {}
    input_dict = {}


    with open(dataPath, 'r') as f:
        reader = csv.reader(f)
        next(reader, None) 

        for point in reader:
            #print(point)    
            traj_points = []
            if point[0] not in data_dict.keys():
                data_dict[point[0]] = {}
                data_dict[point[0]]['traj'] = []
                data_dict[point[0]]['starttime'] = ""
                data_dict[point[0]]['endtime'] = ""
            data_dict[point[0]]['starttime'] = point[1]
            data_dict[point[0]]['endtime'] = point[2]
            traj_points.append(float(point[4]))
            traj_points.append(float(point[5]))
            data_dict[point[0]]['traj'].append(tuple(traj_points))


    with open(inputPath, 'r') as f1:
        reader = csv.reader(f1)
        input_dict['traj'] = []
        input_dict['starttime'] = starttime
        input_dict['endtime'] = endtime
        for point in reader:
            traj_points = []
            traj_points.append(float(point[0]))
            traj_points.append(float(point[1]))
            input_dict['traj'].append(tuple(traj_points))


    #print(input_dict)




    input_dict['time'] = []
    temp_list = []
    input_dict['sampled_trajectory'] = []
    input_dict['sampled_trajectory'] = resample_trajectory(input_dict['traj'], 30)
    #print()
    #print(input_dict)
    sample_length = len(input_dict['sampled_trajectory'])
    #print(sample_length)
    input_dict['time'] = resample_time(input_dict['starttime'], input_dict['endtime'], sample_length)

    #print(input_dict)



    resampled_datasets = {}
    for key in data_dict:
        #print(key)
        new_traj_data = []
        new_sample_time = []
        if key not in resampled_datasets.keys():
            resampled_datasets[key] = {}
            resampled_datasets[key]['trajectory'] = []
            resampled_datasets[key]['time'] = []

        new_traj_data = resample_trajectory(data_dict[key]['traj'], sample_length)
        new_sample_time = resample_time(data_dict[key]['starttime'], data_dict[key]['endtime'], sample_length)
        resampled_datasets[key]['trajectory'] = new_traj_data
        resampled_datasets[key]['time'] = new_sample_time

   # print(resampled_datasets)    


    modified_trajectory = []
    speed = []
    dirdegrees = [] 
    hazardseverity = []
    hazardtype = []
    hazardseverity = []
    #Checking if the sampled input data lies on the polygon.
    #print(len(input_dict['sampled_trajectory']))
    for i in range(0, len(input_dict['sampled_trajectory'])):
        modified_trajectory.append('')
        speed.append('')
        dirdegrees.append('')
        hazardtype.append('')
        hazardseverity.append('')
        airsigmet = {}
        modifiedtraj = []
        #print()
        #print() 
        #print(input_dict['time'][i])
        airsigmet = getairsigmetareas(input_dict['time'][i])
       # print(airsigmet)

        for key in airsigmet:
            #print(input_dict['sampled_trajectory'][i][0])
            #print(input_dict['sampled_trajectory'][i][1])
            #print(airsigmet[key]['area'])
            is_within_polygon = is_point_in_polygon2(input_dict['sampled_trajectory'][i][0], input_dict['sampled_trajectory'][i][1], airsigmet[key]['area'])
            if is_within_polygon:
                #print(key)
                modifiedtraj = check_typical_trajectory(resampled_datasets, airsigmet[key], i)
                #print("----------------------------------------------------------------------------------------")
                #print(modifiedtraj)
                #print("-------------------------------------------------------------------------------")
                if modifiedtraj:
                    modified_trajectory[i] = modifiedtraj
                    dirdegrees[i] = airsigmet[key]['movementdirdegrees']
                    speed[i] = airsigmet[key]['movementspeedknots']
                    hazardtype[i] = airsigmet[key]['hazardtype']
                    hazardseverity[i] = airsigmet[key]['hazardseverity']
                else:
                    if not isinstance(modified_trajectory[i], list):
                        modified_trajectory[i] = '-'
                        if dirdegrees[i] =='':
                            dirdegrees[i] = '-'
                        if speed[i]=='':
                            speed[i] = '-'
                        if hazardtype[i] == '':
                            hazardtype[i] = '-'
                        if hazardseverity[i] =='':
                            hazardseverity[i] = '-'
            else:
                if not isinstance(modified_trajectory[i], list):
                        modified_trajectory[i] = '-'
                        if dirdegrees[i] =='':
                            dirdegrees[i] = '-'
                        if speed[i]=='':
                            speed[i] = '-'
                        if hazardtype[i] == '':
                            hazardtype[i] = '-'
                        if hazardseverity[i] =='':
                            hazardseverity[i] = '-'

    '''
    for i in range(0,len(input_dict['sampled_trajectory'])):
        if modified_trajectory[i] != '-':
            print( input_dict['sampled_trajectory'][i][0],input_dict['sampled_trajectory'][i][1], ":   Modified:  ", modified_trajectory[i], "  Speed: ", speed[i], "  Movement Degrees:  ", dirdegrees[i], "  Hazard Type:  ", hazardtype[i], "   Hazard Severity: ", hazardseverity[i])
        else:
            print(input_dict['sampled_trajectory'][i][0], input_dict['sampled_trajectory'][i][1])

        print()

    return "success"

    #print((modified_trajectory))
    #print(speed)
    #print(dirdegrees)
    #print(hazardseverity)
    #print(hazardtype)
    #print(input_dict['time'])
    #print(airsigmet)
    '''
    lat_traj=[]
    lon_traj=[]
    print()
    print()
    print("-------------------------------------------------")
    print("Predicted Flight Traj:")
    for i in range(0, len(input_dict['sampled_trajectory'])):
        
        if modified_trajectory[i] != '-':
            a = input_dict['sampled_trajectory'][i][0]
            b = input_dict['sampled_trajectory'][i][1]
            lat_traj.append(a)
            lon_traj.append(b)
            print (input_dict['sampled_trajectory'][i][0],"\t", input_dict['sampled_trajectory'][i][1])
            #print (input_dict['sampled_trajectory'][i][0], input_dict['sampled_trajectory'][i][1], ":   Modified:  ", modified_trajectory[i], "  Speed: ", speed[i], "  Movement Degrees:  ", dirdegrees[i], "  Hazard Type:  ", hazardtype[i], "   Hazard Severity: ", hazardseverity[i])
        else:
            a = input_dict['sampled_trajectory'][i][0]
            b = input_dict['sampled_trajectory'][i][1]
            lat_traj.append(a)
            lon_traj.append(b)
            
            print (input_dict['sampled_trajectory'][i][0],"\t", input_dict['sampled_trajectory'][i][1])

    record_list = [ list(item) for item in list(zip(lat_traj, lon_traj)) ]
    
    with open((dataset_dir+"predictedpath.csv"), "w") as fp:
        writer = csv.writer(fp)
        writer.writerows(record_list) 


    with open(dataset_dir+"predictedpath.csv") as in_file:
        with open((dataset_dir+"prediction.csv"), 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

    print("-------------------------------------------------")
    print()
    print()
    print("Predicted Flight Path Saved to File : Prediction.csv")
    print()
    print()







