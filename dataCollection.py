from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import numpy as np
import csv
import requests

url1 = "https://api.collegefootballdata.com/games"
url2 = "https://api.collegefootballdata.com/coaches"
url3 = "https://api.collegefootballdata.com/rankings"
headers = {"Authorization": "Bearer U51LfKTlfcjpvzHgxmFdewwuqdInAIQyrun/viEFsEemK4Fg54RQr9THlFjJEBZB"}

years = list(range(2000, 2021))
weeks = list(range(0,16))

# Test on reduced dataset
#years = list(range(2019, 2021))
#weeks = list(range(0,10))

df = pd.DataFrame()
for year in years:
    #print("Working on year: " + str(year))
    for week in weeks:

        parameters = {"year":year, "week":week, "team": "Notre Dame"}

        req = requests.get(url1, params = parameters, headers=headers)
        try:
            df =  df.append(json.loads(req.text))
        except IndexError:
            pass
        continue

df_trunc = df[["season", "week", "home_team", "home_points", "away_team", "away_points"]]
# If we wanted to add a column of the winner (Syntax - np.where(condition, value if condition is true, value if condition is false))
# I haven't used pandas before and we get a weird error, so we might need to try something else.  I think it works though since we never drop the home/away team name
df_trunc["winner"] = np.where(df_trunc["home_points"] > df_trunc["away_points"], df_trunc["home_team"], df_trunc["away_team"])

df2 = pd.DataFrame()
team = "Notre Dame"
for year in years:
    #print("Working on year: " + str(year))
    parameters = {"year":year, "team":team}

    req = requests.get(url2, params = parameters, headers=headers)
    try:
        df2 =  df2.append(json.loads(req.text))
    except IndexError:
        pass
    continue

df2_trunc = df2[["first_name", "last_name"]]
# I think this could be good to display the coach's name in order with a space
df2_trunc["coach"] = df2_trunc["first_name"] + " " + df2_trunc["last_name"]
df2_trunc["year"] = years

req = []
df3 = pd.DataFrame()
for year in years:
    for week in weeks:
        parameters = {"year":year, "week":week}
        req = requests.get(url3, params = parameters, headers=headers)
        try:
            df3 = df3.append(req.json())
        except IndexError:
            pass
        continue

df3_trunc = df3[['season', 'week', 'polls']]
d = []
for index, row in df3_trunc.iterrows():
    for i in range(len(row['polls'])):
        if row['polls'][i]['poll'] == 'AP Top 25':
            for r in row['polls'][i]['ranks']:
                if r['school'] == 'Notre Dame':
                    temp = r
                    temp['season'] = row['season']
                    temp['week'] = row['week']
                    del temp['firstPlaceVotes']
                    del temp['points']
                    d.append(temp)

df3_trunc = pd.DataFrame(d)

df_merge = pd.merge(df_trunc, df2_trunc, left_on='season', right_on='year', how='left')
df_merge.drop("year", inplace=True, axis=1)
df_merge = pd.merge(df_merge, df3_trunc, left_on=['season', 'week'], right_on=['season', 'week'], how='left')
df_merge.drop("school", inplace=True, axis=1)
df_merge[['rank', 'conference']] = df_merge[['rank', 'conference']].fillna(value=0)
df_merge = df_merge.astype({'rank': int})
df_merge.to_csv('data/data.csv', sep=',', encoding='utf-8')
#df_merge.to_csv('data/data_test.csv', sep=',', encoding='utf-8')
