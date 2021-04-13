from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import csv
import requests

url1 = "https://api.collegefootballdata.com/games"
url2 = "https://api.collegefootballdata.com/coaches"
headers = {"Authorization": "Bearer U51LfKTlfcjpvzHgxmFdewwuqdInAIQyrun/viEFsEemK4Fg54RQr9THlFjJEBZB"}

years = list(range(2000, 2021))

weeks = list(range(0,16))

req = []
df = pd.DataFrame()
for year in years:
    for week in weeks:

        parameters = {"year":year, "week":week, "team": "Notre Dame"}

        req = requests.get(url1, params = parameters, headers=headers)
        try:
            df =  df.append(json.loads(req.text))
        except IndexError:
            pass
        continue

df_trunc = df[["season", "week", "home_team", "home_points", "away_team", "away_points"]]

df2 = pd.DataFrame()
team = "Notre Dame"
for year in years:
    parameters = {"year":year, "team":team}

    req = requests.get(url2, params = parameters, headers=headers)
    try:
        df2 =  df2.append(json.loads(req.text))
    except IndexError:
        pass
    continue

df2_trunc = df2[["first_name", "last_name"]]
df2_trunc["year"] = years

print(df_trunc)
print(df2_trunc)

df_merge = pd.merge(df_trunc, df2_trunc, left_on='season', right_on='year', how='left')
df_merge.drop("year", inplace=True, axis=1)
df_merge.to_csv('data.csv', sep=',', encoding='utf-8')
