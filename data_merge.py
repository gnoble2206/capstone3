import pandas as pd 
import numpy as np
import datetime

def batting_preprocessing():
    batting = pd.read_csv('../data/team_batting/allbatting.csv')

    ####need to change this date section
    def incomplete_rows(df):
        df.dropna(subset=['Date'], inplace=True)


def last_three(df, col_list):
    last_3 = lambda x: x.rolling(3).mean().shift(1)

    df[col_list].apply(last_3)
    #this works
    df[['IP_3', 'H_3', 'R_3', 'ER_3',
       'UER_3', 'BB_3', 'SO_3', 'HR_3', 'HBP_3', 'ERA_3', 'BF_3', 'Pit_3', 'Str_3', 'IR_3',
       'IS_3', 'SB_3', 'CS_3', 'AB_3', '2B_3', '3B_3', 'IBB_3', 'SH_3', 'SF_3', 'ROE_3']] = df[['IP', 'H', 'R', 'ER',
       'UER', 'BB', 'SO', 'HR', 'HBP', 'ERA', 'BF', 'Pit', 'Str', 'IR',
       'IS', 'SB', 'CS', 'AB', '2B', '3B', 'IBB', 'SH', 'SF', 'ROE']].apply(last_3)

    #### bad way to do this
    

    for x in avg_bat_cols:
        colname = 'last3_' + x
        batting[colname] = last_3(batting, x)
        batting[colname] = last_10(batting, x)

    return batting

    

def pitching_preprocessing():
    batting = pd.read_csv('../data/team_batting/allbatting.csv')
    avg_bat_cols = ['PA', 'AB', 'R', 'H',
       '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SH', 'SF',
       'ROE', 'GDP', 'SB', 'CS', 'BA', 'OBP', 'SLG', 'OPS', 'LOB', '#']

    def last_3(df, col_string):
        i_list = df[col_string].index.tolist()
        three_avg_list= []
        for i in range(len(i_list)):
            if len(three_avg_list) < 3:
                three_avg_list.append(df[col_string][:i].mean())
            else:
                three_avg = df[col_string][i - 3: i].mean()
                three_avg_list.append(three_avg)
        return three_avg_list

    for x in avg_bat_cols:
        colname = 'last3_' + x
        batting[colname] = last_3(batting, x)

def odds_preprocessing():
    # df =pd.read_csv('home_fav.csv')
    df_14 = pd.read_excel('../data/mlb_odds_2014.xlsx')
    df_15 = pd.read_excel('../data/mlb odds 2015.xlsx')
    df_16 = pd.read_excel('../data/mlb odds 2016.xlsx')
    df_17 = pd.read_excel('../data/mlb odds 2017.xlsx')
    df_14['Year'] = 2014
    df_15['Year'] = 2015
    df_16['Year'] = 2016
    df_17['Year'] = 2017
    df_total = pd.concat([df_14, df_15, df_16, df_17], ignore_index=True)
    vis = df_total.iloc[::2].copy()
    home = df_total.iloc[1::2].copy()
    vis.columns = ['Date', 'Rot', 'VH', 'Visitor Team', 'Visitor Pitcher', '1st', '2nd', '3rd', '4th',
       '5th', '6th', '7th', '8th', '9th', 'Final', 'Open', 'Close', 'Visitor RL',
       'Open OU', 'Open OU Price', 'Close OU', 'Close OU Price', 'Year']
    home.columns = ['Date', 'Rot', 'VH', 'Home Team', 'Home Pitcher', '1st', '2nd', '3rd', '4th',
       '5th', '6th', '7th', '8th', '9th', 'Final', 'Home Open ML', 'Home Close ML', 'Home RL',
       'Open OU', 'Open OU Price', 'Close OU', 'Close OU Price', 'Year']
    game_count = [i for i in range(1,9857)]
    vis['game_id'] = game_count
    home['game_id'] = game_count
    combined = pd.merge(vis, home, on='game_id')
    combined[['Visitor RL','Visitor RL Price']] = combined['Visitor RL'].str.split('\(|\)', expand=True).iloc[:,[0,1]]
    combined[['Home RL','Home RL Price']] = combined['Home RL'].str.split('\(|\)', expand=True).iloc[:,[0,1]]
    combined['Date_x'] = combined['Date_x'].astype('str')
    combined['Date_x'] = combined['Date_x'].str.zfill(4)
    combined['Year_x'] = combined['Year_x'].astype('str')
    combined['date'] = combined['Year_x'] + combined['Date_x']
    combined['date'] = pd.to_datetime(combined['date'])
    rl = combined.copy()
    rl.drop([5777], inplace=True)
    rl['Visitor RL'] = rl['Visitor RL'].str.strip('+')
    rl['Home RL'] = rl['Home RL'].str.strip('+')
    rl['Visitor RL Price'] = rl['Visitor RL Price'].str.strip('+')
    rl['Home RL Price'] = rl['Home RL Price'].str.strip('+')
    home_rl = rl['Home RL']
    rl['Home RL'] = pd.to_numeric(home_rl)
    rl['Home RL Price'] = pd.to_numeric(rl['Home RL Price'])
    rl['Visitor RL'] = pd.to_numeric(rl['Visitor RL'])
    rl['Visitor RL Price'] = pd.to_numeric(rl['Visitor RL Price'])
    rl['Final_x'] = pd.to_numeric(rl['Final_x'])
    rl['Final_y'] = pd.to_numeric(rl['Final_y'])
    rl['Home Pitch Hand'] = rl['Home Pitcher'].str.split('-', expand=True)[1]
    rl['Visitor Pitch Hand'] = rl['Visitor Pitcher'].str.split('-', expand=True)[1]
    rl['Home Pitcher'] = rl['Home Pitcher'].str[:-2]
    rl['Visitor Pitcher'] = rl['Visitor Pitcher'].str[:-2]
    ###change team codes
    rl['Visitor Team'] = rl['Visitor Team'].map(team_abbrev)
    rl['Home Team'] = rl['Home Team'].map(team_abbrev)
    rl['Home Code'] = rl['Home Team'].map(team_codes)
    rl['Vis Code'] = rl['Visitor Team'].map(team_codes)
    rl['date'] = pd.to_datetime(rl['date'])
    rl['stats_join'] = rl['date'].apply(lambda x: x.strftime('%Y%m%d')) + rl['Home Code'].astype(str) + rl['Vis Code'].astype(str)
    return rl

####need to seriously refactor this section
def incomplete_rows(df):
    df1 = df[df['Gtm'] != 2014]
    df1 = df1[df1['Gtm'] != 2015]
    df1 = df1[df1['Gtm'] != 2016]
    df1 = df1[df1['Gtm'] != 2017]
    df1 = df1[df1['Gtm'] != 2018]
    df1 = df1[df1['Gtm'] != 2019]
    return df

#####need to find the code that joins all batting to pitching
def merge_df(batting, pitching)
    bat_pitch = batting.merge(pitching, how="inner", left_index=True, right_index=True)
    return bat_pitch

def change_dates(df3):
    df[' Year_x'].astype(int, inplace=True)
    bat_pitch['date_month'] = bat_pitch['Date_x'].str.split(' ', expand=True)[0]
    bat_pitch['date_day'] = bat_pitch['Date_x'].str.split(' ', expand=True)[1]
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    bat_pitch['date_month'] = bat_pitch['date_month'].map(months)

    
team_abbrev = {
'LOS': 'LAD',
'TAM': 'TBR',    
'MIL': 'MIL',
'SEA': 'SEA',
'TOR': 'TOR',
'LAA': 'LAA',
'OAK': 'OAK',
'HOU': 'HOU',
'KAN': 'KCR',
'BOS': 'BOS',
'PHI': 'PHI',
'ARI': 'ARI',
'CUB': 'CHC',
'ATL': 'ATL',
'SFO': 'SFG',
'COL': 'COL',
'NYM': 'NYM',
'SDG': 'SDP',
'TEX': 'TEX',
'MIN': 'MIN',
'NYY': 'NYY',
'WAS': 'WSN',
'STL': 'STL',
'BAL': 'BAL',
'PIT': 'PIT',
'CIN': 'CIN',
'CLE': 'CLE',
'CWS': 'CHW',
'MIA': 'MIA',
'DET': 'DET'
}


team_codes = {
'LAD': '01',
'TBR': '02',    
'MIL': '03',
'SEA': '04',
'TOR': '05',
'LAA': '06',
'OAK': '07',
'HOU': '08',
'KCR': '09',
'BOS': '10',
'PHI': '11',
'ARI': '12',
'CHC': '13',
'ATL': '14',
'SFG': '15',
'COL': '16',
'NYM': '17',
'SDP': '18',
'TEX': '19',
'MIN': '20',
'NYY': '21',
'WSN': '22',
'STL': '23',
'BAL': '24',
'PIT': '25',
'CIN': '26',
'CLE': '27',
'CHW': '28',
'MIA': '29',
'DET': '30'
}


# bat_pitch['opp_code'] = bat_pitch['Opp_y'].map(team_codes)

def compress_rows(df3):
    bat_pitch['full_date'] = bat_pitch['full_date'].astype(str)
    bat_pitch['date_day'] = bat_pitch['date_day'].str.zfill(2)
    bat_pitch['date_month'] = bat_pitch['date_month'].astype(str)
    bat_pitch['date_month'] = bat_pitch['date_month'].str.zfill(2)
    bat_pitch[' Year_x'] = bat_pitch[' Year_x'].astype(str)
    bat_pitch['full_date'] = bat_pitch[' Year_x'] + '-'+ bat_pitch['date_month'] + '-' + bat_pitch['date_day']
    bat_pitch['full_date'] = bat_pitch['full_date'].str.rstrip('susp')
    bat_pitch['full_date'] = pd.to_datetime(bat_pitch['full_date'])
    bat_pitch = bat_pitch.sort_values(by=['full_date', 'Umpire'])
    team1 = bat_pitch.iloc[::2].copy()
    team2 = bat_pitch.iloc[1::2].copy()
    game_count = [i for i in range(1,13639)]
    team1['game_id'] = game_count
    team2['game_id'] = game_count
    bat_pitch = pd.merge(team1, team2, on='game_id')

def last_10(df, col_string):
    i_list = df[col_string].index.tolist()
    ten_avg_list= [0,1,0,0,0,1,0,0,0]
    for i in range(10, len(i_list) + 1):
        ten_avg = df[col_string][i - 10: i].mean()
        ten_avg_list.append(ten_avg)
    return ten_avg_list

def odds_join():


if __name__ == '__main__':
    # rl = odds_preprocessing()
    # df1 = pd.read_csv('../data/team_batting/allbatting.csv')
    # all_batting = incomplete_rows(df1)
    # df2 = pd.read_csv('../data/team_pitching/allpitching.csv')
    # all_pitching = incomplete_rows(df2)
    # bat_pitch = all_batting.merge(all_pitching, how="inner", left_index=True, right_index=True)
    

