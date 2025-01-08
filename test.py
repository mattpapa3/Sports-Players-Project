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
cursor.execute("SELECT * FROM Props WHERE name=? AND cat=?", ("Zach LaVine", "points"))
result = cursor.fetchall()
print(result[0][1])
cursor.close()
sqlite_connection.close()