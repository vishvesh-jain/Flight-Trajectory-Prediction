---------------------------------------------------------
READ - ME
---------------------------------------------------------

Requirements - 
1. MongoDb Compass
2. Python 3.6
3. Any web Browser to open output map
4. ensure these files are placed in dataset folder - 
	 - asdiflightplan.csv
	 - asdifpwaypoint.csv
	 - flightstats_airsigmet.csv
	 - flightstats_airsigmetarea.csv
5. Complete Dataset at https://www.kaggle.com/c/flight/data
---------------------------------------------------------
Steps - 

1. Ensure all the packages listed in requirement.txt are installed use the command pip install -r requirement.txt

-> Air Sigmet Data Pre-Processing 
   1. Open MongoDB Compass and establish connection to host by setting following variable - 	
	Hostname - localhost
	port - 27017
	Authentication - None
	SSL - None
	SSH Tunnel - None
   2. As soon as connection is established, Click on Create database Button and set the following values - 	
	Database Name - air_traj_proj
	Collection Name - airsigmet_v2
	keep the capped collection and use custom collation as unchecked and submit the details
   3. Run the python file load_csv_sigmet.py - it builds the file "flightstats_airsigmet_update.csv" and saves it in project directory in dataset folder.
   4. In MongoDb Compass, select collection airsigmet_v2 under air_traj_proj and select Collection option from menu bar and click on import data option
   5. Select CSV File Upload option, browse the file "flightstats_airsigmet_update.csv" under the dataset folder in the project directory and select it

-> Run The GUI
   1. Run the python file "gui_test.py"
   2. in the visible GUI, enter roigin and destination airport
   3. Select the input flight plan by selecting the file after browing through the directory
   4. File containing input flight plan is a csv file with 2 values i.e latitude and longitude, a sample input flight plan file is saved in project directory under the folder Input
   5. The output is displayed in the web browser in form of maps and also the predicted flight plan is saved in dataset folder of Project under the filename "prediction.csv".

-> Why we used DBSCAN
   1. Run the file clustering_compare.py

Warning :-
Some temporary csv files are generated during the execution of the project under the folder dataset.


Additional Info - 2 dataset files are missing as they cant be uploaded due to size issues.
Mail me @ vish.vj412@gmail.com














---------------------------------------------------------
