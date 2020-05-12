
import shutil
import tempfile
import json
import re

from urllib.request     import  Request, urlopen
from urllib.error       import  URLError, HTTPError
from lxml               import  html, etree

import crawl_wmeter_definitions as definitions

print ('Trying to crawl ' + definitions.wmeter_countries_list_url_prefix + ' ... ', end='')

# Connect to worldometers.info and save the coronavirus title page to a temporary file
request = Request(definitions.wmeter_countries_list_url_prefix, headers={'User-Agent': definitions.wmeter_user_agent})

try:
        response = urlopen(request)
except HTTPError as http_error:
        print("Can't get the countries list from " + definitions.wmeter_countries_list_url_prefix)
        print('HTTP Error code: ', http_error.code)
except URLError as http_error:
        print("Can't connect to " + definitions.wmeter_countries_list_url_prefix)
        print('Reason: ', http_error.reason)
else:
    print ( ' success.' )

    # Put the HTML page in a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as countries_list_tmp_file:
        shutil.copyfileobj(response, countries_list_tmp_file)

        # tmp file was opened to write into it in binary mode, so we can't read characters from it
        # opening it in character mode to pass to the parser
        with open(countries_list_tmp_file.name, encoding="utf8") as countries_list_html:

            # Parse HTML and create a list of dictionatries [ {'name' : <country name>, "url" : <country page url> } ]
            html_parser     = etree.HTMLParser()
            html_tree       = etree.parse(countries_list_html, parser = html_parser)

            # HTML parsing black magic is in the definitions module
            country_links   = definitions.get_country_links(html_tree)

            country_list    = []

            for country_i in country_links:
                country             = {}
                country['cname']    = definitions.country_cname_from_href( country_i.attrib['href'] )
                country['name']     = country_i.text
                country['url']      = definitions.wmeter_countries_list_url_prefix + country_i.attrib['href']

                country_list.append(country)

            # Dump the list to a json file
            with open(definitions.countries_list_json_filename, 'w', encoding='utf8') as countries_list_json_file:
                json.dump(country_list, countries_list_json_file, indent=4)
