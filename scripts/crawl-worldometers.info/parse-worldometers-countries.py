import crawl_wmeter_definitions as definitions

import shutil
import tempfile
import json

from urllib.request import  Request, urlopen
from urllib.error   import  URLError, HTTPError
from lxml           import  html, etree
from jsonfinder     import  jsonfinder

# Get the countries list from json

with open(definitions.countries_list_json_filename, encoding='utf8') as countries_list_json_file:
    country_list = json.load(countries_list_json_file)


all_countries_data = {}

for country in country_list:
    request = Request( country['url'], headers={'User-Agent': definitions.wmeter_user_agent} )

    print ('Trying to get ' + country['name'] + ' data... ', end='')

    try:
            response = urlopen(request)
    except HTTPError as http_error:
            print("Can't get the countries list from " + country['url'])
            print('HTTP Error code: ', http_error.code)
    except URLError as http_error:
            print("Can't connect to " + country['url'])
            print('Reason: ', http_error.reason)
    else:
        print ("success.")

        with tempfile.NamedTemporaryFile(delete=True) as country_tmp_file:
            shutil.copyfileobj(response, country_tmp_file)

            # tmp file was opened to write into it in binary mode, so we can't read characters from it
            # opening it in character mode to pass to the parser
            with open(country_tmp_file.name, encoding="utf8") as country_page_html:
                print ('Parsing ' + country['name'])

                html_parser     = etree.HTMLParser()
                html_tree       = etree.parse(country_page_html, parser = html_parser)

                country_data    = definitions.get_country_data_cumulative_linear( html_tree )

                all_countries_data[country['cname']]            = {}
                all_countries_data[country['cname']]['name']    = country['name']
                all_countries_data[country['cname']]['data']    = country_data

                country_data_filename = definitions.data_dir + country['cname'] + definitions.countries_datafiles_extention
                print ('Writing output data to ', country_data_filename)
                with open(country_data_filename, 'w', encoding='utf8') as country_data_file:
                    definitions.create_gnuplot_data(country_data, country_data_file)

print ('Dumping all countries data to ', definitions.countries_data_json_filename)
with open(definitions.countries_data_json_filename, 'w', encoding='utf8') as all_countries_data_file:
    json.dump(all_countries_data, all_countries_data_file, indent=4)
