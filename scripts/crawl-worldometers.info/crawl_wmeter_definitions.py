
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

### Constants

wmeter_countries_list_url_prefix   =   'https://www.worldometers.info/coronavirus/'
wmeter_user_agent                  =   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

countries_list_json_filename       =    '../../data/worldmeters_countries.json'

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
    for date, value in zip(data['xAxis']['categories'], data['series'][0]['data']):
        if date not in res:
            res[date] = {}
        res[date]['cases'] = value

    # Running parser for deaths and add the data to the results object
    data = parse_chart_script( tree, 'coronavirus-deaths-linear' )

    # Iterate through dates and number of deaths
    # and create a dictionaty { date : { 'deaths': value } }
    for date, value in zip(data['xAxis']['categories'], data['series'][0]['data']):
        if date not in res:
            res[date] = {}
        res[date]['deaths'] = value

    return res
