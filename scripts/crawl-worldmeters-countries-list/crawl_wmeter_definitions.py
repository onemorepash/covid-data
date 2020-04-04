
from lxml               import html, etree

wmeter_countries_list_url_prefix   =   'https://www.worldometers.info/coronavirus/'
wmeter_user_agent                  =   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

countries_list_json_filename       =    '../../data/worldmeters_countries.json'


# Function which parses the main page HTML with xpath magic  and returns a list of <a> etree elements
def get_country_links(tree):
    return tree.xpath('.//table[@id="main_table_countries_today"]')[0].xpath('.//a[@class="mt_a"]')
