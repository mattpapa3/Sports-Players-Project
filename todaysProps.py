from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from pyvirtualdisplay import Display
import sqlite3
import nba
import json
from bs4 import BeautifulSoup
import MLB.mlb as mlb
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
import pickle
from datetime import datetime

team_mapping = {
    "Boston" : 1,
    "Brooklyn" : 2,
    "New York" : 3,
    "Philadelphia" : 4,
    "Toronto" : 5,
    "Golden State" : 6,
    "Clippers" : 7,
    "Lakers" : 8,
    "Phoenix" : 9,
    "Sacramento" : 10,
    "Chicago" : 11,
    "Cleveland" : 12,
    "Detroit" : 13,
    "Indiana" : 14,
    "Milwaukee" : 15,
    "Atlanta" : 16,
    "Charlotte" : 17,   
    "Miami" : 18,
    "Orlando" : 19,
    "Washington" : 20,
    "Denver" : 21,
    "Minnesota" : 22,
    "Thunder" : 23,
    "Portland" : 24,
    "Utah" : 25,
    "Dallas" : 26,
    "Houston" : 27,
    "Memphis" : 28,
    "New Orleans" : 29,
    "San Antonio" : 30
}

position_mapping = {
    "Guard": 0,
    "Point Guard": 1,
    "Shooting Guard": 2,
    "Small Forward": 3,
    "Power Forward": 4,
    "Center": 5,
    "Forward": 6
}
hittersRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/hittersHitRegressionmodel.pkl", "rb"))
strikeoutRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/strikeoutHitRegressionmodel.pkl", "rb"))
earnedRunsRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/earnedRunsAllowedRegressionmodel.pkl", "rb"))
pointsRegressionMdoel = pickle.load(open("/root/propscode/propscode/NBA/pointsRegressionmodel.pkl", "rb"))
praRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/praRegressionmodel.pkl", "rb"))
reboundsRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/reboundsRegressionmodel.pkl", "rb"))
assistsRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/assistsRegressionmodel.pkl", "rb"))
threePtRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/threepointRegressionmodel.pkl", "rb"))
stealsRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/stealsRegressionmodel.pkl", "rb"))
blocksRegressionModel = pickle.load(open("/root/propscode/propscode/NBA/blocksRegressionmodel.pkl", "rb"))


def getHits_Runs_RBISLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Hits + Runs + RBIs']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'hrb'])
		i += 1

	driver.quit()

	return props


def getTotal_BasesLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Total Bases O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'tb'])
		i += 1

	driver.quit()

	return props


def getRuns_ScoredLines():
	display = Display(visible=0, size=(1920, 1080))
	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props")

	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Runs Scored']")))
	element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'r'])
		i += 1

	driver.quit()

	return props


def getStrikeoutsLines():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


    props = []
    driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Strikeouts Thrown O/U']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-outcome-cell__line')))
    elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
    lines = []
    m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
    for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
        if m % 2 != 0:
            lines.append(title.text)
        m += 1
    names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
    i = 0
    for name in names:
        props.append([name.text, lines[i], 'k'])
        i += 1

    return props


def getPitcherOutsLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Outs Recorded']")))
	driver.execute_script("arguments[0].scrollIntoView();", element) 
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-outcome-cell__line')))
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'outs'])
		i += 1

	return props



def getHitsAllowedLines():
	#display = Display(visible=0, size=(1920, 1080))
	#display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Hits Allowed O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-outcome-cell__line')))
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'hits'])
		i += 1

	return props


def getEarnedRunsAllowedLines():
	#display = Display(visible=0, size=(1920, 1080))
	#display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Earned Runs Allowed']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-outcome-cell__line')))
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'era'])
		i += 1

	return props

def getNBAPointsLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Points O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], 'points'])
		i += 1
	

	driver.quit()

	return props

def getNBAReboundsLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props?category=player-rebounds&subcategory=rebounds")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Rebounds O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], 'rebounds'])
		i += 1
	

	driver.quit()

	return props

def getNBAAssistsLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props?category=player-assists&subcategory=assists")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Assists O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], 'assists'])
		i += 1
	

	driver.quit()

	return props

def getNBA3PTLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props?category=player-threes&subcategory=threes")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Threes O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], '3-pt'])
		i += 1
	

	driver.quit()

	return props

def getNBAPRALines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props?category=player-combos&subcategory=pts-%2B-reb-%2B-ast")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Pts + Reb + Ast O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], 'pra'])
		i += 1
	

	driver.quit()

	return props

def getNBAStealBlockLines():
#	display = Display(visible=0, size=(1920, 1080))
#	display.start()
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--disable-extensions")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


	props = []
	driver.get("https://sportsbook.draftkings.com/nba-player-props?category=player-defense&subcategory=steals")
	#element = driver.find_element(By.XPATH, "//a[@id='subcategory_Total Bases']")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Steals O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		props.append([name.text, lines[i], 'steals'])
		i += 1
	
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='subcategory_Blocks O/U']")))
	driver.execute_script("arguments[0].scrollIntoView();", element)
	driver.execute_script("arguments[0].click();", element)
	#element.click()

	WebDriverWait(driver, 10)
	elements = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__line')
	lines = []
	m = 0
	#names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name') 
	for title in elements: 
	#	# select H2s, within element, by tag name 
	#	heading = title.find_element(By.TAG_NAME, 'span').text 
		# print H2s
		if m % 2 != 0:
			lines.append(title.text)
		m += 1
	names = driver.find_elements(By.CLASS_NAME, 'sportsbook-row-name')
	i = 0
	for name in names:
		val = name.text
		val.replace("'", "")
		props.append([val, lines[i], 'blocks'])
		i += 1
	

	driver.quit()

	return props


def getNBAProps():
	#links = nba.getGamesNew()
	#print(links[:2])
	today = datetime.now()
	gameinfo = nba.getNbaTodayGames()
	print(gameinfo)
	arr_games = np.array(gameinfo)
	sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
	cursor = sqlite_connection.cursor()
	for i in gameinfo:
		cursor.execute("SELECT * FROM nbaTodaysGames WHERE game=?", (i[0],))
		result = cursor.fetchall()
		if len(result) == 0:
			cursor.execute("INSERT INTO nbaTodaysGames(game,spread,overunder) VALUES(?,?,?)", (i[0],i[1],i[2]))
			sqlite_connection.commit()
	
#	props = []
	props = getNBAPointsLines()
	props += getNBA3PTLines()
	props += getNBAAssistsLines()
	props += getNBAPRALines()
	props += getNBAReboundsLines()
	props += getNBAStealBlockLines()
	props.sort()
	games = arr_games[:,0]
	previous = ""
	for i in props:
		if i[0] != previous:
			cursor.execute("SELECT * FROM nbaInfo WHERE name=?", (i[0],))
			result = cursor.fetchall()
			# If not retrieve info and add to database
			if len(result) == 0:
				names = i[0].split()
				#if len(names) > 2:
				print(i[0])
				id = nba.getPlayerID(names[0], names[1])
				if id == -1:
					print("CAN'T GET ID")
					continue
				else:
					print(id)
				position, team = nba.getPlayerInfo(id)
				cursor.execute("""INSERT INTO nbaInfo(id, name, position, team) VALUES(?,?,?,?);""", (id, i[0], position,team))
				sqlite_connection.commit()
			else:
				for a, b, c, d in result:
					id = a
					position = c
				print(i[0])
				_, team = nba.getPlayerInfo(id)
		previous = i[0]
		# print("PLAYER INFO")
		# print(id)
		# print(position)
		# print(team)
		game_index = np.char.find(games, team)
		print(game_index)
		if game_index.size == 0:
			print(team)
			print(games)
			print("TEAM NOT FOUND/PLAYING")
			continue
		index = np.where(game_index != -1)[0]
		if len(index) > 0:
			# print(index)
			# print(games[index[0]])
			# print(gameinfo[index[0]][1])
			# print(gameinfo[index[0]][2])
			cursor.execute("SELECT * FROM Props WHERE name=? AND cat=?", (i[0], i[2]))
			result = cursor.fetchall()
			if len(result) == 0:
				cursor.execute("""INSERT INTO Props(name, stat, cat, views, over, under, date, game, totalscore, spread) VALUES(?,?,?,?,?,?,?,?,?,?);""", (i[0], i[1], i[2],\
																																		0, 0, 0, today, games[index][0],\
																																			gameinfo[index[0]][2],gameinfo[index[0]][1]))
				sqlite_connection.commit()

	if sqlite_connection:
		cursor.close()
		sqlite_connection.close()
	
def getMLBProps():
	props = []
	#props += getHits_Runs_RBISLines()
	print("2")
	props += getTotal_BasesLines()
	#props += getRuns_ScoredLines()
	print("1")
	props += getEarnedRunsAllowedLines()
	print("3")
	props += getHitsAllowedLines()
	print("4")
	props += getPitcherOutsLines()
	print("5")
	props += getStrikeoutsLines()
	print("DONE")


	#gameinfo = mlb.getGameInfo()
	gameinfo = [["Los Angeles Dodgers @ New York Yankees", "8.5", "67", "7"]]
	props.sort()
	print(props)
	sqlite_connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')
	cursor = sqlite_connection.cursor()
	previous = ""
	arr = np.array(gameinfo)
	for i in gameinfo:
		cursor.execute("SELECT * FROM mlbTodaysGames WHERE game=?", (i[0],))
		result = cursor.fetchall()
		if len(result) == 0:
			cursor.execute("""INSERT INTO mlbTodaysGames(game, temperature, wind, overunder) VALUES(?,?,?,?);""", (i[0],i[2],i[3],i[1]))
			sqlite_connection.commit()
	games = arr[:,0]
	for i in props:
		if i[0] != previous:
			# Check if we have player info in database
			cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;",(i[0],))
			result = cursor.fetchall()
			# If not retrieve info and add to database
			if len(result) == 0:
				names = i[0].split()
				#if len(names) > 2:
				print(i[0])
				id = mlb.getMLBPlayerID(names[0], names[1])
				if id == -1:
					print("CAN'T GET ID")
					continue
				else:
					print(id)
				position, team, leftright = mlb.getPlayerInfo(id)
				team = mlb.MLBteamname(team)
				cursor.execute("""INSERT INTO mlbPlayer(id, name, position, team, rightleft) VALUES(?,?,?,?,?);""", (id, i[0], position, team, leftright))
				sqlite_connection.commit()
			else:
				for a, b, c, d, e, f in result:
					id = a
					team = d
			game_index = np.char.find(games, team)
			if game_index.size == 0:
				print(team)
				print(games)
				print("TEAM NOT FOUND/PLAYING")
				break
		index = np.where(game_index != -1)[0]
		print(game_index)
		if len(index) > 0:
			print(index)
			print(games[index[0]])
			print(gameinfo[index[0]][1])
			cursor.execute("SELECT * FROM Props WHERE name=? AND cat=?", (i[0], i[2]))
			result = cursor.fetchall()
			if len(result) == 0:
				cursor.execute("""INSERT INTO Props(name, stat, cat, views, over, under, game, overunder) VALUES(?,?,?,?,?,?,?,?);""", (i[0], i[1], i[2],\
																																		0, 0, 0, games[index][0],\
																																			gameinfo[index[0]][1]))
				sqlite_connection.commit()
		previous = i[0]

def calcScore():
	sqlite_connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')
	cursor = sqlite_connection.cursor()
	cursor.execute("SELECT * FROM Props WHERE regressionLine IS NULL;")
	result = cursor.fetchall()
	teamstats = mlb.getMLBTeamStats()
	for a,b,c,d,e,f,g,h,i in result:
		if c == 'tb' or c == 'k' or c == 'era':
			name = a
			cat = c
			line = b
			overunder = h
			cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;",(name,))
			result2 = cursor.fetchall()
			print(name)
			for z,y,x,w,q,r in result2:
				id = z
				position = x
				team = w
				rightleft = q
				pybaseballID = int(r)
			print(team)
			cursor.execute("SELECT game, wind, temperature FROM mlbTodaysGames;")
			result2 = cursor.fetchall()
			oppTeam = ""
			for z,y,x in result2:
				if team in z[:z.find('@')]:
					oppTeam = z[z.find('@') + 2:]
					homeint = 0
					home = False
					game = z
					wind = y
					temperature = x
					break
				elif team in z[z.find('@'):]:
					oppTeam = z[:z.find('@') - 1]
					homeint = 1
					home = True
					game = z
					wind = y
					temperature = x
					break
			log = mlb.getMLBGameLog(id, position, False)
			log2023 = mlb.getMLB2022Log(id, position, False)
			if len(oppTeam) < 1:
				home = mlb.MLBhomeoraway(id)
				oppTeam = mlb.getMLBOppTeam(id, home)
			print(game)
			if cat == 'tb':
				log = np.array(log)
				pitcher = ""
				cursor.execute("SELECT name FROM Props WHERE game=? AND cat=?;",(game,'k'))
				result2 = cursor.fetchall()
				for z in result2:
					cursor.execute("SELECT team FROM mlbPlayer WHERE name=?;",(z[0],))
					team = cursor.fetchall()
					if oppTeam in team[0]:
						pitcher = z[0]
				if len(pitcher) == 0:
					pitcher = mlb.getOppStartingPitcher(id,home)
				pitcher_first = pitcher[:pitcher.find(" ")]
				if '(' in pitcher:
					pitcher = pitcher_first + " " + pitcher[pitcher.find(" ") + 1:pitcher.find("(") - 1]
				else:
					pitcher = pitcher_first + " " + pitcher[pitcher.find(" ") + 1:]
				print(pitcher)
				cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;", (pitcher,))
				result2 = cursor.fetchall()
				if len(result2) > 0:
					for z,y,w,x,q,r in result2:
						pitcherID = z
						pybaseballPitcherID = int(r)
						throw = q
					oppPitcherStats, opphbp, oppbattersfaced = mlb.getPitcherStats(pitcherID)
				else:
					print(f"ERROR IN PITCHER {pitcher} CHECK DATABASE")
					continue
				if len(oppPitcherStats) > 0:
					oppPitchfip = mlb.calculateFIP(oppPitcherStats, opphbp)
					oppwhip = (float(oppPitcherStats[9]) + float(oppPitcherStats[13])) / float(oppPitcherStats[8])
					oppwhip = round(oppwhip, 2)
				else:
					oppPitchfip = 0.0
					oppwhip = 0.0
				cursor.execute("SELECT id FROM mlbTeams WHERE name=?;", (oppTeam,))
				teamid = cursor.fetchall()
				teamid = teamid[0]
				last5Hit = 0
				last10Hit = 0
				logHit = 0
				for num, game in enumerate(log):
					singles = float(game[5]) - (float(game[6]) + float(game[7]) + float(game[8]))
					tot = singles + (float(game[6]) * 2) + (float(game[7]) * 3) + (float(game[8]) * 4)
					if tot > float(line):
						logHit += 1
						if num < 5:
							last5Hit += 1
							last10Hit += 1
						elif num < 10:
							last10Hit += 1
				if logHit > 0:
					logHit = logHit / len(log)
				oppteamname = mlb.MLBteamname(mlb.MLBabbrev(oppTeam))
				print(oppteamname)
				oppteamnum = mlb.get_team_number(oppteamname)
				print(oppteamnum)
				if len(log) >= 5:
					last5 = np.array(log[:5])
				else:
					last5 = np.array(log)
				if len(last5) > 0:
					last5ops = last5[:, 18]
					last5ops = np.sum(np.float64(last5ops)) / len(last5ops)
					last5ops = round(last5ops,3)
				else:
					last5ops = 0
				_, avg_vs_FF, avg_vs_off, avg_vs_pitchFF, percentFastballs, avg_spin_ff, avg_spin_off = mlb.calculatepitchAVGs(pybaseballID, pybaseballPitcherID)
				features2 = [[ float(line),last10Hit, last5Hit, logHit, oppwhip, float(temperature), oppPitchfip, percentFastballs, avg_vs_FF, avg_vs_off, avg_vs_pitchFF,avg_spin_ff,avg_spin_off]]
				print(features2)
				regressionPrediction = hittersRegressionmodel.predict(features2)
				#regressionLine = float(regressionPrediction) - float(line)
				cursor.execute("UPDATE Props SET regressionLine = ? WHERE name=?;", (regressionPrediction[0], name))
				sqlite_connection.commit()
			else:
				oppTeam_abbrev = mlb.MLBabbrev(oppTeam)
				stats, hbp, battersfaced = mlb.getPitcherStats(id)
				if len(stats) > 0:
					k9 = (float(stats[14]) / float(stats[8])) * 9
					k9 = round(k9, 2)
					fip = mlb.calculateFIP(stats, hbp)

					# Caluclate WHIP
					whip = (float(stats[9]) + float(stats[13])) / float(stats[8])
					whip = round(whip, 2)

					#Calculate K%
					kpercent = float(stats[14]) / float(battersfaced)
					kpercent = round(kpercent, 2)

					if stats[14] == '0' or stats[13] == '0':
						kwalk = 0
					else:
						kwalk = float(stats[14]) / float(stats[13])
				else:
					k9 = 0.0
					whip = 0.0
					kpercent = 0.0
					kwalk = 0
					fip = 0.0

				log = np.array(log)

				if len(log) > 3:
					last3 = np.array(log[:3, 3])
				elif len(log) == 0:
					last3 = np.array([])
				else:
					last3 = np.array(log[:, 3])
				last3 = np.float64(last3)
				if len(last3.shape) == 0:
					inningslast3 = [last3]
				elif last3.shape[0] == 0:
					inningslast3 = [0]
				else:
					inningslast3 = np.sum(last3) / last3.shape
				
				if len(log) >= 5:
					last5 = np.array(log[:5])
				else:
					last5 = np.array(log)
				
				oppTeamRank = mlb.getMLBStrikoutRanks(oppTeam_abbrev)
				
				if cat == 'k':
					print(teamstats)
					for tempteam in teamstats:
						if tempteam[0] == oppTeam:
							walkKTeam = float(tempteam[10]) / float(tempteam[11])
							print("found opp team!")
							break
					if len(log) >= 5:
						kLast5 = np.float64(log[:5, 9])
						print(kLast5)
						numLast5 = np.where(kLast5 > float(line))
						last5Hit = numLast5[0].shape[0]
					elif len(log) > 0:
						kLast5 = np.float64(log[:, 9])
						numLast5 = np.where(kLast5 > float(line))
						last5Hit = numLast5[0].shape[0]
					else:
						last5Hit = 0
					features2 = [[ float(line), oppTeamRank, last5Hit, inningslast3[0], kpercent, float(temperature), fip, walkKTeam,  kwalk]]
					print(features2)
					prediction2 = strikeoutRegressionmodel.predict(features2)
					#regressionLine = float(prediction2) - float(line)
					cursor.execute("UPDATE Props SET regressionLine = ? WHERE name=? AND cat=?;", (prediction2[0], name, cat))
					sqlite_connection.commit()
				elif cat =='era':
					if len(last5) > 0:
						eraLast5 = np.float64(last5[:, 6])
						numLast5 = np.where(eraLast5 > float(line))
						last5Hit = numLast5[0].shape[0]
					else:
						last5Hit = 0
					oppTeamNum = mlb.mapTeamInt(oppTeam)
					features2 = [[float(line), oppTeamRank, last5Hit, inningslast3[0], float(temperature), float(wind),fip]]
					prediction2 = earnedRunsRegressionmodel.predict(features2)
					#regressionLine = float(prediction2) - float(line)
					cursor.execute("UPDATE Props SET regressionLine = ? WHERE name=? AND cat=?;", (prediction2[0], name, cat))
					sqlite_connection.commit()

	cursor.close()
	sqlite_connection.close()

def calcScoreNBA():
    props = []
    centerrankings = nba.getTeamPos('GC-0 C')
    pfrankings = nba.getTeamPos('GC-0 PF')
    sfrankings = nba.getTeamPos('GC-0 SF')
    sgrankings = nba.getTeamPos('GC-0 SG')
    pgrankings = nba.getTeamPos('GC-0 PG')
    assistsRank = nba.getAssistsRank()
    threeptRank = nba.get3ptRank()
    pointsRank = nba.getPointsRank()
    praRank = nba.getpraRank()
    bRank = nba.getBlocksRank()
    sRank = nba.getStealsRank()
    sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM Props WHERE regressionLine IS NULL;")
    result = cursor.fetchall()
    for a,b,c,d,e,f,g,h,i,j,k,l,m in result:
        props.append([a,b,c,j,k,l[l.find('-')+1:]])
    props.sort()
    print(props)
    previous = ""
    for i in props:
        if i[0] != previous:
            cursor.execute("SELECT * FROM nbaInfo WHERE name=?", (i[0],))
            result = cursor.fetchall()
			# If not retrieve info and add to database
            if len(result) == 0:
                names = i[0].split()
                print(i[0])
                id = nba.getPlayerID(names[0], names[1])
                if id == -1:
                    print("CAN'T GET ID")
                    continue
                else:
                    print(id)
                position, team = nba.getPlayerInfo(id)
                cursor.execute("""INSERT INTO nbaInfo(id, name, position, team) VALUES(?,?,?,?);""", (id, i[0], position,team))
                sqlite_connection.commit()
            else:
                for a, b, c, d in result:
                    id = a
                    position = c
                _, team = nba.getPlayerInfo(id)
            log = nba.getGameLog(id, False)
            if len(log) >= 5:
                last5log = log[:5]
            else:
                last5log = log
            atIndex = i[3].find("@")
            teamIndex = i[3].find(team)
            if teamIndex < atIndex:
                home = 0
                oppTeam = i[3][atIndex + 2:]
            else:
                home = 1
                oppTeam = i[3][:atIndex - 1]
            print(oppTeam)
            if len(log) > 1:
                tot = 0
                totshots = 0
                for m in last5log:
                    tot += int(m[3])
                    totshots += int(m[4][m[4].find('-') + 1:])
                minutes = tot / len(last5log)
                shotslast5 = totshots / len(last5log)
                mpg, shots = nba.getMinutes(id)
                minutes = round(minutes - float(mpg), 2)
                shots = round(shotslast5 - float(shots), 2)
            else:
                minutes = 0
                shots = 0
            positionnum = position_mapping.get(position)
            if positionnum == 1:
                posrankings = pgrankings
            elif positionnum == 2 or positionnum == 0:
                posrankings = sgrankings
            elif positionnum == 3:
                posrankings = sfrankings
            elif positionnum == 4 or positionnum == 6:
                posrankings = pfrankings
            elif i[0] == 'Ron Holland II':
                positionnum = 6
                posrankings = pfrankings
            else:
                posrankings = centerrankings
            
            fulloppteam = nba.teamnameFull(nba.teamname(nba.oppteamname2(oppTeam)))
            if fulloppteam == "LA Clippers":
                oppTeam2 = "Clippers"
            elif oppTeam == "Los Angeles Clippers":
                oppTeam2 = "Clippers"
            elif fulloppteam == "LA Lakers":
                oppTeam2 = "Lakers"
            elif oppTeam == "Los Angeles Lakers":
                oppTeam2 = "Lakers"
            elif fulloppteam == "Okla City":
                oppTeam2 = "Thunder"
            elif oppTeam == "Oklahoma City Thunder":
                oppTeam2 = "Thunder"
            else:
                oppTeam2 = fulloppteam
            previous = i[0]
            print(oppTeam2)
            oppTeamNum = team_mapping.get(oppTeam2)
         #   lastyearLog = nba.getGameLog(id,True) 
        gamescore = float(i[4])
        spread = float(i[5])
        line = float(i[1])
        print(position)
        if i[2] == "points":
            for x in posrankings[0]:
                if oppTeam2 in x[1]:
                   posrank = x[0]	   
            for x in pointsRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            features = [[line, positionnum, rank, nba.last10Hit(log,"points",i[1]), posrank, gamescore, minutes, shots, spread]]
            print(features)
            print(i)
            prediction = pointsRegressionMdoel.predict(features)
        elif i[2] == 'rebounds':
            for x in posrankings[1]:
                if oppTeam2 in x[1]:
                   posrank = x[0]
                   break
          #  logHit = nba.logHit(lastyearLog, 'rebounds', i[1])
            features = [[ line, nba.last10Hit(log,"rebounds",i[1]), nba.last5Hit(log,'rebounds',i[1]), posrank, gamescore, minutes, shots, spread]]
            prediction = reboundsRegressionModel.predict(features)
            print(i)
            print(features)
        elif i[2] == "assists":
            for x in posrankings[2]:
                if oppTeam2 in x[1]:
                    posrank = x[0]
                    break

            for x in assistsRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            last10Hit = nba.last10Hit(log, 'assists', i[1])
            #logHit = nba.logHit(lastyearLog, 'assists', i[1])
            features = [[home, rank, last10Hit, nba.last5Hit(log,'assists',i[1]), posrank, gamescore, minutes, spread]]
            prediction = assistsRegressionModel.predict(features)
            print(i)
            print(features)
        elif i[2] == '3-pt':
            for x in posrankings[3]:
               if oppTeam2 in x[1]:
                  posrank = x[0]
                  break
			
            for x in threeptRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            features = [[line, rank, nba.last10Hit(log,"3-pt",i[1]), nba.last5Hit(log,'3-pt',i[1]), posrank, oppTeamNum, gamescore, minutes, shots, spread]]
            print(features)
            prediction = threePtRegressionModel.predict(features)
            print(i)
            print(features)
        elif i[2] == 'pra':
            for x in posrankings[4]:
                if oppTeam2 in x[1]:
                    posrank = x[0]
                    break
            for x in pointsRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            features = [[line, positionnum, rank, nba.last10Hit(log,"points",i[1]), posrank, oppTeamNum, gamescore, minutes, shots, spread]]
            print(features)
            prediction = praRegressionModel.predict(features)
            print(i)
            print(features)
        elif i[2] == "steals":
            for x in posrankings[6]:
                if oppTeam2 in x[1]:
                    posrank = x[0]
                    break
            for x in sRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            features = [[line, positionnum, rank, nba.last10Hit(log,"steals",i[1]), posrank, minutes,shots]]
            print(features)
            prediction = stealsRegressionModel.predict(features)
            print(i)
            print(features)
        elif i[2] == "blocks":
            for x in posrankings[5]:
                if oppTeam2 in x[1]:
                    posrank = x[0]
                    break
            for x in bRank:
                if fulloppteam in x:
                   rank = int(x[0])
                   break
            features = [[home, line, rank, nba.last10Hit(log,"blocks",i[1]), nba.last5Hit(log,'steals',i[1]), oppTeamNum, gamescore, minutes, shots, spread]]
            print(features)
            prediction = blocksRegressionModel.predict(features)
            print(i)
            print(features)
        cursor.execute("UPDATE Props SET regressionLine = ? WHERE name = ? AND cat = ?;", (prediction[0], i[0], i[2]))
        sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
            

            

	
if __name__ == "__main__":
	getNBAProps()
#	calcScoreNBA()
