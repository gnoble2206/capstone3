import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import random
import csv

# team_abbrs = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAD', 'FLA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']
#Rk Gtm Date        Opp Rslt    PA  AB  R   H   2B  3B  HR  RBI BB  IBB SO  HBP SH  SF  ROE GDP SB  CS  BA  OBP SLG OPS LOB #   Thr Opp. Starter (GmeSc)
# for x in team_abbrs:
with open('team_stats.csv', 'w') as f:
w = csv.writer(f)
url = 'https://www.baseball-reference.com/teams/tgl.cgi?team=ARI&t=b&year=2019'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
stats = soup.select('#team_batting_gamelogs tr')
for x in stats:
    cells = x.find_all('td')
    if len(cells) > 0:
        game_num = cells[0].text
        date = cells[1].text
        #@ columns in here messing things up
        opp = cells[3].text
        rslt = cells[4].text
        pa = cells[5].text
        ab = cells[6].text
        runs = cells[7].text
        hits = cells[8].text
        doubles = cells[9].text
        triples = cells[10].text
        hrs = cells[11].text
        rbi = cells[12].text
        bb = cells[13].text
        ibb = cells[14].text
        so = cells[15].text
        hbp = cells[16].text
        sh = cells[17].text
        sf = cells[18].text
        roe = cells[19].text
        gdp = cells[20].text
        sb = cells[21].text
        cs = cells[22].text
        ba = cells[23].text
        obp = cells[24].text
        slg = cells[25].text
        ops = cells[26].text
        lob = cells[27].text
        num_players = cells[28].text
        pitch_hand = cells[29].text
        opp_starter = cells[30].text
        w.writerow([game_num, date, opp, rslt, pa, ab, runs, hits, doubles, triples, hrs, rbi, bb, ibb, so, hbp, sh, sf, roe, gdp, sb, cs, ba, obp, slg, ops, lob, num_players, pitch_hand, opp_starter])

# headers = ['game_num', 'date', '_@' 'opp', 'rslt', 'pa', 'ab', 'runs', 'hits', 'doubles', 'triples', 'hrs', 'rbi', 'bb', 'ibb', 'so', 'hbp', 'sh', 'sf', 'roe', 'gdp', 'sb', 'cs', 'ba', 'obp', 'slg', 'ops', 'lob', 'num_players', 'pitch_hand', 'opp_starter']
# cell_var = []
# for x in stats:
#     cells = x.find_all('td')
#     if len(cells) > 0:
#         for idx, i in enumerate(headers):
#             i = cells[idx].text
#             cell_var.append(i)
    
#     w.writerow(cell_var)
            

