import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import random
import csv

team_abbrs = ['ARI', 'ATL', 'BAL'] #'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAD', 'FLA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']
years = ['2019', '2018'] #'2017', '2016', '2015', '2014']
for z in team_abbrs:
    for y in years:
        with open('{}_{}.csv'.format(z, y), 'w') as f:
            w = csv.writer(f)
            url = 'https://www.baseball-reference.com/teams/tgl.cgi?team='+ z + '&t=b&year=' + y
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats = soup.select('#team_batting_gamelogs tr')

            headers = ['game_num', 'date', '_@', 'opp', 'rslt', 'pa', 'ab', 'runs', 'hits', 'doubles', 'triples', 'hrs', 'rbi', 'bb', 'ibb', 'so', 'hbp', 'sh', 'sf', 'roe', 'gdp', 'sb', 'cs', 'ba', 'obp', 'slg', 'ops', 'lob', 'num_players', 'pitch_hand', 'opp_starter']
            for x in stats:
                cell_var = []
                cells = x.find_all('td')
                if len(cells) > 0:
                    for idx, i in enumerate(headers):
                        i = cells[idx].text
                        cell_var.append(i)
           
                w.writerow(cell_var)
                

