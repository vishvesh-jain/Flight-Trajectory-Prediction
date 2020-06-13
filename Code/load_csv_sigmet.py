
import sys
import pandas as pd
from pymongo import MongoClient
import json
import os


def import_content(filepath):
    
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    client = MongoClient("mongodb://localhost:27017/")
    db = client.air_traj_proj
    collection = db.airsigmet_v2

    
    data_json = json.loads(data.to_json(orient='records'))
    collection.remove()
    collection.insert(data_json)
    print("done")

def run_load():
  os.chdir("..")
  base_dir = os.getcwd()
  
  
  print(base_dir)
  dataset_dir = base_dir+'\\Dataset\\'
  
  filepath = dataset_dir+'flightstats_airsigmet.csv'  
  cdir = os.path.dirname(__file__)
  file_res = os.path.join(cdir, filepath)

  data = pd.read_csv(file_res)
  data = data.drop('rawtext',axis=1)
  data = data.drop('altitudeminft',axis=1)
  data = data.drop('altitudemaxft',axis=1)
  url = dataset_dir+'flightstats_airsigmet_update.csv'
  data.to_csv ((dataset_dir+'flightstats_airsigmet_update.csv'), index = False, header=True)
  print("Updated    ")

  #filepath2 = 'C:/Users/vishv/OneDrive/Desktop/final_major_proj/Dataset/flightstats_airsigmet_update.csv'
  #import_content(filepath2)

run_load()