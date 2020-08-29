"""
preprocess: Module to preprocess raw data
=============================================

.. moduleauthor:: Jean-Claude RAZAFINDRAKOTO <jrazafindrakoto@scor.com>

"""

import pandas as pd

# global settings
from src.mysettings import *

# helper functions
from src.helpers import computeRatio, regions_of_country, select_data, computeSource, delete_spaces, computeDatecode, meltDataframe, time_delta, computeDateFormat, build_time_metrics



##########################################
# Load in memory needed data :
# Harmonised data on cases, deaths, tests
# Population data (worldwide)
# US states population

print('Importation of CSV files...')
df_harmonised = pd.read_csv(HARMONISED_DATA_PATH, skiprows = [0, 1, 2])
pop_by_country = pd.read_csv(POPULATION_DATA_PATH, sep = ';')
pop_usa_states =  pd.read_csv(USSTATES_DATA_PATH, sep = ';')
df_harmonised = df_harmonised[
    ['Country', 'Region', 'Date', 'Sex', 'Age', 'Cases', 'Deaths', 'Tests']
                            ]
print('Done')

###################################
# Functions

def delete_multiple_sources(df, A, G):
    """Deletes from the dataframe detected unwanted sources

    Parameters:
    -----------
    df : dataframe
       dataframe to be transformed 

    A : int list
        selected age ranges
    
    G : str list
        selected genders
       
    Returns:
    --------
        df : Pandas DataFrame
            The coresponding dataframe (Pandas dataframe)
    """
    dfFranceAll = select_data(df, ['France'], ['All'], A, G)
    dfUKAll = select_data(df, ['UK'], ['All'], A, G)

    df_list = [dfFranceAll, dfUKAll]
    unwanted_source = ['FRheb..', 'GB_EN..']

    for i in range(len(df_list)):
        dataframe = df_list[i]

        for index, row in dataframe.iterrows():
            if computeSource(row['Code']) == unwanted_source[i]:
                df.drop(index, inplace = True)
                
    return df

def computeValuebyPop(row):
    """Computes values divided by the coountry population

    Parameters:
    -----------
    row : Pandas Serie
        row of a DataFrame
       
    Returns:
    --------
        Val : float
            the corresponding value (original value by millions of inhabitants)
    """
    try:
        Val = int(
                100 * 1000000 * row.Value 
                / pop_by_country[pop_by_country['Country'] == row.Country]['pop'].values[0]
                ) / 100
    except OverflowError:
        Val = None

    return Val

def divide_US_Dataframe(df, unit):
    """Divides values of metrics of the US dataframe by a certain unit

    Parameters:
    -----------
    df : dataframe
       dataframe (assumed to be not melted (short format))
    
    unit : str
        gives the unit to divide values by

    Returns:
    --------
        df : Pandas dataframe
            The coresponding dataframe (long format, melted)
    """
    if unit == 'Per million inhabitants':
        df['Value'] = df.apply(
                                lambda row:  int( 100 * 1000000 * row['Value']
                                                / int(
                                                        delete_spaces(
                                                            pop_usa_states[pop_usa_states['State'] == row.Region]['pop'].values[0]
                                                                    )
                                                    )
                                                ) / 100, 
                                axis = 1
                                )
    else:
        pass

    return df

###########################################
# Delete detected untrue source
df_harmonised = df_harmonised[-df_harmonised['Region'].isin(['Texas'])]

###########################################
# Taking subset of data for experimentation
print('Taking subset of data for experimentation...')

# for tests
# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['Mali', 'Burkina Faso', 'Finland', 'Gambia', 'Rwanda', 'Costa Rica', 'Switzerland', 'Algeria'])]

# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['Guatemala',
#  'Honduras',
#  'Cameroon',
#  'Malawi',
#  'Burkina Faso',
#  'UK',
#  'Panama',
#  'Uganda',
#  'New Zealand',
# ])]



df_harmonised = df_harmonised[df_harmonised['Country'].isin(['France'])]

df_harmonised = df_harmonised[df_harmonised['Region'].isin(['Corse'])]
df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
df_harmonised = df_harmonised[df_harmonised['Age'].isin([80])]


# for histograms
# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['France'])]
# df_harmonised = df_harmonised[df_harmonised['Region'].isin(['Ile-de-France'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]


# for demo
# df1 = df_harmonised[df_harmonised['Region'].isin(['All'])].copy()
# df1 = df1[df1['Sex'].isin(['b'])]
# df1 = df1[df1['Age'].isin([80])]

# df2 = df_harmonised[df_harmonised['Country'] == 'France'].copy()

# df3 = df_harmonised[df_harmonised['Country'].isin(['USA'])]
# df3 = df3[df3['Sex'].isin(['b'])]

# df_harmonised = df3.merge(df1.merge(df2, 'outer'), 'outer')

# hist/charts
# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['France'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
# df_harmonised = df_harmonised[df_harmonised['Region'].isin(['All'])]


# world map
# df_harmonised = df_harmonised[df_harmonised['Region'].isin(['All'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]
# df_harmonised = df_harmonised[df_harmonised['Age'].isin([80])]

# usa map
# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['USA'])]
# df_harmonised = df_harmonised[df_harmonised['Sex'].isin(['b'])]

# Half of the data
# df_harmonised = df_harmonised[df_harmonised['Country'].isin( list(set(df_harmonised.Country))[0:0]+['USA', 'France', 'Germany', 'Canada', 'Australia', 
#                                                                                                     'Brazil', 'Spain', 'Belgium'] )]

# df_harmonised = df_harmonised[df_harmonised['Country'].isin(['USA', 'France', 'Germany', 'Canada', 'Australia', 
#                                                     'Brazil', 'Spain', 'Belgium', 'Italy', 'China', 'Japan' ] )]

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

def merge_multiple(list_of_files):
    df = pd.read_csv('data_for_presentation/' + list_of_files[0])
    for filename in list_of_files[1:]:
        df = df.merge(pd.read_csv('data_for_presentation/' + filename), 'outer')
    return df

def dataPreprocessed():
    """Uploading dataframes and useful dictionaries 

    Return:
    -------
        Needed data 
    """
    df_harmonised = merge_multiple(['dfp1.csv', 'dfp2.csv', 'dfp3.csv', 'dfp4_0.csv','dfp4_1.csv','dfp4_2.csv','dfp5.csv','dfp6.csv', 'dfp7.csv', 
    'dfp8.csv', 'dfp9.csv','dfp10.csv', 'dfBelgium.csv', 'dfUSA.csv', 'dfBrazilCanada.csv', 'dfItaly.csv', 'dfJapan.csv', 'dfFrance.csv', 'dfrattrapage0.csv'])

    return df_harmonised, pop_by_country, pop_usa_states, label_gender, code_state, code_country