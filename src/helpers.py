"""
helpers: Helper functions to preprocess data
=============================================

.. moduleauthor:: Lilian MAREY <lilian.marey@ensae.fr>

"""
import numpy as np
from datetime import date, timedelta

# functions for regression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from src.mysettings import firsts_of_the_month

def delete_spaces(s):
    """Deletes all the spaces of a string

    Parameters:
    -----------
    s : str

    Returns
    -----------
        The corresponding string
    """
    s = ''.join(i for i in s if i != ' ')

    return s

def time_delta(date1,date2):
    """Gives the number of days between two dates

    Parameters:
    -----------
    -date1 : str
        the first date (format : 'DD MM YYYY')
    -date2 : str
        the second date (format : 'DD MM YYYY')
    
    Returns:
    -----------
        Either -1 (wrong date format)
        Or the number of days between the two dates (int)
    """

    try:
        day1, month1, year1 = int(date1[:2]), int(date1[3:5]), int(date1[6:10])
        day2, month2, year2 = int(date2[:2]), int(date2[3:5]), int(date2[6:10])
        delta = int((date(year2, month2, day2) - date(year1, month1, day1)).days)
    
    except:
        delta = -1
    
    return delta

def computeDatecodeFromGap(n):
    """Computes a Datecode from a gap_in_day value

    Parameters:
    -----------
    n : int
        the number of days between the wanted date and 2020.01.01

    Returns
    -----------
        datecode : int
            the corresponding datecode
    """
    D = date(2020, 1, 1) + timedelta(days = n)
    D = str(D)
    datecode = int(D[:4] + D[5:7] + D[8:10])

    return datecode

def ageRange(row):
    """Gives the age range label for histogram
    -----------
    row : pandas Series 
        row of a dataset

    Returns
    -----------
       label : str
            the corresponding label
    """
    if row.Age == 100:
        label = '100-104'

    else:
        label = str(row.Age) + '-' + str(row.Age + 9)

    return label

def regionError(df, C, R):
    """Detects if a selected region is not part of one of the selected countries

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    C : str list
        list of selected countries

    R : str list
        list of selected regions

    Returns
    -----------
        bool
        True if the error is detected
    """
    if C == None:
        C = ['USA']
    available_regions = list(regions_of_country(df, C)) + ['All_regions', 'All']

    for region in R:
        if not(region in available_regions):
            return True

    return False

def adaptMetricsInterval(metrics, interval):
    """Transforms the selected metrics and the time interval (daily, weekly, etc.) into a understandable metrics
    Parameters:
    -----------
    metrics : str list
        list of cumulatives selected metrics

    interval : str
        time intervall (daily, weekly, biweekly, monthly, or none)

    Returns
    -----------
        M : str list
            the list of correspondiing metrics
    """
    if interval == None:
        I = ''

    else:
        I = interval

    M = [I + metric if metric in ['Cases', 'Deaths', 'Tests'] 
        else metric for metric in metrics ] 

    return M

def adaptDataframeHistogram(df, max_gap):
    """Builds dataframe used to display histogram
    -----------
    df : Pandas DataFrame
        the original dataframe

    max_gap : int
        the latest authorized gap_in_day value

    Returns
    -----------
       df : Pandas DataFrame
            the corresponding dataframe
    """
    df0 = df[df['gap_in_day'] <= max_gap].copy()

    for age in range(0, 101, 10):
        df1 = df0[df0['Age'] == age]
        df0 = df0.drop(list(df1.index.values)[:-1])
        
    return df0

def dfadaptDateRange(df, start_date, end_date):
    """Slices dataframe keeping values between start-date and end_date

    Parameters:
    -----------
    -df : Pandas DataFrame
        the dataset, asuming that it is sorted by date (with "Date_code")
    -start_date : str 
        format : YYYY MM DD
    -end_date : str 
        format : YYYY MM DD

    Returns:
    -----------
        The coresponding dataset (pandas DataFrame)
    """

    day1, month1, year1 = start_date[8:10], start_date[5:7], start_date[:4]
    day2, month2, year2 = end_date[8:10], end_date[5:7], end_date[:4]

    datecode1, datecode2 = int(year1 + month1 + day1), int(year2 + month2 + day2)

    df0 = df[df['Date_code'] <= datecode2]
    df0 = df0[df0['Date_code'] >= datecode1]

    return df0

def computeRatio(indicator1, indicator2):
    """Computation of ratio of 2 inidcators.
    Parameters:
    -----------
    indicator1 : float
    indicator1 : float

    Returns:
    --------
        Either None (division by zero)
        Or the computed ratio (float)
    """
    try:
        ratio = indicator1 / indicator2

    except ZeroDivisionError:
       return None

    else:
        return ratio

def computeDateFormat(row):
    """Converts Date_code row into dates with US format (YYYY MM DD)

    Parameters:
    -----------
    row : pandas Series 
        row of a dataset
    
    Returns:
    -----------
        The date with the corresponding format (str)
    """
    s = str(row.Date_code)
    
    return s[:4] + '/' + s[4:6] + '/' + s[6:8]

def computeDatecode(row):
    """Creates a datecode (which permits sorting the dates ascending) for each row in the original dataset.
    
    Parameters: 
    -----------
    row : pandas Series 
        row of a dataset
    
    Returns:
    -----------
        Either None (wrong date format)
        Or the computed code (int)
    """
    try:
        day, month, year = row.Date[:2], row.Date[3:5], row.Date[6:10]
        N = int(year + month + day)
    
    except:
        N = None

    return N   

def computeSource(s):
    """Deletes the non digit leters of a word (used to identify 
        different sources of data in the dataset)

    Parameters:
    -----------
    row : pandas Series 
        row of a dataset
    
    Returns:
    -----------
        The corresponding word (str)
    """
    s = ''.join(i for i in s if not i.isdigit())

    return s

def select_data(df, countries_list, regions_list, ages_list, genders_list):
    """Extracts from the dataset the data corresponding to many criterias.
    Parameters:
    -----------
    df : Pandas DataFrame
       dataset 
    
    countries_list : list of str 
       countries to be selected
    
    regions_list : list of str
       regions to be selected

    ages_list : list of int
       age ranges to be selected
    
    genders_list : list of str
       genders to be selected
    
    Returns:
    -----------
        The corresponding dataset (pandas DataFrame)
    """
    df0 = df[df['Country'].isin(countries_list)]
    df1 = df0[df0['Region'].isin(regions_list)]
    df2 = df1[df1['Age'].isin(ages_list)]
    df3 = df2[df2['Sex'].isin(genders_list)]
        
    return df3

def regions_of_country(df, list_of_countries):
    """Gives the list of the regions of a list of countries

    Parameters:
    -----------
    -df : Pandas DataFrame
        the original dataset
        
    -list_of_countries : str list
        the list of the countries to select

    Returns:
    -----------
        The list of the regions (string list)
    """
    if isinstance(list_of_countries, str):
        list_of_countries = [list_of_countries]

    L = list(
            set(
                df[df['Country'].isin(list_of_countries) ]['Region']
                )
            )
    L = sorted(L)
    
    try:
        L.remove('All')

    except ValueError:
        pass
    
    L = np.array(L)

    return L

def meltDataframe(df):
    """Melting the df to get a 'Metric' columns with elements of metrics (list) as values

    Parameters:
    -----------
    df : dataframe
       dataframe to be transformed from wide to long format

    Returns:
    --------
        df : Pandas dataframe
            The coresponding dataframe
    """
    df_long = df.melt(
            id_vars = ['Date', 'Sex', 'Country', 'Region', 'Age', 'Date_code'],
            var_name = 'Metric',
            value_name = 'Value',
            value_vars = ['Cases', 'Deaths', 'Tests', 'CFR', 'Tests by cases']
                    )

    df_long = df_long[df_long['Value'] > 0.001]

    return df_long

def compute_daily_metrics(df, metric):
    """Computes daily metrics from cumulative ones and inserts it in data frame in 'Metric' column

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    metric : the cumulative metric to use for computing daily one

    Returns
    -----------
        df : Pandas Dataframe
        the correspunding dataframe
    """
    df0 = df[df['Metric'] == metric]
    new_metric = 'Daily ' + metric
    identities = list(
                        set(
                            df0['Country - Region - Age - Gender'].values
                            )
                    )

    for ide in identities:
        print(ide)
        df1 = df0[df0['Country - Region - Age - Gender'] == ide]
        L = [(index, row) for index, row in df1.iterrows()]

        new_rows_list = []

        for row_number in range(len(L) - 1):
            row0 = L[row_number][1]
            row1 = L[row_number+1][1]

            for j in range(row0.gap_in_day + 1, row1.gap_in_day + 1):
                new_row = row0.copy()
                new_row.gap_in_day = j
                new_row.Metric = new_metric

                try:
                    new_row.Value = int(
                                        100 * (row1.Value - row0.Value) / (row1.gap_in_day - row0.gap_in_day)
                                        ) / 100

                except ZeroDivisionError:
                    new_row.Value = None

                new_rows_list.append(new_row)
                    
        for i in range(len(new_rows_list)):
            new_row = new_rows_list[i]
            df.loc[-1] = new_row
            df.index = df.index + 1

    print('daily metric computed')
    return df

def start_first_monday(df):
    """Slices the dataset keeping data dated after the first monday available

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    Returns
    -----------
        df : Pandas DataFrame
            the corresponding dataset
    """

    first_date_gap = df.iloc[0].gap_in_day
    next_monday_gap = first_date_gap + (4 - first_date_gap % 7) % 7
    
    df0 = df[df['gap_in_day'] >= next_monday_gap]

    return df0

def compute_weekly_metrics(df, metric):
    """Computes weekly metrics from daily ones and inserts it in data frame in 'Metric' column

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    metric : the metric to use for computing weekly one

    Returns
    -----------
        df : Pandas Dataframe
        the correspunding dataframe
    """
    df0 = df[df['Metric'] == 'Daily ' + metric]
    new_metric = 'Weekly ' + metric
    identities = list(
                    set(
                        df0['Country - Region - Age - Gender'].values
                        )
                    )

    for ide in identities:
        df1 = df0[df0['Country - Region - Age - Gender'] == ide]
        df1 = start_first_monday(df1)
        L = [row for _, row in df1.iterrows()][1:]

        for i in range((len(L) - 1) // 7):
            value = sum([row.Value for row in L[7 * i: 7 * i + 7]])
            
            for j in range(7 * i + 1, 7 * i + 8):

                if j % 7 == 0:
                    row = L[j]
                    new_row = row.copy()
                    new_row['gap_in_day', 'Metric', 'Value'] = row.gap_in_day, new_metric, value
                        
                    df.loc[-1] = new_row
                    df.index = df.index + 1
                else:
                    pass

    print('weekly metric computed')
    return df

def compute_biweekly_metrics(df, metric):
    """Computes biweekly metrics (14 days) from daily ones and inserts it in data frame in 'Metric' column

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    metric : the metric to use for computing biweekly one

    Returns
    -----------
        df : Pandas Dataframe
        the correspunding dataframe
    """
    df0 = df[df['Metric'] == 'Daily ' + metric]
    new_metric = 'Biweekly ' + metric
    identities = list(
                    set(
                        df0['Country - Region - Age - Gender'].values
                        )
                    )

    for ide in identities:
        df1 = df0[df0['Country - Region - Age - Gender'] == ide]
        df1 = start_first_monday(df1)

        L = [row for _, row in df1.iterrows()][1:]

        for i in range((len(L) - 1) // 14):
            value = sum([row.Value for row in L[14 * i: 14 * i + 14]])
            
            for j in range(14 * i + 1, 14 * i + 15):
                if j % 14 == 0:
                    row = L[j]
                    new_row = row.copy()
                    new_row['gap_in_day', 'Metric', 'Value'] = row.gap_in_day, new_metric, value
                        
                    df.loc[-1] = new_row
                    df.index = df.index + 1

    print('biweekly metric computed')
    return df

def start_first_of_the_month(df):
    """Slices the dataset keeping data dated after the first available first day of the month
    and before the last avaible first day of the month

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    Returns
    -----------
        df : Pandas DataFrame
            the corresponding dataset
    """
    first_date_gap = df.iloc[0].gap_in_day
    try:
        first_of_month_gap = min([i - 1 for i in firsts_of_the_month if i - 1 >= first_date_gap])
    except:
        return df

    last_date_gap = df.iloc[-1].gap_in_day
    try:
        last_of_month_gap = min([i - 1 for i in firsts_of_the_month if i >= last_date_gap])
    except:
        return df

    df = df[df['gap_in_day'] >= first_of_month_gap]
    df = df[df['gap_in_day'] <= last_of_month_gap]

    return df

def compute_monthly_metrics(df, metric):
    """Computes monthly metrics from daily ones and inserts it in data frame in 'Metric' column

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    metric : the metric to use for computing monthly one

    Returns
    -----------
        df : Pandas Dataframe
        the correspunding dataframe
    """
    df0 = df[df['Metric'] == 'Daily ' + metric]
    new_metric = 'Monthly ' + metric
    identities = list(
                    set(
                        df0['Country - Region - Age - Gender'].values
                        )
                    )

    for ide in identities:
        df1 = df0[df0['Country - Region - Age - Gender'] == ide]
        df1 = start_first_of_the_month(df1)
        checkpoint = 0
        L = [row for _, row in df1.iterrows()][1:]

        try:
            first_month_number = firsts_of_the_month.index(L[0].gap_in_day)
        except IndexError:
            continue

        for i in range((len(L) - 1) // 30):
            month_number = first_month_number + i
            month_length = firsts_of_the_month[month_number + 1] - firsts_of_the_month[month_number]
            
            value = sum([row.Value for row in L[checkpoint: checkpoint + month_length]])

            checkpoint+= month_length

            row = L[checkpoint-2]
            new_row = row.copy()
            new_row[
                'gap_in_day', 
                'Date_code', 
                'Metric', 
                'Value'
                    ] = row.gap_in_day, computeDatecodeFromGap(row.gap_in_day),new_metric, value                  

            df.loc[-1] = new_row
            df.index = df.index + 1

    print('monthly metric computed')
    return df

def build_time_metrics(df):
    """Builds time metrics from dataframe containing cumulative metrics

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset (assumed to have one 'Metric' column (long format))

    Returns
    -----------
        df : Pandas dataframe
            the corresponding dataframe with the new metrics (long format)
    """
    for metric in ['Deaths', 'Cases', 'Tests']:
        df = compute_daily_metrics(df, metric)
        df = compute_weekly_metrics(df, metric)
        df = compute_biweekly_metrics(df, metric)
        df = compute_monthly_metrics(df, metric)

    return df

def regression(df, degree, forecast, by_pop):
    """Computes polynomal regressions on plotted data

    Parameters:
    -----------
    df : Pandas DataFrame
        the dataset, assumed to be have one 'Metric' column

    degree: int
        degree of the polynomial regression

    forecast : int
        the number of days to forecast 

    by_pop : bool
        if true, consider values py millions inhabitants 
        else consider gross values 
    
    Returns:
    -----------
        regressons_list : (numpy array, numpy array) list
            the list of the several modelizations got by regression
    """

    if by_pop :
        V = 'Value_by_pop'
    else:
        V = 'Value'

    metrics = list(
                    set(
                        df['Metric'].values
                        )
                )

    regressions_list = []

    for metric in metrics:
        df0 = df[df['Metric'] == metric]
        identities = list(
                         set(
                            df0['Country - Region - Age - Gender'].values
                            )
                         )

        for ide in identities:
            df1 = df0[df0['Country - Region - Age - Gender'] == ide]

            x = np.array(
                    df1['gap_in_day']
                        )
            y = np.array(
                    df1[V]
                        )
            X = x[:, np.newaxis]

            model = make_pipeline(
                                PolynomialFeatures(degree),     
                                Ridge()
                                )

            model.fit(X, y)

            x_plot = np.linspace(
                            min(x),
                            max(df1['gap_in_day']) + forecast,
                            1000
                                )
            X_plot = x_plot[:, np.newaxis]

            regressions_list.append(
                                (x_plot, model.predict(X_plot))
                                    )

    return regressions_list

def regression_histogram(df, degree):
    """Computes polynomal regressions on data of the histogram

    Parameters:
    -----------
    df : Pandas DataFrame
        the dataset, assumed to be have one 'Metric' column

    degree: int
        degree of the polynomial regression
    
    Returns:
    -----------
        X, Y : numpy arrays
            the model got by regression
    """
    x = np.array(
            df['Age']
                )
    y = np.array(
            df['Value']
                )

    X = x[:, np.newaxis]

    model = make_pipeline(
                    PolynomialFeatures(degree), 
                    Ridge()
                        )
    model.fit(X, y)

    x_plot = np.linspace(
                        min(x),
                        max(x),
                        1000
                        )
    X_plot = x_plot[:, np.newaxis]

    X, Y = (x_plot + 5, model.predict(X_plot))
                            
    return X, Y