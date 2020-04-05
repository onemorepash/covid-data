
import shutil
import tempfile
import json
import subprocess

from   jinja2   import Template

import crawl_wmeter_definitions as definitions

gnuplot_jinja2_template_filename = '../gnuplot/plot-countries.plot.jinja2'

with open(gnuplot_jinja2_template_filename, encoding='utf8') as gnuplot_jinja2_template_file:
    gnuplot_template = Template( gnuplot_jinja2_template_file.read() )

# Get the countries list from json

with open(definitions.countries_list_json_filename, encoding='utf8') as countries_list_json_file:
    country_list = json.load(countries_list_json_file)

for country in country_list:

    country_gnuplot_script = gnuplot_template.render( country_cname = country['cname'],
                                                      country_name  = country['name'] )

    with tempfile.NamedTemporaryFile(delete=True, mode='w', encoding='utf8') as country_gnuplot_tmp_file:
        country_gnuplot_tmp_file.write(country_gnuplot_script)

        country_gnuplot_tmp_file.flush()

        print ('Plotting ' + country['name'] )
        gnuplot_process = subprocess.run(['gnuplot ' + country_gnuplot_tmp_file.name], shell=True )
