# -*- coding: utf-8 -*-


import numpy as np
import griddb_python as griddb
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    # Get GridStore object
    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    # Define the container names
    data_container = "data_container"

    # Get the containers
    obtained_data = gridstore.get_container(data_container)
    
    # Fetch all rows - language_tag_container
    query = obtained_data.query("select *")
    
    rs = query.fetch(False)
    print(f"{data_container} Data")

    
    # Iterate and create a list
    retrieved_data= []
    while rs.has_next():
        data = rs.next()
        retrieved_data.append(data)

    # Convert the list to a pandas data frame
    data = pd.DataFrame(retrieved_data,
                        columns=['species', 'spMeanMass', 'spMeanWing', 'spMeanMW', 'year', 'mass',
                                 'wing', 'mw', 'temp_lag0_dry', 'temp_lag2_dry', 'precip_lag0_dry',
                                 'precip_lag2_dry'])

    # Get the data frame details
    print(data)
    data.info()
    
    
except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print("[", i, "]")
        print(e.get_error_code(i))
        print(e.get_location(i))
        print(e.get_message(i))
        
##Analysis

species_groupby = data.groupby(["species", "year"], as_index = False).mean()


species_list = species_groupby["species"].unique()

## generating plots
for i in range(len(species_list)):
    species_data = species_groupby[species_groupby["species"] == species_list[i]]
    sns.lineplot(data = species_data, x ="year", y ="mw")
    plt.title(species_list[i])
    plt.show()
    
weather_groupby = data.groupby(["year"], as_index = False).mean()

sns.lineplot(data = weather_groupby, x ="year", y ="precip_lag2_dry")
plt.show()

sns.lineplot(data = weather_groupby, x ="year", y ="temp_lag2_dry")
plt.show()
