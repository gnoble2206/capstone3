import pandas as pd 
import numpy as np 

df =pd.read_csv('home_fav.csv')
df_14 = pd.read_excel('data/mlb_odds_2014.xlsx')
df_15 = pd.read_excel('data/mlb odds 2015.xlsx')
df_16 = pd.read_excel('data/mlb odds 2016.xlsx')
df_17 = pd.read_excel('data/mlb odds 2017.xlsx')
df_14['Year'] = 2014
df_15['Year'] = 2015
df_16['Year'] = 2016
df_17['Year'] = 2017
df_total = pd.concat([df_14, df_15, df_16, df_17], ignore_index=True)
vis = df_total.iloc[::2].copy()
home = df_total.iloc[1::2].copy()
combined = pd.merge(vis, home, on='game_id')
combined[['Visitor RL','Visitor RL Price']] = combined['Visitor RL'].str.split('\(|\)', expand=True).iloc[:,[0,1]]
combined[['Home RL','Home RL Price']] = combined['Home RL'].str.split('\(|\)', expand=True).iloc[:,[0,1]]
combined['Date_x'] = combined['Date_x'].astype('str')
combined['Date_x'] = combined['Date_x'].str.zfill(4)
combined['Year_x'] = combined['Year_x'].astype('str')
combined['date'] = combined['Year_x'] + combined['Date_x']
combined['date'] = pd.to_datetime(combined['date'])
rl = combined[['game_id', 'date','Visitor Team', 'Visitor Pitcher', 'Home Team', 'Home Pitcher', 'Open Visitor ML', 'Close Visitor ML',   'Home Open ML', 'Home Close ML',
        'Final_x' , 'Final_y', 'Visitor RL', 'Visitor RL Price', 'Home RL','Home RL Price']].copy()
rl['Visitor RL'] = rl['Visitor RL'].str.strip('+')
rl['Home RL'] = rl['Home RL'].str.strip('+')
rl['Visitor RL Price'] = rl['Visitor RL Price'].str.strip('+')
rl['Home RL Price'] = rl['Home RL Price'].str.strip('+')
home_rl = rl['Home RL']
rl['Home RL'] = pd.to_numeric(home_rl)
rl['Home RL Price'] = pd.to_numeric(rl['Home RL Price'])
rl['Visitor RL'] = pd.to_numeric(rl['Visitor RL'])
rl['Visitor RL Price'] = pd.to_numeric(rl['Visitor RL Price'])
rl.drop([5777], inplace=True)
rl['Final_x'] = pd.to_numeric(rl['Final_x'])
rl['Final_y'] = pd.to_numeric(rl['Final_y'])

###depends on strategy from here
home_fav_rl['final_spread'] = home_fav_rl['Final_y'] - home_fav_rl['Final_x']
home_fav_rl['payout_ratio'] = home_fav_rl[home_fav_rl['final_spread'] < abs(home_fav_rl['Home RL'])]['Visitor RL Price'].apply(lambda x: 100/abs(x) + 1 if x < 100 else x/100 + 1)
home_fav_rl['payout_ratio'] = home_fav_rl['payout_ratio'].fillna(-1.0)
home_fav_rl['winnings'] = home_fav_rl['payout_ratio'] * 10
home_fav_rl['wager'] = 10
home_fav_rl['winnings'] = home_fav_rl['wager'] * home_fav_rl['payout_ratio']
def bootstrap_confidence_interval(sample, stat_function=np.mean, resamples=1000, ci=95):
    """Calculate the CI of chosen sample statistic using bootstrap sampling.

    CI = confidence interval

    Parameters
    ----------
    sample: Numpy array
        1-d numeric data

    stat_function: function, optional (default=np.mean)
        Function for calculating as sample statistic on data

    iterations: int, optional (default=1000)
        Number of bootstrap samples to create

    ci: int, optional (default=95)
        Percent of distribution encompassed by CI, 0<ci<100

    Returns
    -------
    tuple: lower_ci(float), upper_ci(float), bootstrap_samples_statistic(array)
        Lower and upper bounds of CI, sample stat from each bootstrap sample
    """
    boostrap_samples = bootstrap(sample, resamples=resamples)
    bootstrap_samples_stat = list(map(stat_function, boostrap_samples))
    low_bound = (100. - ci) / 2
    high_bound = 100. - low_bound
    lower_ci, upper_ci = np.percentile(bootstrap_samples_stat,
                                       [low_bound, high_bound])
    return lower_ci, upper_ci, bootstrap_samples_stat

def home_team(df, home_team):
#     home_teams = list(df['Home Team'].unique())
#     return home_teams
    df[df['Home Team'] == home_team]['Visitor RL Price'].hist()
    
    #plot Mean and Median Pricing for each home team
def vis_price_mean(df, home_team):
    return df[df['Home Team'] == home_team]['Visitor RL Price'].mean()

def vis_price_median(df, home_team):
    return df[df['Home Team'] == home_team]['Visitor RL Price'].median()

home_fav_rl['no_cover'] = home_fav_rl[home_fav_rl['final_spread'] < abs(home_fav_rl['Home RL'])]['payout_ratio'].apply(lambda x: x*0 + 1 if x > 1 else x*0)
home_fav_rl['no_cover'] = home_fav_rl['no_cover'].fillna(0)

def bootstrap(x, resamples=1000):
    #ensure bootstrap samples are same size as sample size
    n_obs = x.shape[0]
    boot_samples = []
    for k in range(resamples):
        boot_idxs = np.random.randint(n_obs, size=n_obs)
        boot_sample = x[boot_idxs]
        boot_samples.append(boot_sample)
    return boot_samples

home_fav_rl = home_fav_rl.dropna()
home_fav_rl = home_fav_rl.reset_index(drop=True)

def bootstrap(x, resamples=1000):
    #ensure bootstrap samples are same size as sample size
    n_obs = x.shape[0]
    boot_samples = []
    for k in range(resamples):
        boot_idxs = np.random.randint(n_obs, size=n_obs)
        boot_sample = x[boot_idxs]
        boot_samples.append(boot_sample)
    return boot_samples

boot_sample_means = []
for sample in boot_samples:
    boot_sample_means.append(sample.mean())
plt.hist(np.array(boot_sample_means))
plt.xlabel('Winning Percentage Taking Visitor Run Line')
plt.show()

sns.set_style('whitegrid')
sns.kdeplot(boot_sample_means)

sns.set_style('whitegrid')
sns.set(font_scale=2)
# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(15, 7))
plt.xlim(0.51, 0.65)
plt.axvline(0.6124677, 0, c='r')
plt.axvline(0.5238, 0, c='r')
plt.axvline(0.5811288, 0, c='g')
plt.axvline(0.604945, 0, c='g')
plt.axvline(0.5932751030376903, 0, c='b')
plt.xlabel('Winning Percentage of Strategy')
plt.tight_layout()
plt.title("Sampling Distribution of Sample Means of Betting Strategy")
# sns.distplot(boot_sample_means)
sns.kdeplot(boot_sample_means)
plt.savefig('sampdistmlb.png')

def bootstrap_confidence_interval(sample, stat_function=np.mean, resamples=1000, ci=95):
    """Calculate the CI of chosen sample statistic using bootstrap sampling.

    CI = confidence interval

    Parameters
    ----------
    sample: Numpy array
        1-d numeric data

    stat_function: function, optional (default=np.mean)
        Function for calculating as sample statistic on data

    iterations: int, optional (default=1000)
        Number of bootstrap samples to create

    ci: int, optional (default=95)
        Percent of distribution encompassed by CI, 0<ci<100

    Returns
    -------
    tuple: lower_ci(float), upper_ci(float), bootstrap_samples_statistic(array)
        Lower and upper bounds of CI, sample stat from each bootstrap sample
    """
    boostrap_samples = bootstrap(sample, resamples=resamples)
    bootstrap_samples_stat = list(map(stat_function, boostrap_samples))
    low_bound = (100. - ci) / 2
    high_bound = 100. - low_bound
    lower_ci, upper_ci = np.percentile(bootstrap_samples_stat,
                                       [low_bound, high_bound])
    return lower_ci, upper_ci #, bootstrap_samples_stat
rl_by_team = home_fav_rl.groupby(['Home Team'])[['Visitor RL Price', 'Home Team']].mean()
rl_by_team.reset_index(inplace=True)
rl_by_team = rl_by_team.drop([13], axis=0)
rl_by_team = rl_by_team.reset_index()
rl_by_team = rl_by_team.drop(['index'], axis=1)



df['Home Pitch Hand'] = df['Home Pitcher'].str.split('-', expand=True)[1]
df['Visitor Pitch Hand'] = df['Visitor Pitcher'].str.split('-', expand=True)[1]
df['Home Pitcher'] = df['Home Pitcher'].str[:-2]
df['Visitor Pitcher'] = df['Visitor Pitcher'].str[:-2]