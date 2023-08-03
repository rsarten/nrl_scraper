from os import listdir
from os.path import isfile, join

import numpy as np
import pandas as pd

from src.meta_lookups import map_col_names, logo_team_lookup

player_stats = ['data/player_stats/'+f for f in listdir('data/player_stats') if isfile(join('data/player_stats/', f))]
stats = [pd.read_csv(player_stat) for player_stat in player_stats]
all_stats = pd.concat(stats)

all_stats.rename(columns=map_col_names, inplace=True)

## remove state of origin games ~ 200 games
all_stats = all_stats.loc[all_stats['team'].isin(logo_team_lookup.keys())]
## remove non-regular-season games
## need to revisit this at some point
all_stats = all_stats.loc[~all_stats['round'].isin(['FW1', 'FW2', 'FW3', 'GF'])]
all_stats['round'] = all_stats['round'].astype(int)
all_stats['team'] = all_stats['team'].map(logo_team_lookup) # rename logos
all_stats = all_stats.sort_values(['team', 'player', 'season', 'round'], ascending=[True, True, False, False])

## set price values to numbers
all_stats['price'] = all_stats['price'].str.extract('\$([0-9k]+)')
all_stats['price'] = all_stats['price'].str.replace('k', '000').astype(float)

def agg_stats(df):
    d = []
    d.append(df['price'].sum())
    d.append(df['price'].mean())
    d.append(df['price'].std())
    d.append(df['break_even'].sum())
    d.append(df['fantasy_points'].sum())
    res = df['break_even'] - df['fantasy_points']
    d.append(res.mean())
    d.append(res.std())
    return pd.Series(d, index=['team_total_price', 'team_price_mean', 'team_price_std', 'team_total_be', 'team_total_fp', 'team_diff_mean', 'team_diff_std'])

team_summaries = all_stats.groupby(['team', 'season', 'round']).apply(agg_stats).reset_index().sort_values(['team', 'season', 'round'], ascending=[True, False, False])

agg_values = ['team_total_price', 'team_price_mean', 'team_price_std', 'team_total_be', 'team_total_fp', 'team_diff_mean', 'team_diff_std']
for agg_value in agg_values:
    team_summaries[f"prev_{agg_value}"] = team_summaries.groupby('team')[agg_value].shift(-1)

team_summaries.set_index(['team', 'season', 'round'], inplace=True)

base_stats = all_stats.loc[:,['team', 'player', 'season', 'round', 'opponent', 'break_even', 'fantasy_points', 'price', 'position', 'minutes_played']]
base_stats = pd.merge(base_stats, team_summaries, on=['team', 'season', 'round'])
base_stats = base_stats.join(team_summaries, on=['opponent', 'season', 'round'], rsuffix='_opponent')
base_stats['prev_position'] = base_stats.groupby('player')['position'].shift(-1)
base_stats['prev_minutes_played'] = base_stats.groupby('player')['minutes_played'].shift(-1)
base_stats['prev_break_even'] = base_stats.groupby('player')['break_even'].shift(-1)
base_stats['prev_fantasy_points'] = base_stats.groupby('player')['fantasy_points'].shift(-1)
#base_stats['next_fantasy_points'] = base_stats.groupby('player')['fantasy_points'].shift(1)
base_stats.columns
base_stats

all_stats.to_csv('data/summarised/all_stats.csv', index=False)
base_stats.to_csv('data/summarised/base_stats.csv', index=False)
