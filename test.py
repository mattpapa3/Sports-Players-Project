import nba
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import MLB.mlb as mlb
import numpy as np
import pandas as pd
import sqlite3
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.library.http import NBAStatsHTTP
from datetime import datetime

# _, team = nba.getPlayerInfo("4594268")
log = nba.getGameLog("1966", False)
print(log[0])
today = datetime.now()
# Calculate yesterday's date
yesterday = today - timedelta(days=1)
# Format yesterday's date as MM/DD
formatted_date = yesterday.strftime("%m/%d")
if formatted_date[len(formatted_date) - 1] == '0' and formatted_date[0] == '0':     #If /10 or /20 or /30
    formatted_date = formatted_date[1:]    #Remove first 0 of month 01/10 = 1/10
elif formatted_date[formatted_date.find('/') + 1] == '0' and formatted_date[formatted_date.find('/') - 1] == '0':                                   # If /01
    formatted_date = formatted_date[:formatted_date.find('/') + 1] + formatted_date[formatted_date.find('/') + 2:]
elif formatted_date[formatted_date.find('/') - 1] != '0':
    formatted_date = formatted_date.replace('0', '')
print(formatted_date)
