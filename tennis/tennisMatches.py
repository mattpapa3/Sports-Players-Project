import tennis
import numpy as np
import sqlite3
from datetime import datetime

def getMatches():
    today_date = datetime.today().strftime("%d-%b-%Y")
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/tennis/tennis.db")
    cursor = sqlite_connection.cursor()
    lines = tennis.getLines()
    print(lines[1:2])
    for i in lines[1:2]:
        vs_index = i[0].find("vs")
        odds_index = i[1].find("vs")
        if i[1][odds_index+3] == "+":
            underdog = i[0][vs_index + 3:]
            favorite = i[0][:vs_index - 1]
            fav_odds = i[1][:odds_index - 1]
            dog_odds = i[1][odds_index+3:]
        elif i[1][0] == '+':
            favorite = i[0][vs_index + 3:]
            underdog = i[0][:vs_index - 1]
            dog_odds = i[1][:odds_index - 1]
            fav_odds = i[1][odds_index+3:]
        elif int(i[1][1:odds_index - 1]) > int(i[1][odds_index+4:]):
            underdog = i[0][vs_index + 3:]
            favorite = i[0][:vs_index - 1]
            fav_odds = i[1][:odds_index - 1]
            dog_odds = i[1][odds_index+3:]
        else:
            favorite = i[0][vs_index + 3:]
            underdog = i[0][:vs_index - 1]
            dog_odds = i[1][:odds_index - 1]
            fav_odds = i[1][odds_index+3:]
        print(f"FAVORITE: {favorite} at LINE: {fav_odds}")
        print(f"UNDERDOG: {underdog} at LINE: {dog_odds}")
        underdog = underdog.replace(" ", "")
        favorite = favorite.replace(" ", "")
        print(underdog)
        dog_recent, dog_career, dog_rank, dog_rightleft = tennis.getStats(underdog)
        dog_recent = np.array(dog_recent)
        DR_ratio = dog_recent[:,8]
        DR_ratio = DR_ratio[DR_ratio != '']
        dog_mean_DR = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,9]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        dog_mean_AceRate = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,10]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        dog_mean_FaultRate = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,11]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        dog_mean_1stServe = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,12]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        dog_mean_1stWon = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,13]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        dog_mean_2ndWon = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = dog_recent[:,14]
        DR_ratio = DR_ratio[DR_ratio != '']
        numerators, denominators = zip(*[map(float, frac.split('/')) for frac in DR_ratio])
        float_values = np.array(numerators) / np.array(denominators)
        float_values = np.nan_to_num(float_values, nan=0.0)
        dog_bp_saved = round(np.mean(float_values), 2)
        DR_ratio = dog_recent[:,15]
        DR_ratio = DR_ratio[DR_ratio != '']
        time_in_seconds = np.array([int(min_sec.split(':')[0]) * 60 + int(min_sec.split(':')[1]) 
                                for min_sec in DR_ratio])
        dog_time = round(np.mean(time_in_seconds),2)

        # Favorite
        print(favorite)
        fav_recent, fav_career, fav_rank, fav_rightleft = tennis.getStats(favorite)
        fav_recent = np.array(fav_recent)
        DR_ratio = fav_recent[:,8]
        DR_ratio = DR_ratio[DR_ratio != '']
        fav_mean_DR = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,9]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        fav_mean_AceRate = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,10]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        fav_mean_FaultRate = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,11]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        fav_mean_1stServe = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,12]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        fav_mean_1stWon = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,13]
        DR_ratio = DR_ratio[DR_ratio != '']
        DR_ratio = np.char.replace(DR_ratio, '%', '')
        fav_mean_2ndWon = round(np.mean(np.float64(DR_ratio)), 2)
        DR_ratio = fav_recent[:,14]
        DR_ratio = DR_ratio[DR_ratio != '']
        numerators, denominators = zip(*[map(float, frac.split('/')) for frac in DR_ratio])
        float_values = np.array(numerators) / np.array(denominators)
        float_values = np.nan_to_num(float_values, nan=0.0)
        fav_bp_saved = round(np.mean(float_values), 2)
        DR_ratio = fav_recent[:,15]
        DR_ratio = DR_ratio[DR_ratio != '']
        time_in_seconds = np.array([int(min_sec.split(':')[0]) * 60 + int(min_sec.split(':')[1]) 
                                for min_sec in DR_ratio])
        fav_time = round(np.mean(time_in_seconds),2)
        print(fav_career)

        if i[2] == 'hard':
            dog_ground_stats = dog_career[0]
            fav_ground_stats = fav_career[0]
        elif i[2] == 'clay':
            dog_ground_stats = dog_career[1]
            fav_ground_stats = fav_career[1]
        elif i[2] == 'grass':
            dog_ground_stats = dog_career[2]
            fav_ground_stats = fav_career[2]
        

        # Get UnderDog Right vs Left Stats
        if dog_rightleft == 0:
            for i in fav_career:
                if 'Right' in i[0]:
                    fav_rightleft_stats = i
                    break
        else:
            for i in fav_career:
                if 'Left' in i[0]:
                    fav_rightleft_stats = i
                    break
        
        # Get Favorite Right vs Left Stats
        if fav_rightleft == 0:
            for i in dog_career:
                if 'Right' in i[0]:
                    dog_rightleft_stats = i
                    break
        else:
            for i in dog_career:
                if 'Left' in i[0]:
                    dog_rightleft_stats = i
                    break
        dog_rightleft_stats = [item.replace('%', '') for item in dog_rightleft_stats]
        fav_rightleft_stats = [item.replace('%', '') for item in fav_rightleft_stats]
        dog_ground_stats = [item.replace('%', '') for item in dog_ground_stats]
        fav_ground_stats = [item.replace('%', '') for item in fav_ground_stats]
        dog_rightleft_stats = [item.replace('-', '0') for item in dog_rightleft_stats]
        fav_rightleft_stats = [item.replace('-', '0') for item in fav_rightleft_stats]
        dog_ground_stats = [item.replace('-', '0') for item in dog_ground_stats]
        fav_ground_stats = [item.replace('-', '0') for item in fav_ground_stats]
        cursor.execute("""INSERT INTO matches(fav, dog, date, dogOdds, favOdds, dogRank, favRank, dogDR, favDR, dogACERatio, favACERatio, dogFaultRate,\
                        favFaultRate, dog1stServe, fav1stServe, dog1stWon, fav1stWon, dog2ndWon, fav2ndWon, dogBPSaved, favBPSaved, dogTime, favTime,\
                       dogGroundWin, favGroundWin, dogRightLeftWin, favRightLeftWin, dogGroundSetWin, favGroundSetWin, dogRightLeftSetWin, favRightLeftSetWin,\
                       dogGroundGameWin, favGroundGameWin, dogRightLeftGameWin, favRightLeftGameWin, dogGroundTieBreak, favGroundTieBreak, dogRightLeftTieBreak,\
                       favRightLeftTieBreak, dogGroundHold, favGroundHold, dogRightLeftHold, favRightLeftHold, dogGroundBreak, favGroundBreak, dogRightLeftBreak,\
                       favRightLeftBreak, dogGroundAce, favGroundACE, dogRightLeftAce, favRightLeftAce, dogGroundDF, favGroundDF, dogRightLeftDF, favRightLeftDF,\
                        dogGround1st, favGround1st, dogRightLeft1st, favRightLeft1st, dogGround1stWon, favGround1stWon, dogRightLeft1stWon, favRightLeft1stWon, dogGround2nd, favGround2nd, dogRightLeft2nd, favRightLeft2nd, dogGroundService,\
                       favGroundService, dogRightLeftService, favRightLeftService, dogGroundReturn, favGroundReturn, dogRightLeftReturn, favRightLeftReturn,\
                       dogGroundTPW, favGroundTPW, dogRightLeftTPW, favRightLeftTPW, dogGroundDR, favGroundDR, dogRightLeftDR, favRightLeftDR) VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?);""", (favorite, underdog, today_date, dog_odds, fav_odds, dog_rank, fav_rank,\
                                                                                               dog_mean_DR, fav_mean_DR, dog_mean_AceRate, fav_mean_AceRate, dog_mean_FaultRate, fav_mean_FaultRate,\
                                                                                                dog_mean_1stServe, fav_mean_1stServe, dog_mean_1stWon, fav_mean_1stWon, dog_mean_2ndWon, fav_mean_2ndWon,\
                                                                                                    dog_bp_saved, fav_bp_saved, dog_time, fav_time, float(dog_ground_stats[4]),float(fav_ground_stats[4]),\
                                                                                                        float(dog_rightleft_stats[4]),float(fav_rightleft_stats[4]),float(dog_ground_stats[6]),float(fav_ground_stats[6]),\
                                                                                                            float(dog_rightleft_stats[6]),float(fav_rightleft_stats[6]),float(dog_ground_stats[8]),float(fav_ground_stats[8]),\
                                                                                                                float(dog_rightleft_stats[8]),float(fav_rightleft_stats[8]),float(dog_ground_stats[10]),float(fav_ground_stats[10]),\
                                                                                                                    float(dog_rightleft_stats[10]),float(fav_rightleft_stats[10]),float(dog_ground_stats[12]),float(fav_ground_stats[12]),\
                                                                                                                        float(dog_rightleft_stats[12]),float(fav_rightleft_stats[12]),float(dog_ground_stats[13]),float(fav_ground_stats[13]),\
                                                                                                                            float(dog_rightleft_stats[13]),float(fav_rightleft_stats[13]),float(dog_ground_stats[14]),float(fav_ground_stats[14]),\
                                                                                                                                float(dog_rightleft_stats[14]),float(fav_rightleft_stats[14]),float(dog_ground_stats[15]),float(fav_ground_stats[15]),\
                                                                                                                                    float(dog_rightleft_stats[15]),float(fav_rightleft_stats[15]),float(dog_ground_stats[16]),float(fav_ground_stats[16]),\
                                                                                                                                        float(dog_rightleft_stats[16]),float(fav_rightleft_stats[16]),float(dog_ground_stats[17]),float(fav_ground_stats[17]),\
                                                                                                                                            float(dog_rightleft_stats[17]),float(fav_rightleft_stats[17]),float(dog_ground_stats[18]),float(fav_ground_stats[18]),\
                                                                                                                                                float(dog_rightleft_stats[18]),float(fav_rightleft_stats[18]),float(dog_ground_stats[19]),float(fav_ground_stats[19]),\
                                                                                                                                                    float(dog_rightleft_stats[19]),float(fav_rightleft_stats[19]),float(dog_ground_stats[20]),float(fav_ground_stats[20]),\
                                                                                                                                                        float(dog_rightleft_stats[20]),float(fav_rightleft_stats[20]),float(dog_ground_stats[21]),float(fav_ground_stats[21]),\
                                                                                                                                                            float(dog_rightleft_stats[21]),float(fav_rightleft_stats[21]),float(dog_ground_stats[22]),float(fav_ground_stats[22]),\
                                                                                                                                                                float(dog_rightleft_stats[22]),float(fav_rightleft_stats[22])))
        sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()

def updateMatches():
    # 0 = Dog Won, 1 = Favorite Won
    winner = 1
    sqlite_connection = sqlite3.connect("/root/propscode/propscode/tennis/tennis.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM matches;")
    result = cursor.fetchall()
    for fav, dog, date, dogOdds, favOdds, dogRank, favRank, dogDR, favDR, dogACERatio, favACERatio, dogFaultRate,\
                        favFaultRate, dog1stServe, fav1stServe, dog1stWon, fav1stWon, dog2ndWon, fav2ndWon, dogBPSaved, favBPSaved, dogTime, favTime,\
                       dogGroundWin, favGroundWin, dogRightLeftWin, favRightLeftWin, dogGroundSetWin, favGroundSetWin, dogRightLeftSetWin, favRightLeftSetWin,\
                       dogGroundGameWin, favGroundGameWin, dogRightLeftGameWin, favRightLeftGameWin, dogGroundTieBreak, favGroundTieBreak, dogRightLeftTieBreak,\
                       favRightLeftTieBreak, dogGroundHold, favGroundHold, dogRightLeftHold, favRightLeftHold, dogGroundBreak, favGroundBreak, dogRightLeftBreak,\
                       favRightLeftBreak, dogGroundAce, favGroundACE, dogRightLeftAce, favRightLeftAce, dogGroundDF, favGroundDF, dogRightLeftDF, favRightLeftDF,\
                        dogGround1st, favGround1st, dogRightLeft1st, favRightLeft1st, dogGround1stWon, favGround1stWon, dogRightLeft1stWon, favRightLeft1stWon, dogGround2nd, favGround2nd, dogRightLeft2nd, favRightLeft2nd, dogGroundService,\
                       favGroundService, dogRightLeftService, favRightLeftService, dogGroundReturn, favGroundReturn, dogRightLeftReturn, favRightLeftReturn,\
                       dogGroundTPW, favGroundTPW, dogRightLeftTPW, favRightLeftTPW, dogGroundDR, favGroundDR, dogRightLeftDR, favRightLeftDR in result:
        cursor.execute("""INSERT INTO traindataMatches(fav, dog, date, dogOdds, favOdds, dogRank, favRank, dogDR, favDR, dogACERatio, favACERatio, dogFaultRate,\
                        favFaultRate, dog1stServe, fav1stServe, dog1stWon, fav1stWon, dog2ndWon, fav2ndWon, dogBPSaved, favBPSaved, dogTime, favTime,\
                       dogGroundWin, favGroundWin, dogRightLeftWin, favRightLeftWin, dogGroundSetWin, favGroundSetWin, dogRightLeftSetWin, favRightLeftSetWin,\
                       dogGroundGameWin, favGroundGameWin, dogRightLeftGameWin, favRightLeftGameWin, dogGroundTieBreak, favGroundTieBreak, dogRightLeftTieBreak,\
                       favRightLeftTieBreak, dogGroundHold, favGroundHold, dogRightLeftHold, favRightLeftHold, dogGroundBreak, favGroundBreak, dogRightLeftBreak,\
                       favRightLeftBreak, dogGroundAce, favGroundACE, dogRightLeftAce, favRightLeftAce, dogGroundDF, favGroundDF, dogRightLeftDF, favRightLeftDF,\
                        dogGround1st, favGround1st, dogRightLeft1st, favRightLeft1st, dogGround1stWon, favGround1stWon, dogRightLeft1stWon, favRightLeft1stWon, dogGround2nd, favGround2nd, dogRightLeft2nd, favRightLeft2nd, dogGroundService,\
                       favGroundService, dogRightLeftService, favRightLeftService, dogGroundReturn, favGroundReturn, dogRightLeftReturn, favRightLeftReturn,\
                       dogGroundTPW, favGroundTPW, dogRightLeftTPW, favRightLeftTPW, dogGroundDR, favGroundDR, dogRightLeftDR, favRightLeftDR, winner) VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?);""", (fav, dog, date, dogOdds, favOdds, dogRank, favRank, dogDR, favDR, dogACERatio, favACERatio, dogFaultRate,\
                        favFaultRate, dog1stServe, fav1stServe, dog1stWon, fav1stWon, dog2ndWon, fav2ndWon, dogBPSaved, favBPSaved, dogTime, favTime,\
                       dogGroundWin, favGroundWin, dogRightLeftWin, favRightLeftWin, dogGroundSetWin, favGroundSetWin, dogRightLeftSetWin, favRightLeftSetWin,\
                       dogGroundGameWin, favGroundGameWin, dogRightLeftGameWin, favRightLeftGameWin, dogGroundTieBreak, favGroundTieBreak, dogRightLeftTieBreak,\
                       favRightLeftTieBreak, dogGroundHold, favGroundHold, dogRightLeftHold, favRightLeftHold, dogGroundBreak, favGroundBreak, dogRightLeftBreak,\
                       favRightLeftBreak, dogGroundAce, favGroundACE, dogRightLeftAce, favRightLeftAce, dogGroundDF, favGroundDF, dogRightLeftDF, favRightLeftDF,\
                        dogGround1st, favGround1st, dogRightLeft1st, favRightLeft1st, dogGround1stWon, favGround1stWon, dogRightLeft1stWon, favRightLeft1stWon, dogGround2nd, favGround2nd, dogRightLeft2nd, favRightLeft2nd, dogGroundService,\
                       favGroundService, dogRightLeftService, favRightLeftService, dogGroundReturn, favGroundReturn, dogRightLeftReturn, favRightLeftReturn,\
                       dogGroundTPW, favGroundTPW, dogRightLeftTPW, favRightLeftTPW, dogGroundDR, favGroundDR, dogRightLeftDR, favRightLeftDR, winner))
        sqlite_connection.commit()
        cursor.execute("DELETE FROM matches WHERE fav=? AND dog=?;",(fav,dog))
        sqlite_connection.commit()
        break
    cursor.close()
    sqlite_connection.close()

if __name__ == "__main__":
    getMatches()
    # updateMatches()