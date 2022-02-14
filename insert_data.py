# -*- coding: utf-8 -*-


import griddb_python as griddb
import sys
import pandas as pd

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    
    #Reading csv file
    data_unprocessed = pd.read_csv("dataset.csv")
    
    
    #preprocessing
    
    data_unprocessed = data_unprocessed.drop(["guild", "stratum", "bn", "age","timestamp","age_group", "mass_scaled", "wing_scaled", "mw_scaled", "temp_lag1_wet", "precip_lag1_wet"],axis = 1)
    
    
    data_unprocessed.dropna(inplace=True)
    data_unprocessed.reset_index(drop=True, inplace=True)
    data_unprocessed.index.name = 'ID'
    
    #save it into csv
    data_unprocessed.to_csv("preprocessed.csv")
    
    #read the cleaned data from csv
    data_processed = pd.read_csv("preprocessed.csv")

    for row in data_unprocessed.itertuples(index=False):
            print(f"{row}")

    # View the structure of the data frames
    data_processed.info()

    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    #Create container 
    data_container = "data_container"

    # Create containerInfo
    data_containerInfo = griddb.ContainerInfo(data_container,
                    [["ID", griddb.Type.INTEGER],
        		    ["species", griddb.Type.STRING],
         		    ["spMeanMass", griddb.Type.FLOAT],
                    ["spMeanWing", griddb.Type.FLOAT],
                    ["spMeanMW", griddb.Type.FLOAT],
         		    ["year", griddb.Type.INTEGER],
                    ["mass", griddb.Type.FLOAT],
                    ["wing", griddb.Type.FLOAT],
                    ["mw", griddb.Type.FLOAT],
         		    ["temp_lag0_dry", griddb.Type.FLOAT],
                    ["temp_lag2_dry", griddb.Type.FLOAT],
                    ["precip_lag0_dry", griddb.Type.FLOAT],
                    ["precip_lag2_dry", griddb.Type.FLOAT]],
                    griddb.ContainerType.COLLECTION, True)
    
    data_columns = gridstore.put_container(data_containerInfo)

    print("container created and columns added")
    
    
    # Put rows
    data_columns.put_rows(data_processed)
    
    print("Data Inserted using the DataFrame")

except griddb.GSException as e:
    print(e)
    for i in range(e.get_error_stack_size()):
        print(e)
        # print("[", i, "]")
        # print(e.get_error_code(i))
        # print(e.get_location(i))
        print(e.get_message(i))
