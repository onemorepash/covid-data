import shutil
import tempfile
import json

from urllib.request     import Request, urlopen
from urllib.error       import URLError, HTTPError

from lxml               import html, etree

import crawl_wmeter_definitions as definitions


# Get the countries list from json

with open('path_to_file/person.json') as f:
  data = json.load(f)
