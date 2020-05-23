# covid-data

Parses worldometers.info and plots fine curbes for all countries

`scripts/crawl-worldmeters.info/` folder contains the following scripts:
- `crawl_worldometers_countries_list.py` — crawler which parses worldmeters.info covid19 per country main page and constructs a list of countries, monitored by worldmeters.
- `parse-worldometers-countries.py` — takes the list of countries and parses all per country pages to get cases and deaths data. Puts this data into per country column-based data files (see `data/worldmeters.info` folder) for gnuplot use and creates a common json datafaile `data/worldmeters.info/all_countries_data.json` which contains all data for all countries. Countries list is sorted accodring to decending cumulative deaths order.
- `plot-all.py` — plot graphs for all countries using gnuplot. For each country a new process of gnuplot is run, using `scrips/gnuplot/plot-countries.jinja2` gnuplot-definition jinga2 tempfile. First this template is rendered with country specific variables, sored in a temporary file, that it's fed to gnuplot process.
- `crawl_wmeter_definitions.py` — definitions file, describing variables and constant-specific functions to parse the worldmeters.info html and javasccript.
