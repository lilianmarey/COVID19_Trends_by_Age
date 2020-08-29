"""
app: Module to run the app
=============================================

.. moduleauthor:: Lilian MAREY <lilian.marey@ensae.fr>

"""
import pandas as pd

# global settings
from src.mysettings import *

# helper functions
from src.helpers import delete_spaces


##########################################
# Load in memory needed data :
# Harmonised data on cases, deaths, tests
# Population data (worldwide)
# US states population

print('Importation of population datasets...')
pop_by_country = pd.read_csv(POPULATION_DATA_PATH, sep = ';')
pop_usa_states =  pd.read_csv(USSTATES_DATA_PATH, sep = ';')
print('Done')

###################################
# Functions

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
