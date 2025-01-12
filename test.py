import nba
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import MLB.mlb as mlb
import numpy as np
import pandas as pd
import sqlite3


sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
cursor = sqlite_connection.cursor()
cursor.execute("SELECT id FROM nbaInfo WHERE name=?;", ("Anfernee Simons",))
result = cursor.fetchall()
log = nba.getGameLog(result[0][0], False)
print(log[0])
cursor.close()
sqlite_connection.close()