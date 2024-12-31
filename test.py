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
cursor.execute("SELECT * FROM traindataNBA2;")
result = cursor.fetchall()
for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o in result:
    cursor.execute("UPDATE traindataNBA SET minutes=? WHERE homeaway=? AND line=? AND hit=? AND position=? AND opp=? AND cat=? AND last10=?\
                    AND last5=? AND log=? AND oppposrank=? AND oppteam=? AND gamescore=?", (m,a,b,c,d,e,f,g,h,i,j,k,l))
    sqlite_connection.commit()
    cursor.execute("UPDATE traindataNBA SET shots=? WHERE homeaway=? AND line=? AND hit=? AND position=? AND opp=? AND cat=? AND last10=?\
                    AND last5=? AND log=? AND oppposrank=? AND oppteam=? AND gamescore=?", (n,a,b,c,d,e,f,g,h,i,j,k,l))
    sqlite_connection.commit()
    cursor.execute("UPDATE traindataNBA SET spread=? WHERE homeaway=? AND line=? AND hit=? AND position=? AND opp=? AND cat=? AND last10=?\
                    AND last5=? AND log=? AND oppposrank=? AND oppteam=? AND gamescore=?", (o,a,b,c,d,e,f,g,h,i,j,k,l))
    sqlite_connection.commit()
cursor.close()
sqlite_connection.close()