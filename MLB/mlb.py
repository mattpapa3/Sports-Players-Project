import requests
from bs4 import BeautifulSoup
import json
import numpy as np
from datetime import datetime, timedelta, date
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

team_mapping = {
    "Miami Marlins" : 1,
    "New York Mets" : 2,
    "Oakland Athletics" : 3,
    "Tampa Bay Rays" : 4,
    "Cincinnati Reds" : 5,
    "Philadelphia Phillies" : 6,
    "Detroit Tigers" : 7,
    "New York Yankees" : 8,
    "Baltimore Orioles" : 9,
    "Chicago White Sox" : 10,
    "Pittsburgh Pirates" : 11,
    "Seattle Mariners" : 12,
    "Cleveland Guardians" : 13,
    "Houston Astros" : 14,
    "Minnesota Twins" : 15,
    "St. Louis Cardinals" : 16,
    "Milwaukee Brewers" : 17,   
    "Texas Rangers" : 18,
    "Chicago Cubs" : 19,
    "Washington Nationals" : 20,
    "Colorado Rockies" : 21,
    "Kansas City Royals" : 22,
    "San Francisco Giants" : 23,
    "Toronto Blue Jays" : 24,
    "Los Angeles Angels" : 25,
    "Los Angeles Dodgers" : 26,
    "Arizona Diamondbacks" : 27,
    "San Diego Padres" : 28,
    "Atlanta Braves" : 29,
    "Boston Red Sox" : 30
}


def getStartingPitchers():
    team = requests.get("https://www.espn.com/mlb/scoreboard", headers={"User-Agent": "Mozilla/5.0"})
    schedule = team.text
    schedule = BeautifulSoup(schedule, 'html5lib')

    pitchers = []
    teams = []
    matchups = []
    id = []
    gameOver = 0
    inGame = 0
    save = 0
    dueUp = 0
    for row in schedule.findAll('span', attrs={'class': 'Athlete__PlayerName'}):
        pitchers.append(row.text)

    for row in schedule.findAll('span', attrs={'class': 'Athlete__NameDetails ml2 clr-gray-04 di ns9'}):
        if len(row.text) > 0:
            teams.append(row.text[3:])

    for row in schedule.findAll('a', attrs={'class': 'Athlete db Athlete__Link clr-gray-01'}):
        id.append(row['href'].split('/')[-1])

    for row in schedule.findAll('a', attrs={'class': 'AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100 mr2'}):
        if row.text == "Highlights":
            gameOver += 1
        if row.text == "Play-by-Play":
            inGame += 1
    for row in schedule.findAll('div', attrs={'class':'clr-gray-04 ttu n10 w-25'}):
        if row.text == "SAVE":
            save += 1
    for row in schedule.findAll('h4', attrs={'class':'clr-gray-04 n8 fw-normal ttu mb3'}):
        if row.text == "due up":
            dueUp += 1
    

    id = id[inGame * 2:len(pitchers) - (gameOver * 2) - save]
    pitchers = pitchers[(inGame * 2) + dueUp:len(pitchers) - (gameOver * 2) - save]

    i = 0
    m = 0
    print(pitchers)
    while i+1 < len(pitchers):
        if pitchers[i] == 'Undecided':
            matchups.append([pitchers[i], teams[i], pitchers[i+1], teams[i+1], id[m]])
            m += 1
        elif pitchers[i+1] == 'Undecided':
            matchups.append([pitchers[i], teams[i], id[m], pitchers[i+1], teams[i+1]])
            m += 1
        else:
            matchups.append([pitchers[i], teams[i], id[m], pitchers[i+1], teams[i+1], id[m+1]])
            m += 2
        i += 2

    return matchups


def getMLBTeamvs(schedule, oppTeam):
    vs = []
    stats = []
    wins = 0
    loss = 0
    runs = 0
    for i in schedule:
        if MLBabbrev(oppTeam) in MLBabbrev(i[1]):
            vs.append(i)
    m = 0
    if len(vs) > 0:
        for i in vs:
            index = i[2].find('-')
            if 'L' in i[2] and "Post" not in i[2]:
                loss += 1
                m += 1
                runs += int(i[2][index + 1])
            elif "Post" not in i[2]:
                wins += 1
                runs += int(i[2][1])
                m += 1
        total = round(runs / m, 1)
        stats.append(str(wins) + "-" + str(loss))
        stats.append(total)
    return stats

def MLBteamname(abbrev):
    team = abbrev
    if abbrev == "MIA" or abbrev == "Miami":
        team = "Miami Marlins"
    elif abbrev == "NYM" or abbrev == "Mets" or abbrev == "NY Mets":
        team = "New York Mets"
    elif abbrev == "OAK" or abbrev == "Oakland":
        team = "Oakland Athletics"
    elif abbrev == "TB" or abbrev == "Bay" or abbrev == "Tampa Bay":
        team = "Tampa Bay Rays"
    elif abbrev == "CIN" or abbrev == "Cincinnati":
        team = "Cincinnati Reds"
    elif abbrev == "PHI" or abbrev == "Philadelphia":
        team = "Philadelphia Phillies"
    elif abbrev == "DET" or abbrev == "Detroit":
        team = "Detroit Tigers"
    elif abbrev == "NYY" or abbrev == "Yankees" or abbrev == "NY Yankees":
        team = "New York Yankees"
    elif abbrev == "BAL" or abbrev == "Baltimore":
        team = "Baltimore Orioles"
    elif abbrev == "CHW" or abbrev == "Chi Sox":
        team = "Chicago White Sox"
    elif abbrev == "PIT" or abbrev == "Pittsburgh" or abbrev == "Pirates":
        team = "Pittsburgh Pirates"
    elif abbrev == "SEA" or abbrev == "Seattle":
        team = "Seattle Mariners"
    elif abbrev == "CLE" or abbrev == "Cleveland":
        team = "Cleveland Guardians"
    elif abbrev == "HOU" or abbrev == "Houston":
        team = "Houston Astros"
    elif abbrev == "MIN" or abbrev == "Minnesota":
        team = "Minnesota Twins"
    elif abbrev == "STL" or "Louis" in abbrev:
        team = "St. Louis Cardinals"
    elif abbrev == "MIL" or abbrev == "Milwaukee":
        team = "Milwaukee Brewers"
    elif abbrev == "TEX" or abbrev == "Texas":
        team = "Texas Rangers"
    elif abbrev == "CHC" or "Cubs" in abbrev:
        team = "Chicago Cubs"
    elif abbrev == "WSH" or abbrev == "Washington" or abbrev == "WAS":
        team = "Washington Nationals"
    elif abbrev == "COL" or abbrev == "Colorado":
        team = "Colorado Rockies"
    elif abbrev == "KC" or abbrev == "Kansas City":
        team = "Kansas City Royals"
    elif abbrev == "SF" or abbrev == "SF Giants":
        team = "San Francisco Giants"
    elif abbrev == "TOR" or abbrev == "Toronto":
        team = "Toronto Blue Jays"
    elif abbrev == "LAA" or "Angels" in abbrev:
        team = "Los Angeles Angels"
    elif abbrev == "LAD" or abbrev == "LA Dodgers" or abbrev == "Dodgers":
        team = "Los Angeles Dodgers"
    elif abbrev == "ARI" or abbrev == "Arizona" or abbrev == "AZ":
        team = "Arizona Diamondbacks"
    elif abbrev == "SD" or "Diego" in abbrev:
        team = "San Diego Padres"
    elif abbrev == "ATL" or abbrev == "Atlanta":
        team = "Atlanta Braves"
    elif abbrev == "BOS" or abbrev == "Boston":
        team = "Boston Red Sox"
    return team



def getPitcherRecord(id):
    player = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    team = player.text
    team = BeautifulSoup(team, 'html5lib')
    record = ""

    for row in team.findAll('div', attrs={'class': 'StatBlockInner__Value tc fw-medium n2 clr-gray-02'}):
        record = row.text
        break
    
    return record

def getRoadHomeRunsPerGame(schedule, home):
    i = 0
    count = 0
    runs = 0
    if home:
        sub = "vs"
    else:
        sub = "@"
    while i < len(schedule):
        if sub in schedule[i][1] and "Post" not in schedule[i][2]:
            index = schedule[i][2].find('-')
            if 'L' in schedule[i][2]:
                index2 = schedule[i][2].find(' ')
                runs += int(schedule[i][2][index + 1:index2])
            else:
                runs += int(schedule[i][2][1:index])
            count += 1
        i += 1

    avg = runs / count

    return avg


def getLast10avgRuns(schedule):
    i = 0
    m = len(schedule) - 1
    runs = 0
    while i < 10:
        index = schedule[m][2].find('-')
        if 'L' in schedule[m][2] and "Post" not in schedule[m][2]:
            index2 = schedule[m][2].find(' ')
            runs += int(schedule[m][2][index + 1:index2])
            i += 1
        elif "Post" not in schedule[m][2]:
            runs += int(schedule[m][2][1:index])
            i += 1
        m -= 1

    avg = runs / 10
    return avg


def recordAtHomeAway(log, home):
    wins = 0
    loss = 0
    if home:
        sub = "vs"
    else:
        sub = "@"
    
    for i in log:
        if sub in i[1]:
            if 'L' in i[2]:
                loss += 1
            elif 'W' in i[2]:
                wins += 1
    
    record = str(wins) + "-" + str(loss)
    return record


def getAvgRunsScoredWithPitcher(log):
    runs = 0
    m = 0
    avg = 0
    for i in log:
        if 'L' in i[2] and "Post" not in i[2]:
            runs += int(i[2][len(i[2]) - 1])
            m += 1
        elif "Post" not in i[2]:
            runs += int(i[2][1])
            m += 1
    
    if m > 0:
        avg = runs / m
    return avg

def getTeamSchedule(teamAbbrev):
    teamAbbrev = MLBabbrev(teamAbbrev)
    team = requests.get(f"https://www.espn.com/mlb/team/schedule/_/name/{teamAbbrev}", headers={"User-Agent": "Mozilla/5.0"})
    schedule = team.text
    schedule = BeautifulSoup(schedule, 'html5lib')

    i = 0
    scores = []
    stop = False
    for row in schedule.findAll('td', attrs ={'class': 'Table__TD'}):
        if row.text == "DATE":
            stop = True
        if row.text == "DATE" and len(scores) > 0:
            break
        if not stop and i < 3:
            scores.append(row.text)
        if stop and i == 7:
            stop = False
        if i == 7 or row.text == "Postponed":
            i = -1
        i += 1
        if "Los Angeles" in row.text:
            tag = row.find('a')
            if 'angels' in tag['href']:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("Los Angeles", "Angels")
            else:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("Los Angeles", "Dodgers")
        if "New York" in row.text:
            tag = row.find('a')
            if 'yankees' in tag['href']:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("New York", "Yankees")
            else:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("New York", "Mets")
        if "Chicago" in row.text:
            tag = row.find('a')
            if 'cubs' in tag['href']:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("Chicago", "Cubs")
            else:
                scores[len(scores) - 1] = scores[len(scores) - 1].replace("Chicago", "White Sox")

    team = requests.get(f"https://www.espn.com/mlb/team/schedule/_/name/{teamAbbrev}/seasontype/2/half/1")
    scores1 = []
    schedule = team.text
    schedule = BeautifulSoup(schedule, 'html5lib')
    i = 0
    stop = False

    for row in schedule.findAll('td', attrs ={'class': 'Table__TD'}):
        if row.text == "DATE":
            stop = True
        if row.text == "DATE" and len(scores1) > 0:
            break
        if not stop and i < 3:
            scores1.append(row.text)
        if stop and i == 7:
            stop = False
        if i == 7 or row.text == "Postponed":
            i = -1
        i += 1
        if "Los Angeles" in row.text:
            tag = row.find('a')
            if 'angels' in tag['href']:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("Los Angeles", "Angels")
            else:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("Los Angeles", "Dodgers")
        if "New York" in row.text:
            tag = row.find('a')
            if 'yankees' in tag['href']:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("New York", "Yankees")
            else:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("New York", "Mets")
        if "Chicago" in row.text:
            tag = row.find('a')
            if 'cubs' in tag['href']:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("Chicago", "Cubs")
            else:
                scores1[len(scores1) - 1] = scores1[len(scores1) - 1].replace("Chicago", "White Sox")

    scores = scores1 + scores
    schedule = []
    i = 0
    while i < len(scores):
        schedule.append([scores[i], scores[i+1], scores[i+2]])
        i += 3
    
    return schedule


def getMatchupsOverUnders():
    lines = requests.get("https://www.espn.com/mlb/scoreboard", headers={"User-Agent": "Mozilla/5.0"})
    teams = lines.text
    teams = BeautifulSoup(teams, 'html5lib')
    lines = []
    matchups = []
    gameOver = 0
    gameStarted = 0
    for row in teams.findAll('a', attrs={'class': 'AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100 mr2'}):
        if row.text == "Highlights":
            gameOver += 1
        if row.text == "Play-by-Play":
            gameStarted += 1

    for row in teams.findAll('div', attrs={'class': 'OddsStripWrapper flex flex-row justify-between'}):
        print(row.text)
        if len(row.text) > 0:
            lines.append(row.text)

    for row in teams.findAll('div', attrs={'class': 'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):
        matchups.append(row.text)

    matchups = matchups[gameStarted*2:(len(matchups) - gameOver*2)]

    total = []
    i = 0
    m = 0
    print(lines)
    while i < len(matchups):
        if m < len(lines):
            if MLBabbrev(matchups[i]) in lines[m] or MLBabbrev(matchups[i+1]) in lines[m] or "EVEN" in lines[m]:
                total.append([matchups[i], matchups[i + 1], lines[m]])
                m += 1
            else:
                total.append([matchups[i], matchups[i + 1]])
        else:
            total.append([matchups[i], matchups[i + 1]])
        i += 2

    slash = '/'
    for i in total:
        if len(i) > 2:
            index = i[2].find(slash)
            i[2] = i[2][:index - 1] + ' ' + i[2][index - 1:]

    return total


def getMLBPlayerID(firstname, lastname):
    firstname = firstname.lower()
    lastname = lastname.lower()
    if firstname[len(firstname) - 1] == " ":
        firstname = firstname[:-1]
    
    if lastname[len(lastname) - 1] == " ":
        lastname = lastname[:-1]
    player_found = True
    fullname = "/" + firstname + "-" + lastname
    player_API = requests.get(f'http://www.espn.com/mlb/players/_/search/{lastname}', headers={"User-Agent": "Mozilla/5.0"})  
    player = player_API.text
    player_soup = BeautifulSoup(player, 'html5lib')
    temp = 'No players'
    for row in player_soup.findAll('tr', attrs = {'class':'oddrow'}):
        if temp in row.text:
            player_found = False
    if fullname == "/julio-rodriguez":
        player = player[:player.rfind(fullname)]
        index = player.rfind('/')               # index of last occurence of "/"
        id = player[index + 1:]
    elif player_found == True:
        player = player[:player.find(fullname)]
        if len(player) > 60000:
            id = -1
        else:
            index = player.rfind('/')               # index of last occurence of "/"
            id = player[index + 1:]
    else:
        id = -1                                                  # Right after last occurence of "/" is players id
    return id

def getMLBGameLog(id, pos, shohei):
   # if shohei:
   #     log_api = requests.get('https://www.espn.com/mlb/player/gamelog/_/id/39832/year/2023/category/batting', headers={"User-Agent": "Mozilla/5.0"})
    #else:
    log_api = requests.get(f'https://www.espn.com/mlb/player/gamelog/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    lines = log_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')

    log = []
    stats_log = []

    stop = False
    i = 0
    m = 0
    n = 0

    if pos != 'Starting Pitcher' and pos != 'Relief Pitcher': #or shohei:
        for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
            m = m + 1
            if row.text == 'Totals' or row.text == 'april' or row.text == 'Milwaukee' or row.text == 'Texas' or row.text == 'Baltimore' or row.text == 'Cleveland' or row.text == 'Seattle'\
                or row.text == 'NY Yankees' or row.text == 'Los Angeles' or row.text == 'Philadelphia' or row.text == "Houston":
                break
            if row.text == 'april' or row.text == 'Postseason' or row.text == 'october' or row.text == 'september' or row.text == 'august' or row.text =='july' or row.text =='june' or row.text =='may':
                stop = True
            if row.text == 'march':
                break
            if not stop and m != 0 and 'Previously' not in row.text:
                stats_log.append(row.text)
            if stop:
                i = i + 1
            if i == 16:
                stop = False
                i = 0
                m = -1
            if m == 18:
                m = 0

        stop = False
        n  = 0
        check = len(stats_log)

        while n < check:
            log.append(stats_log[n:n+19])
            n = n + 19
    
    else:
        for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
            m = m + 1
            if row.text == 'Totals' or row.text == 'Milwaukee' or row.text == "Houston":
                break
            if row.text == 'april' or row.text == 'march' or row.text == 'Postseason' or row.text == 'october' or row.text == 'september' or row.text == 'august' or row.text =='july' or row.text =='june' or row.text =='may':
                stop = True
            if not stop and m != 0 and 'Previously' not in row.text:
                stats_log.append(row.text)
            if stop:
                i = i + 1
            if i == 15:
                stop = False
                i = 0
                m = -1
            if m == 17:
                m = 0

        stop = False
        n  = 0

        check = len(stats_log)

        while n < check:
            log.append(stats_log[n:n+18])
            n = n + 18
        
        l = len(log) - 1
        if l > 0:
            while l != 0:
                if checkString(log[l][0]):
                    break
                else:
                    log.pop(l)
                l = len(log) - 1
        
    for row in lines_soup.findAll('div', attrs = {'class': "NoDataAvailable__Msg__Content"}):
        if row.text == "No available information.":
            log = []
        
    
    return log


def checkString(s):
    check = False
    for x in s:
        if x.isdigit():
            check = True
            break
    
    return check



def getMLBPosition(id):
    nba_API = requests.get(f'https://www.espn.com/mlb/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    position = ''
    soup2 = BeautifulSoup(recent_data, 'html5lib')

    i = 0
    for row in soup2.findAll('li', attrs = {'class':''}):
        if i == 1:
            position = row.text
        i = i + 1
    
    return position


def getMLB2022Log(id, pos, shohei):
    if shohei:
        log_api = requests.get('https://www.espn.com/mlb/player/gamelog/_/id/39832/year/2023/category/batting', headers={"User-Agent": "Mozilla/5.0"})
    else:
        log_api = requests.get(f'https://www.espn.com/mlb/player/gamelog/_/id/{id}/year/2023', headers={"User-Agent": "Mozilla/5.0"})
    lines = log_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')

    log = []
    stats_log = []

    stop = False
    i = 0
    m = 0
    n = 0

    if pos != 'Starting Pitcher' and pos != 'Relief Pitcher' or shohei:
        for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
            m = m + 1
            if row.text == 'Totals' or row.text == 'march':
                break
            if row.text == 'april' or row.text == 'Postseason' or row.text == 'october' or row.text == 'september' or row.text == 'august' or row.text =='july' or row.text =='june' or row.text =='may':
                stop = True
            if not stop and m != 0 and 'Previously' not in row.text:
                stats_log.append(row.text)
            if stop:
                i = i + 1
            if i == 16:
                stop = False
                i = 0
                m = -1
            if m == 18:
                m = 0

        stop = False
        n  = 0

        check = len(stats_log)

        while n < check:
            log.append(stats_log[n:n+19])
            n = n + 19
    
    else:
        for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
            m = m + 1
            if row.text == 'Totals':
                break
            if row.text == 'april' or row.text == 'march' or row.text == 'Postseason' or row.text == 'october' or row.text == 'september' or row.text == 'august' or row.text =='july' or row.text =='june' or row.text =='may':
                stop = True
            if not stop and m != 0 and 'Previously' not in row.text:
                stats_log.append(row.text)
            if stop:
                i = i + 1
            if i == 15:
                stop = False
                i = 0
                m = -1
            if m == 17:
                m = 0

        stop = False
        n  = 0

        check = len(stats_log)

        while n < check:
            log.append(stats_log[n:n+18])
            n = n + 18
        
        l = len(log) - 1
        if l != -1:
            while l != 0:
                if checkString(log[l][0]):
                    break
                else:
                    log.pop(l)
                l = len(log) - 1
    
    return log

def MLBhomeoraway(id):
    player_API = requests.get(f'https://www.espn.com/mlb/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    player = player_API.text
    soup = BeautifulSoup(player, 'html5lib')
    home = True

    for row in soup.findAll('div', attrs = {'class':'PlayerHeader__Team n8 mt3 mb4 flex items-center mt3 mb4 clr-gray-01'}):
        team = row.text
        break

    team = team[:team.find('#')]
    team_ab = team.split()
    l = len(team_ab)
    i = 0
    if team_ab[1] == "Cubs":
        team_ab[l - 1] = "Cubs"
    elif team_ab[0] == "Chicago":
        team_ab[l - 1] = "White Sox"
    elif team_ab[0] == "Boston":
        team_ab[l - 1] = "Red Sox"
    elif team_ab[0] == "Toronto":
        team_ab[l - 1] = "Blue Jays"
    

    for row in soup.findAll('div', attrs = {'class': 'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):
        if row.text == team_ab[l - 1] and i == 0:
            home = False
        if row.text == team_ab[l - 1] and i == 1:
            home = True
        i = i + 1
    
    return home


def getOppStartingPitcher(id,home):
    pitcher = ""
    game = requests.get(f'https://www.espn.com/mlb/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')

    game_link = soup.find("a",{"class": "Gamestrip__Competitors relative flex Gamestrip__Competitors--border"}).get("href")

    game = requests.get(game_link, headers={"User-Agent": "Mozilla/5.0"})
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')

    firstdiv = soup.find('div', attrs = {'class':'PageLayout__LeftAside'})
    rows = firstdiv.find_all('div', class_='mLASH VZTD GFuaT CFZbp GpQCA')

    for num, row in enumerate(rows):
        child_div = row.find('div', attrs={'class': 'ToujM AsfGG ucZkc UmfeF'})
        if num == 0 and home:
            pitcher = child_div.text
            break
        elif num == 1 and not home:
            pitcher = child_div.text
            break
    
    return pitcher


def getMLBOppTeam(id, home):
    game = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    oppTeamID = -1
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    o = 0
    opp_team = "None"
    for row in soup.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):     #Find what team player is on
        if home and o == 0:
            opp_team = row.text
        elif not home and o == 1:
            opp_team = row.text
        o = o + 1
    return opp_team

def getMLBOppTeamID(id, home):
    game = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    oppTeamID = -1
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    o = 0
    for row in soup.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):     #Find what team player is on
        if home and o == 0:
            opp_team = row.text
        elif not home and o == 1:
            opp_team = row.text
        o = o + 1
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')

    for row in soup.findAll('option',{"data-url":"#"}):
        if opp_team in row.text:
            oppTeamID = row.get("value")
    
    return oppTeamID

def getMLBStrikoutRanks(oppTeam):
    game = requests.get("https://www.teamrankings.com/mlb/stat/strikeouts-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    rank = 0
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)

    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBabbrev(row.text)])
        i += 1

    for i in ranks:
        if oppTeam == i[1]:
            rank = int(i[0])
    
    return rank


def getMLBRunsPerGameRanks(oppTeam):
    game = requests.get("https://www.teamrankings.com/mlb/stat/runs-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    rank = 0
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)

    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBteamname(row.text)])
        i += 1

    for i in ranks:
        if oppTeam == i[1]:
            rank = int(i[0])
    
    return rank


def getMLBHitsPerGameRanks(oppTeam):
    game = requests.get("https://www.teamrankings.com/mlb/stat/hits-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    rank = 0
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)

    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBteamname(row.text)])
        i += 1

    for i in ranks:
        if oppTeam == i[1]:
            rank = int(i[0])
    
    return rank

def getMLBStrikoutRanksTeams():
    game = requests.get("https://www.teamrankings.com/mlb/stat/strikeouts-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)
    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBteamname(row.text)])
        i += 1
    return ranks

def getMLBRunsPerGameRanksTeams():
    game = requests.get("https://www.teamrankings.com/mlb/stat/runs-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    rank = 0
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)

    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBteamname(row.text)])
        i += 1
    
    return ranks

def getMLBHitsPerGameRanksTeams():
    game = requests.get("https://www.teamrankings.com/mlb/stat/hits-per-game")
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    ranks = []
    for row in soup.findAll('td', attrs = {'class':'rank text-center'}):
        ranks.append(row.text)

    i = 0
    for row in soup.findAll('td', attrs = {'class':'text-left nowrap'}):
        ranks[i] = ([ranks[i], MLBteamname(row.text)])
        i += 1
    
    return ranks


def getHittervsPitcherStats(id,teamid, pitcher):
    HittervsPitcherLog = []
    go = False
    i = 0
    game = requests.get(f"https://www.espn.com/mlb/player/batvspitch/_/id/{id}/teamId/{teamid}", headers={"User-Agent": "Mozilla/5.0"})
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    for row in soup.findAll('td', attrs = {'class':'Table__TD'}):
        if go:
            HittervsPitcherLog.append(row.text)
            i += 1
        if row.text == pitcher:
            go = True
            print("FOUND!!")
        if i == 10:
            break
    
    return HittervsPitcherLog


def getPitcherThrowingArm(id):
    game = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    throw = ""
    i = 0
    for row in soup.findAll('div', attrs = {'class':'fw-medium clr-black'}):
        if i == 2:
            throw = row.text
            break
        i += 1

    throw = throw[throw.find('/') + 1:]
    if "Los Angeles" in throw:
        throw = "Right"
    return throw


def getPlayerInfo(id):
    player = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    data = player.text
    soup = BeautifulSoup(data, 'html5lib')
    
    position = ""
    team = ""
    leftright = ""
    i = 0
    for row in soup.findAll('li', attrs = {'class':''}):
        if i == 1:
            position = row.text
        i = i + 1
    
    for row in soup.findAll('a', attrs = {'class':'AnchorLink clr-black'}):
        team = row.text
    
    i = 0
    for row in soup.findAll('div', attrs = {'class':'fw-medium clr-black'}):
        if i == 2:
            leftright = row.text
            break
        i += 1
    
    if "Pitcher" not in position:
        leftright = leftright[:leftright.find("/")]
    else:
        leftright = leftright[leftright.find("/") + 1:]
    
    if leftright == "Right":
        leftright = 0
    elif leftright == "Left":
        leftright = 1
    elif leftright == "Both":
        leftright = 2
    return position, team, leftright

def get_team_number(team_name):
    team_mapping = {
        "Miami Marlins": 1,
        "New York Mets": 2,
        "Oakland Athletics": 3,
        "Tampa Bay Rays": 4,
        "Cincinnati Reds": 5,
        "Philadelphia Phillies": 6,
        "Detroit Tigers": 7,
        "New York Yankees": 8,
        "Baltimore Orioles": 9,
        "Chicago White Sox": 10,
        "Pittsburgh Pirates": 11,
        "Seattle Mariners": 12,
        "Cleveland Guardians": 13,
        "Houston Astros": 14,
        "Minnesota Twins": 15,
        "St. Louis Cardinals": 16,
        "Milwaukee Brewers": 17,
        "Texas Rangers": 18,
        "Chicago Cubs": 19,
        "Washington Nationals": 20,
        "Colorado Rockies": 21,
        "Kansas City Royals": 22,
        "San Francisco Giants": 23,
        "Toronto Blue Jays": 24,
        "Los Angeles Angels": 25,
        "Los Angeles Dodgers": 26,
        "Arizona Diamondbacks": 27,
        "San Diego Padres": 28,
        "Atlanta Braves": 29,
        "Boston Red Sox": 30
    }
    return team_mapping.get(team_name, "Team not found")





def rightvsLeftStats(id, throw):
    game = requests.get(f"https://www.espn.com/mlb/player/splits/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    stats = []
    i = 0
    m = 0
    if throw == "Left":
        for row in soup.findAll('td', attrs = {'class': 'Table__TD'}):
            if m == 2 and i < 13:
                stats.append(row.text)
                i += 1
            if row.text == "OPS":
                m += 1
            
    else:
        for row in soup.findAll('td', attrs = {'class': 'Table__TD'}):
            if m == 2:
                i += 1
            if i > 16 and i < 30:
                stats.append(row.text)
            if row.text == "OPS":
                m += 1
    return stats


def MLBabbrev(teamname):
    if "Miami" in teamname or "Marlins" in teamname:
        teamname = "MIA"
    elif "Mets" in teamname or "NY Mets" in teamname:
        teamname = "NYM"
    elif "Oakland" in teamname or "Athletics" in teamname:
        teamname = "OAK"
    elif "Rays" in teamname or "Tampa Bay" in teamname:
        teamname = "TB"
    elif "Reds" in teamname or "Cincinnati" in teamname:
        teamname = "CIN"
    elif "Phillies" in teamname or "Philadelphia" in teamname:
        teamname = "PHI"
    elif "Tigers" in teamname or "Detroit" in teamname:
        teamname = "DET"
    elif "Yankees" in teamname or "York" in teamname:
        teamname = "NYY"
    elif "Orioles" in teamname or "Baltimore" in teamname:
        teamname = "BAL"
    elif "White Sox" in teamname or "Chi Sox" in teamname:
        teamname = "CHW"
    elif "Pirates" in teamname or "Pittsburgh" in teamname:
        teamname = "PIT"
    elif "Mariners" in teamname or "Seattle" in teamname:
        teamname = "SEA"
    elif "Guardians" in teamname or "Cleveland" in teamname:
        teamname = "CLE"
    elif "Astros" in teamname or "Houston" in teamname:
        teamname = "HOU"
    elif "Twins" in teamname or "Minnesota" in teamname:
        teamname = "MIN"
    elif "Cardinals" in teamname or "St. Louis" in teamname:
        teamname = "STL"
    elif "Brewers" in teamname or "Milwaukee" in teamname:
        teamname = "MIL"
    elif "Rangers" in teamname or "Texas" in teamname:
        teamname = "TEX"
    elif "Cubs" in teamname or "Chi Cubs" in teamname:
        teamname = "CHC"
    elif "Nationals" in teamname or "Washington" in teamname:
        teamname = "WSH"
    elif "Rockies" in teamname or "Colorado" in teamname:
        teamname = "COL"
    elif "Royals" in teamname or "Kansas City" in teamname:
        teamname = "KC"
    elif "Giants" in teamname or "San Francisco" in teamname:
        teamname = "SF"
    elif "Blue Jays" in teamname or "Toronto" in teamname:
        teamname = "TOR"
    elif "Angels" in teamname:
        teamname = "LAA"
    elif "Dodgers" in teamname:
        teamname = "LAD"
    elif "Diamondbacks" in teamname or "Arizona" in teamname:
        teamname = "ARI"
    elif "Padres" in teamname or "San Diego" in teamname:
        teamname = "SD"
    elif "Braves" in teamname or "Atlanta" in teamname:
        teamname = "ATL"
    elif "Boston" in teamname or "Red Sox" in teamname:
        teamname = "BOS"
    return teamname


def getFirstInnLog(id, lastyear):
    if lastyear:
        game = requests.get(f'https://www.espn.com/mlb/player/gamelog/_/id/{id}/year/2022/', headers={"User-Agent": "Mozilla/5.0"})
    else:
        game = requests.get(f"https://www.espn.com/mlb/player/_/id/{id}", headers={"User-Agent": "Mozilla/5.0"})
    home = False
    data = game.text
    soup = BeautifulSoup(data, 'html5lib')
    o = 0
    FirstinnLog = []
    team = soup.find('img', attrs = {'class':'Image Logo Logo__sm'})
    team = MLBabbrev(team.get('title'))
    for row in soup.findAll('a', attrs = {'class':'AnchorLink'}):     #Find what team player is on
        temp = row.get('href')
        if "gameId" in temp and "https" in temp:
            game = requests.get(temp)
            data = game.text
            soup2 = BeautifulSoup(data, 'html5lib')
            i = 0
            for row in soup2.findAll('div', attrs = {'class':'flex items-start mr7'}):
                if row.text in team and i == 0:
                    home = False
                elif row.text in team and i == 1:
                    home = True
                i += 1
            m = 0
            if(home):
                for row in soup2.findAll('tr', attrs={'class':'Table__TR Table__TR--sm Table__even'}):
                    if m == 1:
                        temp = 'vs' + row.text
                    if m == 3:
                        FirstinnLog.append([temp,row.text[0]])
                        break
                    m += 1
            else:
                for row in soup2.findAll('tr', attrs={'class':'Table__TR Table__TR--sm Table__even'}):
                    if m == 2:
                        temp = '@' + row.text
                    if m == 4:
                        FirstinnLog.append([temp,row.text[0]])
                        break
                    m += 1
    return FirstinnLog


def getMLBPlayerScore(log, pos, home, stat, num_stat, lastYearlog, opp_Team, shohei):
    score = 0
    if len(lastYearlog) < 2:
        lastYearlog = []
    opp_Team = MLBabbrev(opp_Team)
    if pos != "Starting Pitcher" and pos != 'Relief Pitcher' and not shohei:
        if stat == 'tb':
            if home:
                sub = "vs"
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        tb = float(log[l][5])
                        tb = tb + float(log[l][6])
                        tb = tb + (float(log[l][7]) * 2)
                        tb = tb + (float(log[l][8]) * 3)
                        if tb > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        tb = float(lastYearlog[l][5])
                        tb = tb + float(lastYearlog[l][6])
                        tb = tb + (float(lastYearlog[l][7]) * 2)
                        tb = tb + (float(lastYearlog[l][8]) * 3)
                        if tb > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.12
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            if not home:
                sub = "@"
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        tb = float(log[l][5])
                        tb = tb + float(log[l][6])
                        tb = tb + (float(log[l][7]) * 2)
                        tb = tb + (float(log[l][8]) * 3)
                        if tb > float(num_stat):
                            over += 1
                    l += 1
                ratio = 0
                if total > 0:
                    ratio = over / total

                if ratio > 0.7:
                    score = score + 1
                elif ratio > 0.6:
                    score = score + 0.5
                elif ratio > 0.5:
                    score = score + 0.25
                elif ratio < 0.3:
                    score = score - 1
                elif ratio < 0.4:
                    score = score - 0.5
                elif ratio < 0.5:
                    score = score - 0.25
                
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        tb = float(lastYearlog[l][5])
                        tb = tb + float(lastYearlog[l][6])
                        tb = tb + (float(lastYearlog[l][7]) * 2)
                        tb = tb + (float(lastYearlog[l][8]) * 3)
                        if tb > float(num_stat):
                            over += 1
                    l += 1
                
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.12
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            
            over = 0
            l = 0
            tb = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    tb = float(log[l][5])
                    tb = tb + float(log[l][6])
                    tb = tb + (float(log[l][7]) * 2)
                    tb = tb + (float(log[l][8]) * 3)
                    if float(tb) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    tb = float(log[l][5])
                    tb = tb + float(log[l][6])
                    tb = tb + (float(log[l][7]) * 2)
                    tb = tb + (float(log[l][8]) * 3)
                    if float(tb) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1.5
            if ratio >= 0.8:
                score = score + 1
            elif ratio >= 0.7:
                score = score + 0.5
            elif ratio >= 0.6:
                score = score + 0.25
            elif ratio <= 0.1:
                score = score - 1.5
            elif ratio <= 0.2:
                score = score - 1
            elif ratio <= 0.3:
                score = score - 0.5
            elif ratio <= 0.4:
                score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            tb = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    tb = float(log[l][5])
                    tb = tb + float(log[l][6])
                    tb = tb + (float(log[l][7]) * 2)
                    tb = tb + (float(log[l][8]) * 3)
                    if float(log[l][15]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            tb = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    tb = float(lastYearlog[l][5])
                    tb = tb + float(lastYearlog[l][6])
                    tb = tb + (float(lastYearlog[l][7]) * 2)
                    tb = tb + (float(lastYearlog[l][8]) * 3)
                    if float(lastYearlog[l][15]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 0.75
                elif ratio >= 0.8:
                    score = score + 0.5
                elif ratio >= 0.7:
                    score = score + 0.25
                elif ratio >= 0.6:
                    score = score + 0.12
                elif ratio <= 0.1:
                    score = score - 0.75
                elif ratio <= 0.2:
                    score = score - 0.5
                elif ratio <= 0.3:
                    score = score - 0.25
                elif ratio <= 0.4:
                    score = score - 0.12
        
        elif stat == 'r':
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.12
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                ratio = over / total

                if ratio > 0.7:
                    score = score + 1
                elif ratio > 0.6:
                    score = score + 0.5
                elif ratio > 0.5:
                    score = score + 0.25
                elif ratio < 0.3:
                    score = score - 1
                elif ratio < 0.4:
                    score = score - 0.5
                elif ratio < 0.5:
                    score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.1
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            
            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1.5
            if ratio >= 0.8:
                score = score + 1
            elif ratio >= 0.7:
                score = score + 0.5
            elif ratio >= 0.6:
                score = score + 0.25
            elif ratio <= 0.1:
                score = score - 1.5
            elif ratio <= 0.2:
                score = score - 1
            elif ratio <= 0.3:
                score = score - 0.5
            elif ratio <= 0.4:
                score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    if float(lastYearlog[l][4]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
        
        elif stat == 'hrb':
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        hrb = float(log[l][4]) + float(log[l][5]) + float(log[l][9])
                        if float(hrb) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                tb = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        hrb = float(lastYearlog[l][4]) + float(lastYearlog[l][5]) + float(lastYearlog[l][9])
                        if float(hrb) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.12
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        hrb = float(log[l][4]) + float(log[l][5]) + float(log[l][9])
                        if float(hrb) > float(num_stat):
                            over += 1
                    l += 1
                ratio = 0
                if total > 0:
                    ratio = over / total

                if ratio > 0.7:
                    score = score + 1
                elif ratio > 0.6:
                    score = score + 0.5
                elif ratio > 0.5:
                    score = score + 0.25
                elif ratio < 0.3:
                    score = score - 1
                elif ratio < 0.4:
                    score = score - 0.5
                elif ratio < 0.5:
                    score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        hrb = float(lastYearlog[l][4]) + float(lastYearlog[l][5]) + float(lastYearlog[l][9])
                        if float(hrb) > float(num_stat):
                            over += 1
                    l += 1
                    
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.5
                    elif ratio > 0.6:
                        score = score + 0.25
                    elif ratio > 0.5:
                        score = score + 0.1
                    elif ratio < 0.3:
                        score = score - 0.5
                    elif ratio < 0.4:
                        score = score - 0.25
                    elif ratio < 0.5:
                        score = score - 0.12
            
            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    hrb = float(log[l][4]) + float(log[l][5]) + float(log[l][9])
                    if float(hrb) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    hrb = float(log[l][4]) + float(log[l][5]) + float(log[l][9])
                    if float(hrb) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1.5
            if ratio >= 0.8:
                score = score + 1
            elif ratio >= 0.7:
                score = score + 0.5
            elif ratio >= 0.6:
                score = score + 0.25
            elif ratio <= 0.1:
                score = score - 1.5
            elif ratio <= 0.2:
                score = score - 1
            elif ratio <= 0.3:
                score = score - 0.5
            elif ratio <= 0.4:
                score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    hrb = float(log[l][4]) + float(log[l][5]) + float(log[l][9])
                    if float(hrb) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    hrb = float(lastYearlog[l][4]) + float(lastYearlog[l][5]) + float(lastYearlog[l][9])
                    if float(hrb) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
    
    else:
        if stat == 'k':
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][9]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][9]) > float(num_stat):
                            over += 1
                    l += 1
                
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
            
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][9]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][9]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25

            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    if float(log[l][9]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    if float(log[l][9]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1
            if ratio >= 0.8:
                score = score + 0.5
            elif ratio >= 0.7:
                score = score + 0.25
            elif ratio >= 0.6:
                score = score + 0.12
            elif ratio <= 0.1:
                score = score - 1
            elif ratio <= 0.2:
                score = score - 0.5
            elif ratio <= 0.3:
                score = score - 0.25
            elif ratio <= 0.4:
                score = score - 0.12
        
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    if float(log[l][9]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    if float(lastYearlog[l][9]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
        
        elif stat == 'era':
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][6]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][6]) > float(num_stat):
                            over += 1
                    l += 1
                ratio = over / total

                if ratio > 0.7:
                    score = score + 0.75
                elif ratio > 0.6:
                    score = score + 0.5
                elif ratio > 0.5:
                    score = score + 0.25
                elif ratio < 0.3:
                    score = score - 0.75
                elif ratio < 0.4:
                    score = score - 0.5
                elif ratio < 0.5:
                    score = score - 0.25
            
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][6]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][6]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25

            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    if float(log[l][6]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    if float(log[l][6]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1
            if ratio >= 0.8:
                score = score + 0.5
            elif ratio >= 0.7:
                score = score + 0.25
            elif ratio >= 0.6:
                score = score + 0.12
            elif ratio <= 0.1:
                score = score - 1
            elif ratio <= 0.2:
                score = score - 0.5
            elif ratio <= 0.3:
                score = score - 0.25
            elif ratio <= 0.4:
                score = score - 0.12
        
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    if float(log[l][6]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    if float(lastYearlog[l][6]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
        elif stat == "hits":
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
            
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        if float(log[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        if float(lastYearlog[l][4]) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25

            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1
            if ratio >= 0.8:
                score = score + 0.5
            elif ratio >= 0.7:
                score = score + 0.25
            elif ratio >= 0.6:
                score = score + 0.12
            elif ratio <= 0.1:
                score = score - 1
            elif ratio <= 0.2:
                score = score - 0.5
            elif ratio <= 0.3:
                score = score - 0.25
            elif ratio <= 0.4:
                score = score - 0.12
        
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    if float(log[l][4]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    if float(lastYearlog[l][4]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
        
        elif stat == 'outs':
            if home:
                sub = "vs"
                total = 0
                over = 0
                l = 0
                outs = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        temp = int(float(log[l][3]))
                        temp2 = (float(log[l][3]) - float(temp)) * 10
                        outs = (float(temp) * 3) + float(temp2)
                        if float(outs) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        temp = int(float(lastYearlog[l][3]))
                        temp2 = (float(lastYearlog[l][3]) - float(temp)) * 10
                        outs = (float(temp) * 3) + float(temp2)
                        if float(outs) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
            
            if not home:
                sub = "@"
                total = 0
                over = 0
                l = 0
                while l < len(log):
                    if sub in log[l][1]:
                        total += 1
                        temp = int(float(log[l][3]))
                        temp2 = (float(log[l][3]) - float(temp)) * 10
                        outs = (float(temp) * 3) + float(temp2)
                        if float(outs) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 1
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 1
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25
                
                total = 0
                over = 0
                l = 0
                while l < len(lastYearlog):
                    if sub in lastYearlog[l][1]:
                        total += 1
                        temp = int(float(lastYearlog[l][3]))
                        temp2 = (float(lastYearlog[l][3]) - float(temp)) * 10
                        outs = (float(temp) * 3) + float(temp2)
                        if float(outs) > float(num_stat):
                            over += 1
                    l += 1
                if total != 0:
                    ratio = over / total

                    if ratio > 0.7:
                        score = score + 0.75
                    elif ratio > 0.6:
                        score = score + 0.5
                    elif ratio > 0.5:
                        score = score + 0.25
                    elif ratio < 0.3:
                        score = score - 0.75
                    elif ratio < 0.4:
                        score = score - 0.5
                    elif ratio < 0.5:
                        score = score - 0.25

            over = 0
            l = 0
            if len(log) >= 10:
                total = 10
                while l < 10:                               # Last 10 games
                    temp = int(float(log[l][3]))
                    temp2 = (float(log[l][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    if float(outs) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            elif len(log) < 10:
                total = len(log)
                while l < total:
                    temp = int(float(log[l][3]))
                    temp2 = (float(log[l][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    if float(outs) > float(num_stat):
                        over = over + 1
                    l = l + 1
            
            ratio = over / total
            if ratio >= 0.9:
                score = score + 1
            if ratio >= 0.8:
                score = score + 0.5
            elif ratio >= 0.7:
                score = score + 0.25
            elif ratio >= 0.6:
                score = score + 0.12
            elif ratio <= 0.1:
                score = score - 1
            elif ratio <= 0.2:
                score = score - 0.5
            elif ratio <= 0.3:
                score = score - 0.25
            elif ratio <= 0.4:
                score = score - 0.12
        
            over = 0
            l = 0
            total = 0
            while l < len(log):
                if opp_Team in log[l][1]:
                    total = total + 1
                    temp = int(float(log[l][3]))
                    temp2 = (float(log[l][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    if float(outs) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
            
            over = 0
            l = 0
            total = 0
            while l < len(lastYearlog):
                if opp_Team in lastYearlog[l][1]:
                    total = total + 1
                    temp = int(float(lastYearlog[l][3]))
                    temp2 = (float(lastYearlog[l][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    if float(lastYearlog[l][6]) > float(num_stat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio >= 0.9:
                    score = score + 1
                elif ratio >= 0.8:
                    score = score + 0.75
                elif ratio >= 0.7:
                    score = score + 0.5
                elif ratio >= 0.6:
                    score = score + 0.25
                elif ratio <= 0.1:
                    score = score - 1
                elif ratio <= 0.2:
                    score = score - 0.75
                elif ratio <= 0.3:
                    score = score - 0.5
                elif ratio <= 0.4:
                    score = score - 0.25
     
    return score

def getMLBLast10(log, stat):
    last10 = []
    i = 0
    if stat == 'tb':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                tb = float(log[i][5])
                tb = tb + float(log[i][6])
                tb = tb + (float(log[i][7]) * 2)
                tb = tb + (float(log[i][8]) * 3)
                last10.append([temp, int(tb)])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                tb = float(log[i][5])
                tb = tb + float(log[i][6])
                tb = tb + (float(log[i][7]) * 2)
                tb = tb + (float(log[i][8]) * 3)
                last10.append([temp, int(tb)])
                i = i + 1
    elif stat == 'r':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][4])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][4])])
                i = i + 1
    elif stat == 'hrb':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                hrb = float(log[i][4]) + float(log[i][5]) + float(log[i][9])
                last10.append([temp, int(hrb)])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                hrb = float(log[i][4]) + float(log[i][5]) + float(log[i][9])
                last10.append([temp, int(hrb)])
                i = i + 1
    elif stat == 'k':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][9])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][9])])
                i = i + 1
    elif stat == 'era':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][6])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][6])])
                i = i + 1
    elif stat == 'hits':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][4])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][4])])
                i = i + 1
    elif stat == 'outs':
        if len(log) >= 10:
            while i < 10:
                temp3 = log[i][0] + " " + log[i][1]
                temp = int(float(log[i][3]))
                temp2 = (float(log[i][3]) - float(temp)) * 10
                outs = (float(temp) * 3) + float(temp2)
                last10.append([temp3, int(outs)])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp3 = log[i][0] + " " + log[i][1]
                temp = int(float(log[i][3]))
                temp2 = (float(log[i][3]) - float(temp)) * 10
                outs = (float(temp) * 3) + float(temp2)
                last10.append([temp3, int(outs)])
                i = i + 1
    elif stat == 'nrfi':
            if len(log) >= 10:
                while i < 10:
                    last10.append([log[i][0],log[i][1]])
                    i += 1

            else:
                while i < len(log):
                    last10.append([log[i][0],log[i][1]])
                    i += 1
    
    return last10

def getMLBHomeAwayLog(log, stat, home):
    homeAway = []
    i = 0
    if home:
        sub = 'vs'
        if stat == 'tb':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    tb = float(log[i][5])
                    tb = tb + float(log[i][6])
                    tb = tb + (float(log[i][7]) * 2)
                    tb = tb + (float(log[i][8]) * 3)
                    homeAway.append([temp, int(tb)])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][4])])
                i = i + 1
        elif stat == 'hrb':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    hrb = float(log[i][4]) + float(log[i][5]) + float(log[i][9])
                    homeAway.append([temp, int(hrb)])
                i = i + 1
        elif stat == 'k':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][9])])
                i = i + 1
        elif stat == 'era':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][6])])
                i = i + 1
        elif stat == 'hits':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][4])])
                i = i + 1
        elif stat == 'outs':
            while i < len(log):
                if sub in log[i][1]:
                    temp = int(float(log[i][3]))
                    temp2 = (float(log[i][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    temp3 = log[i][0] + " " + log[i][1]
                    homeAway.append([temp3, int(outs)])
                i += 1
        elif stat == 'nrfi':
            while i < len(log):
                if sub in log[i][0]:
                    homeAway.append([log[i][0],log[i][1]])
                i += 1

    else:
        sub = '@'
        if stat == 'tb':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    tb = float(log[i][5])
                    tb = tb + float(log[i][6])
                    tb = tb + (float(log[i][7]) * 2)
                    tb = tb + (float(log[i][8]) * 3)
                    homeAway.append([temp, int(tb)])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][4])])
                i = i + 1
        elif stat == 'hrb':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    hrb = float(log[i][4]) + float(log[i][5]) + float(log[i][9])
                    homeAway.append([temp, int(hrb)])
                i = i + 1
        elif stat == 'k':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][9])])
                i = i + 1
        elif stat == 'era':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][6])])
                i = i + 1
        elif stat == 'hits':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][4])])
                i = i + 1
        elif stat == 'outs':
            while i < len(log):
                if sub in log[i][1]:
                    temp = int(float(log[i][3]))
                    temp2 = (float(log[i][3]) - float(temp)) * 10
                    outs = (float(temp) * 3) + float(temp2)
                    temp3 = log[i][0] + " " + log[i][1]
                    homeAway.append([temp3, int(outs)])
                i += 1
        elif stat == 'nrfi':
            while i < len(log):
                if sub in log[i][0]:
                    homeAway.append([log[i][0],log[i][1]])
                i += 1

    return homeAway

def getMLBvsLog(log, stat, oppTeam):
    vsLog = []
    i = 0
    if stat == 'tb':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                tb = float(log[i][5])
                tb = tb + float(log[i][6])
                tb = tb + (float(log[i][7]) * 2)
                tb = tb + (float(log[i][8]) * 3)
                vsLog.append([temp, int(tb)])
            i = i + 1
    elif stat == 'r':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][4])])
            i = i + 1
    elif stat == 'hrb':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                hrb = float(log[i][4]) + float(log[i][5]) + float(log[i][9])
                vsLog.append([temp, int(hrb)])
            i = i + 1
    elif stat == 'k':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][9])])
            i = i + 1
    elif stat == 'era':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][6])])
            i = i + 1
    elif stat == 'hits':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][4])])
            i = i + 1
    elif stat == 'outs':
        while i < len(log):
            if oppTeam in log[i][1]:
                temp = int(float(log[i][3]))
                temp2 = (float(log[i][3]) - float(temp)) * 10
                outs = (float(temp) * 3) + float(temp2)
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(outs)])
            i += 1
    elif stat == 'nrfi':
        while i < len(log):
            if oppTeam in log[i][0]:
                vsLog.append([log[i][0], log[i][1]])
            i += 1
    
    return vsLog


def getOverUnders():
    data = requests.get("https://sportsbook.draftkings.com/leagues/baseball/mlb")
    games = data.text
    soup = BeautifulSoup(games, 'html5lib')

    overunders = []
    for row in soup.findAll('div', attrs = {'class': "sportsbook-outcome-cell__body"}):
        if '.' in row['aria-label'][2:] and '+' not in row['aria-label'][2:] and '-' not in row['aria-label'][2:]:
            overunders.append(row['aria-label'][2:])
    
    overunders = np.array(overunders)

    return overunders[1::2]


def getGameInfo():
    data = requests.get("https://www.covers.com/sports/mlb/weather")
    weather = data.text
    temperatures = []
    today = datetime.now()
    # Get tomorrow's date
    tomorrow = today + timedelta(days=1)
    # Check if the day is a single digit
    if tomorrow.day < 10:
        # Format tomorrow's date without leading zero for single-digit days
        formatted_date = tomorrow.strftime('%B %-d, %Y')
    else:
        # Format tomorrow's date with leading zero for double-digit days
        formatted_date = tomorrow.strftime('%B %d, %Y')
    weather = weather[:weather.find(formatted_date)]

    soup = BeautifulSoup(weather, 'html5lib')

    for row in soup.findAll('div', attrs={'class': 'covers-coversweatherPage-Temp'}):
        span_tag = row.find('span')
        if span_tag is not None:
            temperatures.append(span_tag.text.strip()[:-3])
    
    print(temperatures)
    wind = []
    for row in soup.findAll('div', attrs={'class': 'covers-coversweatherPage-fieldBrickDetails'}):
        index = row.text.find('.')
        if row.text[index-2].isdigit():
            wind.append(row.text[index-2:index+2])
        elif index == -1:
            index = row.text.find('mph')
            wind.append(row.text[index-3:index-1])
        else:
            wind.append(row.text[index-1:index+2])
    print(wind)

    games = []

    for num, row in enumerate(soup.findAll('div', attrs={'class': 'col-md-12 col-xs-12 covers-CoversWeather-brickHeader'})):
        match = re.search(r'(\w+)\s+([\+\-]?\d+)\s+@\s+(\w+)\s+([\+\-]?\d+)', row.text)
        if match:
            team1 = MLBteamname(match.group(1))
            team2 = MLBteamname(match.group(3))
            if team1 == "Francisco":
                team1 = "San Francisco Giants"
            elif team2 == "Francisco":
                team2 = "San Francisco Giants"
            if team1 == "City":
                team1 = "Kansas City Royals"
            elif team2 == "City":
                team2 = "Kansas City Royals"
            if team1 == "Sox":
                team1 = "Chicago White Sox"
            elif team2 == "Sox":
                team2 = "Chicago White Sox"
            game = team1 + " @ " + team2
        child_tag = row.findAll('span', class_='covers-coversweather-line')
        over_under = child_tag[-1].text
        if '.' in over_under:
            over_under = over_under[over_under.find('U')+2:over_under.find(".")+2]
        elif 'Off' in over_under:
            over_under = "9"
        else:
            matches = list(re.finditer(r'\d+', over_under))
            index = matches[-1].start()
            over_under = over_under[over_under.find('U') + 2:index + 1]
    #    ou_match = re.search(r'O/U:\s*([\d.]+)', over_under)
    #    if ou_match:
    #        over_under = ou_match.group(1)
    #    else:
    #        over_under =""
        
        games.append([game, over_under, temperatures[num], wind[num]])
    
        
    
    return games


def calculateFIP(stats, hbp):
    fipconstant = 0
    game = requests.get("https://www.fangraphs.com/guts.aspx?type=cn")
    chart = game.text
    soup = BeautifulSoup(chart, 'html5lib')

    for num, row in enumerate(soup.findAll('td', attrs={'class': 'grid_line_regular'})):
        if num == 13:
            fipconstant = float(row.text)
            break
    print(stats)
    fip = ((13 * float(stats[12])) + (3 * (float(stats[13]) + float(hbp))) - (2 * float(stats[14]))) /  float(stats[8]) + fipconstant

    return fip


def getPitcherStats(id):
    stats = requests.get(f'https://www.espn.com/mlb/player/splits/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    player = stats.text
    soup = BeautifulSoup(player, 'html5lib')
    start = False
    stats = []
    count = 0
    hbp = 0
    battersfaced = 0

    for row in soup.findAll('td', attrs={'class': 'Table__TD'}):
        if row.text == 'AB':
            start = False
        if not start and len(stats) == 16:
            count += 1
        if start:
            stats.append(row.text)
        if row.text == 'OBA':
            start = True
        if count == 25:
            hbp = row.text
            break
        if count == 17:
            battersfaced = row.text
    print(stats)
    return stats, hbp, battersfaced


def getLineups(link):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


    awaylineup = []
    players = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    teams = players.text
    soup = BeautifulSoup(teams, 'html5lib')

    for row in soup.findAll('a', attrs={'class': 'AnchorLink Boxscore__Athlete_Name truncate db'}):
        awaylineup.append(row.text.replace(".",""))
    

    # Get Home lineup
    check = awaylineup[-1]
    driver.get(link)

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.AnchorLink.Boxscore__Athlete_Name.truncate.db')))
    elements = driver.find_elements(By.CSS_SELECTOR, 'a.AnchorLink.Boxscore__Athlete_Name.truncate.db')

    homelineup = []
    start = False
    for row in elements:
        if start:
            homelineup.append(row.text.replace(".",""))
        if row.text.replace(".", "") == check:
            start = True

    driver.quit()

    return homelineup, awaylineup

def getLastGameLink(id, date):
    games = requests.get(f'https://www.espn.com/mlb/player/gamelog/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    logs = games.text
    logs = logs[logs.find(date):]
    soup = BeautifulSoup(logs, 'html5lib')

    for num, row in enumerate(soup.findAll('a', attrs={'class':'AnchorLink'})):
        if "gameId" in row['href']:
            link = row['href']
            break
        #if num == 2:
         #   link = row['href']
          #  break
    print(link)
    return link

def getMLBTeamStats():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.get("https://www.espn.com/mlb/stats/team/_/season/2024/seasontype/2")
    teams = []

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.pr3.TeamLink__Logo')))
    elements = driver.find_elements(By.CSS_SELECTOR, 'span.pr3.TeamLink__Logo')

    for span in elements:
        img_tag = span.find_element(By.TAG_NAME, 'img')
        teams.append([img_tag.get_attribute('title')])
    
    elements = driver.find_elements(By.CSS_SELECTOR, 'td.Table__TD')
    go = False
    num = 0
    index = 0

    for td in elements:
        try:
            # Find the div inside each td and get its text
            div = td.find_element(By.TAG_NAME, 'div')
            text = div.text.replace(',', '')  # Remove commas if necessary
            if text.isdigit() or go:
                go = True
                num += 1
                teams[index].append(text)
            if num == 16:
                index += 1
                num = 0
        except Exception as e:
            continue
    
    
    driver.quit()
    
    return teams

def getMLBPlayerName(id):
    games = requests.get(f'https://www.espn.com/mlb/player/stats/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    logs = games.text
    soup = BeautifulSoup(logs, 'html5lib')
    
    title = soup.find('title')
    title = title.text
    first_space_index = title.find(" ")

    # Find the index of the second space by searching after the first space
    second_space_index = title.find(" ", first_space_index + 1)

    name = title[:second_space_index]
    return name

def calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID):
    yesterday = date.today() - timedelta(days=1)
    one_year_ago = yesterday - timedelta(days=365)
    one_year_ago = one_year_ago.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")
    print(one_year_ago)
    print(yesterday)
    data = statcast_pitcher(one_year_ago, yesterday, player_id = pitcherpybaseballID)
    data_ff =data[(data['pitch_type'].isin(['FF', 'SI']))]
    avg_velo_ff = np.mean(data_ff['release_speed'])
    filtered_offspeed = data[~data['pitch_type'].isin(['FF', 'SI', 'FC'])]
    
    # Calculate spin rates
    data_ff =data[(data['pitch_type'].isin(['FF', 'SI', 'FC']))]
    spin_ff = np.mean(data_ff['release_spin_rate'])
    spin_off = np.mean(filtered_offspeed['release_spin_rate'])
    pitches = data['pitch_type'].value_counts()
    #  print(pitches)
    fastballs = []
    if 'FF' in pitches:
        fastballs.append("FF")
    if "SI" in pitches:
        fastballs.append("SI")
    if "FC" in pitches:
        fastballs.append("FC")
    percentFastballs = round(len(data[data['pitch_type'].isin(fastballs)]) / np.sum(pitches), 3)
    if np.sum(pitches) == 0 or len(data[data['pitch_type'].isin(fastballs)]) == 0:
        percentFastballs = 0.0
    data = statcast_batter(one_year_ago, yesterday, player_id = hitterpybaseballID)
    filtered_ff = data[(data['pitch_type'].isin(fastballs)) & data['events'].notna() & (data['events'] != 'walk') & (data['events'] != 'hit_by_pitch') & (data['events'] != 'caught_stealing_2b')]

    if avg_velo_ff >= 95.0:
        hittervspitcherFF = data[data['events'].notna() & (data['release_speed'] >= 95) & (data['events'] != 'walk') & (data['events'] != 'hit_by_pitch') & (data['events'] != 'caught_stealing_2b')]
        events_hitter_pitcherFF = hittervspitcherFF['events'].value_counts()
        valueSTR = "Average vs 95+ Fastballs: "
    else:
        hittervspitcherFF = data[data['events'].notna() & (data['release_speed'] < 95) & (data['events'] != 'walk') & (data['events'] != 'hit_by_pitch') & (data['events'] != 'caught_stealing_2b')]
        events_hitter_pitcherFF = hittervspitcherFF['events'].value_counts()
        valueSTR = "Average vs Fastballs < 95: "
    filtered_offspeed = data[~data['pitch_type'].isin(['FF', 'SI', 'FC']) & data['events'].notna() & (data['events'] != 'walk') & (data['events'] != 'hit_by_pitch') & (data['events'] != 'caught_stealing_2b')]
    tot_offspeed = len(filtered_offspeed)
    events_hitter_off = filtered_offspeed['events'].value_counts()

    tot_hitter = len(filtered_ff)
    events_hitter = filtered_ff['events'].value_counts()
    events_to_sum = []
    events_to_sum_off = []
    events_to_sum_off_FF = []
    if 'home_run' in events_hitter:
        events_to_sum.append('home_run')
    if 'single' in events_hitter:
        events_to_sum.append('single')
    if 'double' in events_hitter:
        events_to_sum.append('double')
    if 'triple' in events_hitter:
        events_to_sum.append('triple')
    
    if 'home_run' in events_hitter_off:
        events_to_sum_off.append('home_run')
    if 'single' in events_hitter_off:
        events_to_sum_off.append('single')
    if 'double' in events_hitter_off:
        events_to_sum_off.append('double')
    if 'triple' in events_hitter_off:
        events_to_sum_off.append('triple')
    
    if 'home_run' in events_hitter_pitcherFF:
        events_to_sum_off_FF.append('home_run')
    if 'single' in events_hitter_pitcherFF:
        events_to_sum_off_FF.append('single')
    if 'double' in events_hitter_pitcherFF:
        events_to_sum_off_FF.append('double')
    if 'triple' in events_hitter_pitcherFF:
        events_to_sum_off_FF.append('triple')
    
    hits = events_hitter[events_to_sum].sum()
    avg_vs_FF = round(hits/tot_hitter, 3)
    if hits == 0:
        avg_vs_FF = 0.0
    hits = events_hitter_off[events_to_sum_off].sum()
    avg_vs_off = round(hits/tot_offspeed, 3)
    if hits == 0:
        avg_vs_off = 0.0
    hits = events_hitter_pitcherFF[events_to_sum_off_FF].sum()
    avg_vs_pitchFF = round(hits / len(hittervspitcherFF),3)
    if hits == 0:
        avg_vs_pitchFF = 0.0
    
    
    # Averages vs spin rates
   
    filtered_ff = filtered_ff[(filtered_ff['release_spin_rate'] >= spin_ff - 100) & (filtered_ff['release_spin_rate'] <= spin_ff + 100)]
    tot = len(filtered_ff)
    events_hitter = filtered_ff['events'].value_counts()
    events_to_sum = []
    if 'home_run' in events_hitter:
        events_to_sum.append('home_run')
    if 'single' in events_hitter:
        events_to_sum.append('single')
    if 'double' in events_hitter:
        events_to_sum.append('double')
    if 'triple' in events_hitter:
        events_to_sum.append('triple')
    hits = events_hitter[events_to_sum].sum()
    if tot == 0 or hits == 0:
        avg_spin_FF = 0.0
    else:
        avg_spin_FF = round(hits/tot, 3)
    print(avg_spin_FF)

    # Get average vs off speed spin rate
    filtered_ff = filtered_offspeed[(filtered_offspeed['release_spin_rate'] >= spin_off - 100) & (filtered_offspeed['release_spin_rate'] <= spin_off + 100)]
    tot = len(filtered_ff)
    events_hitter = filtered_ff['events'].value_counts()
    events_to_sum = []
    if 'home_run' in events_hitter:
        events_to_sum.append('home_run')
    if 'single' in events_hitter:
        events_to_sum.append('single')
    if 'double' in events_hitter:
        events_to_sum.append('double')
    if 'triple' in events_hitter:
        events_to_sum.append('triple')
    hits = events_hitter[events_to_sum].sum()
    print(hits)
    print(tot)
    if tot == 0 or hits == 0:
        avg_spin_off = 0.0
    else: 
        avg_spin_off = round(hits/tot, 3)
    print(avg_spin_off)

    return valueSTR, avg_vs_FF, avg_vs_off, avg_vs_pitchFF, percentFastballs, avg_spin_FF, avg_spin_off

def mapTeamInt(team):
    return team_mapping.get(team)