import pandas as pd
import numpy as np 
from time import time
from time import sleep
from random import randint
from datetime import date, timedelta
import requests
import csv
import re
import sys
from bs4 import BeautifulSoup

response = requests.get('https://swishanalytics.com/optimus/mlb/batter-vs-pitcher-stats?date=2019-07-15')
soup = str(BeautifulSoup(response.text, 'lxml'))
bs = re.findall("(?s)(?<=function Model).*?(?=}];)", soup)
bs1 = bs[0].split('},{')
print(bs1[57])
### need to clean the data next and "automate" the date url

