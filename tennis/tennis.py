from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import numpy as np
from selenium.common.exceptions import NoSuchElementException

def getLines():
    # Put whatever tennis moneylines from DraftKings you want
    page = requests.get("https://sportsbook.draftkings.com/leagues/tennis/australian-open-men-qualifiers")
    page = page.text
    page_soup = BeautifulSoup(page, 'html5lib')
    matches = []
    match = ""
    lines = []

    # Get players
    for num, row in enumerate(page_soup.findAll('span', attrs = {'class':'sportsbook-outcome-cell__label'})):
        if num % 2 == 0:
            match = row.text
        else:
            match = match + " vs " + row.text
            matches.append(match)
    
    # Get lines of matches
    line = ""
    for num, row in enumerate(page_soup.findAll('span', attrs = {'class':'sportsbook-odds american default-color'})):
        if num % 2 == 0:
            line = row.text
        else:
            line = line + " vs " + row.text
            lines.append(line)
    tot = []
    for num, i in enumerate(matches):
        tot.append([i, lines[num], 'hard'])
    
    return tot

def getStats(name):
    if "'" in name:
        name = name.replace("'","")
        if name == "ChristopherOConnell":
            name = "ChristopherOconnell"
    if '-' in name:
        name = name.replace('-',"")
        #name = name[:name.find('-')]
        print(name)
    if name == "SoonwooKwon":
        name = "SoonWooKwon"
    if name == "DanEvans":
        name = "DanielEvans"
    if name == "MackenzieMcDonald":
        name = "MackenzieMcdonald"
    recentstats = []
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.get(f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={name}")
    table = driver.find_element(By.ID, "recent-results")
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    for row in rows:
        cells = row.find_elements(By.XPATH, ".//td")
    
        # Create a list of text from each cell
        cell_texts = [cell.text for cell in cells]
        
        # Print or process the extracted data
        recentstats.append(cell_texts)
    
    current_rank_element = driver.find_element(By.XPATH, "//tr[3]/td[1]/b")

    # Extract the text from the element
    current_rank = current_rank_element.text

    print(current_rank)
    if current_rank.isnumeric() and int(current_rank) > 1000:
    
        table = driver.find_element(By.XPATH, "//table[@style='border-spacing:0']")

        # Find the td containing 'Current rank:'
        current_rank_label = table.find_element(By.XPATH, ".//td[contains(text(), 'Current rank:')]")

        # Find the b element that contains the rank value next to the label
        current_rank = current_rank_label.find_element(By.XPATH, ".//b").text
        print(current_rank)

    if name == "RinkyHijikata" or name == "AlexMichelsen" or name == "BillyHarris" or name == "BuYunchaokete" or name == "NisheshBasavareddy" \
        or name == "EliotSpizzirri" or name == "MaksKasnikowski" or name == "AdamWalton" or name == "AleksandarKovacevic" or name == "JakubMensik":
        plays_value = 'Right'
    elif name == "LearnerTien":
        plays_value = 'Left'
    else:
        plays_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Plays:')]")

        # Extract the full text from the element
        plays_text = plays_element.text
        # Remove the "Plays: " part and keep the rest
        plays_value = plays_text.replace("Plays: ", "")

    if 'Right' in plays_value:
        rightleft = 0
    else:
        rightleft = 1
    
    careerstats = []
    try:
        table = driver.find_element(By.ID, "career-splits")
        print("Found table with ID 'career-splits'")
    except NoSuchElementException:
        try:
            table = driver.find_element(By.ID, "career-splits-chall")  # Replace with your second table's ID
            print("Found table with ID 'other-table-id'")
        except NoSuchElementException:
            print("Neither table found.")
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    for row in rows:
        cells = row.find_elements(By.XPATH, ".//td")
    
        # Create a list of text from each cell
        cell_texts = [cell.text for cell in cells]
        
        # Print or process the extracted data
        careerstats.append(cell_texts)

    # Close the WebDriver after scraping is complete
    driver.quit()

    return recentstats, careerstats, current_rank, rightleft
