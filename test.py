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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
import time
import undetected_chromedriver as uc

# _, team = nba.getPlayerInfo("4594268")
# log = nba.getGameLog("3978", False)
# print(log[0])
# today = datetime.now()
# # Calculate yesterday's date
# yesterday = today - timedelta(days=1)
# # Format yesterday's date as MM/DD
# formatted_date = yesterday.strftime("%m/%d")
# if formatted_date[len(formatted_date) - 1] == '0' and formatted_date[0] == '0':     #If /10 or /20 or /30
#     formatted_date = formatted_date[1:]    #Remove first 0 of month 01/10 = 1/10
# elif formatted_date[formatted_date.find('/') + 1] == '0' and formatted_date[formatted_date.find('/') - 1] == '0':                                   # If /01
#     formatted_date = formatted_date[:formatted_date.find('/') + 1] + formatted_date[formatted_date.find('/') + 2:]
# elif formatted_date[formatted_date.find('/') - 1] != '0':
#     formatted_date = formatted_date.replace('0', '')
# print(formatted_date)

def stealthy():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")
    options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            )

    url = "https://sportsbook.fanduel.com/navigation/nba"
    driver.get(url)
    elements = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/basketball/nba/')]")))
    hrefs = [element.get_attribute("href") for element in elements]
    print(hrefs)
    driver.quit()

stealthy()