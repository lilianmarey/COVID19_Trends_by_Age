"""
mysettings: Module with global settings
======================================

.. moduleauthor:: Jean-Claude RAZAFINDRAKOTO <jrazafindrakoto@scor.com>

"""
import pathlib
import plotly.io as pio
from matplotlib import image

# Relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../data').resolve()

########################
# PATHS for needed data :
# Harmonised data on cases, deaths, tests
# Population data (worldwide)
# US states population

HARMONISED_DATA_PATH = DATA_PATH.joinpath('Output_10.csv')
POPULATION_DATA_PATH = DATA_PATH.joinpath('./population_datasets/Countries_pop.csv')
USSTATES_DATA_PATH = DATA_PATH.joinpath('./population_datasets/States_of_the_USA_pop.csv')

#dictionary for genders label
label_gender = {
    'b' : 'Both sexes',
    'm' : 'Males',
    'f' : 'Females'
                }

#dictionary for codes of the US states
code_state = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
    }


#dictionary for codes of the world countries (Alpha-3 Code)
code_country = {
    'Afghanistan': 'AFG',
    'Albania': 'ALB',
    'Algeria': 'DZA',
    'American Samoa': 'ASM',
    'Andorra': 'AND',
    'Angola': 'AGO',
    'Anguilla': 'AIA',
    'Antarctica': 'ATA',
    'Antigua and Barbuda': 'ATG',
    'Argentina': 'ARG',
    'Armenia': 'ARM',
    'Aruba': 'ABW',
    'Australia': 'AUS',
    'Austria': 'AUT',
    'Azerbaijan': 'AZE',
    'Bahamas': 'BHS',
    'Bahrain': 'BHR',
    'Bangladesh': 'BGD',
    'Barbados': 'BRB',
    'Belarus': 'BLR',
    'Belgium': 'BEL',
    'Belize': 'BLZ',
    'Benin': 'BEN',
    'Bermuda': 'BMU',
    'Bhutan': 'BTN',
    'Bolivia': 'BOL',
    'Bonaire, Sint Eustatius and Saba': 'BES',
    'Bosnia and Herzegovina': 'BIH',
    'Botswana': 'BWA',
    'Bouvet Island': 'BVT',
    'Brazil': 'BRA',
    'British Indian Ocean Territory': 'IOT',
    'Brunei Darussalam': 'BRN',
    'Bulgaria': 'BGR',
    'Burkina Faso': 'BFA',
    'Burundi': 'BDI',
    'Cambodia': 'KHM',
    'Cameroon': 'CMR',
    'Canada': 'CAN',
    'Cape Verde': 'CPV',
    'Cayman Islands': 'CYM',
    'Central African Republic': 'CAF',
    'Chad': 'TCD',
    'Chile': 'CHL',
    'China': 'CHN',
    'Christmas Island': 'CXR',
    'Cocos (Keeling) Islands': 'CCK',
    'Colombia': 'COL',
    'Comoros': 'COM',
    'Congo': 'COG',
    'Congo, the Democratic Republic of the': 'COD',
    'Cook Islands': 'COK',
    'Costa Rica': 'CRI',
    'Ivory Coast': 'CIV',
    'Croatia': 'HRV',
    'Cuba': 'CUB',
    'Cyprus': 'CYP',
    'Czechia': 'CZE',
    'Denmark': 'DNK',
    'Djibouti': 'DJI',
    'Dominica': 'DMA',
    'Dominican Republic': 'DOM',
    'Ecuador': 'ECU',
    'Egypt': 'EGY',
    'El Salvador': 'SLV',
    'Equatorial Guinea': 'GNQ',
    'Eritrea': 'ERI',
    'Estonia': 'EST',
    'Ethiopia': 'ETH',
    'Falkland Islands (Malvinas)': 'FLK',
    'Faroe Islands': 'FRO',
    'Fiji': 'FJI',
    'Finland': 'FIN',
    'France': 'FRA',
    'French Guiana': 'GUF',
    'French Polynesia': 'PYF',
    'French Southern Territories': 'ATF',
    'Gabon': 'GAB',
    'Gambia': 'GMB',
    'Georgia': 'GEO',
    'Germany': 'DEU',
    'Ghana': 'GHA',
    'Gibraltar': 'GIB',
    'Greece': 'GRC',
    'Greenland': 'GRL',
    'Grenada': 'GRD',
    'Guadeloupe': 'GLP',
    'Guam': 'GUM',
    'Guatemala': 'GTM',
    'Guernsey': 'GGY',
    'Guinea': 'GIN',
    'Guinea-Bissau': 'GNB',
    'Guyana': 'GUY',
    'Haiti': 'HTI',
    'Honduras': 'HND',
    'Hong Kong': 'HKG',
    'Hungary': 'HUN',
    'Iceland': 'ISL',
    'India': 'IND',
    'Indonesia': 'IDN',
    'Iran, Islamic Republic of': 'IRN',
    'Iraq': 'IRQ',
    'Ireland': 'IRL',
    'Isle of Man': 'IMN',
    'Israel': 'ISR',
    'Italy': 'ITA',
    'Jamaica': 'JAM',
    'Japan': 'JPN',
    'Jersey': 'JEY',
    'Jordan': 'JOR',
    'Kazakhstan': 'KAZ',
    'Kenya': 'KEN',
    'Kiribati': 'KIR',
    'South Korea': 'KOR',
    'Kuwait': 'KWT',
    'Kyrgyzstan': 'KGZ',
    'Latvia': 'LVA',
    'Lebanon': 'LBN',
    'Lesotho': 'LSO',
    'Liberia': 'LBR',
    'Libya': 'LBY',
    'Liechtenstein': 'LIE',
    'Lithuania': 'LTU',
    'Luxembourg': 'LUX',
    'Macao': 'MAC',
    'Macedonia, the former Yugoslav Republic of': 'MKD',
    'Madagascar': 'MDG',
    'Malawi': 'MWI',
    'Malaysia': 'MYS',
    'Maldives': 'MDV',
    'Mali': 'MLI',
    'Malta': 'MLT',
    'Marshall Islands': 'MHL',
    'Martinique': 'MTQ',
    'Mauritania': 'MRT',
    'Mauritius': 'MUS',
    'Mayotte': 'MYT',
    'Mexico': 'MEX',
    'Micronesia, Federated States of': 'FSM',
    'Moldova, Republic of': 'MDA',
    'Monaco': 'MCO',
    'Mongolia': 'MNG',
    'Montenegro': 'MNE',
    'Montserrat': 'MSR',
    'Morocco': 'MAR',
    'Mozambique': 'MOZ',
    'Myanmar': 'MMR',
    'Namibia': 'NAM',
    'Nauru': 'NRU',
    'Nepal': 'NPL',
    'Netherlands': 'NLD',
    'New Caledonia': 'NCL',
    'New Zealand': 'NZL',
    'Nicaragua': 'NIC',
    'Niger': 'NER',
    'Nigeria': 'NGA',
    'Niue': 'NIU',
    'Norfolk Island': 'NFK',
    'Northern Mariana Islands': 'MNP',
    'Norway': 'NOR',
    'Oman': 'OMN',
    'Pakistan': 'PAK',
    'Palau': 'PLW',
    'Palestine': 'PSE',
    'Panama': 'PAN',
    'Papua New Guinea': 'PNG',
    'Paraguay': 'PRY',
    'Peru': 'PER',
    'Philippines': 'PHL',
    'Pitcairn': 'PCN',
    'Poland': 'POL',
    'Portugal': 'PRT',
    'Puerto Rico': 'PRI',
    'Qatar': 'QAT',
    'Romania': 'ROU',
    'Russian Federation': 'RUS',
    'Rwanda': 'RWA',
    'Saint Helena, Ascension and Tristan da Cunha': 'SHN',
    'Saint Kitts and Nevis': 'KNA',
    'Saint Lucia': 'LCA',
    'Saint Martin (French part)': 'MAF',
    'Saint Pierre and Miquelon': 'SPM',
    'Saint Vincent and the Grenadines': 'VCT',
    'Samoa': 'WSM',
    'San Marino': 'SMR',
    'Sao Tome and Principe': 'STP',
    'Saudi Arabia': 'SAU',
    'Senegal': 'SEN',
    'Serbia': 'SRB',
    'Seychelles': 'SYC',
    'Sierra Leone': 'SLE',
    'Singapore': 'SGP',
    'Sint Maarten (Dutch part)': 'SXM',
    'Slovakia': 'SVK',
    'Slovenia': 'SVN',
    'Solomon Islands': 'SLB',
    'Somalia': 'SOM',
    'South Africa': 'ZAF',
    'South Georgia and the South Sandwich Islands': 'SGS',
    'South Sudan': 'SSD',
    'Spain': 'ESP',
    'Sri Lanka': 'LKA',
    'Sudan': 'SDN',
    'Suriname': 'SUR',
    'Svalbard and Jan Mayen': 'SJM',
    'Swaziland': 'SWZ',
    'Sweden': 'SWE',
    'Switzerland': 'CHE',
    'Syrian Arab Republic': 'SYR',
    'Taiwan': 'TWN',
    'Tajikistan': 'TJK',
    'Tanzania, United Republic of': 'TZA',
    'Thailand': 'THA',
    'Timor-Leste': 'TLS',
    'Togo': 'TGO',
    'Tokelau': 'TKL',
    'Tonga': 'TON',
    'Trinidad and Tobago': 'TTO',
    'Tunisia': 'TUN',
    'Turkey': 'TUR',
    'Turkmenistan': 'TKM',
    'Turks and Caicos Islands': 'TCA',
    'Tuvalu': 'TUV',
    'Uganda': 'UGA',
    'Ukraine': 'UKR',
    'United Arab Emirates': 'ARE',
    'United Kingdom': 'GBR',
    'USA': 'USA',
    'United States Minor Outlying Islands': 'UMI',
    'Uruguay': 'URY',
    'Uzbekistan': 'UZB',
    'Vanuatu': 'VUT',
    'Venezuela': 'VEN',
    'Viet Nam': 'VNM',
    'Virgin Islands, British': 'VGB',
    'Virgin Islands, U.S.': 'VIR',
    'Wallis and Futuna': 'WLF',
    'Western Sahara': 'ESH',
    'Yemen': 'YEM',
    'Zambia': 'ZMB',
    'Zimbabwe': 'ZWE',
}

# set template for charts
pio.templates.default = 'plotly_white'

# dictionnary for the axis names for the charts
label_dic = {
    'CFR' : 'CFR',
    'Tests by cases' : 'Number of tests by cases',
    'Cases' : 'Number of total cases',
    'Deaths' : 'Number of total deaths',
    'Tests' : 'Number of total tests',
    'Daily Cases' : 'Number of daily cases',
    'Daily Deaths' : 'Number of daily deaths',
    'Daily Tests' : 'Number of daily tests',
    'Weekly Cases' : 'Number of Weekly cases',
    'Weekly Deaths' : 'Number of Weekly deaths',
    'Weekly Tests' : 'Number of Weekly tests',
    'Monthly Cases' : 'Number of Monthly cases',
    'Monthly Deaths' : 'Number of Monthly deaths',
    'Monthly Tests' : 'Number of Monthly tests',
    'Biweekly Cases' : 'Number of Biweekly cases',
    'Biweekly Deaths' : 'Number of Biweekly deaths',
    'Biweekly Tests' : 'Number of Biweekly tests',
            }

# months code for x axis labels
months_list = [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]

# list of the day number of 01/01, 02/01/, 03/01, etc.
firsts_of_the_month = [
                    1, 32, 61, 
                    92, 122, 153, 
                    183, 214, 245, 
                    275, 306, 336
                    ]
