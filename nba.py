import json
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime, date
import copy

def oppteamname(teamname):
    if teamname == "Celtics":
        teamname = "Boston Celtics"
    elif teamname == "Nets":
        teamname = "Brooklyn Nets"
    elif teamname == "Knicks":
        teamname = "New York Knicks"
    elif teamname == "76ers":
        teamname = "Philadelphia 76ers"
    elif teamname == "Raptors":
        teamname = "Toronto Raptors"
    elif teamname == "Warriors":
        teamname = "Golden State Warriors"
    elif teamname == "Clippers":
        teamname = "LA Clippers"
    elif teamname == "Lakers":
        teamname = "Los Angeles Lakers"
    elif teamname == "Suns":
        teamname = "Phoenix Suns"
    elif teamname == "Kings":
        teamname = "Sacramento Kings"
    elif teamname == "Bulls":
        teamname = "Chicago Bulls"
    elif teamname == "Cavaliers":
        teamname = "Cleveland Cavaliers"
    elif teamname == "Pistons":
        teamname = "Detroit Pistons"
    elif teamname == "Pacers":
        teamname = "Indiana Pacers"
    elif teamname == "Bucks":
        teamname = "Milwaukee Bucks"
    elif teamname == "Hawks":
        teamname = "Atlanta Hawks"
    elif teamname == "Hornets":
        teamname = "Charlotte Hornets"
    elif teamname == "Heat":
        teamname = "Miami Heat"
    elif teamname == "Magic":
        teamname = "Orlando Magic"
    elif teamname == "Wizards":
        teamname = "Washington Wizards"
    elif teamname == "Nuggets":
        teamname = "Denver Nuggets"
    elif teamname == "Timberwolves":
        teamname = "Minnesota Timberwolves"
    elif teamname == "Thunder":
        teamname = "Oklahoma City Thunder"
    elif teamname == "Trail Blazers":
        teamname = "Portland Trail Blazers"
    elif teamname == "Jazz":
        teamname = "Utah Jazz"
    elif teamname == "Mavericks":
        teamname = "Dallas Mavericks"
    elif teamname == "Rockets":
        teamname = "Houston Rockets"
    elif teamname == "Grizzlies":
        teamname = "Memphis Grizzlies"
    elif teamname == "Pelicans":
        teamname = "New Orleans Pelicans"
    elif teamname == "Spurs":
        teamname = "San Antonio Spurs"
    return teamname

def oppteamname2(teamname):
    if teamname == "Boston Celtics":
        return "Celtics"
    elif teamname == "Brooklyn Nets":
        return "Nets"
    elif teamname == "New York Knicks":
        return "Knicks"
    elif teamname == "Philadelphia 76ers":
        return "76ers"
    elif teamname == "Toronto Raptors":
        return "Raptors"
    elif teamname == "Golden State Warriors":
        return "Warriors"
    elif teamname == "LA Clippers":
        return "Clippers"
    elif teamname == "Los Angeles Lakers":
        return "Lakers"
    elif teamname == "Phoenix Suns":
        return "Suns"
    elif teamname == "Sacramento Kings":
        return "Kings"
    elif teamname == "Chicago Bulls":
        return "Bulls"
    elif teamname == "Cleveland Cavaliers":
        return "Cavaliers"
    elif teamname == "Detroit Pistons":
        return "Pistons"
    elif teamname == "Indiana Pacers":
        return "Pacers"
    elif teamname == "Milwaukee Bucks":
        return "Bucks"
    elif teamname == "Atlanta Hawks":
        return "Hawks"
    elif teamname == "Charlotte Hornets":
        return "Hornets"
    elif teamname == "Miami Heat":
        return "Heat"
    elif teamname == "Orlando Magic":
        return "Magic"
    elif teamname == "Washington Wizards":
        return "Wizards"
    elif teamname == "Denver Nuggets":
        return "Nuggets"
    elif teamname == "Minnesota Timberwolves":
        return "Timberwolves"
    elif teamname == "Oklahoma City Thunder":
        return "Thunder"
    elif teamname == "Portland Trail Blazers":
        return "Trail Blazers"
    elif teamname == "Utah Jazz":
        return "Jazz"
    elif teamname == "Dallas Mavericks":
        return "Mavericks"
    elif teamname == "Houston Rockets":
        return "Rockets"
    elif teamname == "Memphis Grizzlies":
        return "Grizzlies"
    elif teamname == "New Orleans Pelicans":
        return "Pelicans"
    elif teamname == "San Antonio Spurs":
        return "Spurs"
    return teamname


def teamname(teamname):
    if teamname == "Celtics":
        teamname = "BOS"
    elif teamname == "Nets":
        teamname = "BKN"
    elif teamname == "Knicks":
        teamname = "NY"
    elif teamname == "76ers":
        teamname = "PHI"
    elif teamname == "Raptors":
        teamname = "TOR"
    elif teamname == "Warriors":
        teamname = "GS"
    elif teamname == "Clippers":
        teamname = "LAC"
    elif teamname == "Lakers":
        teamname = "LAL"
    elif teamname == "Suns":
        teamname = "PHX"
    elif teamname == "Kings":
        teamname = "SAC"
    elif teamname == "Bulls":
        teamname = "CHI"
    elif teamname == "Cavaliers":
        teamname = "CLE"
    elif teamname == "Pistons":
        teamname = "DET"
    elif teamname == "Pacers":
        teamname = "IND"
    elif teamname == "Bucks":
        teamname = "MIL"
    elif teamname == "Hawks":
        teamname = "ATL"
    elif teamname == "Hornets":
        teamname = "CHA"
    elif teamname == "Heat":
        teamname = "MIA"
    elif teamname == "Magic":
        teamname = "ORL"
    elif teamname == "Wizards":
        teamname = "WSH"
    elif teamname == "Nuggets":
        teamname = "DEN"
    elif teamname == "Timberwolves":
        teamname = "MIN"
    elif teamname == "Thunder":
        teamname = "OKC"
    elif teamname == "Trail Blazers":
        teamname = "POR"
    elif teamname == "Jazz":
        teamname = "UTA"
    elif teamname == "Mavericks":
        teamname = "DAL"
    elif teamname == "Rockets":
        teamname = "HOU"
    elif teamname == "Grizzlies":
        teamname = "MEM"
    elif teamname == "Pelicans":
        teamname = "NO"
    elif teamname == "Spurs":
        teamname = "SA"
    return teamname


def teamnameFull(teamname):
    if teamname == "BOS":
        teamname = "Boston"
    elif teamname == "BKN":
        teamname = "Brooklyn"
    elif teamname == "NY":
        teamname = "New York"
    elif teamname == "PHI":
        teamname = "Philadelphia"
    elif teamname == "TOR":
        teamname = "Toronto"
    elif teamname == "GS":
        teamname = "Golden State"
    elif teamname == "LAC":
        teamname = "LA Clippers"
    elif teamname == "LAL":
        teamname = "LA Lakers"
    elif teamname == "PHX":
        teamname = "Phoenix"
    elif teamname == "SAC":
        teamname = "Sacramento"
    elif teamname == "CHI":
        teamname = "Chicago"
    elif teamname == "CLE":
        teamname = "Cleveland"
    elif teamname == "DET":
        teamname = "Detroit"
    elif teamname == "IND":
        teamname = "Indiana"
    elif teamname == "MIL":
        teamname = "Milwaukee"
    elif teamname == "ATL":
        teamname = "Atlanta"
    elif teamname == "CHA":
        teamname = "Charlotte"
    elif teamname == "MIA":
        teamname = "Miami"
    elif teamname == "ORL":
        teamname = "Orlando"
    elif teamname == "WSH":
        teamname = "Washington"
    elif teamname == "DEN":
        teamname = "Denver"
    elif teamname == "MIN":
        teamname = "Minnesota"
    elif teamname == "OKC":
        teamname = "Okla City"
    elif teamname == "POR":
        teamname = "Portland"
    elif teamname == "UTA" or teamname == "UTAH":
        teamname = "Utah"
    elif teamname == "DAL":
        teamname = "Dallas"
    elif teamname == "HOU":
        teamname = "Houston"
    elif teamname == "MEM":
        teamname = "Memphis"
    elif teamname == "NO":
        teamname = "New Orleans"
    elif teamname == "SA":
        teamname = "San Antonio"
    return teamname

def teamnamemap(teamname):
    if teamname == "Boston":
        teamname = 1
    elif teamname == "Brooklyn":
        teamname = 2
    elif teamname == "New York":
        teamname = 3
    elif teamname == "Philadelphia":
        teamname = 4
    elif teamname == "Toronto":
        teamname = 5
    elif teamname == "Golden State":
        teamname = 6
    elif teamname == "LA Clippers":
        teamname = 7
    elif teamname == "LA Lakers":
        teamname = 8
    elif teamname == "Phoenix":
        teamname = 9
    elif teamname == "Sacramento":
        teamname = 10
    elif teamname == "Chicago":
        teamname = 11
    elif teamname == "Cleveland":
        teamname = 12
    elif teamname == "Detroit":
        teamname = 13
    elif teamname == "Indiana":
        teamname = 14
    elif teamname == "Milwaukee":
        teamname = 15
    elif teamname == "Atlanta":
        teamname = 16
    elif teamname == "Charlotte":
        teamname = 17
    elif teamname == "Miami":
        teamname = 18
    elif teamname == "Orlando":
        teamname = 19
    elif teamname == "Washington":
        teamname = 20
    elif teamname == "Denver":
        teamname = 21
    elif teamname == "Minnesota":
        teamname = 22
    elif teamname == "Okla City":
        teamname = 23
    elif teamname == "Portland":
        teamname = 24
    elif teamname == "Utah" or teamname == "UTAH":
        teamname = 25
    elif teamname == "Dallas":
        teamname = 26
    elif teamname == "Houston":
        teamname = 27
    elif teamname == "Memphis":
        teamname = 28
    elif teamname == "New Orleans":
        teamname = 29
    elif teamname == "San Antonio":
        teamname = 30
    return teamname

def getPlayerID(firstname, lastname):
    firstname = firstname.lower()
    lastname = lastname.lower()
    if firstname[len(firstname) - 1] == " ":
        firstname = firstname[:-1]
    
    if lastname[len(lastname) - 1] == " ":
        lastname = lastname[:-1]
    player_found = True
    fullname = "/" + firstname + "-" + lastname
    player_API = requests.get(f'http://www.espn.com/nba/players/_/search/{lastname}', headers={"User-Agent": "Mozilla/5.0"})
    player = player_API.text
    player_soup = BeautifulSoup(player, 'html5lib')
    temp = 'No players'
    for row in player_soup.findAll('tr', attrs = {'class':'oddrow'}):
        if temp in row.text:
            player_found = False

    if player_found == True:
        #tag = player_soup.find('meta', attrs = {'property':'og:url'})
        #print(tag)
        player = player[:player.find(fullname)]
        index = player.rfind('/')               # index of last occurence of "/"
        id = player[index + 1:]                                                   # Right after last occurence of "/" is players id

    else:
        id = -1

    return id


def getGameLog(id, lastYear):
    if not lastYear:
        log_api = requests.get(f'https://www.espn.com/nba/player/gamelog/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    else:
        log_api = requests.get(f'https://www.espn.com/nba/player/gamelog/_/id/{id}/type/nba/year/2024', headers={"User-Agent": "Mozilla/5.0"})
    lines = log_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')
    log = []
    stats_log = []

    stop = False
    stop2 = False
    i = 0
    m = -1
    n = 0

    for row in lines_soup.findAll('td', attrs = {'class':'Table__TD'}):
        m = m + 1
        if row.text == 'december' or row.text == 'november' or row.text == 'october' or row.text == 'january' or row.text == 'february' or row.text == 'march' or row.text == "april" or "Conference" in row.text or "Totals" in row.text or "Finals" in row.text and "Game" not in row.text:
            stop = True
        
     #   if '2/19' in row.text:
      #      stop2 = True
        if not stop and not stop2 and row.text != 'NBA Mexico City Game 2022' and row.text != 'Averages' and row.text != 'NBA Paris Game 2023' and "Previously" not in row.text and 'All-Star' not in row.text and 'Round' not in row.text and 'Game' not in row.text and 'In-Season' not in row.text and 'Makeup' not in row.text and 'Play-In' not in row.text \
            and "Cup" not in row.text:
            stats_log.append(row.text)
        if stop or stop2:
            i = i + 1
        if i == 17 and stop2:
            stop2 = False
            i = 0
            m = -1
        if i == 15 and stop:
            stop = False
            i = 0
            m = -1
        if row.text == 'october' or row.text == 'Averages' or 'Preseason' in row.text:
            break
        if m == 16:
            m = -1
        

    stop = False
    n  = 0
    i = 0

    check = len(stats_log)
    while n < check:
        log.append(stats_log[n:n+17])
        log[i][0] = log[i][0][4:]
        n = n + 17
        i = i + 1
    
    if len(log) > 0:
        while '/' not in log[len(log) - 1][0]:
            log.pop()
            if len(log) == 0:
                break
    return log


def getTeamStats():
    team_api = requests.get("https://www.espn.com/nba/stats/team/_/view/opponent/season", headers={"User-Agent": "Mozilla/5.0"})
    team = team_api.text
    team = team[team.find("</thead>"):]
    real_team = team[:team.find("<li>Statistics are updated nightly</li>")]
    team_soup = BeautifulSoup(real_team, 'html5lib')
    teams = []
    team_stats = []
    i = 0
    num = 1

    for row in team_soup.findAll('a', attrs = {'class':'AnchorLink'}):
        if i == 30:
            break
        if num % 2 == 0:
            teams.append(row.text)
            i = i + 1
        num = num + 1

    updated_team = real_team[real_team.find("PF</a></span>"):]
    team_soup2 = BeautifulSoup(updated_team, 'html5lib')
    i = 0
    n = 0
    for row in team_soup2.findAll('div', attrs = {'class':''}):
        if i == 0:
            team_stats.append([teams[n], row.text])
        else:
            team_stats[n].append(row.text)
        
        i = i + 1
        if i == 19:
            i = 0
            n = n + 1
    
    return team_stats


def getPosition(id):
    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    position = ''
    soup2 = BeautifulSoup(recent_data, 'html5lib')

    i = 0
    for row in soup2.findAll('li', attrs = {'class':''}):
        if 'Guard' in row.text or 'Forward' in row.text or 'Center' in row.text:
            position = row.text
        i = i + 1
    
    #if position == 'Point Guard':
     #   new_pos = 'GC-0 PG'
    #elif position == 'Shooting Guard':
    #    new_pos = 'GC-0 SG'
    #elif position == 'Small Forward':
     #   new_pos = 'GC-0 SF'
    #elif position == 'Power Forward':
     #   new_pos = 'GC-0 PF'
    #elif position == 'Center':
     #   new_pos = 'GC-0 C'
    #elif position == 'Guard':
     #   new_pos = 'GC-0 SG'
    #elif position == 'Forward':
     #   new_pos = 'GC-0 PF'
    
    return position


def getGameLines():
    lines_api = requests.get("https://www.espn.com/nba/scoreboard/_/date", headers={"User-Agent": "Mozilla/5.0"})     #Find lines of games today 
    lines = lines_api.text
    lines_soup = BeautifulSoup(lines, 'html5lib')
    spreads = []
    for row in lines_soup.findAll('div', attrs = {'class':'Odds__Message'}):
        temprow = row.text[:row.text.find('O/U')]
        temprow = temprow[temprow.find(': '):]
        temprow = temprow[2:]
        spreads.append(temprow)
    
    return spreads


def getTeam(id, home):
    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    o = 0
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

    team = teamname(team)
    return team


def getOppTeam(id, home):
    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    o = 0
    for row in soup2.findAll('div', attrs = {'class':'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName db'}):     #Find what team player is on
        if home and o == 1:
            team = row.text
        elif home and o == 0:
            opp_team = row.text
        elif not home and o == 0:
            team = row.text
        elif not home and o == 1:
            opp_team = row.text
        o = o + 1

    return opp_team


def homeoraway(id):
    player_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
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

    for row in soup.findAll('div', attrs = {'class': 'ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db'}):
        if row.text == team_ab[l - 1] and i == 0:
            home = False
        if row.text == team_ab[l - 1] and i == 1:
            home = True
        i = i + 1
    
    return home

    
def getTeamPos(new_pos):
    team_api = requests.get('https://www.fantasypros.com/daily-fantasy/nba/defense-vs-position.php')
    stats = team_api.text
    stats_soup = BeautifulSoup(stats, 'html5lib')
    opp_pos = []
    n = 0
    m = 0

    for row in stats_soup.findAll('tr', attrs = {'class':new_pos}):
        line = row.text[3:]
        for count, i in enumerate(line):
            if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                if line[count+2] != 'e' and line[count+1] != 'e':
                    break
            n = n + 1
        #val = 2
        line = line[:n] + ' ' + line[n+2:]    # CHANGE THE 1 to 2 once the teams have played 10 games
        n = n + 6
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        n = n + 5
        line = line[:n] + ' ' + line[n:]
        line.split(" ", 8)
        opp_pos.append(line)
        n = 0
    n = 0
    rankings = []
    for i in opp_pos:
        
        temp_rankings = []
        for m in i:
            if m == '1' or m == '2' or m =='3':
                break
            n = n + 1
        if new_pos == 'GC-0 C':
            temp_rankings.append(i[:n - 1])
            temp = n
            n = n + 6
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 6
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            rankings.append(temp_rankings)
        else:
            temp_rankings.append(i[:n - 1])
            temp = n
            n = n + 6
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            temp_rankings.append(i[temp:n - 1])
            temp = n
            n = n + 5
            rankings.append(temp_rankings)

        n = 0
    # Sort the rankings by category
    point_rankings = sorted(rankings, key=lambda x: float(x[1]))
    rebound_rankings = sorted(rankings, key=lambda x: float(x[2]))
    assist_rankings = sorted(rankings, key=lambda x: float(x[3]))
    threepoint_rankings = sorted(rankings, key=lambda x: float(x[4]))
    pra_rankings = sorted(rankings, key=lambda x: float(x[1]) + float(x[2]) + float(x[3]))
    block_rankings = sorted(rankings, key=lambda x: float(x[6]))
    steal_rankings = sorted(rankings, key=lambda x: float(x[5]))

    #make a deepcopy of ranking so they aren't pointed to same space in memory
    point_rankings = copy.deepcopy(point_rankings)
    rebound_rankings = copy.deepcopy(rebound_rankings)
    assist_rankings = copy.deepcopy(assist_rankings)
    threepoint_rankings = copy.deepcopy(threepoint_rankings)
    pra_rankings = copy.deepcopy(pra_rankings)
    steal_rankings = copy.deepcopy(steal_rankings)
    block_rankings = copy.deepcopy(block_rankings)

    #Add ranking numbers to rankings
    for i in range(0,len(point_rankings)):
        point_rankings[i].insert(0, i+1)
        rebound_rankings[i].insert(0, i+1)
        assist_rankings[i].insert(0, i+1)
        threepoint_rankings[i].insert(0, i+1)
        pra_rankings[i].insert(0, i+1)
        steal_rankings[i].insert(0, i+1)
        block_rankings[i].insert(0, i+1)
    return point_rankings, rebound_rankings, assist_rankings, threepoint_rankings, pra_rankings, block_rankings, steal_rankings


def getPlayerStats(id):
    nba_API = requests.get(f'https://www.espn.com/nba/player/splits/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    newdata = data[:data.find('<div data-box-type="fitt-adbox-native')]
    realdata = newdata[newdata.find('fake'):]
    realdata = realdata[realdata.find('<div'):]

    soup = BeautifulSoup(realdata, 'html5lib')

    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}')
    recent_data = nba_API.text
    soup2 = BeautifulSoup(recent_data, 'html5lib')
    stats = []
    i = 1
    m = 0
    n = 0
    go = False
    increment = False

    temp = 0
    temp2 = 0
    while i < 100:
        for row in soup.findAll('td', attrs = {'class':'Table__TD'}):
            if row.text != "split" and row.text != "Month" and row.text != "Result" and row.text != "Position" and row.text != "Day" and row.text != "Opponent" and row.text != "GP":
                stats.append(row.text)

            if row.text == "Opponent":
                i = 101
                break

    i = 1
    check = len(stats)
    real_stats = []
    while m < check:
        for row in soup.findAll('td', attrs = {'class':'Table__TD'}):
            if row.text == "GP":
                temp = i + 17
                go = False
            
            if go == True:
                if i != temp and n < check:
                    real_stats[n].append(row.text)

            if i == temp:
                temp += 17
                if increment == True:
                    n += 1
                if n < check:
                    real_stats.append([stats[n], row.text])
                increment = True
                go = True
                m = m + 1
                      
            i += 1
    
    temp = 0
    n = len(stats)
    keepgoing = True
    increment = False
    while(keepgoing):
        for row in soup2.findAll('td', attrs = {'class':'Table__TD'}):
            if row.text == "L10":
                increment = True

            if temp == 1 or temp == 14 and increment:
                real_stats.append([stats[n], row.text])

            if temp == 0 and increment:
                stats.append(row.text)

            if temp == 13 and increment:
                stats.append(row.text)
                n = n + 1

            if row.text == "Home" or row.text == "Road":
                keepgoing = False
                break
                
            if temp != 14 and temp != 1 and temp != 0 and temp != 13 and increment:
                real_stats[n].append(row.text)

            if increment:
                temp = temp + 1
    
    return real_stats

def getGamesNew():
    games_API = requests.get("https://sportsbook.draftkings.com/leagues/basketball/nba?sf242589544=1&name=NBA")
    games = games_API.text
    games_soup = BeautifulSoup(games, 'html5lib')
    tags = games_soup.find_all('th', class_='sportsbook-table__column-row')
    links = []
    king = "https://sportsbook.draftkings.com"
    for num, i in enumerate(tags):
        if num % 2 == 0:
            tag = i.find('a')
            link = tag['href']
            home = link[link.rfind('-') + 1:link.rfind('/')]
            home = home.capitalize()
            away = link[link.find('-') + 1:link.find("-%40")]
            away = away.capitalize()
            game  = away + " @ " + home
            link = king + link
            links.append([link, game])
    
    return links

def getLast10(log, stat):
    last10 = []
    i = 0
    if stat == 'pra':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                last10.append([temp, int(pra)])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                last10.append([temp, int(pra)])
                i = i + 1
    elif stat == 'p':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][16])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][16])])
                i = i + 1
    elif stat == 'a':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][11])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][11])])
                i = i + 1
    elif stat == 'r':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][10])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][10])])
                i = i + 1
    elif stat == '3':
        if len(log) >= 10:
            while i < 10:
                threepoint = log[i][6]
                threepoint = threepoint[:threepoint.find('-')]
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(threepoint)])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                threepoint = log[i][6]
                threepoint = threepoint[:threepoint.find('-')]
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(threepoint)])
                i = i + 1
    elif stat == 't':
        if len(log) >= 10:
            while i < 10:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][15])])
                i = i + 1
        else:
            m = len(log)
            while i < m:
                temp = log[i][0] + " " + log[i][1]
                last10.append([temp, int(log[i][15])])
                i = i + 1
    
    return last10

def getHomeAwayLog(log, stat, home):
    homeAway = []
    i = 0
    if home:
        sub = 'vs'
        if stat == 'pra':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                    homeAway.append([temp, int(pra)])
                i = i + 1
        elif stat == 'p':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 't':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][15])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if sub in log[i][1]:
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(threepoint)])
                i = i + 1

    else:
        sub = '@'
        if stat == 'pra':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                    homeAway.append([temp, int(pra)])
                i = i + 1
        elif stat == 'p':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][16])])
                i = i + 1
        elif stat == 'r':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][10])])
                i = i + 1
        elif stat == 'a':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][11])])
                i = i + 1
        elif stat == 't':
            while i < len(log):
                if sub in log[i][1]:
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(log[i][15])])
                i = i + 1
        elif stat == '3':
            while i < len(log):
                if sub in log[i][1]:
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    homeAway.append([temp, int(threepoint)])
                i = i + 1

    return homeAway

def getVSLog(log, stat, opp_team):
    vsLog = []
    temp_opp = teamname(opp_team)
    i = 0
    if stat == 'pra':
        while i < len(log):
            if temp_opp == "SA": 
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    temp = log[i][0] + " " + log[i][1]
                    pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                    vsLog.append([temp, int(pra)])
            elif temp_opp in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                pra = int(log[i][16]) + int(log[i][11]) + int(log[i][10])
                vsLog.append([temp, int(pra)])
            i = i + 1
    elif stat == 'p':
        while i < len(log):
            if temp_opp == "SA": 
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][16])])
            elif temp_opp in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][16])])
            i = i + 1
    elif stat == 'a':
        while i < len(log):
            if temp_opp == "SA":
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][11])])
            elif temp_opp in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][11])])
            i = i + 1
    elif stat == 'r':
        while i < len(log):
            if temp_opp == "SA":
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][10])])
            elif temp_opp in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][10])])
            i = i + 1
    elif stat == 't':
        while i < len(log):
            if temp_opp == "SA":
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(log[i][15])])
            elif temp_opp in log[i][1]:
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(log[i][15])])
            i = i + 1
    elif stat == '3':
        while i < len(log):
            if temp_opp == "SA":
                if log[i][1] == "vsSA" or log[i][1] == "@SA":
                    threepoint = log[i][6]
                    threepoint = threepoint[:threepoint.find('-')]
                    temp = log[i][0] + " " + log[i][1]
                    vsLog.append([temp, int(threepoint)])
            elif temp_opp in log[i][1]:
                threepoint = log[i][6]
                threepoint = threepoint[:threepoint.find('-')]
                temp = log[i][0] + " " + log[i][1]
                vsLog.append([temp, int(threepoint)])
            i = i + 1
    return vsLog


def getPointsRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-points-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks


def getAssistsRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-assists-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def getReboundsRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-total-rebounds-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def getpraRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-points-plus-rebounds-plus-assists-per-gam")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def get3ptRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-three-pointers-made-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def getBlocksRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-blocks-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def getStealsRank():
    ranks_api = requests.get("https://www.teamrankings.com/nba/stat/opponent-steals-per-game")
    ranks_text = ranks_api.text
    ranks_soup = BeautifulSoup(ranks_text, 'html5lib')

    ranks = []

    for i in range(1,31):
        ranks.append([i])
    i = 0
    for row in ranks_soup.findAll('td', attrs={'class': 'text-left nowrap'}):
        ranks[i].append(row.text)
        i += 1
    
    return ranks

def last10Hit(log,cat, line):
    last10hit = 0
    if len(log) == 0:
       return 0.0
    if cat == '3-pt':
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][6][0]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[6][0]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "points":
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][16]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[16]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "rebounds":
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][10]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[10]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "assists":
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][11]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[11]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "pra":
        if len(log) >= 10:
            for i in range(0,10):
                tot = float(log[i][11]) + float(log[i][10]) + float(log[i][16])
                if float(tot) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                tot = float(m[11]) + float(m[10]) + float(m[16])
                if float(tot) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "steals":
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][13]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[13]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "blocks":
        if len(log) >= 10:
            for i in range(0,10):
                if float(log[i][12]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 10
        else:
            for m in log:
                if float(m[12]) > float(line):
                    last10hit += 1
    
    return last10hit


def last5Hit(log,cat, line):
    last10hit = 0
    if len(log) == 0:
       return 0.0
    if cat == '3-pt':
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][6][0]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[6][0]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "points":
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][16]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[16]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "rebounds":
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][10]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[10]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "assists":
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][11]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[11]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "pra":
        if len(log) >= 5:
            for i in range(0,5):
                tot = float(log[i][11]) + float(log[i][10]) + float(log[i][16])
                if float(tot) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                tot = float(m[11]) + float(m[10]) + float(m[16])
                if float(tot) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "steals":
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][13]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[13]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    elif cat == "blocks":
        if len(log) >= 5:
            for i in range(0,5):
                if float(log[i][12]) > float(line):
                    last10hit += 1
            last10hit = last10hit / 5
        else:
            for m in log:
                if float(m[12]) > float(line):
                    last10hit += 1
            last10hit = last10hit / len(log)
    
    return last10hit

def logHit(log,cat, line):
    last10hit = 0
    if len(log) == 0:
       return 0.0
    if cat == '3-pt':
        for i in range(0,len(log)):
            if float(log[i][6][0]) > float(line):
                last10hit += 1
        last10hit = last10hit / len(log)
    elif cat == "points":
        for i in range(0,len(log)):
            if float(log[i][16]) > float(line):
                last10hit += 1
        last10hit = last10hit / len(log)
    elif cat == "rebounds":
        for i in range(0,len(log)):
            if float(log[i][10]) > float(line):
                last10hit += 1
        last10hit = last10hit / len(log)
    elif cat == "assists":
        for i in range(0,len(log)):
            if float(log[i][11]) > float(line):
                last10hit += 1
        last10hit = last10hit / len(log)
    elif cat == "pra":
        for i in range(0,len(log)):
            tot = float(log[i][11]) + float(log[i][10]) + float(log[i][16])
            if float(tot) > float(line):
                last10hit += 1
        last10hit = last10hit / len(log)
    
    return last10hit

def getMinutes(id):
    nba_API = requests.get(f'https://www.espn.com/nba/player/splits/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    data_soup = BeautifulSoup(data, 'html5lib')

    element = data_soup.findAll('tr', attrs={'data-idx':'1', 'class':"Table__TR Table__TR--sm Table__even"})
    if(len(element) <= 1):
        return 0,0
    for num, i in enumerate(element[1]):
        if num == 1:
            minutes = i.text
        elif num == 2:
            shots = i.text
            break
    
    shots = shots[shots.find('-') + 1:]
    return minutes, shots

def getNbaTodayGames():
    nba_API = requests.get(f'https://www.espn.com/nba/scoreboard', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    data_soup = BeautifulSoup(data, 'html5lib')
    games = []


    element = data_soup.findAll('div', attrs={'class':"ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName db"})
    away = False
    home = False
    for num, row in enumerate(element):
        if row.text != None and not away:
            away = True
            awayTeam = oppteamname(row.text)
        elif row.text != None and not home:
            home = True
            homeTeam = oppteamname(row.text)
        if home and away:
            games.append([awayTeam + " @ " + homeTeam])
            home = False
            away = False
    element = data_soup.findAll('span', attrs={'class':"VZTD mLASH rIczU LNzKp jsU hfDkF FoYYc FuEs"})
    index = 0
    #print(games)
    for num, row in enumerate(element):
        if row.text != None:
            games[index].append(row.text)
            if num % 2 != 0 and num != 0:
                index += 1

    # Get game IDs
    # element = data_soup.findAll('a', attrs={'class':"AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100 mr2"})
    # index = 0
    # for num, row in enumerate(element):
    #     #if num % 3 == 0:
    #     temp = row['href'][row['href'].find("gameId/"):]
    #     id = temp[temp.find('/') + 1:temp.find('/', temp.find('/') + 1)]
    #     games[index].append(id)
    #     index += 1
    return games

def getPlayerInfo(id):
    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    soup = BeautifulSoup(data, 'html5lib')

    position = ""
    team = ""
    i = 0
    for row in soup.findAll('li', attrs = {'class':''}):
        if i == 1:
            position = row.text
        i = i + 1
    
    for row in soup.findAll('a', attrs = {'class':'AnchorLink clr-black'}):
        team = oppteamname(row.text)
        break
    print(position)
    print(team)
    return position, team

def getPlayerInfoNBA(id):
    nba_API = requests.get(f'https://www.espn.com/nba/player/_/id/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    soup = BeautifulSoup(data, 'html5lib')

    position = ""
    team = ""
    i = 0
    for row in soup.findAll('li', attrs = {'class':''}):
        if i == 1:
            position = row.text
        i = i + 1
    
    for row in soup.findAll('a', attrs = {'class':'AnchorLink clr-black'}):
        team = oppteamname(row.text)
        break
    print(position)
    print(team)
    return position, team

def getDNPPlayers(id):
    nba_API = requests.get(f'https://www.espn.com/nba/boxscore/_/gameId/{id}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    data_soup = BeautifulSoup(data, 'html5lib')
    element = data_soup.findAll('tr', attrs={'class':"Table__TR Table__TR--sm Table__even"})
    awayTeamDNP = 0
    homeTeamDNP = 0
    team = 0
    appendTeams = False
    awayTeam = []
    homeTeam = []
    for row in element:
        if row.text == 'team':
            team += 1
            appendTeams = False
        elif row.text == 'starters':
            appendTeams = True
        elif appendTeams and row.text != 'bench':
            if 'Jr.' in row.text:
                name = row.text[:row.text.find('.', row.text.find('.') + 1) - 1]
            else:
                name = row.text[:row.text.find('.') - 1]
            if team == 0:
                awayTeam.append(name)
            elif team == 1:
                homeTeam.append(name)
        if team == 1 and 'DNP' in row.text:
            awayTeamDNP += 1
        if team == 2 and 'DNP' in row.text:
            homeTeamDNP += 1
        
    awayDNP = awayTeam[len(awayTeam) - awayTeamDNP:]
    homeDNP = homeTeam[len(homeTeam) - homeTeamDNP:]
  #  print(f"Away Team Players DNP:{awayTeam[len(awayTeam) - awayTeamDNP:]}")
  #  print(f"Home Team Players DNP: {homeTeam[len(homeTeam) - homeTeamDNP:]}")

    return awayDNP, homeDNP


def getInjuredPlayers(teamABBV, teamName):
    teamABBV = teamABBV.lower()
    teamName = teamName.lower()
    team = teamName.split()
    name = ""
    for i in team:
        name += i
        name += '-'
    name = name[:-1]
    nba_API = requests.get(f'https://www.espn.com/nba/team/injuries/_/name/{teamABBV}/{name}', headers={"User-Agent": "Mozilla/5.0"})
    data = nba_API.text
    data_soup = BeautifulSoup(data, 'html5lib')
    element = data_soup.findAll('span', attrs={'class':"Athlete__PlayerName"})
    players = []
    for row in element:
        players.append(row.text)
    
    return players