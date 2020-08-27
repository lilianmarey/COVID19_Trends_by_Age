"""
app: Module to run the app
=============================================

.. moduleauthor:: Lilian MAREY <lilian.marey@ensae.fr>

"""
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

from datetime import date

from src.mysettings import months_list, firsts_of_the_month
from src.helpers import regions_of_country, regionError, adaptMetricsInterval
import src.preprocess as pp
import src.plots as plt 

##########################################
# Import needed data

print('data importation : ')

df, pop_by_country, pop_usa_states, label_gender, code_state, code_country = pp.dataPreprocessed()

print('done')

##########################################
# Create the hole app layout

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            className = 'fill_void'
            ),  

     html.Div(
         [
             html.Img(
                 src = '/assets/logo3.png', 
                 style = {'height':'100%', 'width':'100%'}
                 )
        ],
        className = 'logo0'
            ), 

     html.Div(
         [
             html.H2(
                 children = 'COVID-19: Trends by Age'
                 )
        ],
        className = 'header'
            ),

    html.Div(
        className = 'rectangle_top'
             ),

    html.Div(
        className = 'rectangle_left'
             ),

    html.Div(
        className = 'rectangle_corner'
             ),

     html.Div(
         [
             html.H5(children = 'COVID-19 Web App')
        ],
        className = 'description1'
            ), 

    html.Div(
        [
            dcc.Markdown('''
            [About this project](https://dev.azure.com/LMAREY/Covid_age)          
            [About the COVerAGE project](https://github.com/timriffe/covid_age) \n         
            [Download the complete COVerAge dataset](https://osf.io/mpwjq/)
            ''') 
        ],
        className = 'description2'
            ),

     html.Div(
        id = 'country_column_title',
        children = [
             html.H4(children = 'Country: ')
                    ],
        className = 'country_column_title'
            ), 

    html.Div(
        id = 'country_column',
        children = [
            dcc.Dropdown(
                id = 'country_checklist',
                options = [
                    {'label' : i, 'value' : i} for i in 
                        sorted(list(
                                    set(
                                        df['Country']
                                        )
                                    )
                                )
                        ],
                value = ['France'],
                multi = True
                        )
                    ],
        className = 'country_column'
            ),

     html.Div(
        id = 'region_column_title',
        children = [
             html.H4(
                 children = 'Region: '
                    )
                    ],
        className = 'region_column_title'
            ), 

    html.Div(
        id = 'region_column',
        children = [
            dcc.Dropdown(
                id = 'region_checklist',
                value = ['All'],
                multi = True
                        )
                    ],
        className = 'region_column'
            ),

     html.Div(
        id = 'age_row_title',
        children = [
             html.H4(children = 'Age range: ')
                    ],
        className = 'age_row_title'
            ), 

    html.Div(
        id = 'age_row',
        children = [
            dcc.Dropdown(
                id = 'age_checklist',
                options = [{'label' : 'All ranges', 'value' : 888}] + [{'label' : str(10 * i) + '-' + str(10 * i + 9) + ' year olds', 'value' : 10 * i} for i in range(10)]
                + [{'label' : str(100 ) + '-' + str(104) + ' year olds', 'value' : 100}],
                value = [10 * i for i in range(4,9)],
                multi = True
                        )
                    ],
        className = 'age_row'
            ),

     html.Div(
        id = 'metric_row_title',
        children = [
             html.H4(children = 'Metrics: ')
                    ],
        className = 'metric_row_title'
            ), 

    html.Div(
        id = 'metric_row',
        children = [
            dcc.Dropdown(
                id = 'metric_checklist',
                options = [
                {'label' : 'Deaths', 'value' : 'Deaths'},
                {'label' : 'Cases', 'value' : 'Cases'},
                {'label' : 'CFR' , 'value' : 'CFR'},
                {'label' : 'Tests by cases' , 'value' : 'Tests by cases'},
                {'label' : 'Tests' , 'value' : 'Tests'},
                        ],
                value = ['Deaths'],
                multi = True
                        )
                    ],
        className = 'metric_row'
        ),

     html.Div(
        id = 'time_scale_row_title',
        children = [
             html.H4(children = 'Time interval: ')
                    ],
        className = 'time_scale_row_title'
            ), 

    html.Div(
        id = 'time_scale_row',
        children = [
            dcc.Dropdown(
                id = 'time_scale_checklist',
                options = [
                {'label' : 'Cumulative', 'value' : ''},
                {'label' : 'Daily', 'value' : 'Daily '},
                {'label' : 'Weekly', 'value' : 'Weekly '},
                {'label' : 'Biweekly', 'value' : 'Biweekly '},
                {'label' : 'Monthly', 'value' : 'Monthly '},
                    ],
                value = '',
                multi = False
                        )
        ],
        className = 'time_scale_row'
        ),

     html.Div(
         [
             html.H4(children = 'Gender: ')
        ],
        className = 'gender_row_title'
            ), 

    html.Div(
        [
            dcc.Dropdown(
                id = 'gender_checklist',
                options = [
                {'label' : label_gender[i] , 'value' : i} for i in ['b', 'f', 'm']
                    ],
                value = ['b'],
                multi = True
                        )
            ],
            className = 'gender_row'
            ),

    html.Div(
        id = 'scale_row',
        children = [
            dcc.RadioItems(
                id = 'scale_option',
                options = [
                {'label' : 'Log scale' , 'value' : 'log'},
                {'label' : 'Linear scale' , 'value' : 'lin'} 
                        ],
                value = 'lin'
                        )
                    ],
        className = 'scale_row'
            ),

    html.Div(
        id = 'rug_row',
        children = [
            dcc.Checklist(
                id = 'rug_checklist',
                options = [
                    {'label': 'Rug plot', 'value': 'rug'},
                        ],
                value = []
                        )
                    ], 
        className = 'rug_row'
            ),

    html.Div(
        id = 'select_reverse_axis',
        children = [
            dcc.Checklist(
                id = 'reverse_axis_button',
                options = [
                    {'label' : 'Reverse axis' , 'value' : 'reverse'}
                            ],
                value = []
                        )
                    ],
        className = 'select_reverse_axis'
            ),

    html.Div(
        [
            dcc.RadioItems(
                id = 'map_button',
                options = [
                        {'label' : 'Chart' , 'value' : 'chart'},
                        {'label' : 'Histogram by Ages' , 'value' : 'hist'},
                        {'label' : 'World Map' , 'value' : 'worldmap'},
                        {'label' : 'USA Map' , 'value' : 'usamap'} 
                            ],
                value = 'chart',
                labelStyle = {'display': 'block'}
                        )
        ],
        className = 'select_map'
            ),

     html.Div(
        id = 'date_range_title',
        children = [
             html.H4(children='Date range: ')
                    ],
        className = 'date_range_title'
            ),   

    html.Div(
        id = 'date_range_div',
        children = [
            dcc.DatePickerRange(
                id = 'date_range',
                start_date = date(2020, 1, 1),
                end_date = date(2020, 8, 6),
                min_date_allowed = date(2020, 1, 1),
                display_format = 'MM DD YYYY',
                initial_visible_month = '2020 08 07'                     
                                )
                    ],
        className = 'date_range'
            ),

     html.Div(
        id = 'trend_row_title',
        children = [
             html.H4(children='Trend method : ')
                    ],
        className = 'trend_row_title'
            ), 

    html.Div(
        id = 'trend_row',
        children = [
            dcc.Dropdown(
                id = 'trend_checklist',
                options = [
                {'label' : i , 'value' : i} for i in ['No trend'] + [str(i) + " Degree Polynom" for i in range(1, 10)]
                        ],
                value = 'No trend',
                multi = False
                        )
                    ],
        className = 'trend_row'
        ), 

     html.Div(
        id = 'forecast_row_title',
        children = [
             html.H4(children = 'Forecast (days) : ')
                    ],
        className = 'forecast_row_title'
            ), 

    html.Div(
        id = 'forecast_row',
        children = [
            dcc.Slider(
                    id = 'forecast_slider',
                    min = 0,
                    max = 10,
                    marks = {i: '{}'.format(i) for i in range(11)},
                    value = 0,
                    )  
                    ],
        className = 'forecast_row'
        ), 

     html.Div(
        id = 'unit_row_title',
        children = [
             html.H4(children = 'Unit: ')
                    ],
        className = 'unit_row_title'
            ), 

    html.Div(
        id = 'unit_row',
        children = [
            dcc.Dropdown(
                id = 'unit_checklist',
                options = [
                {'label' : 'None' , 'value' : 'None'},
                {'label' : 'Per million inhabitants (available for all countries & USA states)', 'value' : 'Per million inhabitants'},
                        ],
                value = 'None',
                multi = False
                        )
                    ],
        className = 'unit_row'
        ), 

    html.Div(
        [
            dcc.Graph(
                id = 'plot', 
                config = {'scrollZoom' : True}, 
                    )
        ], 
        className = 'main_graph'
            ),

    # html.Div(
    #         [
    #             dcc.Markdown('''
    #             This app has been the object of [Lilian Marey](https://www.linkedin.com/in/lilian-marey-5b656b193/)'s internship at Scor
    #             ''') 
    #         ],
    #         className = 'description3'
    #             ),

    html.Div(
        id = 'select_table',
        children = [
            dcc.RadioItems(
                id = 'table_button',
                options = [
                        {'label' : 'Graph' , 'value' : 'graph'},
                        {'label' : 'Table' , 'value' : 'table'} 
                            ],
                value = 'graph'
                        )
                    ],
        className = 'select_table'
            ),

    html.Div(
        id = 'bottom_slider',
        style = {'display': 'none'},
        children = [
                    dcc.Slider(
                            id='date_grad_hist_slider',
                            # marks={30*i: 'gap in day = {}'.format(30*i) for i in range(7)},
                            min = 0,
                            max = 246,
                            value = 230,
                            step = 7,
                            updatemode = 'drag',
                            marks = {
                                    firsts_of_the_month[i] : months_list[i] + ' 2020' for i in range(9)
                                    }                           
                                )
                    ],
        className = 'date_grad_hist'
        ), 

     html.Div(
         [
             html.Img(
                 src = '/assets/logo5.png', 
                 style = {'height':'100%', 'width':'100%'}
                 )
        ], 
        className = 'logo1'
            ), 

    ]
                )


@app.callback(
    [
    Output('country_column_title', component_property = 'style'),
    Output('country_column', component_property = 'style'),
    Output('region_column_title', component_property = 'style'),
    Output('region_column', component_property = 'style'),
    Output('age_row_title', component_property = 'style'),
    Output('age_row', component_property = 'style'),
    Output('metric_row_title', component_property = 'style'),
    Output('metric_row', component_property = 'style'),
    Output('time_scale_row', component_property = 'style'),
    Output('time_scale_row_title', component_property = 'style'),
    Output('scale_row', component_property = 'style'),
    Output('rug_row', component_property = 'style'),
    Output('select_reverse_axis', component_property = 'style'),
    Output('date_range_div', component_property = 'style'),
    Output('date_range_title', component_property = 'style'),
    Output('trend_row', component_property = 'style'),
    Output('trend_row_title', component_property = 'style'),
    Output('forecast_row', component_property = 'style'),
    Output('forecast_row_title', component_property = 'style'),
    Output('unit_row', component_property = 'style'),
    Output('unit_row_title', component_property = 'style'),
    Output('select_table', component_property = 'style'),
    Output('bottom_slider', component_property = 'style'),
    Output('country_checklist', component_property = 'multi'),
    Output('region_checklist', component_property = 'multi'),
    Output('age_checklist', component_property = 'multi'),
    Output('metric_checklist', component_property = 'multi'),
    Output('gender_checklist', component_property = 'multi'),


    ],
    [
        Input('map_button', 'value')
    ]
            )
def global_display_callback(selected_graph):
    """Sets the grey part of the global displaying

    Parameters:
    -----------
    selected_graph : str 
        the graph to plot

    Returns:
    --------
    display_option : dict
        the displaying option of the html div
    """

    if selected_graph == 'chart':
        display_option = [{'opacity': 1} for i in range(22)]+[{'opacity': .2}, True, True, True, True, True]

    elif selected_graph == 'hist':
            display_option = [
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                {'opacity': 1},
                                False,
                                False,
                                True,
                                False,
                                False
                            ]

    else:   
        display_option = [     
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                {'opacity': 1},
                                {'opacity': 0.2},
                                {'opacity': 1},
                                False,
                                False,
                                False,
                                False,
                                False
                            ]


    return display_option

@app.callback(
    Output('region_checklist', 'options'),
    [
        Input('country_checklist', 'value')
    ]
            )
def second_checklist_callback(selected_countries):
    """Gives the regions checklist options from selected_countries

    Parameters:
    -----------
    selected_countries : str list
        list of the countries selcted in the coresponding checklist

    Returns:
    --------
    options : dict list
        the "options" argument of the regions checklist
    """
    if selected_countries == None:
        selected_countries = ['USA']
    regions_list = regions_of_country(df, selected_countries)
    options = [{'label' : 'All regions', 'value' : 'All_regions'}] + [{'label' : i, 'value' : i} for i in regions_list]

    return options

@app.callback(
    Output('plot', 'figure'),
    [
    Input('country_checklist', 'value'), 
    Input('region_checklist', 'value'), 
    Input('age_checklist', 'value'), 
    Input('metric_checklist', 'value'),
    Input('time_scale_checklist', 'value'), 
    Input('scale_option', 'value'), 
    Input('gender_checklist', 'value'),
    Input('map_button', 'value'), 
    Input('date_range', 'start_date'), 
    Input('date_range', 'end_date'), 
    Input('rug_checklist', 'value'),
    Input('reverse_axis_button', 'value'),
    Input('trend_checklist', 'value'),
    Input('forecast_slider', 'value'),
    Input('unit_checklist', 'value'),
    Input('table_button', 'value'),
    Input('date_grad_hist_slider', 'value')
    ]
            )
def graph_callback(
    selected_countries, selected_regions, selected_ages, 
    selected_metrics, selected_interval, selected_scale,
    selected_genders, selected_graph, start_date, end_date, 
    rug_value, reverse_axis_value, selected_trend, forecast, 
    selected_unit, chart_or_table, hist_end_date
                ):
    """Plotting what has to be displayed (charts or map)

    Parameters:
    -----------        
    selected_countries : str list 
        the list of the countries to select

    selected_regions : str list
        the list of the region to select

    selected_ages : int list
        the list of the age ranges to select

    selected_metrics : str list
        the metrics that we want to plot
    
    selected_interval : str
        the time interval used to display data (Cumulative, Daily, Weekly, etc.)

    selected_scale : str
        defines wether y axis has logarithmic or linear scale ('lin' for linear, everything else for logarithmic)

    selected_genders : str list
        the list of the genders to select

    selected_graph : str
        defines wether the USA map or the charts are displayes ('map' for the map, everything else for charts)

    start_date : str
        the first date to be considered

    end_date : str 
        the last date to be considered

    rug_value : bool
        activates the rug plot option

    reverse_axis_value : bool
        activates the reverse axis option
    
    selected_trend : str
        the trend that we want to plot

    forecast : int
        the number of forcasted days to display 

    selected_unit : str
        the selected unit with which data is divided

    chart_or_table : str
        activates the table display option
        
    hist_end_date : int
        the last date to be considered

    Returns:
    --------
    fig : plotly Figure
        the corresponding plot
    """
    if isinstance(selected_countries, str):
        C = [selected_countries]
    else:
        C = selected_countries
    if selected_countries in [[], None]:
        C = ['France']
    else:
        pass

    if isinstance(selected_regions, str):
        R = [selected_regions]
    else:
        R = selected_regions
    if selected_regions in [[], None] or regionError(df, selected_countries, R):
        R = ['All']
    elif 'All_regions' in selected_regions:
        regions_list = list(regions_of_country(df, C))
        if regions_list == []:
            R = ['All']
        else:
            R = regions_list
    else:
        pass

    if  isinstance(selected_ages, int):
        A = [selected_ages]
    else:
        A = selected_ages
    if selected_ages in [[], None]:
        A = [i * 10 for i in range(4, 9)]
    elif 888 in A:
        A = [10 * i for i in range(11)]
    else:
        pass

    if isinstance(selected_metrics, str):
        M = [selected_metrics]
    else:
        M = selected_metrics
    if selected_metrics in [[], None]:
        M = ['Deaths']
    else:
        M = adaptMetricsInterval(M, selected_interval)

    if selected_scale == 'lin':
        S = False
    else:
        S = True

    if isinstance(selected_genders, str):
        G = [selected_genders]
    else:
        G = selected_genders
    if selected_genders in [[], None]:
        G = ['b']
    else:
        pass

    if rug_value == ['rug']:
        rug = 'rug'
    else:
        rug = ''

    if reverse_axis_value == ['reverse']:
        reverse = True
    else:
        reverse = False

    if selected_trend in ['No trend', None]:
        trend = 0
    else:
        trend = int(selected_trend[0])
    
    if chart_or_table == 'table':
        T = True
    else:
        T = False
    
    if selected_graph == 'worldmap':
        fig = plt.plot_world_map(df, A[0], G[0], M[0], selected_unit, hist_end_date)

        return fig

    elif selected_graph == 'usamap':
        fig = plt.plot_usa_map(df, A[0], G[0], M[0], selected_unit, hist_end_date)

        return fig

    elif selected_graph == 'hist':
        if R == []:
            R = ['All']
        else:
            pass
        fig = plt.plot_histogram(df, C[0], R[0], G[0], M[0], S, trend, T, hist_end_date)

        return fig

    else:
        fig = plt.plot_metrics(
                                df, C, R, A, G, M, S, 
                                start_date, end_date, 
                                rug, reverse, trend, forecast, 
                                selected_unit, T)

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)