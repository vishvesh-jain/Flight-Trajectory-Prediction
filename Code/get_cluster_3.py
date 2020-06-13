#! /usr/bin/python  
from math import sqrt, pow  
import csv
import os
import re






class DBSCAN:  
 
    def __init__(self):  

        self.DB = [] #Database  
        self.esp = 0.02 #neighborhood distance for search  
        self.MinPts = 2 #minimum number of points required to form a cluster  
        self.cluster_inx = -1  
        self.cluster = []  
        self.centroid = []
        self.flightplanPoint = ""
       
    def DBSCAN(self):  
      for i in range(len(self.DB)):  
        p_tmp = self.DB[i]  
        if (not p_tmp.visited):  
          p_tmp.visited = True  
          NeighborPts = self.regionQuery(p_tmp)  
          if(len(NeighborPts) < self.MinPts):  
            p_tmp.isnoise = True  
          else:  
            self.cluster.append([])  
            self.cluster_inx = self.cluster_inx + 1  
            self.expandCluster(p_tmp, NeighborPts)     
       
    def expandCluster(self, P, neighbor_points):  
      self.cluster[self.cluster_inx].append(P)  
      iterator = iter(neighbor_points)  
      while True:  
        try:   
          npoint_tmp = iterator.__next__()  
        except StopIteration:  
         
          break  
        if (not npoint_tmp.visited):  
          
          npoint_tmp.visited = True  
          NeighborPts_ = self.regionQuery(npoint_tmp)  
          if (len(NeighborPts_) >= self.MinPts):  
            for j in range(len(NeighborPts_)):  
              neighbor_points.append(NeighborPts_[j])  
        if (not self.checkMembership(npoint_tmp)):  
          self.cluster[self.cluster_inx].append(npoint_tmp)  
   
    def checkMembership(self, P):  

      ismember = False  
      for i in range(len(self.cluster)):  
        for j in range(len(self.cluster[i])):  
          if (P.flightid == self.cluster[i][j].flightid): #RAG
            ismember = True  
      return ismember  
       
    def regionQuery(self, P):  
      pointInRegion = []  
      for i in range(len(self.DB)):  
        p_tmp = self.DB[i]  
        if (self.dist(P, p_tmp) < self.esp and P.flightid != p_tmp.flightid): #RAG 
          pointInRegion.append(p_tmp)  
      return pointInRegion  

    def identifycluster(self):
        for i in range(len(self.cluster)):
            if(self.dist(self.flightplanPoint, self.centroid[i]) < 0.2):
                self.flightplanPoint.belongstoCluster.append(i);

    def showCluster(self,abcd,dataset_dir):
        count = 0
        if len(self.flightplanPoint.belongstoCluster) == 0 :
            print ("The input historical flight trajectory does not belong to any cluster")
            print("false")
            return ("false")
        else:
            outputfile_handle = open((dataset_dir+'typicaltrajectory-flightid.csv'), 'w')
            print ("The input historical trajectory belongs to cluster", ' '.join(str(self.flightplanPoint.belongstoCluster)))
            for clusterid in self.flightplanPoint.belongstoCluster:
                #print(abcd.cluster[clusterid])
                for j in range(len(abcd.cluster[clusterid])):  
                    count = count+1
                    outputfile_handle.write(str(self.cluster[clusterid][j].getFlightID()))
                    outputfile_handle.write('\n')
            #print(count)
            outputfile_handle.close()

   
    def dist(self, p1, p2):  
   
      dx = (p1.x - p2.x)  
      dy = (p1.y - p2.y)  
      return sqrt(pow(dx,2) + pow(dy,2))  

   
class Point:  
    def __init__(self, x = 0, y = 0, flightid = 0, visited = False, isnoise = False):  
      self.x = x  
      self.y = y  
      self.flightid = flightid
      self.visited = False  
      self.isnoise = False  
      self.belongstoCluster = []
   
    def show(self):  
      return self.flightid  

    def show1(self):  
      return self.x,self.y  
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getFlightID(self):
        return self.flightid


 
def run_getcluster(inputPath_main):  
    vecPoint = []
    flightplan = []
    centroidX = []
    centroidY = []
    



    print()
    print()
    print("--------------------------------------------------------------")
    base_dir = os.getcwd()
   # print(base_dir)
    dataset_dir = base_dir+'\\Dataset\\'
    
    dataPath = dataset_dir+'avgcluster.csv'
    inputPath = inputPath_main
    with open(dataPath,'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            vecPoint.append(Point(float(row[1]),float(row[2]), int(row[0])))

    with open(inputPath,'r') as f1:
        reader = csv.reader(f1)
        for row in reader:
            flightplan.append((float(row[0]),float(row[1])))

   
    dbScan = DBSCAN()  
    
    dbScan.DB = vecPoint;  
    #print(vecPoint)
  
    dbScan.DBSCAN()  
  
    for i in range(len(dbScan.cluster)):
        print ('Cluster: ', str(i))
        sumx = 0
        sumy = 0
        for j in range(len(dbScan.cluster[i])):  
            sumx += dbScan.cluster[i][j].getX()
            sumy += dbScan.cluster[i][j].getY()
            print (dbScan.cluster[i][j].show())
        centroidX.append(sumx/float(len(dbScan.cluster[i])))
        centroidY.append(sumy/float(len(dbScan.cluster[i])))

  
    for i in range(len(centroidY)):
        print ('Centroid ', i)
        dbScan.centroid.append(Point(float(centroidX[i]), float(centroidY[i])))
        print (dbScan.centroid[i].show1())

  
    distance = tuple(map(lambda y: sum(y) / float(len(y)), zip(*flightplan)))
    dbScan.flightplanPoint = Point(float(distance[0]),float(distance[1]))

    dbScan.identifycluster()
    dbScan_2=dbScan
    result = dbScan.showCluster(dbScan_2,dataset_dir)


    print("--------------------------------------------------------------")
    print("")
    print("CLUSTERING DONE")
    if result =="false":
      return ("false")
    return ("yes")