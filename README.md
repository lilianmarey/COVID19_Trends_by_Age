# COVID19: Trends by Age

Dash-based app

data_preprocessing.py and app.py can be run from terminal :
        - data_preprocessing.py creates a CSV file in /data/ folder that can be used by the app
        - app.py launches the application using the CSV file created by data_preprocessing.py

The file /data/preprocessed_data.csv is an example of whole database processing (it takes time to compute).

Data visualisation project on Covid-19 cases, deaths by age bands

Main data source : https://osf.io/mpwjq/

# PROJECT OWNER

Lilian Marey

# SQUAD 

Lilian Marey

Jean-Claude Razafindrakoto

Marius Pascariu

# STRUCTURE OF PROJECT

COVID19_Trends_by_Age

    |
    |
    |---- data           : Datatabases we work with

            |
            |
            |--- population_datasets        : Databases used for weighting
            |
            |--- Output_10.csv              : The main database with the number of cases, deaths, tests, etc. by age and region
    |        
    |
    |---- documentation  : Documentation (resources, codebook)
    |
    |---- assets         : deals with the front end presentation
    |
    |---- src            : Documented scripts after iterations 
    |
    |---- app.py         : Web app in Dash 
    |
    |---- data_preprocessing.py         : Data processor to run before launching the app
    |
    |____ README.md      
