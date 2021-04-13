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
headers = {"Authorization": "Bearer U51LfKTlfcjpvzHgxmFdewwuqdInAIQyrun/viEFsEemK4Fg54RQr9THlFjJEBZB"}

years = list(range(2000, 2021))

weeks = list(range(0,16))

# Test on reduced dataset
#years = list(range(2020, 2021))
#weeks = list(range(0,5))

req = []
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

print(df_trunc)
print(df2_trunc)

df_merge = pd.merge(df_trunc, df2_trunc, left_on='season', right_on='year', how='left')
df_merge.drop("year", inplace=True, axis=1)
df_merge.to_csv('data.csv', sep=',', encoding='utf-8')
#df_merge.to_csv('data_test.csv', sep=',', encoding='utf-8')
