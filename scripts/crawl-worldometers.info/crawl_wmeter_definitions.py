
#
# This module defines the worldometers.info constants and parsing functions
# it's full and black magic xpath's and regex'es.
#
# The goal is to keep all this in one place and let other modules
# be functional and mess-agnostic.
#

import re
import demjson

from lxml       import  html, etree
from datetime   import  datetime


### Constants

wmeter_countries_list_url_prefix   =    'https://www.worldometers.info/coronavirus/'
wmeter_user_agent                  =    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

data_dir                           =    '../../data/worldmeters.info/'
countries_list_json_filename       =    data_dir + 'worldmeters_countries.json'
countries_data_json_filename       =    data_dir + 'all_countries_data.json'

countries_datafiles_extention      =    '.txt'

### Parsing functions

def country_cname_from_href( href ):
    cname = re.search('country\/([a-z,-]+)\/', href).group(1)
    return cname

# Function which parses the main page HTML with xpath magic  and returns a list of <a> etree elements
def get_country_links( tree ):
    return tree.xpath('.//table[@id="main_table_countries_today"]')[0].xpath('.//a[@class="mt_a"]')


# Magic wich parses a country page HTML and
# returns a object with lists of dates and values
def parse_chart_script( tree, chart_name ):

    # Find the script code inside HTML and get the JS object,
    # which is passed as an argument to Highcharts.chart() function in the JS code
    script_content     = tree.xpath('.//script[contains( text(), "Highcharts.chart(\'' + chart_name + '\'" )]' )

    if not script_content:
        return ''

    script_content     = ' '.join( script_content[0].text.split() )
    js_object_argument = re.search( "Highcharts.chart\('" + chart_name + "\', (\{.*\})\); ", script_content ).group(1)

    # debjson.decode() converts a javascript object to a python object:
    # adds quote symbols wherever needed etc
    return demjson.decode( js_object_argument )

# Wrapper which calls parse_chart_script() for cases and deaths separately and composes a joint object with all data
def get_country_data_cumulative_linear(tree):

    res = {}

    # Running parser for cases and add the data to the results object
    data = parse_chart_script( tree, 'coronavirus-cases-linear' )

    # Iterate through dates and number of cases
    # and create a dictionaty { date : { 'cases': value } }
    if data:
        for dd, value in zip(data['xAxis']['categories'], data['series'][0]['data']):
            date = str(datetime.strptime(dd, '%b %d, %Y').date())
            if date not in res:
                res[date] = {}
            res[date]['cases'] = value


    # Running parser for deaths and add the data to the results object
    data = parse_chart_script( tree, 'coronavirus-deaths-linear' )

    # Iterate through dates and number of deaths
    # and create a dictionaty { date : { 'deaths': value } }
    if data:
        for dd, value in zip(data['xAxis']['categories'], data['series'][0]['data']):
            date = str(datetime.strptime(dd, '%b %d, %Y').date())
            if date not in res:
                res[date] = {}
            res[date]['deaths'] = value

    return res


def create_gnuplot_data(country_data, datafile):
    # Convert country data into whitespace delimited columns gnuplot data files: on line, one date
    # Calculate daily growth rate and deily increment for cases and deaths.

    datafile.write( '{:10},{:>15},{:>15},{:>15},{:>15},{:>15},{:>15}\n'.format( '"Date"', '"Total Cases"', '"Cases Rate"', '"Cases Inc"',
                                                                                 '"Total Deaths"', '"Deaths Rate"', '"Deaths Inc"'
                                                                            )
                  )

    cases_prev  = 0
    deaths_prev = 0

    for date, values in country_data.items():

        cases_cur   = ''
        deaths_cur  = ''

        cases_daily_rate    =   ''
        deaths_daily_rate   =   ''
        cases_daily_inc     =   ''
        deaths_daily_inc    =   ''

        out_string      = ''
        format_string   = ''

        if 'cases' in values.keys() and values['cases']:
            cases_cur   = values['cases']

        if 'deaths' in values.keys() and values['deaths']:
            deaths_cur  = values['deaths']

        # Placeholder for date
        format_string  += '{:10},'

        # Placeholder for cases_cur
        format_string  += '{:>15},'

        # Calculate and print cases daily rate and dayly inc
        # and add 2 placeholders to the format_string
        if cases_cur:
            if cases_prev != 0:
                cases_daily_rate = round( cases_cur/cases_prev, 3 )
            cases_daily_inc = cases_cur - cases_prev

        format_string      += '{:>15},'
        format_string      += '{:>15},'


        # Placeholder for deaths_cur
        format_string  += '{:>15},'

        # Calculate and print deaths daily rate and dayly inc
        # and add 2 placeholders to the format_string
        if deaths_cur:
            if deaths_prev != 0:
                deaths_daily_rate = round( deaths_cur/deaths_prev, 3 )
            deaths_daily_inc = deaths_cur - deaths_prev

        format_string      += '{:>15},'
        format_string      += '{:>15},'

        format_string      += '\n'
        out_string  = format_string.format( date,
                                            cases_cur,
                                            cases_daily_rate,
                                            cases_daily_inc,
                                            deaths_cur,
                                            deaths_daily_rate,
                                            deaths_daily_inc)

        datafile.write( out_string )

        if cases_cur:
            cases_prev  = cases_cur
        if deaths_cur:
            deaths_prev = deaths_cur
