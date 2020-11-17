"""
plots: functions to plot needed data
=============================================

.. moduleauthor:: Lilian MAREY <lilian.marey@ensae.fr>

"""

import pandas as pd
from math import isnan
import plotly.graph_objects as go
import plotly.express as px

from src.mysettings import label_dic, months_list, code_state, code_country, firsts_of_the_month
from src.helpers import select_data, regions_of_country, dfadaptDateRange,computeDateFormat, regression, computeDatecode, adaptDataframeHistogram, ageRange, regression_histogram
from src.preprocess import divide_US_Dataframe



def plot_metrics(df, countries_list, regions_list, ages_list, genders_list, 
                metrics, logvalue, start_date, end_date, rug_value, 
                reverse, trend, forecast, unit, table_option
                ):
    """Plotting several metrics (e.g cases, deaths or tests) depending on criteria (parameters)

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset
        
    countries_list : str list 
        the list of the countries to select

    regions_list : str list
        the list of the region to select

    ages_list : int list
        the list of the age ranges to select

    genders_list : str list
        the list of the genders to select

    metrics : str list
        the metrics that we want to plot

    logvalue : bool
        activates logarithmic scale for y axis

    start_date : str
        the first date to be considered

    end_date : str 
        the last date to be considered

    rug_value : bool
        activates the rug plot option

    reverse : bool
        activates the reverse axis option

    trend : int
        the degree of the polynom we want to modelize

    forecast : int
        the number of forcasted days to display 

    unit : str
        unit used to divide data
    
    table_option : bool
        activates the table displaying option

    Returns:
    --------
        fig : plotly Figure
            the corresponding plot
    """
    if 'All' in regions_list and ('UK' in countries_list) :
        # df0 = delete_multiple_sources(df, ages_list, genders_list)
        df0 = df
    else:
        df0 = df

    df0 = select_data(
                        df, 
                        countries_list, 
                        regions_list, 
                        ages_list, 
                        genders_list
                    )
    
    df0 = dfadaptDateRange(df0, start_date, end_date)
    df0 = df0[df0['Metric'].isin(metrics)]

    df0[['Date_format', 'Metric', 'Value', 'Country', 'Region', 'Age', 'Sex']].to_csv('data/download/data_download.csv')
    
    if df0.empty:
        fig = go.Figure(
                    go.Indicator(
                                title = {"text" : "No data available"}
                                )
                        )

        fig.update_layout(paper_bgcolor = "rgba(188,188,188, 0.33)")

        return fig

    elif table_option:
        fig = go.Figure(data=
                            [
                                go.Table(header = dict( 
                                                        values = list(['Date', 'Metric', 'Value', 'Country', 'Region', 'Age', 'Gender']),
                                                        fill_color = 'rgba(0,131,138,0.5)',
                                                    ),
                                        cells = dict(
                                                    values=[df0.Date_format, df0.Metric, df0.Value, df0.Country, df0.Region, df0.Age, df0.Sex],
                                                    fill_color = 'white',
                                                    )
                                        )
                            ]
                        ) 

        fig.update_layout(autosize=False,
                        width= 1425,
                        height=710,
                        )

        return fig

    else:
        pass

    if unit ==  'Per million inhabitants' and regions_list == ['All']:
        unit_tag = ' (Per million inhabitants)'
        Y = df0['Value_by_pop']
    else:
        unit_tag = ''
        Y = df0['Value']

    if reverse:
        X,Y = Y, df0['gap_in_day']
    else:
        X,Y =  df0['gap_in_day'], Y

    if regions_list == ['All']:
        region_tag = ''
    else:
        region_tag = ' (Regions)'

    fig = px.scatter(df0, 
                    x = X,
                    y = Y,
                    log_y = logvalue, 
                    opacity = 1 / (len(metrics) ** 0.2), 
                    color = 'Country - Region - Age - Gender',
                    symbol = 'Metric', 
                    symbol_sequence = ['circle', 'cross', 'x', 'star-triangle-up', 'star', 'diamond', 'hexagon'],
                    hover_name = 'Country - Region - Age - Gender',
                    labels = {
                        'Date_format' : 'Date', 
                        'gap_in_day' : 'Date',
                        'Value_by_pop' : 'Value by M inhabitants'
                            },
                    hover_data = {
                        'gap_in_day' : True,
                        'Date' : False,
                        'Date_format' : True,
                        'Metric' : True,
                        'Value' : True,
                        'Country - Region - Age - Gender' : False,
                                },
                    title = 'COVID-19 : ' +  ', '.join(metrics) + ' in '+  ', '.join(countries_list) + region_tag,
                    marginal_y = rug_value,
                    template = 'plotly_white',
                    )

    fig.update_traces(marker = dict(
                                    size = 8,
                                    line = dict(
                                                width = .25,
                                                color ='grey'
                                                )
                                    ),
                    selector = dict(mode = 'markers')
                    )
    
    fig.update_layout(
                    autosize = False,
                    width = 1425,
                    height = 710,
                    )

    if reverse:
        fig.update_yaxes(
                        tickvals = [i - 1 for i in firsts_of_the_month],
                        ticktext = [ i + ' 2020' for i in months_list],
                        tickwidth = 2, 
                        tickcolor = 'grey', 
                        ticklen = 10,
                        col = 1,
                        showline = True, 
                        linewidth = 2, 
                        linecolor = 'black',
                        title_font = dict(size = 18), 
                        )

        x_axis = ', '.join(
                        [label_dic[i] for i in metrics]
                        ) + unit_tag

        fig.update_xaxes(
            showline = True, 
            linewidth = 2, 
            linecolor = 'black', 
            title_text = x_axis, 
            title_font = dict(size = 18), 
                        )    
    else:
        fig.update_xaxes(
            tickvals = [i - 1 for i in firsts_of_the_month],
            ticktext = [ i + ' 2020' for i in months_list],
            tickwidth = 2, 
            tickcolor = 'grey', 
            ticklen = 10,
            col = 1,
            showline = True, 
            linewidth = 2, 
            linecolor = 'black',
            title_font = dict(size = 18), 
                        )

        y_axis = ', '.join(
                        [label_dic[i] for i in metrics]
                        ) + unit_tag

        fig.update_yaxes(
            showline = True, 
            linewidth = 2, 
            linecolor = 'black', 
            title_text = y_axis, 
            title_font = dict(size = 18), 
                        )

    if trend>0:
        reg = regression(df0, trend, forecast, unit ==  'Per million inhabitants')

        for X, Y in reg:

            if reverse:
                Y, X = X, Y

            else:
                pass

            fig.add_trace(
                    go.Scatter(
                                x = X, 
                                y = Y,
                                mode = 'lines',
                                line = {
                                        'color' : 'DarkSlateGrey', 
                                        'width' : 2
                                        },
                                name = '',
                                showlegend = False
                                )
                        )
    else:
        pass

    return fig

def plot_histogram(df, country, region, gender, metric, 
                    logvalue, trend, table_option, end_date
                ):
    """Plotting histogram by age ranges depending on criteria (parameters)

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset
        
    country : str  
        the selected_coutry

    region : str 
        the selected region

    gender : str 
        the selected gender

    metric : list
        the selected metric

    logvalue : bool
        activates logarithmic scale for y axis

    trend : int
        the degree of the polynom we want to modelize
    
    table_option : bool
        activates the table displaying option

    end_date : int
        gap_in_day value of the last date to consider

    Returns:
    --------
        fig : plotly Figure
            the corresponding plot
    """
    df0 = df.copy()
    df0 = select_data(
                        df, 
                        [country], 
                        [region], 
                        [i*10 for i in range(11)], 
                        [gender]
                    )
    
    df0 = df0[df0['Metric'] == metric]
    df0 = adaptDataframeHistogram(df0, end_date)

    if df0.empty:
        fig = go.Figure(
                    go.Indicator(
                                title = {"text" : "No data available"}
                                )
                        )
        fig.update_layout(paper_bgcolor = "rgba(188,188,188, 0.33)")

        return fig

    elif table_option:
        fig = go.Figure(data=
                            [
                                go.Table(header = dict( 
                                                        values = list(['Date', 'Metric', 'Value', 'Country', 'Region', 'Age', 'Gender']),
                                                        fill_color = 'rgba(0,131,138,0.5)',
                                                    ),
                                        cells = dict(
                                                    values=[df0.Date_format, df0.Metric, df0.Value, df0.Country, df0.Region, df0.Age, df0.Sex],
                                                    fill_color = 'white',
                                                    )
                                        )
                            ]
                        ) 
        fig.update_layout(
                        autosize=False,
                        width= 1425,
                        height=710,
                        )

        return fig

    else:
        if region == 'All':
            region_tag = ''

        else:
            region_tag = region + ', '

        df0['Age range'] = df0.apply(ageRange, axis = 1)
        df0.sort_values(by = ['Date_code'], ascending=False)

        fig = px.histogram(
                            df0, 
                            x = 'Age',
                            y = 'Value',
                            category_orders = {
                                'Age': [10*i for i in range(11)],
                                            },
                            color = 'Date_format',
                            template = 'simple_white',
                            log_y = logvalue, 
                            title = 'COVID-19 : ' + metric + ' in ' + region_tag + country,
                            nbins = 11,
                            color_discrete_sequence=['rgba(0,131,138,0.87)', 'rgba(0,166,170,0.87)'],
                            labels = {
                                'Date_format' : 'Latest data : ', 
                                    },
                            )
        
        fig.update_layout(
                            autosize = False,
                            width = 1425,
                            height = 710,
                        )
        fig.update_layout(hovermode = "x unified")
        fig.update_traces(hovertemplate = None) 
        fig.update_xaxes(
                        tickvals = [10 * i + 5 for i in range(11)],
                        ticktext = [str(10 * i) + ' - ' + str(10 * i + 9)+ ' y.o' for i in range(10)]+['100 - 105 y.o'],
                        tickwidth = 0, 
                        ticklen = 0,
                        showline = True, 
                        linewidth = 2, 
                        linecolor = 'black',
                        title_font = dict(size = 18), 
                        )
        y_axis = ', '.join(
                            [label_dic[i] for i in [metric]]
                        )
        fig.update_yaxes(
                        showline = True, 
                        linewidth = 2, 
                        linecolor = 'black', 
                        title_text = y_axis, 
                        title_font = dict(size = 18), 
                        )

        if trend > 0:
            X, Y = regression_histogram(df0, trend)
            fig.add_trace(
                        go.Scatter(
                                    x = X, 
                                    y = Y,
                                    mode = 'lines',
                                    line = {
                                            'color' : 'DarkSlateGrey', 
                                            'width' : 2
                                            },
                                    name = '',
                                    showlegend = False
                                    )
                        )
        
        return fig


def plot_usa_map(df, age, gender, metric, selected_unit, end_date):
    """Plotting choropleth map of the USA depending on criteria (parameters)

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    age : int
        the age range to select

    gender : str
        the genders to select

    metric : str
        the metric that we want to plot

    selected_unit : str
        the selected unit with which data is divided

    end_date : str 
        the last date to be considered

    Returns:
    --------
        fig : plotly Figure
            the corresponding plot
    """
    States = regions_of_country(df,['USA'])
    df0 = select_data(
                        df, 
                        ['USA'], 
                        States, 
                        [age], 
                        [gender]
                    )

    df0['Date_code'] = df0.apply(computeDatecode, axis = 1)
    df0['Date_format'] = df0.apply(computeDateFormat, axis = 1)
    df0 = df0.sort_values(by = ['Date_code'])

    df0 = df0[df0['Metric'] == metric]
    df0 = df0[df0['gap_in_day'] <= end_date]

    values_list = []
    dates_list = []

    for state in States:
        df1 = select_data(
                            df0, 
                            ['USA'], 
                            [state], 
                            [age], 
                            [gender]
                        )

        df1 = divide_US_Dataframe(df1, selected_unit)

        if len(df1) == 0:
            values_list.append('nan')
            dates_list.append('nan')

        else:
            index = len(df1) - 1
            value = list(df1['Value'])[index]
            date = list(df1['Date_format'])[index]

            while isnan(value) and index > 0:
                index -= 1
                value = list(df1['Value'])[index]
                date = list(df1['Date_format'])[index]

            values_list.append(value)
            dates_list.append(date)

    Code = [code_state[state] for state in States]

    df2 = pd.DataFrame(
                {'state' : States, 'code' : Code, 'Value' : values_list, 'Date' : dates_list}
                    )

    for col in df2.columns:
        df2[col] = df2[col].astype(str)

    df2['text'] = df2['state'] + '<br>' + 'Value : ' + df2['Value']  + '<br>' + df2['Date'] + '<br>' + metric

    fig = go.Figure(
            data=go.Choropleth(
                                locations = df2['code'],
                                z = df2['Value'].astype(float),
                                locationmode = 'USA-states',
                                colorscale = 'Reds',
                                autocolorscale = False,
                                text = df2['text'], 
                                marker_line_color = 'rgb(0, 131, 138)', 
                                colorbar_title = metric,
                                hoverinfo = 'text',
                                )
                    )

    if selected_unit ==  'Per million inhabitants':
        unit_tag = ' (Per million inhabitants)'

    else:
        unit_tag = ''

    fig.update_layout(
                        title_text = 'Number of ' +  metric + ' by state ' + 'for ' +
                        str(age) + ' - ' + str(age + 9) + ' year olds' + unit_tag,
                        geo = dict(
                                    scope='usa',
                                    projection = go.layout.geo.Projection(type = 'albers usa'),
                                    showlakes = False,
                                    lakecolor = 'rgb(255, 255, 255)'
                                    ),
                    ),

    fig.update_layout(
                        autosize=False,
                        width= 1425,
                        height=710
                    )

    return fig

def plot_world_map(df, age, gender, metric, selected_unit, end_date):
    """Plotting choropleth world map depending on criteria (parameters)

    Parameters:
    -----------
    df : Pandas DataFrame
        the original dataset

    age : int
        the age range to select

    gender : str
        the genders to select

    metric : str
        the metric that we want to plot

    selected_unit : str
        the selected unit with which data is divided

    end_date : str 
        the last date to be considered

    Returns:
    --------
        fig : plotly Figure
            the corresponding plot
    """

    Countries = list(
                    set(
                        df['Country']
                        )
                    )

    for country in ['England and Wales', 'England', 'Scotland', 'Northern Ireland', 'Senegal', 'Eswatini']: # England, Scotland, N. Ireland are already in UK country
        try:
            Countries.remove(country)

        except ValueError:
            pass

    df0 = select_data(
                        df, 
                        Countries, 
                        ['All'], 
                        [age], 
                        [gender]
                    )
    df0['Date_code'] = df0.apply(computeDatecode, axis = 1)
    df0 = df0.sort_values(by = ['Date_code'])
    df0['Date_format'] = df0.apply(computeDateFormat, axis = 1)
    df0 = df0[df0['Metric'] == metric]
    df0 = df0[df0['gap_in_day'] <= end_date]

    values_list = []
    dates_list = []
    
    for country in Countries:
        df1 = select_data(
                            df0, 
                            [country], 
                            ['All'], 
                            [age], 
                            [gender]
                        )

        if selected_unit == 'Per million inhabitants':
            column = 'Value_by_pop'
        else:
            column = 'Value'

        if len(df1) == 0:
            values_list.append('nan')
            dates_list.append('nan')
        else:
            index = len(df1)-1
            value = list(df1[column])[index]
            date = list(df1['Date_format'])[index]

            while isnan(value) and index > 0:
                index -= 1
                value = list(df1[column])[index]
                date = list(df1['Date_format'])[index]

            values_list.append(value)
            dates_list.append(date)

    Code = [code_country[country] for country in Countries]
    df2 = pd.DataFrame(
                {'Country' : Countries, 'code' : Code, 'Value' : values_list, 'Date' : dates_list}
                    )

    for col in df2.columns:
        df2[col] = df2[col].astype(str)

    df2['text'] = df2['Country'] + '<br>' + 'Value : ' + df2['Value']  + '<br>' + df2['Date'] + '<br>' + metric

    fig = go.Figure(
            data = go.Choropleth(
                                    locations = df2['code'],
                                    z = df2['Value'],
                                    hoverinfo = 'text',
                                    text = df2['text'],
                                    colorscale = 'Reds',
                                    marker_line_color = 'rgb(0, 131, 138)',
                                    colorbar_title = metric,
                                )
                    )

    if selected_unit ==  'Per million inhabitants':
        unit_tag = ' (Per million inhabitants)'
    else:
        unit_tag = ''

    fig.update_layout(
                        title_text = 'Number of ' +  metric + ' by country ' + 'for ' +
                                str(age) + ' - ' + str(age + 9) + ' year olds' + unit_tag,
                        geo = dict(
                                showframe = False,
                                showcoastlines = True,
                                ),
                   )
    fig.update_layout(
                        autosize = False,
                        width = 1425,
                        height = 710
                    )

    return fig

def build_download_file(df, countries_list, regions_list, ages_list, genders_list, 
                metrics, start_date, end_date
                ):


    if 'All' in regions_list and ('UK' in countries_list) :
            # df0 = delete_multiple_sources(df, ages_list, genders_list)
            df0 = df
    else:
        df0 = df

    df0 = select_data(
                        df, 
                        countries_list, 
                        regions_list, 
                        ages_list, 
                        genders_list
                    )
    
    df0 = dfadaptDateRange(df0, start_date, end_date)
    df0 = df0[df0['Metric'].isin(metrics)]
    
    df0 = df0[['Date_format', 'Metric', 'Value', 'Country', 'Region', 'Age', 'Sex']]

    print(df0.head())

    # elif table_option:
    #     fig = go.Figure(data=
    #                         [
    #                             go.Table(header = dict( 
    #                                                     values = list(['Date', 'Metric', 'Value', 'Country', 'Region', 'Age', 'Gender']),
    #                                                     fill_color = 'rgba(0,131,138,0.5)',
    #                                                 ),
    #                                     cells = dict(
    #                                                 values=[df0.Date_format, df0.Metric, df0.Value, df0.Country, df0.Region, df0.Age, df0.Sex],
    #                                                 fill_color = 'white',
    #                                                 )
    #                                     )
    #                         ]
    #                     ) 

        # fig.update_layout(autosize=False,
        #                 width= 1425,
        #                 height=710,
        #                 )

    return None