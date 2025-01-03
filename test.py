import nba
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import MLB.mlb as mlb
import numpy as np
import pandas as pd
import sqlite3

id = nba.getPlayerID("Jordan", "Poole")
log = nba.getGameLog(id, False)
print(nba.getAVGHomeAway(log, True, "3"))