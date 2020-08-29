#COVID-19 : Trends by Age Web app documentation 

 

##Introduction : 

This web app is a contribution to the COVerAGE-DB project. 

COVerAGE-DB project is currently in development. The aim of this project is to build a database of COVID-19 confirmed cases, deaths and tests as reported by statistical agencies, in harmonized age groups. The database is refreashed every day on the web page of the project, and it is free access. 

The app aims illustrating the database with several data vizualisation tools (charts, histograms, maps), but also computing relevant metrics which allow having a better comprehension of the of the progression of the epidemic. 

 

## 1. Charts 

This functionality allows the user to plot charts of selected metrcis for a selected population sample. 

Each curve refers to a specific sample, for a specific metric. Curves refering to the same population have same color. Different symbols correspond to different metrics. 

 

### a. Selecting a sample of population

In the left column, one can select which sample of population to consider for plotting data. The 3 criterias for selecting it are : 

 

-Age ranges : selecting data by age ranges is the main benefit of the app. The dataset proposes 10 age intervals of 10 years from 0 to 100 years old, and an interval of 5 years between 100 and 105 year olds. 

 

-Gender : the user can select data for males, or for females, or for both of them. 

 

-Location : the location part can work two different ways. 

First, when there isn’t any region selected, the app does a comparison by countries. The selected data is this from all the countries selected in the “Country” column, considering their overall population. 

Then, when at least one region is selected, the app does a comparison by regions. The category “Region” regroups many types of country subdivisions (actually regions for France, but states for the USA, e.g.). The selected data is this from all the regions selected in the “Region” column. In order to select a specific region from a specific country, the user should first select the country in question in the “Country” column, then, all the available regions of this country will appear in the scrolling menu of the “Region” column. The user should now select the region in question. 

Countries of “Country” scrolling menu are those for which ther is at least on data in the whole dataset. It is common that some metrics are missing for some countries. *For example, for Brazil, only deaths values are available.* 

It is also common that some regions are not availlable for some countries. Some countries only propose national counts. *For example,* *about* *half of the USA states are available**.* 

 

For all of those categories, the user can select several options at the same time. Then, a curve is plotted in the chart for each population sample. 

 

 

### b. Selecting plotting instructions

In the rectangle above, the user can select plotting options. The user will be able to chose : 

-Metrics : 

Deaths (directly available in the dataset): number of registered deaths. 

Cases (directly available in the dataset) : number of registered diagnosed cases. 

Tests (directly available in the dataset) : number of registered tests. 

CFR (computed) : Case Fatality Ratio : ratio of number of deaths by number of diagnosed cases. It represents a first measure of disease severity, evenif a CFR can only be considered final when all the cases have been resolved (either died or recovered). This ratio is computed only if Deaths and Cases have been reported the same day. 

Tests by cases (computed) : ratio of number of tests by number of diagnosed cases. It represents the mean of the number of tests to do in order to find one case. This ratio is computed only if Tests and Cases have been reported the same day. 

Sometimes, CFR and Tests by cases metrics can’t be computed because of a lack of data. 

 

-Time interval : 

Cumulative (directly available in the dataset) : cumulative data recorded since the beginning of the epidemic. 

Daily (computed) : computed as the average change by day of a value between two consecutive measures. It allows to have one point every day since the date of the first recorded data until the last one. 

Weekly (computed) : computed from daily metrics. It is the sum of the daily values from Monday to the next Sunday, and this value is assigned to this Sunday. 

Biweekly (computed) : computed from daily metrics. It is the sum of the daily values from Monday to the Sunday 14 days after, and the value is assigned to this Sundays. 

Monthly (computed) : computed from daily metrics. It is the sum of the daily values from the 1st of a certain month, until the last day of this month, and the value is assigned to this last day. 

Only Deaths, Cases and Tests are available with daily, weekly, biweekly and monthly intervals. If an other metric (CFR, Tests by cases) is selected, the cumulative option will always be the plotted one. 

 

-Trending and forecasting : the trending method is a polynomial regression on displayed data. The regression is done thanks to Scikitlearn package. The user can choose the degree of the polynom, between 1 and 9. Sometimes, the data matrix is “Ill-conditionned” for this regression so the result may not be accurate. The forecasting option is available only if a trend method is selected. In this case, it displays the computed polynom on a wider interval on x axis. 

 

-Unit : 

None : brute values (not weighted) are displayed. 

Per million inhabitants (computed) : this option is available only for country comparisons. Values are then divided by the population of the country in question, then multiplied by 1 million. 

 

-Date range : the user can select data between two dates. The two selected days are included. 

 

-Log/linear scale : the user can activate a logarithmic scale for y axis (log-10 scale). 

 

-Rug plot : the user can display a rug plot of the data 

 

-Reverse axis : the user can switch x axis with y axis. 

 

-Graph/Table : the user can choose to display the table of selected metrics data for the selected population sample. 

 

## 2. Histogram by Ages 

This functionality allows to plot an histogram by age ranges categories. 

 The options for selecting population samples and plotting instructions are in general the same as those described in Charts part. 

However : 

-for Country, Region, Gender, and Metrics options, the user can select only one element. 

-the selection of age ranges are useless, the histogram will always consider all the available age ranges. 

-Forecast, dividing by population, rug plot, reverse axis and date range options are no longer available. 

The slider at the bottom allows to select a date (week by week) : latest data before this date will be considered to plot the histogram. 

Sometimes, latest data for two different age ranges are not samely recent. In this cases, bins will appear in different colors and the two dates will be put in legend. 

 

## 3. Maps 

 

### a. World map 

This functionality allows to plot a world map with a comparison by country thanks to a color scale. Countries without any data appear white. 

 The options for selecting population samples and plotting instructions are in general the same as those described in Charts part. 

However : 

-for Age ranges, Gender, and Metrics options, the user can select only one element. 

-the selection of countries and regions are useless, the map will always consider all the countries and will do a country comparison. 

-Forecast, dividing by population, log scale, rug plot, reverse axis and date range options are no longer available. 

The slider at the bottom works the same as for the histogram. 

 

### b. USA map 

This functionality allows to plot a USA map with a comparison by states thanks to a color scale. States without any data appear white. 

 The options for selecting population samples and plotting instructions are in general the same as those described in Charts part. 

However : 

\- the user can divide by the population of the state thanks to the “Unit” option. 

-for Age ranges, Gender, and Metrics options, only the first selected item is considered. 

-the selection of countries and regions are useless, the map will always consider all the states of the USA and will do a region comparison. 

-Forecast, log scale, rug plot, reverse axis and date range options are no longer available. 

The slider at the bottom works the same as for the histogram. 

 

## Detected issues 

Sometimes, there are two sources giving different numbers for the same measure. I decided to let them both displayed (UK, all the country, deaths e. g.). 

Data from Texas has been removed because data was false (every data from 2020/07/29 is way too high). 

 

 

 

 