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
log = nba.getGameLog("4594268", False)
if int(log[0][0][:log[0][0].find('/')]) < 9:
    date1 = log[0][0] + "/25"
else:
    date1 = log[0][0] + "/24"

if int(log[1][0][:log[0][0].find('/')]) < 9:
    date2 = log[0][0] + "/25"
else:
    date2 = log[0][0] + "/24"
date1 = datetime.strptime(date1, '%m/%d/%y')
date2 = datetime.strptime('12/24/24', '%m/%d/%y')
difference = abs((date2 - date1).days)
print(difference)
