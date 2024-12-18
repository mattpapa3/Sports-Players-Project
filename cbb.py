#!/bin/env python
import json
from bs4 import BeautifulSoup
import requests
import random
import re

def getID(firstname, lastname):
    #firstname = firstname.lower()
 #   lastname = lastname.lower()
    
    if firstname[len(firstname) - 1] == " ":
        firstname = firstname[:-1]
    
    if lastname[len(lastname) - 1] == " ":
        lastname = lastname[:-1]
    
    player_found = True
  #  firstname = firstname.lower()
#    lastname = lastname.lower()
   # fullname = "/" + firstname + "-" + lastname
   # player_API = requests.get(f"http://www.espn.com/mens-college-basketball/players/_/search/{lastname}")
    player_API = requests.get(f"http://m.espn.com/ncb/playersearch?search={lastname}&wjb", headers={"User-Agent": "Mozilla/5.0"})
    player = player_API.text
    print(firstname.capitalize())
    nameIndex = player.find(firstname.capitalize())
    tempplayer = player[nameIndex - 40:]
    index = tempplayer.find("playerId=")
    id = tempplayer[index + 9:tempplayer.find('&')]
  #  player_soup = BeautifulSoup(player, 'html5lib')
   # temp = 'No players'
   # for row in player_soup.findAll('tr', attrs = {'class':'oddrow'}):
    #    if temp in row.text:
     #       player_found = False
    
    #if player_found == True:
     #   player = player[:player.find(fullname)]
      #  if len(player) > 70000:
       #     id = -1
        #else:
         #   index = player.rfind('/')               # index of last occurence of "/"
          #  id = player[index + 1:]         
    #else:
        #id = -1                                                  # Right after last occurence of "/" is players id
    print(id)
    return id

def getGameLines():
    lines_api = requests.get("https://www.espn.com/mens-college-basketball/scoreboard/_/date/20230219/group/50", headers={"User-Agent": "Mozilla/5.0"})     #Find lines of games today 
    lines = lines_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')
    spreads = []
    for row in lines_soup.findAll('div', attrs = {'class':'Odds__Message'}):
        temprow = row.text[:row.text.find('O/U')]
        temprow = temprow[temprow.find(': '):]
        temprow = temprow[2:]
        spreads.append(temprow)
    
    return spreads

def getCBBGameLog(id):
    log_api = requests.get(f'https://www.espn.com/mens-college-basketball/player/gamelog/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    lines = log_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')
    log = []
    stats_log = []
    broken = False
    postseason = False

    for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
        if row.text == '-':
            broken = True
            break
        if '/' in row.text and postseason:
            postseason = False
        if row.text == "Total":
            break
        if "season" in row.text:
            postseason = True
        if contains_number(row.text) and 'Big 12' not in row.text and not postseason and 'Pac-12' not in row.text and 'Atlanti' not in row.text and '1st' not in row.text and '2k22' not in row.text and '2nd' not in row.text and 'Field' not in row.text and 'MAKEUP' not in row.text and 'Basketball' not in row.text or 'vs' in row.text or '@' in row.text:
            stats_log.append(row.text)
    
    check = len(stats_log)
    n = 0
    i = 0

    while n < check:
        log.append(stats_log[n:n+17])
        n = n + 17
        i = i + 1
    if broken:
        log.pop()
    return log


def getTop25():
    top25 = []
    top25_api = requests.get('https://www.espn.com/mens-college-basketball/rankings', headers={"User-Agent": "Mozilla/5.0"})
    top25_txt = top25_api.text
    top25_soup = BeautifulSoup(top25_txt, 'html5lib')

    for row in top25_soup.findAll('div', attrs = {'class':'flex justify-start'}):
        for i in range(len(row.text)):
            if row.text[i].islower():
                temp = i
                break

        team = row.text[:temp - 1]
        top25.append(team)
    return top25

    
def getCBBOppTeamName(id, home):
    nba_API = requests.get(f'https://www.espn.com/mens-college-basketball/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    o = 0
    team = ""
    for row in soup2.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):     #Find what team player is on
        if home and o == 0:
            team = row.text
        elif not home and o == 1:
            team = row.text
        o = o + 1

    if 'State' in team:
        team = team[:-3]
    
    return team


def getCBBOppTeam(id, home):
    nba_API = requests.get(f'https://www.espn.com/mens-college-basketball/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    o = 0
    opp_team = ""
    for row in soup2.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):     #Find what team player is on
        if home and o == 1:
            team = row.text
        elif home and o == 0:
            opp_team = row.text
        elif not home and o == 0:
            team = row.text
        elif not home and o == 1:
            opp_team = row.text
        o = o + 1
    
    data = recent_data[:recent_data.find(opp_team)]
    team_id = data[data.rfind('=') + 1:len(data) - 1]
    data = recent_data[recent_data.rfind(team_id):]
    new_data = data[data.find('abbrev'):]
    opp_team = new_data[9:new_data.find(',') - 1]

    return opp_team


def getOppTeamRank(id, stat, home):
    nba_API = requests.get(f'https://www.espn.com/mens-college-basketball/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    o = 0
    team = ""
    for row in soup2.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):     #Find what team player is on
        if home and o == 0:
            team = row.text
        elif not home and o == 1:
            team = row.text
        o = o + 1

    if 'State' in team:
        team = team[:-3]
    
    rank = 1
    
    if stat == '3':
        ranks_api = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/opponent-points-from-3-pointers')
        recent_data = ranks_api.text
        soup2 = BeautifulSoup(recent_data, 'html5lib')
        for row in soup2.findAll('td', attrs = {'class':'text-left nowrap'}):
            if row.text == team:
                break
            rank = rank + 1
    
    elif stat == 'p':
        ranks_api = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/opponent-points-per-game')
        recent_data = ranks_api.text
        soup2 = BeautifulSoup(recent_data, 'html5lib')
        for row in soup2.findAll('td', attrs = {'class':'text-left nowrap'}):
            if row.text == team:
                break
            rank = rank + 1
    
    elif stat == 'r':
        ranks_api = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/opponent-total-rebounds-per-game')
        recent_data = ranks_api.text
        soup2 = BeautifulSoup(recent_data, 'html5lib')
        for row in soup2.findAll('td', attrs = {'class':'text-left nowrap'}):
            if row.text == team:
                break
            rank = rank + 1
    
    elif stat == 'a':
        ranks_api = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/opponent-assists-per-game')
        recent_data = ranks_api.text
        soup2 = BeautifulSoup(recent_data, 'html5lib')
        for row in soup2.findAll('td', attrs = {'class':'text-left nowrap'}):
            if row.text == team:
                break
            rank = rank + 1

    return rank


def CBBhomeoraway(id):
    player_API = requests.get(f'https://www.espn.com/mens-college-basketball/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    player = player_API.text
    soup = BeautifulSoup(player, 'html5lib')
    home = True
    team = ""
    for row in soup.findAll('div', attrs = {'class':'PlayerHeader__Team n8 mt3 mb4 flex items-center mt3 mb4 clr-gray-01'}):
        team = row.text
        break
    
    team = team[:team.find('#')]
    team_ab = team.split()
    l = len(team_ab)
    i = 0

    for row in soup.findAll('div', attrs = {'class': 'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):
        if team_ab[0] in row.text and i == 0:
            home = False
        if team_ab[0] in row.text and i == 1:
            home = True
        i = i + 1
    return home


def contains_number(string):
    """
    Check if a number is present in the given string.
    Returns True if a number is present, False otherwise.
    """
    for char in string:
        if char.isdigit():
            return True
    return False


def oppTeamTop25(oppTeam):
    top25Teams = getTop25()
    top25 = False
    if oppTeam in top25Teams:
        top25 = True
    
    return top25

def getCBBScore(cat, num_cat, log, home, opp_team, top25):
    lines = getGameLines()
    win = True
    if opp_team in lines:
        win = False

    if cat == 'p':
        score = 0
        l = 0
        total = 0
        over = 0
        

        if win:
            l = 0
            over = 0
            total = 0
            sub = 'W'
            while l < len(log):
                if sub in log[l][2]:
                    total = total + 1
                    if float(log[l][16]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            if total != 0:
                ratio = over / total

                if ratio > 0.8:
                    score = score + 1
                elif ratio > 0.7:
                    score = score + 0.5
                elif ratio > 0.6:
                    score = score + 0.25
                elif ratio < 0.2:
                    score = score - 1
                elif ratio < 0.3:
                    score = score - 0.5
                elif ratio < 0.4:
                    score = score - 0.25
        
        if not win:
            l = 0
            over = 0
            total = 0
            sub = 'L'
            while l < len(log):
                if sub in log[l][1]:
                    total = total + 1
                    if float(log[l][16]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if top25:
            while l < len(log):
                if contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][16]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        if not top25:
            while l < len(log):
                if not contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][16]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            if total > 0:
                ratio = over / total
            else:
                ratio = 0

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.25:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
    
        over = 0
        l = 0
        if len(log) >= 10:
            total = 10
            while l < 10:                               # Last 10 games
                if float(log[l][16]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        elif len(log) < 10:
            total = len(log)
            while l < total:
                if float(log[l][16]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        ratio = over / total
        if ratio >= 0.9:
            score = score + 2
        if ratio >= 0.8:
            score = score + 1.5
        elif ratio >= 0.7:
            score = score + 0.75
        elif ratio >= 0.6:
            score = score + 0.3
        elif ratio <= 0.1:
            score = score - 2
        elif ratio <= 0.2:
            score = score - 1.5
        elif ratio <= 0.3:
            score = score - 0.75
        elif ratio <= 0.4:
            score = score - 0.4
    
        over = 0
        l = 0
        total = 0
        while l < len(log):
            if opp_team in log[l][1]:
                total = total + 1
                if float(log[l][16]) > float(num_cat):
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
    
    if cat == 'a':
        score = 0
        l = 0
        total = 0
        over = 0

    
        
        if win:
            l = 0
            over = 0
            total = 0
            sub = 'W'
            while l < len(log):
                if sub in log[l][2]:
                    total = total + 1
                    if float(log[l][11]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if not win:
            l = 0
            over = 0
            total = 0
            sub = 'L'
            while l < len(log):
                if sub in log[l][2]:
                    total = total + 1
                    if float(log[l][11]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if top25:
            while l < len(log):
                if contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][11]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        if not top25:
            while l < len(log):
                if not contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][11]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.25:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        over = 0
        l = 0
        if len(log) >= 10:
            total = 10
            while l < 10:                               # Last 10 games
                if float(log[l][11]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        else:
            total = len(log)
            while l < total:                               # Last games if they haven't played 10
                if float(log[l][11]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        ratio = over / total
        if ratio >= 0.9:
            score = score + 2
        if ratio >= 0.8:
            score = score + 1.5
        elif ratio >= 0.7:
            score = score + 0.75
        elif ratio >= 0.6:
            score = score + 0.3
        elif ratio <= 0.1:
            score = score - 2
        elif ratio <= 0.2:
            score = score - 1.5
        elif ratio <= 0.3:
            score = score - 0.75
        elif ratio <= 0.4:
            score = score - 0.3
        
        over = 0
        l = 0
        total = 0
        while l < len(log):
            if opp_team in log[l][1]:
                total = total + 1
                if float(log[l][11]) > float(num_cat):
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
    
    if cat == 'r':
        category_name = "rebounds"
        score = 0
        l = 0
        total = 0
        over = 0
        
        
        if win:
            l = 0
            over = 0
            total = 0
            sub = 'W'
            while l < len(log):
                if sub in log[l][2]:
                    total = total + 1
                    if float(log[l][10]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        #print(log)
        if not win:
            l = 0
            over = 0
            total = 0
            sub = 'L'
            while l < len(log):
                if sub in log[l][2]:
                    total = total + 1
                    if float(log[l][10]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if top25:
            while l < len(log):
                if contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][10]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        if not top25:
            while l < len(log):
                if not contains_number(log[l][1]):
                    total = total + 1
                    if float(log[l][10]) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.25:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        over = 0
        l = 0
        if len(log) >= 10:
            total = 10
            while l < 10:                               # Last 10 games
                if float(log[l][10]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        else:
            total = len(log)
            while l < total:
                if float(log[l][10]) > float(num_cat):
                    over = over + 1
                l = l + 1
        
        ratio = over / total
        if ratio >= 0.9:
            score = score + 2
        if ratio >= 0.8:
            score = score + 1.5
        elif ratio >= 0.7:
            score = score + 0.75
        elif ratio >= 0.6:
            score = score + 0.3
        elif ratio >= 0.1:
            score = score - 2
        elif ratio <= 0.2:
            score = score - 1.5
        elif ratio <= 0.3:
            score = score - 0.75
        elif ratio <= 0.4:
            score = score - 0.3
        
        over = 0
        l = 0
        total = 0
        while l < len(log):
            if opp_team in log[l][1]:
                total = total + 1
                if float(log[l][10]) > float(num_cat):
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
    
    if cat == '3':
        category_name = "three-pointer"
        score = 0
        l = 0
        total = 0
        over = 0
     
        
        if win:
            l = 0
            over = 0
            total = 0
            sub = 'W'
            while l < len(log):
                if sub in log[l][2]:
                    threepoint = log[l][6]
                    threepoint = threepoint[:threepoint.find("-")]
                    total = total + 1
                    if float(threepoint) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if not win:
            l = 0
            over = 0
            total = 0
            sub = 'L'
            while l < len(log):
                if sub in log[l][2]:
                    threepoint = log[l][6]
                    threepoint = threepoint[:threepoint.find("-")]
                    total = total + 1
                    if float(threepoint) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1
            elif ratio > 0.7:
                score = score + 0.5
            elif ratio > 0.6:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1
            elif ratio < 0.3:
                score = score - 0.5
            elif ratio < 0.4:
                score = score - 0.25
        
        if top25:
            while l < len(log):
                if contains_number(log[l][1]):
                    threepoint = log[l][6]
                    threepoint = threepoint[:threepoint.find("-")]
                    total = total + 1
                    if float(threepoint) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.2:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        if not top25:
            while l < len(log):
                if not contains_number(log[l][1]):
                    threepoint = log[l][6]
                    threepoint = threepoint[:threepoint.find("-")]
                    total = total + 1
                    if float(threepoint) > float(num_cat):
                        over = over + 1
                l = l + 1
            
            ratio = over / total

            if ratio > 0.8:
                score = score + 1.5
            elif ratio > 0.7:
                score = score + 1
            elif ratio > 0.6:
                score = score + 0.5
            elif ratio > 0.5:
                score = score + 0.25
            elif ratio < 0.25:
                score = score - 1.5
            elif ratio < 0.3:
                score = score - 1
            elif ratio < 0.4:
                score = score - 0.5
            elif ratio < 0.5:
                score = score - 0.25
        
        total = 10
        over = 0
        l = 0
        while l < 10:                               # Last 10 games
            threepoint = log[l][6]
            threepoint = threepoint[:threepoint.find("-")]
            if float(threepoint) > float(num_cat):
                over = over + 1
            l = l + 1
        
        ratio = over / total
        if ratio >= 0.9:
            score = score + 2
        if ratio >= 0.8:
            score = score + 1.5
        elif ratio >= 0.7:
            score = score + 0.75
        elif ratio >= 0.6:
            score = score + 0.3
        elif ratio <= 0.1:
            score = score - 2
        elif ratio <= 0.2:
            score = score - 1.5
        elif ratio <= 0.3:
            score = score - 0.75
        elif ratio <= 0.4:
            score = score - 0.3
        
        over = 0
        l = 0
        total = 0
        while l < len(log):
            if opp_team in log[l][1]:
                threepoint = log[l][6]
                threepoint = threepoint[:threepoint.find("-")]
                total = total + 1
                if float(threepoint) > float(num_cat):
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
    
    score = str(round(score, 2))
    return score
        


def CBBgetVSLog(log, stat, opp_team):
    vsLog = []
    i = 0
    if len(opp_team) > 1:
        if stat == 'p':
            while i < len(log):
                if opp_team in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if opp_team in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if opp_team in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if opp_team in log[i][1]:
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
                i = i + 1
    
    return vsLog


def getTop25Log(log, stat, top25):
    print(log)
    vsLog = []
    i = 0
    if(top25):
        if stat == 'p':
            while i < len(log):
                if contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if contains_number(log[i][1]):
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
                i = i + 1
    
    else:
        if stat == 'p':
            while i < len(log):
                if not contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if not contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if not contains_number(log[i][1]):
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if not contains_number(log[i][1]):
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
                i = i + 1
    
    return vsLog


def getWinLossLog(log, win, stat):
    vsLog = []
    i = 0
    if win == 'W':
        if stat == 'pra':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                    vsLog.append([temp, int(pra)])
                i = i + 1
        elif stat == 'p':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if win in log[i][2]:
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
                i = i + 1
        elif stat == 't':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][15])])
                i = i + 1
    
    else:
        if stat == 'pra':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                    vsLog.append([temp, int(pra)])
                i = i + 1
        elif stat == 'p':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if win in log[i][2]:
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
                i = i + 1
        elif stat == 't':
            while i < len(log):
                if win in log[i][2]:
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][15])])
                i = i + 1
    
    return vsLog


