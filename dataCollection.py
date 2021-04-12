from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import csv
import requests

url = "https://api.collegefootballdata.com/games"
headers = {"Authorization": "Bearer U51LfKTlfcjpvzHgxmFdewwuqdInAIQyrun/viEFsEemK4Fg54RQr9THlFjJEBZB"}

year = 2019

weeks = list(range(0,16))

req = []
df = pd.DataFrame()

for week in weeks:

    parameters = {"year":year, "week":week, "team": "Notre Dame"}

    req = requests.get(url, params = parameters, headers=headers)
    try:
        df =  df.append(json.loads(req.text))
    except IndexError:
        pass
    continue

df2 = df[["season", "week", "home_team", "away_team"]]
df2.to_csv('data.csv', sep=',', encoding='utf-8')
