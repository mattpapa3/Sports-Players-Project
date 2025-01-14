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

# _, team = nba.getPlayerInfo("4594268")
# print(team)

teamstats = nba.getTeamStats("Washington Wizards")
stats = nba.getTotStats("5160992")
print(nba.calc_uasge_perc(stats, teamstats))