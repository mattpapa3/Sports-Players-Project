import time
import sqlite3
from datetime import datetime, timedelta
import nba
import MLB.mlb as mlb
import numpy as np
import unicodedata
import pandas as pd
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

def remove_tilde(text):
    # Normalize the text to decompose characters with diacritics
    normalized_text = unicodedata.normalize('NFD', text)
    # Remove diacritics by filtering out combining characters
    text_without_diacritics = ''.join(char for char in normalized_text if unicodedata.category(char) != 'Mn')
    return text_without_diacritics

def checkPropsMLB():
    kRank = mlb.getMLBStrikoutRanksTeams()
    kRank = np.array(kRank)
    runRank = mlb.getMLBRunsPerGameRanksTeams()
    runRank = np.array(runRank)
    hRank = mlb.getMLBHitsPerGameRanksTeams()
    hRank = np.array(hRank)
    today = datetime.now()
    teamstats = mlb.getMLBTeamStats()
    yesterday = today - timedelta(days=1)
    formatted_date = yesterday.strftime("%m/%d")
    if formatted_date[len(formatted_date) - 1] == '0' and formatted_date[0] == '0':     #If /10 or /20 or /30
        formatted_date = formatted_date[1:]    #Remove first 0 of month 01/10 = 1/10
    elif formatted_date[formatted_date.find('/') + 1] == '0' and formatted_date[formatted_date.find('/') - 1] == '0':                                   # If /01
        formatted_date = formatted_date[:formatted_date.find('/') + 1] + formatted_date[formatted_date.find('/') + 2:]
    elif formatted_date[formatted_date.find('/') - 1] != '0':
        formatted_date = formatted_date.replace('0', '')
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM Props")
    result = cursor.fetchall()
    props = []
    for a,b,c,d,e,f,g,h,i in result:
        props.append([a,b,c,g,h])
    props.sort()
    print(props)
    print(formatted_date)
    name = ""
    for i in props:
        rank = 0
        hit = 0
        cat = i[2]
        last10hit = 0
        last5hit = 0
        logHit = 0
        if i[0] != name:
            name = i[0]
            firstlast = name.split()
            cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;", (name,))
            result = cursor.fetchall()
            for a,b,c,d,e,f in result:
                id = a
                position = c
                team = d
                rightleft = e
            log = mlb.getMLBGameLog(id, position, False)
            if len(log) == 0:
                check = False
                lastGame = [['DONT CHECk']]
            else:
                lastGame = log[0]
            if formatted_date in lastGame[0]:
                print("PLAYED")
                check = True
            else:
                check = False
                print(name + " Not checking")
            print(name)

            if check:
                if len(log) <= 5 and len(log) > 1:
                    last5 = log[1:]
                elif len(log) > 5:
                    last5 = log[1:6]
                else:
                    last5 = []
                
                oppTeam = lastGame[1]
                if oppTeam[0] == "@":
                    home = 0
                    oppTeam = oppTeam[1:]
                else:
                    home = 1
                    oppTeam = oppTeam[2:]
                oppTeam = mlb.MLBteamname(oppTeam)
                cursor.execute("SELECT * FROM mlbTodaysGames WHERE game=?;", (i[3],))
                result = cursor.fetchall()
                for a,b,c,d,e,f in result:
                    temperature = b
                    wind = c
                    overunder = d
                line = float(i[1])

                # Get lineups of game
                cursor.execute("SELECT lineups, awaylineup FROM mlbTodaysGames WHERE game=?;", (i[3],))
                result = cursor.fetchall()
                print(result)
                if len(result) > 0 and result[0][0] != None and result[0][0] != '0':
                    for e,f in result:
                        print(e)
                        print(f)
                        homeLineup = e.split(',')
                        awayLineup = f.split(',')
                else:
                    lastGameLink = mlb.getLastGameLink(id, formatted_date)
                    print(lastGameLink)
                    homeLineup, awayLineup = mlb.getLineups(lastGameLink)
                    homeLineupdb = ','.join(homeLineup)
                    awayLineupdb = ','.join(awayLineup)
                    cursor.execute("UPDATE mlbTodaysGames SET lineups=?, awaylineup=? WHERE game=?", (homeLineupdb, awayLineupdb, i[3]))
                    sqlite_connection.commit()

                if "Pitcher" not in position:
                    if len(log) >= 11:
                        last10 = log[1:11]
                    elif len(log) > 1:
                        last10 = log[1:len(log)]
                    else:
                        last10 = []
                    print(last10)
                    last10 = np.array(last10)
                    # Find opp starting pitcher
                    print(home)
                    if home == 0:
                        oppPitcher = ""
                        for player in homeLineup:
                            if player == 'D Lynch IV':
                                player = 'Daniel Lynch'
                            player = remove_tilde(player)
                            cursor.execute("SELECT * FROM mlbPlayer WHERE name LIKE ? AND team=? and position LIKE ?", ('%' + player[2:] + '%', oppTeam, '%Pitcher%'))
                            result = cursor.fetchall()
                            if len(result) > 0:
                                for a,b,c,d,e,f in result:
                                    oppPitcherID = a
                                    oppPitcher = b
                                    oppPitcherArm = e
                            if len(oppPitcher) > 0:
                                break
                        if len(oppPitcher) == 0:
                            check = False
                        print(oppPitcher)
                    else:
                        oppPitcher = ""
                        for player in awayLineup:
                            player = remove_tilde(player)
                            print(player)
                            print(oppTeam)
                            cursor.execute("SELECT * FROM mlbPlayer WHERE name LIKE ? AND team=? and position LIKE ?", ('%' + player[2:] + '%', oppTeam, '%Pitcher%'))
                            result = cursor.fetchall()
                            #print(result)
                            if len(result) > 0:
                                for a,b,c,d,e,f in result:
                                    oppPitcherID = a
                                    oppPitcher = b
                                    oppPitcherArm = e
                            if len(oppPitcher) > 0:
                                break
                        if len(oppPitcher) == 0:
                            check = False
                        print(oppPitcher)
                    print(oppPitcher)
                    #Get Opp Pitcher Stats
                    oppPitcherStats, oppPitcherhbp, _ = mlb.getPitcherStats(oppPitcherID)
                    print(oppPitcherStats)
                    print(oppPitcherhbp)
                    fip = mlb.calculateFIP(oppPitcherStats, oppPitcherhbp)

                    #Calculate opp pitcher WHIP
                    oppwhip = (float(oppPitcherStats[9]) + float(oppPitcherStats[13])) / float(oppPitcherStats[8])
                    oppwhip = round(oppwhip, 2)
                    print(log)
                    a

                    if len(last5) > 0:
                        last5 = np.array(last5)
                        print(last5)
                        last5ops = last5[:, 18]
                        print(last5ops)
                        last5ops = np.sum(np.float64(last5ops)) / len(last5ops)
                        last5ops = round(last5ops,3)
                    else:
                        last5ops = 0.0
                elif "Pitcher" in position:
                    stats, hbp, battersfaced = mlb.getPitcherStats(id)

                    #Calculate k/9
                    k9 = (float(stats[14]) / float(stats[8])) * 9
                    k9 = round(k9, 2)

                    #Calculate fip
                    fip = mlb.calculateFIP(stats, hbp)

                    # Caluclate WHIP
                    whip = (float(stats[9]) + float(stats[13])) / float(stats[8])
                    whip = round(whip, 2)

                    #Calculate K%
                    kpercent = float(stats[14]) / float(battersfaced)
                    kpercent = round(kpercent, 2)

                    #Find the number of right handed hitters in lineup
                    righthitters = 0
                    if home == 0:
                        for player in homeLineup:
                            cursor.execute("SELECT * FROM mlbPlayer WHERE name LIKE ? AND team=?", ('%' + player[2:] + '%', oppTeam))
                            result = cursor.fetchall()
                            if len(result) > 0:
                                for a,b,c,d,e,f in result:
                                    if "Pitcher" not in c and e != 1:
                                        if e == 2 and rightleft == 1:
                                            righthitters += 1
                                        elif e != 2:
                                            righthitters += 1
                    else:
                        for player in awayLineup:
                            cursor.execute("SELECT * FROM mlbPlayer WHERE name LIKE ? AND team=?", ('%' + player[2:] + '%', oppTeam))
                            result = cursor.fetchall()
                            if len(result) > 0:
                                for a,b,c,d,e,f in result:
                                    if "Pitcher" not in c and e != 1:
                                        if e == 2 and rightleft == 1:
                                            righthitters += 1
                                        elif e != 2:
                                            righthitters += 1
                    
                    #Calculate avg innings pitched last 3
                    last5 = np.array(last5)
                    if len(last5) > 3:
                        last3 = np.array(last5[:3, 3])
                    elif len(last5) == 0:
                        last3 = np.array([])
                    else:
                        last3 = np.array(last5[:,3])
                    print(last3)
                    last3 = np.float64(last3)
                    print(last3)
                    print(last3.shape)
                    if len(last3.shape) == 0:
                        inningslast3 = [last3]
                    elif last3.shape[0] == 0:
                        inningslast3 = [0]
                    else:
                        inningslast3 = np.sum(last3) / last3.shape
                    print(inningslast3[0])
        if check:
            hit = 0
            print(log)
            log = np.array(log)
            if cat == 'era':
                line = float(i[1])
                if float(lastGame[6]) > line:
                    hit = 1
                eraTeams = runRank[:, 1]
                index = np.where(oppTeam == eraTeams)
                rank = int(runRank[index[0][0],0])

                # Get Last 5
                if len(last5) > 0:
                    eraLast5 = np.float64(last5[:, 6])
                    numLast5 = np.where(eraLast5 > line)
                    last5Hit = numLast5[0].shape[0]
                else:
                    last5Hit = 0

                cursor.execute("INSERT INTO traindataPitcherOther(homeaway, line, hit, rightleft, opprank, cat, last5, oppteam, pitcherID, righthitters,\
                               inningspitchedlast3, temperature, wind, fip, overunder) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, rightleft, rank, cat, last5Hit, oppTeam, id, righthitters, inningslast3[0], temperature, wind, fip, overunder))
                sqlite_connection.commit()
            if cat == 'hits':
                line = float(i[1])
                if float(lastGame[4]) > line:
                    hit = 1
                eraTeams = hRank[:, 1]
                index = np.where(oppTeam == eraTeams)
                rank = int(hRank[index[0][0], 0])

                # Get Last 5
                if len(last5) > 0:
                    hitsLast5 = np.float64(last5[:, 4])
                    numLast5 = np.where(hitsLast5 > line)
                    last5Hit = numLast5[0].shape[0]
                else:
                    last5Hit = 0

                cursor.execute("INSERT INTO traindataPitcherOther(homeaway, line, hit, rightleft, opprank, cat, last5, oppteam, pitcherID, righthitters,\
                               inningspitchedlast3, temperature, wind, fip, overunder) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, rightleft, rank, cat, last5Hit, oppTeam, id, righthitters, inningslast3[0], temperature, wind, fip, overunder))
                sqlite_connection.commit()
            
            if cat == 'outs':
                innings = lastGame[3]
                innsplit = innings.split('.')
                outs = (float(innsplit[0]) * 3) + float(innsplit[1])
                line = float(i[1])
                if float(outs) > line:
                    hit = 1
                eraTeams = runRank[:, 1]
                index = np.where(oppTeam == eraTeams)
                rank = int(runRank[index[0][0], 0])

                # Get Last 5
                if len(last5) > 1:
                    innLast5 = last5[:, 3]
                else:
                    innLast5 = []
                last5Hit = 0
                for inn in innLast5:
                    innsplit = inn.split('.')
                    outs = (float(innsplit[0]) * 3) + float(innsplit[1])
                    if outs > line:
                        last5Hit += 1

                cursor.execute("INSERT INTO traindataPitcherOther(homeaway, line, hit, rightleft, opprank, cat, last5, oppteam, pitcherID, righthitters,\
                               inningspitchedlast3, temperature, wind, fip, overunder) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, rightleft, rank, cat, last5Hit, oppTeam, id, righthitters, inningslast3[0], temperature, wind, fip, overunder))
                sqlite_connection.commit()
            
            if cat == 'k':
                line = float(i[1])
                if float(lastGame[9]) > line:
                    hit = 1
                kTeams = kRank[:, 1]
                index = np.where(oppTeam == kTeams)
                rank = int(kRank[index[0][0], 0])

                # Get Last 5
                if len(last5) > 0:
                    kLast5 = np.float64(last5[:, 9])
                    numLast5 = np.where(kLast5 > line)
                    last5Hit = numLast5[0].shape[0]
                else:
                    last5Hit = 0
                if stats[13] == '0':
                    kwalk = 0
                else:
                    kwalk = float(stats[14]) / float(stats[13])
                for team in teamstats:
                    if team[0] == oppTeam:
                        walkKTeam = float(team[10]) / float(team[11])
                        print("found opp team!")
                        break

                cursor.execute("INSERT INTO traindataPitcherStrikeouts(homeaway, line, hit, rightleft, opprank, last5, oppteam, pitcherID, k9, righthitters,\
                               inningspitchedlast3, kpercent, temperature, wind, fip, overunder, walkperKTeam, Kperwalk) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, rightleft, rank, last5Hit, oppTeam, id, k9, righthitters, inningslast3[0], kpercent, temperature, wind, fip, overunder, walkKTeam, kwalk))
                sqlite_connection.commit()
            
            if cat == 'r':
                line = float(i[1])
                if float(lastGame[4]) > line:
                    hit = 1
                if len(last5) > 0:
                    runLast5 = np.float64(last5[:, 4])
                    numLast5 = np.where(runLast5 > line)
                    last5Hit = numLast5[0].shape[0]

                    runLast10 = np.float64(last10[:,4])
                    numLast10 = np.where(runLast10 > line)
                    last10Hit = numLast10[0].shape[0]

                    runLog = np.float64(log[1:, 4])
                    numLog = np.where(runLog > line)
                    logHit = numLog[0].shape[0] 
                    logHit = logHit / len(log)
                else:
                    last5Hit = 0
                    logHit = 0
                    last10Hit = 0


                cursor.execute("INSERT INTO traindataHitters(homeaway, line, hit, pitchrightleft, cat, last10, last5, log, oppteam, overunder, batterID, whip,\
                               OPSlast5, temperature, wind, pitcherID, pitcherfip) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, oppPitcherArm, cat, last10Hit, last5Hit, logHit, oppTeam, overunder, id, oppwhip,\
                                 last5ops, temperature, wind, oppPitcherID, fip))
                sqlite_connection.commit()
            
            if cat == 'tb':
                line = float(i[1])
                singles = float(lastGame[5]) - (float(lastGame[6]) + float(lastGame[7]) + float(lastGame[8]))
                tot = singles + (float(lastGame[6]) * 2) + (float(lastGame[7]) * 3) + (float(lastGame[8]) * 4)
                if tot > line:
                    hit = 1

                last5Hit = 0
                last10Hit = 0
                logHit = 0
                for num, game in enumerate(log[1:]):
                    singles = float(game[5]) - (float(game[6]) + float(game[7]) + float(game[8]))
                    tot = singles + (float(game[6]) * 2) + (float(game[7]) * 3) + (float(game[8]) * 4)
                    if tot > line:
                        logHit += 1
                        if num < 5:
                            last5Hit += 1
                            last10Hit += 1
                        elif num < 10:
                            last10Hit += 1
                if logHit > 0:
                    logHit = logHit / len(log)
                
                cursor.execute("SELECT name FROM mlbPlayer WHERE id=?;", (id,))
                batterName = cursor.fetchall()
                batterName = batterName[0][0]
                cursor.execute("SELECT name FROM mlbPlayer WHERE id=?;", (oppPitcherID,))
                pitcherName = cursor.fetchall()
                if len(pitcherName) == 0:
                    print("PITCHER NOT IN DATABASE: ")
                    pos, team, rightleft = mlb.getPlayerInfo(p)
                    pitcherName = mlb.getMLBPlayerName(p)
                    cursor.execute("INSERT INTO mlbPlayer(id,name,position,team,rightleft) VALUES(?,?,?,?,?);",(p,pitcherName,pos,team,rightleft))
                else:
                    pitcherName = pitcherName[0][0]
                print(batterName)
                print(pitcherName)
                cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (id,))
                result = cursor.fetchall()
                if result[0][0] is None:
                    first_name, last_name = batterName.split()
                    idLook = playerid_lookup(last_name,first_name)
                    if len(idLook) > 1 or len(idLook) == 0:
                        print(batterName)
                        print(idLook)
                        print("CANT FIND PYBASEBALL ID")
                    hitterpybaseballID = idLook['key_mlbam'][0]
                    print(hitterpybaseballID)
                    cursor.execute("UPDATE mlbPlayer SET pybaseballID=? WHERE id=?;", (str(hitterpybaseballID), id))
                    sqlite_connection.commit()
                else:
                    cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (id,))
                    hitterpybaseballID = cursor.fetchall()
                    hitterpybaseballID = int(hitterpybaseballID[0][0])

                cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (oppPitcherID,))
                result = cursor.fetchall()
                if result[0][0] is None:
                    print("hello")
                    first_name, last_name = pitcherName.split()
                    idLook = playerid_lookup(last_name,first_name)
                    if len(idLook) > 1 or len(idLook) == 0:
                        print(pitcherName)
                        print(idLook)
                        print("CANT FIND PYBASEBALL ID")
                    pitcherpybaseballID = idLook['key_mlbam'][0]
                    print(pitcherpybaseballID)
                    cursor.execute("UPDATE mlbPlayer SET pybaseballID=? WHERE id=?;", (str(pitcherpybaseballID), oppPitcherID))
                    sqlite_connection.commit()
                else:
                    cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (oppPitcherID,))
                    pitcherpybaseballID = cursor.fetchall()
                    pitcherpybaseballID = int(pitcherpybaseballID[0][0])
                
                _, avg_vs_FF, avg_vs_off, avg_vs_pitchFF, percentFastballs, avg_spin_FF, avg_spin_off = mlb.calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID)


                cursor.execute("INSERT INTO traindataHitters(homeaway, line, hit, pitchrightleft, cat, last10, last5, log, oppteam, overunder, batterID, whip,\
                               OPSlast5, temperature, wind, pitcherID, pitcherfip,  pitcherFBPercent, avgvsFB, avgvsOFF, avgvsMPHFB, avg_spin_ff, avg_spin_off) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, oppPitcherArm, cat, last10Hit, last5Hit, logHit, oppTeam, overunder, id, oppwhip,\
                                 last5ops, temperature, wind, oppPitcherID, fip, percentFastballs, avg_vs_FF, avg_vs_off, avg_vs_pitchFF, avg_spin_FF, avg_spin_off))
                sqlite_connection.commit()
            
            if cat == 'hrb':
                line = float(i[1])
                tot = float(lastGame[5]) + float(lastGame[9]) + float(lastGame[4])
                if tot > line:
                    hit = 1
                
                last5Hit = 0
                logHit = 0
                last10Hit = 0
                
                if len(log) > 1:

                    last10runs = np.float64(last10[:, 4])
                    last10hits = np.float64(last10[:, 5])
                    last10rbis = np.float64(last10[:, 9])
                    last10hrb = last10runs + last10hits + last10rbis
                    hrblast10 = np.where(last10hrb > line)
                    last10hit = hrblast10[0].shape[0]

                    last5runs = np.float64(last5[:, 4])
                    last5hits = np.float64(last5[:, 5])
                    last5rbis = np.float64(last5[:, 9])
                    last5hrb = last5runs + last5hits + last5rbis
                    hrblast5 = np.where(last5hrb > line)
                    last5hit = hrblast5[0].shape[0]

                    runs = np.float64(log[1:, 4])
                    hits = np.float64(log[1:, 5])
                    rbis = np.float64(log[1:, 9])
                    hrb = hits + runs + rbis
                    hrbLog = np.where(hrb > line)
                    logHit = hrbLog[0].shape[0]
                    logHit = logHit / len(log)


                cursor.execute("INSERT INTO traindataHitters(homeaway, line, hit, pitchrightleft, cat, last10, last5, log, oppteam, overunder, batterID, whip,\
                               OPSlast5, temperature, wind, pitcherID, pitcherfip) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, line, hit, oppPitcherArm, cat, last10Hit, last5Hit, logHit, oppTeam, overunder, id, oppwhip,\
                                 last5ops, temperature, wind, oppPitcherID, fip))
                sqlite_connection.commit()
        print(i)
        cursor.execute("DELETE FROM Props WHERE name=? AND cat=?;", (i[0],i[2]))
        sqlite_connection.commit()
    
    cursor.execute("DELETE FROM mlbTodaysGames;")
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
        


def checkProps():
    props = []
    #Get Team Rankings
    pRank = nba.getPointsRank()
    rRank = nba.getReboundsRank()
    aRank = nba.getAssistsRank()
    bRank = nba.getBlocksRank()
    sRank = nba.getStealsRank()
    threeRank = nba.get3ptRank()
    praRank = nba.getpraRank()
    # Get today's date
    today = datetime.now()
    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)
    # Format yesterday's date as MM/DD
    formatted_date = yesterday.strftime("%m/%d")
    if formatted_date[len(formatted_date) - 1] == '0' and formatted_date[0] == '0':     #If /10 or /20 or /30
        formatted_date = formatted_date[1:]    #Remove first 0 of month 01/10 = 1/10
    elif formatted_date[formatted_date.find('/') + 1] == '0' and formatted_date[formatted_date.find('/') - 1] == '0':                                   # If /01
        formatted_date = formatted_date[:formatted_date.find('/') + 1] + formatted_date[formatted_date.find('/') + 2:]
    elif formatted_date[formatted_date.find('/') - 1] != '0':
        formatted_date = formatted_date.replace('0', '')
    print(formatted_date)
    try:
        sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM Props;")
        result = cursor.fetchall()
        for a, b, c, d, e, f, g, h, n, j, k, l, o, p, q, r, s, t in result:
            props.append([a,b,c,l,j,q,k,r])
        props.sort()
        print(props)
        name = ""
        for i in props:
            rank = 0
            hit = 0
            last10hit = 0
            lastGameHit = 0
            last5hit = 0
            loghit = 0
            posrank = 0
            if i[0] != name:
                name = i[0]
                firstlast = name.split()
                #Check if player is in database
                cursor.execute("SELECT * FROM nbaInfo WHERE name=?", (name,))
                result = cursor.fetchall()
                if len(result) == 0:
                        id = nba.getPlayerID(firstlast[0], firstlast[1])
                        if id.isdigit() and id != -1:
                          #  position = nba.getPosition(id)
                            position, team = nba.getPlayerInfo(id)
                            cursor.execute("INSERT INTO nbaInfo(id, name, position, team) VALUES(?,?,?);",(id, name, position))
                            sqlite_connection.commit()
                        print(name)
                        print(id)
                else:
                    for a, b, c, d in result:
                        id = a
                        position = c
                    _, team = nba.getPlayerInfo(id)
                # Get GameID
                # cursor.execute("SELECT id FROM nbaTodaysGames WHERE game=?", (i[4],))
                # gameId = cursor.fetchall()[0][0]
                # awayDNP, homeDNP = nba.getDNPPlayers(gameId)
                team_abb = nba.teamname(nba.oppteamname2(team))
                if team_abb in i[3]:
                    favorite = 1
                else:
                    favorite = 0
                print(i[3])
                print(favorite)
                log = nba.getGameLog(id, False)
                lastGame = log[0]
                restDays = nba.getRestDays(log, False)
                if formatted_date in lastGame[0]:
                    print("PLAYED")
                    check = True
                else:
                    check = False
                    print(name + " Not checking")
                print(name)
                
                #Get Last 10 games before last night
                if len(log) >= 11:
                    last10 = log[1:11]
                else:
                    last10 = log[1:len(log)]
                if len(log) <= 5:
                    last5 = last10
                else:
                    last5 = log[1:6]
                oppTeam = lastGame[1]
                if oppTeam[0] == "@":
                    home = 0
                    oppTeam = oppTeam[1:]
                else:
                    home = 1
                    oppTeam = oppTeam[2:]
                oppTeam = nba.teamnameFull(oppTeam)
                if team == "LA Clippers":
                    teamstats = nba.getTeamStats("Los Angeles Clippers")
                else:
                    teamstats = nba.getTeamStats(team)

                # Calculate the number of starters/bench players that didn't play
                startersInjured = 0
                benchInjured = 0
                usageInjured = 0.0
                DNPplayers = nba.getInjuredPlayers(team_abb, team)
                for p in DNPplayers:
                    cursor.execute("SELECT id FROM nbaInfo WHERE name=?", (p,))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        DNPid = result[0][0]
                    else:
                        DNPid = nba.getPlayerID(p[:p.find(" ")], p[p.find(" ") + 1:])
                    DNPstats = nba.getTotStats(DNPid)
                    usageInjured += nba.calc_uasge_perc(DNPstats, teamstats)
                    playerMin, _ = nba.getMinutes(DNPid)
                    if float(playerMin) >= 29.0:
                        startersInjured += 1
                    else:
                        benchInjured += 1
                print("INJURIES")
                print(DNPplayers)
                print(startersInjured)
                print(benchInjured)
                print(usageInjured)            


                # Get oppTeam2 for position rankings
                if oppTeam == "LA Clippers":
                    oppTeam2 = "Clippers"
                elif oppTeam == "LA Lakers":
                    oppTeam2 = "Lakers"
                elif oppTeam == "Okla City":
                    oppTeam2 = "Thunder"
                else:
                    oppTeam2 = oppTeam

                #Get new_pos for position rankings
                if position == 'Point Guard':
                   new_pos = 'GC-0 PG'
                elif position == 'Shooting Guard':
                    new_pos = 'GC-0 SG'
                elif position == 'Small Forward':
                   new_pos = 'GC-0 SF'
                elif position == 'Power Forward':
                   new_pos = 'GC-0 PF'
                elif position == 'Center':
                   new_pos = 'GC-0 C'
                elif position == 'Guard':
                   new_pos = 'GC-0 SG'
                elif position == 'Forward':
                   new_pos = 'GC-0 PF'
                posrankings = nba.getTeamPos(new_pos)
                print(oppTeam)
                index = lastGame[2].index('-')
                if "OT" in lastGame[2]:
                    index2 = lastGame[2].index(' ')
                    lastgamescore = int(lastGame[2][1:index]) + int(lastGame[2][index+1:index2])
                    lastgameSpread = abs(int(lastGame[2][1:index]) - int(lastGame[2][index+1:index2]))
                else:
                    lastgamescore = int(lastGame[2][1:index]) + int(lastGame[2][index+1:])
                    lastgameSpread = abs(int(lastGame[2][1:index]) - int(lastGame[2][index+1:]))

                # Get last 5 minutes/shots per game and FG last 5
                FGlast5 = 0.0
                FGlast3 = 0.0
                threePTPercentlast5 = 0.0
                threePTPercentlast3 = 0.0
                minutes = 0
                shots = 0
                if len(log) > 1:
                    tot = 0
                    totshots = 0
                    for num, m in enumerate(last5):
                        tot += int(m[3])
                        totshots += int(m[4][m[4].find('-') + 1:])
                        FGlast5 += float(m[5])
                        threePTPercentlast5 += float(m[7])
                        if num < 3:
                            FGlast3 += float(m[5])
                            threePTPercentlast3 += float(m[7])
                    minutes = tot / len(last5)
                    shotslast5 = totshots / len(last5)
                    mpg, shots = nba.getMinutes(id)
                    minutes = round(minutes - float(mpg), 2)
                    shots = round(shotslast5 - float(shots), 2)
                    FGlast5 /= len(last5)
                    threePTPercentlast5 /= len(last5)
                    if len(log) >= 3:
                        FGlast3 /= 3
                        threePTPercentlast3 /= 3
                    else:
                        FGlast3 /= len(log)
                        threePTPercentlast3 /= len(log)
                totstats = nba.getTotStats(id)
                usageP = nba.calc_uasge_perc(totstats, teamstats)
                print(usageP)
                
                # print(minutes)
                # print(shots)
                # print(FGlast5)
                # print(FGlast3)
                # print(threePTPercentlast3)
                # print(threePTPercentlast5)
                # print(lastgamescore)
                # print(lastgameSpread)
                # print(lastGame)
            
            #If player played in game yesterday (Check)
            if check:
                print(i)
                if i[2] == '3-pt':
                    made = lastGame[6][:lastGame[6].find('-')]
                    if float(i[1]) < float(made):
                        hit = 1
                    for m in threeRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[3]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[6][0]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)
                        
                        for m in last5:
                            if float(m[6][0]) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            if float(log[m][6][0]) > float(i[1]):
                                loghit += 1
                        
                        if float(log[1][6][0]) > float(i[1]):
                            lastGameHit = 1

                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, id, odds, underodds, injuredUsage, usageP, restDays) \
                                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5],i[7], usageInjured, usageP, restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
                elif i[2] == 'points':
                    scored = lastGame[16]
                    if float(scored) > float(i[1]):
                        hit = 1
                    for m in pRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[0]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[16]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in range(1, len(log)):
                            if float(log[m][16]) > float(i[1]):
                                loghit += 1
                            loghit = loghit / (len(log) - 1)
                            loghit = round(loghit, 2)
                        
                        for m in last5:
                            if float(m[16]) > float(i[1]):
                                last5hit += 1
                        
                        if float(log[1][16]) > float(i[1]):
                            lastGameHit = 1
                        last5hit = last5hit / len(last5)
                    
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, id, odds, underodds, injuredUsage, usageP, restDays)\
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7],usageInjured,usageP,restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
                
                elif i[2] == 'rebounds':
                    r = lastGame[10]
                    if float(r) > float(i[1]):
                        hit = 1
                    for m in rRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[1]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[10]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in last5:
                            if float(m[10]) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            if float(log[m][10]) > float(i[1]):
                                loghit += 1
                        
                        if float(log[1][10]) > float(i[1]):
                            lastGameHit = 1
                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                    
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, id, odds, \
                                   underodds, injuredUsage, usageP, restDays) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7], usageInjured, usageP, restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
                
                elif i[2] == 'assists':
                    r = lastGame[11]
                    if float(r) > float(i[1]):
                        hit = 1
                    for m in aRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[2]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[11]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in last5:
                            if float(m[11]) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            if float(log[m][11]) > float(i[1]):
                                loghit += 1
                        
                        if float(log[1][11]) > float(i[1]):
                            lastGameHit = 1
                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, id, odds, underodds, injuredUsage, usageP, restDays) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7], usageInjured, usageP,restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
                
                elif i[2] == 'pra':
                    r = float(lastGame[11]) + float(lastGame[10]) + float(lastGame[16])
                    if float(r) > float(i[1]):
                        hit = 1
                    for m in praRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[4]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            tot = float(m[11]) + float(m[10]) + float(m[16])
                            if float(tot) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in last5:
                            tot = float(m[11]) + float(m[10]) + float(m[16])
                            if float(tot) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            tot = float(log[m][11]) + float(log[m][10]) + float(log[m][16])
                            if float(tot) > float(i[1]):
                                loghit += 1

                        tot = float(log[1][11]) + float(log[1][10]) + float(log[1][16])
                        if tot > float(i[1]):
                            lastGameHit = 1
                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, id, \
                                   odds, underodds, injuredUsage, usageP, restDays) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7], usageInjured, usageP,restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
                elif i[2] == "blocks":
                    r = lastGame[12]
                    if float(r) > float(i[1]):
                        hit = 1
                    for m in bRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[5]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[12]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in last5:
                            if float(m[12]) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            if float(log[m][12]) > float(i[1]):
                                loghit += 1
                        
                        if float(log[1][12]) > float(i[1]):
                            lastGameHit = 1
                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                        cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, lastGameHit, threePTPercentlast5, threePTPercentlast3, \
                                       id, odds, underodds, injuredUsage, usageP,restDays) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7], usageInjured, usageP,restDays))
                        sqlite_connection.commit()
                        cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                    (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                        sqlite_connection.commit()
                    print(hit)
                elif i[2] == "steals":
                    r = lastGame[13]
                    if float(r) > float(i[1]):
                        hit = 1
                    for m in sRank:
                        if oppTeam in m:
                            rank = int(m[0])
                            break
                    
                    #Get Opp team positon rank
                    for m in posrankings[6]:
                        if oppTeam2 in m[1]:
                            posrank = int(m[0])
                            break
                    
                    if len(log) > 1:
                        for m in last10:
                            if float(m[13]) > float(i[1]):
                                last10hit += 1
                        last10hit = last10hit / len(last10)

                        for m in last5:
                            if float(m[13]) > float(i[1]):
                                last5hit += 1
                        last5hit = last5hit / len(last5)

                        for m in range(1, len(log)):
                            if float(log[m][13]) > float(i[1]):
                                loghit += 1
                        
                        if float(log[1][13]) > float(i[1]):
                            lastGameHit = 1
                        loghit = loghit / (len(log) - 1)
                        loghit = round(loghit, 2)
                    print(hit)
                    cursor.execute("INSERT INTO traindataNBA(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, gamescore, minutes, oppteam, shots, spread, date, favorite, injuredStarters, injuredBench, shootingPLast3, shootingPLast5, \
                                   lastGameHit, threePTPercentlast5, threePTPercentlast3, id, odds, underodds, injuredUsage, usageP,restDays) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                   (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, i[6], minutes, oppTeam, shots, i[3], yesterday, favorite, startersInjured, benchInjured, FGlast5, FGlast3, lastGameHit, threePTPercentlast5, threePTPercentlast5, id, i[5], i[7], usageInjured, usageP,restDays))
                    sqlite_connection.commit()
                    cursor.execute("INSERT INTO traindataNBA2(homeaway, line, hit, position, opp, cat, last10, last5, log, oppposrank, oppteam, gamescore, minutes, shots, spread, odds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (home, float(i[1]), hit, position, rank, i[2], last10hit, last5hit, loghit, posrank, oppTeam, lastgamescore, minutes, shots, lastgameSpread, i[5]))
                    sqlite_connection.commit()
            cursor.execute("DELETE FROM Props WHERE name=? AND stat=? AND cat=?", (i[0], i[1], i[2]))
            sqlite_connection.commit()
            print(posrank)
            


    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()

def deleteGames():
    sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("DELETE FROM nbaTodaysGames;")
    sqlite_connection.commit()
    cursor.execute("DELETE FROM Votes;")
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

def deleteProps():

    try:
        sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("DELETE FROM Props;")
        sqlite_connection.commit()
        cursor.execute("DELETE FROM votes;")
        sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()

def checkSubs():
    subs = []
    try:
        sqlite_connection = sqlite3.connect('/root/propscode/propscode/subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM subscribers WHERE cancel=? AND subscribed=?;", ('y', 'y'))
        result = cursor.fetchall()
        for a, b, c, d, e, f in result:
            subs.append([a,b,c,d,e,f])
        
        for i in subs:
            if i[4] == 'y':
                check = int(time.time()) - int(i[1]) 
                if check >= 604800:
                    cursor.execute("""UPDATE subscribers SET subscribed=? WHERE email=?;""", ('n', i[0]))
                    sqlite_connection.commit()
            else:
                check = int(time.time()) - int(i[1]) 
                if check >= 2629743:
                    cursor.execute("""UPDATE subscribers SET subscribed=? WHERE email=?;""", ('n', i[0]))
                    sqlite_connection.commit()
        subs = []
        cursor.execute("SELECT * FROM subscribers WHERE free_trial=? AND subscribed=?;", ('y', 'y'))
        result = cursor.fetchall()
        for a, b, c, d, e, f in result:
            subs.append([a,b,c,d,e,f])
        for i in subs:
            check = int(time.time()) - int(i[1])
            if check >= 604800:
                cursor.execute("""UPDATE subscribers SET free_trial=? WHERE email=?;""", ('n', i[0]))
                sqlite_connection.commit()
                cursor.execute("""UPDATE subscribers SET date = date + ? WHERE email=?;""", (604800, i[0]))
                sqlite_connection.commit()

    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()

def updateStrikeouts():
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM traindataPitcherStrikeouts")
    result = cursor.fetchall()

    teamstats = mlb.getMLBTeamStats()

    for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r in result:
        val = q
        if val is None:
            stats, _, _ = mlb.getPitcherStats(h)
            kwalk = float(stats[14]) / float(stats[13])
            for team in teamstats:
                if team[0] == g:
                    walkKTeam = float(team[10]) / float(team[11])
                    print("found opp team!")
                    break
            cursor.execute("UPDATE traindataPitcherStrikeouts SET walkperKTeam = ?, Kperwalk = ? WHERE line=? AND pitcherID=? AND oppteam=? AND temperature=? AND wind=? AND last5=?",\
                (walkKTeam, kwalk, b, h, g, m, n, f))
            sqlite_connection.commit()
            print(walkKTeam)
            print(kwalk)
            print("\n")
    
    cursor.close()
    sqlite_connection.close()

def updateHitters():
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM traindataHitters WHERE avg_spin_ff IS NULL;")
    result = cursor.fetchall()
    
    for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w in result:
        batterID = k
        pitcherID = p
        print(k)
        print(p)
        cursor.execute("SELECT name FROM mlbPlayer WHERE id=?;", (batterID,))
        batterName = cursor.fetchall()
        if len(batterName) == 0:
            print("BATTER NOT IN DATABASE: ")
            pos, team, rightleft = mlb.getPlayerInfo(k)
            batterName = mlb.getMLBPlayerName(k)
            cursor.execute("INSERT INTO mlbPlayer(id,name,position,team,rightleft) VALUES(?,?,?,?,?);",(k,batterName,pos,team,rightleft))
        else:
            batterName = batterName[0][0]
        cursor.execute("SELECT name FROM mlbPlayer WHERE id=?;", (pitcherID,))
        pitcherName = cursor.fetchall()
        if len(pitcherName) == 0:
            print("PITCHER NOT IN DATABASE: ")
            pos, team, rightleft = mlb.getPlayerInfo(p)
            pitcherName = mlb.getMLBPlayerName(p)
            cursor.execute("INSERT INTO mlbPlayer(id,name,position,team,rightleft) VALUES(?,?,?,?,?);",(p,pitcherName,pos,team,rightleft))
        else:
            pitcherName = pitcherName[0][0]
        print(batterName)
        print(pitcherName)
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (batterID,))
        result = cursor.fetchall()
        if result[0][0] is None:
            first_name, last_name = batterName.split()
            idLook = playerid_lookup(last_name,first_name)
            if len(idLook) > 1 or len(idLook) == 0:
                print(batterName)
                print(idLook)
                print("CANT FIND PYBASEBALL ID")
                break
            hitterpybaseballID = idLook['key_mlbam'][0]
            print(hitterpybaseballID)
            cursor.execute("UPDATE mlbPlayer SET pybaseballID=? WHERE id=?;", (str(hitterpybaseballID), batterID))
            sqlite_connection.commit()
        else:
            cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (batterID,))
            hitterpybaseballID = cursor.fetchall()
            hitterpybaseballID = int(hitterpybaseballID[0][0])

        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (pitcherID,))
        result = cursor.fetchall()
        if result[0][0] is None:
            print("hello")
            first_name, last_name = pitcherName.split()
            idLook = playerid_lookup(last_name,first_name)
            if len(idLook) > 1 or len(idLook) == 0:
                print(pitcherName)
                print(idLook)
                print("CANT FIND PYBASEBALL ID")
                break
            pitcherpybaseballID = idLook['key_mlbam'][0]
            print(pitcherpybaseballID)
            cursor.execute("UPDATE mlbPlayer SET pybaseballID=? WHERE id=?;", (str(pitcherpybaseballID), pitcherID))
            sqlite_connection.commit()
        else:
            cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (pitcherID,))
            pitcherpybaseballID = cursor.fetchall()
            pitcherpybaseballID = int(pitcherpybaseballID[0][0])
        print(hitterpybaseballID)
        print(pitcherpybaseballID)
        
        _, _, _, _, _, avg_spin_ff, avg_spin_off = mlb.calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID)
        cursor.execute("UPDATE traindataHitters SET avg_spin_ff = ?, avg_spin_off = ? \
            WHERE batterID=? AND pitcherID=? AND OPSlast5=? AND temperature=? AND wind=? AND last5=?",
                (avg_spin_ff, avg_spin_off, k, p, m, n, o, g))
        sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

def fixnan():
    df = pd.read_csv("/root/propscode/propscode/MLB/Hitterdata.csv")
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    nan_rows = df[df['avg_spin_off'].isna()]
    for index, row in nan_rows.iterrows():
        id = str(row['batterID'])
        pitcherID = str(row['pitcherID'])
        whip = row['whip']
        ops = row['OPSlast5']
        print(ops)
        last10 = int(row['last10'])
        last5 = int(row['last5'])
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?", (id,))
        result = cursor.fetchall()
        hitterpybaseballID = int(result[0][0])
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?", (pitcherID,))
        result = cursor.fetchall()
        pitcherpybaseballID = int(result[0][0])
        id = int(id)
        pitcherID = int(pitcherID)
        _, _, _, _, _, _, avg_spin_off = mlb.calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID)
        cursor.execute("UPDATE traindataHitters SET avg_spin_off = ? \
            WHERE batterID=? AND pitcherID=? AND whip=? AND last10=? AND last5=?",
                (avg_spin_off, id, pitcherID, whip, last10, last5))
        sqlite_connection.commit()
    nan_rows = df[df['avg_spin_ff'].isna()]
    for index, row in nan_rows.iterrows():
        id = str(row['batterID'])
        pitcherID = str(row['pitcherID'])
        whip = row['whip']
        ops = row['OPSlast5']
        last5 = int(row['last5'])
        last10 = int(row['last10'])
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?", (id,))
        result = cursor.fetchall()
        hitterpybaseballID = int(result[0][0])
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?", (pitcherID,))
        result = cursor.fetchall()
        pitcherpybaseballID = int(result[0][0])
        id = int(id)
        pitcherID = int(pitcherID)
        _, _, _, _, _, avg_spin_ff, _ = mlb.calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID)
        cursor.execute("UPDATE traindataHitters SET avg_spin_ff = ? \
            WHERE batterID=? AND pitcherID=? AND last10=? AND whip=? AND last5=?",
                (avg_spin_ff, id, pitcherID, last10, whip, last5))
        sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

def updatepybaseballID():
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM mlbPlayer WHERE pybaseballID IS NULL")
    result = cursor.fetchall()
    for a,b,c,d,e,f in result:
        print(b)
        try:
            first_name, last_name = b.split()
            idLook = playerid_lookup(last_name,first_name)
        except:
            continue
        if len(idLook) > 1 or len(idLook) == 0:
            print(b)
            print(idLook)
            print("CANT FIND PYBASEBALL ID")
            continue
        pitcherpybaseballID = idLook['key_mlbam'][0]
        print(pitcherpybaseballID)
        cursor.execute("UPDATE mlbPlayer SET pybaseballID=? WHERE id=?;", (str(pitcherpybaseballID), a))
        sqlite_connection.commit()


if __name__ == "__main__":
    #checkSubs()
    checkProps()
    deleteGames()
   # deleteProps()
 #   checkPropsMLB()
#  updatepybaseballID()
