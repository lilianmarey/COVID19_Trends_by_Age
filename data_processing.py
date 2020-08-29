"""
app: Module to run the app
=============================================

.. moduleauthor:: Lilian MAREY <lilian.marey@ensae.fr>

"""
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

from sys import exit
from datetime import date
import pandas as pd

from src.mysettings import *
from src.helpers import *
from src.preprocess import *
import src.plots as plt 

##########################################
# Import needed data
# Harmonised data on cases, deaths, tests

print('Importation of input CSV files...')
df_harmonised = pd.read_csv(HARMONISED_DATA_PATH, skiprows = [0, 1, 2])
df_harmonised = df_harmonised[
    ['Country', 'Region', 'Date', 'Sex', 'Age', 'Cases', 'Deaths', 'Tests']
                            ]
print('Done')

###########################################
# Delete detected untrue source
df_harmonised = df_harmonised[-df_harmonised['Country'].isin(['UK'])]

###########################################
# Taking subset of data for experimentation : different sets depending on what you want to process
print('Taking subset of data for experimentation...')

# for processing the hole data : no selection

# for quick tests

df_harmonised = df_harmonised[df_harmonised['Country'].isin(['France'])]
df_harmonised = df_harmonised[df_harmonised['Region'].isin(['Corse'])]
df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
df_harmonised = df_harmonised[df_harmonised['Age'].isin([80])]


# for an histogram

# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['France'])]
# df_harmonised = df_harmonised[df_harmonised['Region'].isin(['Ile-de-France'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]


# a quite complete set, quite fast to process, for a complete demonstration

# df1 = df_harmonised[df_harmonised['Region'].isin(['All'])].copy()
# df1 = df1[df1['Sex'].isin(['b'])]
# df1 = df1[df1['Age'].isin([80])]
# df2 = df_harmonised[df_harmonised['Country'] == 'France'].copy()
# df3 = df_harmonised[df_harmonised['Country'].isin(['USA'])]
# df3 = df3[df3['Sex'].isin(['b'])]
# df_harmonised = df3.merge(df1.merge(df2, 'outer'), 'outer')


# for a world map

# df_harmonised = df_harmonised[df_harmonised['Region'].isin(['All'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
# df_harmonised = df_harmonised[df_harmonised['Age'].isin([80])]


# for a USA map

# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['USA'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
# df_harmonised = df_harmonised[df_harmonised['Age'].isin([80])]


###########################################
# Adding CFR column to the Harmonised data

print('Adding CFR column to the Harmonised data')
df_harmonised['CFR'] = computeRatio(
                            df_harmonised['Deaths'],
                            df_harmonised['Cases']
                                    )
print('Done')


###########################################
# Adding Tests by cases column to the Harmonised data

print('Adding Cases_by_tests column to the Harmonised data')
df_harmonised['Tests by cases'] = computeRatio(
                            df_harmonised['Tests'],
                            df_harmonised['Cases']
                                    )
print('Done')

###########################################
# Sorting data

print('Done')
print('Data shape : ', df_harmonised.shape)
print('Creating date_code column...')
df_harmonised['Date_code'] = df_harmonised.apply(computeDatecode, axis = 1)
print('Done')
print('Sorting Dataframe...')
df_harmonised = df_harmonised.sort_values(by = ['Date_code'])
print('Done')

###########################################
# Computing dayly/weekly/monthly data 

print('Melting dataframe...')
df_harmonised = meltDataframe(df_harmonised)
print('Done')

###########################################
# Adding gap_in_day and label column to the harmonised data

print('Creating date_code column...')
df_harmonised['gap_in_day'] = df_harmonised.apply(lambda row : time_delta('01/01/2020', row.Date), axis = 1)
print('Done')

print('Creating Country - Region - Age - Gender column...')
df_harmonised['Country - Region - Age - Gender'] = df_harmonised.apply(
                                                    lambda row : str(row.Country) + ' - ' 
                                                                + row.Region + ' - ' 
                                                                + str(row.Age) + '-' 
                                                                + str(row.Age+sum(
                                                                        [4 if row.Age == 100 else 9]
                                                                                )
                                                                    )
                                                                + ' ans - ' + label_gender[row.Sex],
                                                    axis = 1)
print('Done')

###########################################
# Building time metrics

print('Building time metrics...')
df_harmonised = build_time_metrics(df_harmonised)
print('Time metrics built')

###########################################
# Building date label column
df_harmonised['Date_format'] = df_harmonised.apply(computeDateFormat, axis = 1)


###################################
# Corrections on original dataset to fit with other datasets

df_harmonised['Region'] = df_harmonised['Region'].replace('Lousiana', 'Louisiana')
df_harmonised['Region'] = df_harmonised['Region'].replace('NYC', 'New York')

###################################
# Computation of values by population

df_harmonised['Value_by_pop'] = df_harmonised.apply(computeValuebyPop, axis = 1)




###################################
# Creation of file

PATH = pathlib.Path(__file__).parent

df_harmonised.to_csv(str(PATH) + '/data/preprocessed_data_test.csv')

print('File created')

