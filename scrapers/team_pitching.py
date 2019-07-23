import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import random
import csv
from time import sleep
from random import randint

team_abbrs = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBR', 'TEX', 'TOR', 'WSN', 'LAA']
years = ['2019', '2018', '2017', '2016', '2015', '2014']
for z in team_abbrs:
    for y in years:
        with open('../data/team_pitching/{}_{}.csv'.format(z, y), 'w') as f:
            w = csv.writer(f)

            url = 'https://www.baseball-reference.com/teams/tgl.cgi?team='+ z + '&t=p&year=' + y
            sleep(randint(3,5))
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats = soup.select('#team_pitching_gamelogs tr')
            heads = list(stats[0].find_all('th'))
            headers = [head.text for head in heads[1:]]
            w.writerow(headers)
            for x in stats:
                cell_var = []
                cells = x.find_all('td')
                if len(cells) > 0:
                    for idx, i in enumerate(headers):
                        i = cells[idx].text
                        cell_var.append(i)
                cell_var.append(y)
           
                w.writerow(cell_var)
            
                