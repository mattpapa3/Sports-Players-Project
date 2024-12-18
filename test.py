import nba
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import MLB.mlb as mlb
import numpy as np
import pandas as pd
import sqlite3

# _, team = nba.getPlayerInfo("3992")
# team_abb = nba.teamname(nba.oppteamname2(team))
# DNPplayers = nba.getInjuredPlayers(team_abb, team)
# print(DNPplayers)
#log = nba.getGameLog('3992', False)
print(nba.getMinutes('3992'))
