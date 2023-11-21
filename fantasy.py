import mysql.connector
from sleeper_wrapper import User
from sleeper_wrapper import League
from sqlalchemy import create_engine
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np

# Connect to MySQL
cnxn_str = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="NFLStats",
    user="root",
    password="mnmsstar15"
)

host="localhost"
port=3306
database="NFLStats"
user="root"
password="mnmsstar15"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

cursor = cnxn_str.cursor()

def process_data(chunk):
    selected_xvalues = []
    selected_yvalues = []
    # Data processing logic goes here
    for i in range(len(chunk)):
        xvalue1 = get_team_value(chunk[i][5])  # Team 
        xvalue2 = int(chunk[i][11]) # Passing Yards
        xvalue3 = int(chunk[i][12]) # Passing TDs
        xvalue4 = int(chunk[i][13]) # Interceptions
        xvalue5 = int(chunk[i][22]) # Passing 2pt Conversions
        xvalue6 = int(chunk[i][26]) # Rushing Yards
        xvalue7 = int(chunk[i][27]) # Rushing TDs
        xvalue8 = int(chunk[i][28]) # Fumbles
        xvalue14 = int(chunk[i][9]) # Completions
        xvalue15 = int(chunk[i][10]) # Attempts
        xvalue16 = int(chunk[i][18]) # Passing air yards
        xvalue17 = int(chunk[i][19]) # Passing yards after catch
        xvalue18 = int(chunk[i][20]) # Passing first downs
        xvalue19 = int(chunk[i][25]) # Carries
        xvalue20 = int(chunk[i][30]) # Rushing first downs
        xvalue21 = int(chunk[i][32]) # Rushing 2pt conversions
        xvalue22 = float(chunk[i][49]) # Fantasy points

        
        try:
            cursor.execute(f"SELECT * FROM team_data WHERE season = '{chunk[i][6]}' and week = '{chunk[i][7]}' and franchise_id = '{chunk[i][5]}'")
            team = cursor.fetchall()

            if team:
                xvalue9 = get_team_value(team[0][4]) # Opponent Team 
            else:
                # Handle the case when the team list is empty
                xvalue9 = 0

            xvalue11 = 0 # Number of injuries

            cursor.execute("SELECT * FROM Injuries WHERE full_name = %s AND season = %s", (chunk[i][2], chunk[i][6]))
            injury = cursor.fetchall()

            for i in range(len(injury)):
                xvalue11 = xvalue11 + 1

            cursor.execute(f"SELECT * FROM Combined_Offensive_Line_Stats WHERE Team = '{chunk[i][5]}' and Season = '{chunk[i][6]}'")
            oline = cursor.fetchall()
            if oline:
                xvalue12 = int(oline[0][1]) # O-Line Rank
            else:
                xvalue12 = 16


            cursor.execute("SELECT * FROM snap_counts WHERE player = %s and season = %s and week = %s",(chunk[i][2],chunk[i][6],chunk[i][7]))
            snaps = cursor.fetchall()
            if snaps:
                xvalue13 = float(snaps[0][10] * 100) # Snap percentage
            else:
                xvalue13 = 50


            #####################################
            #####################################
            #####################################
            #####################################
            #####################################
            yvalue1 = xvalue2 # Passing yards
            yvalue2 = xvalue3 # Passing TDs
            yvalue3 = xvalue4 # INTs
            yvalue4 = xvalue6 # Rush yards
            yvalue5 = xvalue7 # Rush TDs
            yvalue6 = xvalue8 # Fumbles
            

            selected_xvalues.append([xvalue1,xvalue2,xvalue3,xvalue4,xvalue5,xvalue6,xvalue7,xvalue8,xvalue9,xvalue11,xvalue12,xvalue13, xvalue14, xvalue15, xvalue16, xvalue17, xvalue18, xvalue19, xvalue20, xvalue21, xvalue22])
            selected_yvalues.append([yvalue1,yvalue2,yvalue3,yvalue4,yvalue5,yvalue6])

            print(f"{chunk[i][2]}")
            print(f"Team: {chunk[i][5]}")
            print(f"Passing Yards: {chunk[i][11]}")
            print(f"TDs: {chunk[i][12]}")
            print(f"INTs: {chunk[i][13]}")
            print(f"2pt: {chunk[i][22]}")
            print(f"Rush Yards: {chunk[i][26]}")
            print(f"Rush TDs: {chunk[i][27]}")
            print(f"Fumbles: {chunk[i][28]}")
            print(f"Comp: {chunk[i][9]}")
            print(f"Att: {chunk[i][10]}")
            print(f"Passing Air Yards: {chunk[i][18]}")
            print(f"Pass YAC: {chunk[i][19]}")
            print(f"Pass First Downs: {chunk[i][20]}")
            print(f"Carries: {chunk[i][25]}")
            print(f"Rush First Downs: {chunk[i][30]}")
            print(f"Rush 2pt: {chunk[i][32]}")
            print(f"Fantasy points: {chunk[i][49]}")
            print(f"Opponent: {xvalue9}")
            print(f"Injuries: {xvalue11}")
            print(f"O-Line: {xvalue12}")
            print(f"Snap Percentage: {xvalue13}")
            # cursor.execute("INSERT INTO qb_prediction_model (team, pass_yards, pass_tds, ints, two_pt_conv, rush_yards, rush_tds, fumbles, opp_team, num_injuries, o_line, snap_pct) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(xvalue1,xvalue2,xvalue3,xvalue4,xvalue5,xvalue6,xvalue7,xvalue8,xvalue9,xvalue11,xvalue12,xvalue13))

        finally:
            # Release the lock to allow other threads to acquire it
            lock.release()

    return selected_xvalues, selected_yvalues

def PlayerPredictions():
    player = input("Select a player: ")
    cached_model = load_cached_model()
    cached_model

    if cached_model is None:
        # Cached model doesn't exist, train a new model
        train_model(player)
        cached_model = load_cached_model()
    
    for i in range(18):
        xtest = x_test(player,i)
        # print(xtest)
        prediction = cached_model.predict(xtest)
        print(prediction.astype(int))
        print(f"Passing Yards: {prediction[0][0]}")
        print(f"Passing Touchdowns: {prediction[0][1]}")
        print(f"Interceptions: {prediction[0][2]}")
        print(f"Rushing Yards: {prediction[0][3]}")
        print(f"Rushing Touchdowns: {prediction[0][4]}")
        print(f"Fumbles: {prediction[0][5]}")
    
import os

def load_cached_model():
    file_path = 'qb_cached_model.h5'
    if os.path.exists(file_path):
        model = load_model(file_path)
        return model
    else:
        return None

def train_model(player):
    cursor.execute(f"SELECT * FROM NFL_player_stats WHERE player_display_name = '{player}'")

    rows = cursor.fetchall()

    selected_xvalues = []

    selected_yvalues = []

    if rows[0][3] == 'QB':
        cursor.execute("SELECT * FROM NFL_player_stats WHERE position = 'QB'")

        rows = cursor.fetchall()

        num_threads = 8
        chunk_size = len(rows) // num_threads
        data_chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_data, data_chunks)

        for result in results:
            selected_xvalues.extend(result[0])
            selected_yvalues.extend(result[1])
            
        x_train = np.array(selected_xvalues)
        y_train = np.array(selected_yvalues)

        model = Sequential()
        model.add(Dense(32,activation='relu',input_shape=(21,)))
        model.add(Dense(16,activation='relu'))
        model.add(Dense(6))

        model.compile(optimizer='adam', loss='mean_squared_error')

        model.fit(x_train, y_train, epochs = 8, batch_size= 128)
        
        model.save('qb_cached_model.h5')

    elif rows[0][3] == 'WR':
        cursor.execute("SELECT * FROM NFL_player_stats WHERE position = 'WR'")

        rows = cursor.fetchall()

        for i in len(rows):
            value1 = rows[i][0]
            value2 = rows[i][1]
            value3 = rows[i][2]

            selected_xvalues.append([value1,value2,value3])
        
        x_train = np.array(selected_xvalues)

    elif rows[0][3] == 'TE':
        cursor.execute("SELECT * FROM NFL_player_stats WHERE position = 'TE'")

        rows = cursor.fetchall()

        for i in len(rows):
            value1 = rows[i][0]
            value2 = rows[i][1]
            value3 = rows[i][2]

            selected_xvalues.append([value1,value2,value3])
        
        x_train = np.array(selected_xvalues)

    elif rows[0][3] == 'RB':
        cursor.execute("SELECT * FROM NFL_players_stat WHERE position = 'RB'")

        rows = cursor.fetchall()

        for i in len(rows):
            value1 = rows[i][0]
            value2 = rows[i][1]
            value3 = rows[i][2]

            selected_xvalues.append([value1,value2,value3])
        
        x_train = np.array(selected_xvalues)

def get_team_value(team):
    if team == 'ARI':
        return 1
    elif team == 'ATL':
        return 2
    elif team == 'BAL':
        return 3
    elif team == 'BUF':
        return 4
    elif team == 'CAR':
        return 5
    elif team == 'CHI':
        return 6
    elif team == 'CIN':
        return 7
    elif team == 'CLE':
        return 8
    elif team == 'DAL':
        return 9
    elif team == 'DEN':
        return 10
    elif team == 'DET':
        return 11
    elif team == 'GB':
        return 12
    elif team == 'HOU':
        return 13
    elif team == 'IND':
        return 14
    elif team == 'JAX':
        return 15
    elif team == 'KC':
        return 16
    elif team == 'LAC':
        return 17
    elif team == 'LAR':
        return 18
    elif team == 'LV':
        return 19
    elif team == 'MIA':
        return 20
    elif team == 'MIN':
        return 21
    elif team == 'NE':
        return 22
    elif team == 'NO':
        return 23
    elif team == 'NYG':
        return 24
    elif team == 'NYJ':
        return 25
    elif team == 'PHI':
        return 26
    elif team == 'PIT':
        return 27
    elif team == 'SF':
        return 28
    elif team == 'SEA':
        return 29
    elif team == 'TB':
        return 30
    elif team == 'TEN':
        return 31
    elif team == 'WSH':
        return 32
    else:
        return None

def SleeperConnection():
    user_id = input("Sleeper Username: ")
    user = User(user_id)
    season = int(input("Season: "))
    leagues = user.get_all_leagues("nfl", season)
    for i in range(0, len(leagues)):
        print(i, "-", leagues[i]['name'])
    league_selection = int(input("Select league from above: "))
    league_id = int(leagues[league_selection]['league_id'])
    league = League(league_id)
    users = league.get_users()
    for i in range (0,len(users)):
        print(users[i]['display_name'], "\n")

def SleeperRankings():
    print("Sleeper League Rankings\n ")

def Help():
    print("Help")

def x_test(player,week):
    cursor.execute(f"SELECT * FROM NFL_player_stats WHERE player_display_name = '{player}' and season = '2022'")

    rows = cursor.fetchall()
    print(rows[0][5])

    xtest = []

    yvalue1 = get_team_value(rows[0][5])  # Team

    num_games = 0

    yvalue2 = 0
    yvalue3 = 0
    yvalue4 = 0
    yvalue5 = 0
    yvalue6 = 0
    yvalue7 = 0
    yvalue8 = 0
    yvalue9 = 0
    yvalue11 = 0
    yvalue12 = 0
    yvalue13 = 0
    yvalue14 = 0
    yvalue15 = 0
    yvalue16 = 0
    yvalue17 = 0
    yvalue18 = 0
    yvalue19 = 0
    yvalue20 = 0
    yvalue21 = 0
    yvalue22 = 0
    """
    for i in range(len(rows)):
        num_games = num_games + 1
        yvalue2 = (rows[i][11] + yvalue2) # Passing Yards
        yvalue3 = (rows[i][12] + yvalue3) # Passing TDs
        yvalue4 = (rows[i][13] + yvalue4) # Interceptions
        yvalue5 = (rows[i][22] + yvalue5) # 2pt Conversions
        yvalue6 = (rows[i][26] + yvalue6) # Rushing Yards
        yvalue7 = (rows[i][27] + yvalue7) # Rushing TDs
        yvalue8 = (rows[i][28] + yvalue8) # Fumbles
        yvalue14 = (rows[i][9] + yvalue14) # Completions
        yvalue15 = (rows[i][10] + yvalue15) # Attempts
        yvalue16 = (rows[i][18] + yvalue16) # Passing air yards
        yvalue17 = (rows[i][19] + yvalue17) # Passing yards after catch
        yvalue18 = (rows[i][20] + yvalue18) # Passing first downs
        yvalue19 = (rows[i][25] + yvalue19) # Carries
        yvalue20 = (rows[i][30] + yvalue20) # Rushing first downs
        yvalue21 = (rows[i][32] + yvalue21) # Rushing 2pt conversions
        yvalue22 = (rows[i][49] + yvalue22) # Fantasy points
    
    yvalue2 = int(yvalue2/num_games) # Passing Yards
    yvalue3 = int(yvalue3/num_games) # Passing TDs
    yvalue4 = int(yvalue4/num_games) # Interceptions
    yvalue5 = int(yvalue5/num_games) # 2pt Conversions
    yvalue6 = int(yvalue6/num_games) # Rushing Yards
    yvalue7 = int(yvalue7/num_games) # Rushing TDs
    yvalue8 = int(yvalue8/num_games) # Fumbles
    yvalue14 = int(yvalue14/num_games) # Completions
    yvalue15 = int(yvalue15/num_games) # Attempts
    yvalue16 = int(yvalue16/num_games) # Passing air yards
    yvalue17 = int(yvalue17/num_games) # Passing yards after catch
    yvalue18 = int(yvalue18/num_games) # Passing first downs
    yvalue19 = int(yvalue19/num_games) # Carries
    yvalue20 = int(yvalue20/num_games) # Rushing first downs
    yvalue21 = int(yvalue21/num_games) # Rushing 2pt conversions
    yvalue22 = int(yvalue22/num_games) # Fantasy points

    week = week + 1
    cursor.execute(f"SELECT Week{week} FROM 2023_NFL_Schedule WHERE TEAM = '{rows[0][5]}'")
    team = cursor.fetchone()
    if team:
        matchup = team[0]
        print(f"Matchup for {rows[0][5]} in Week {week}: {matchup}")
    yvalue9 = get_team_value(team[0]) # Opponent Team 

    yvalue11 = 0 # Number of injuries

    cursor.execute(f"SELECT * FROM Injuries WHERE full_name = '{player}' and season = '2022'")
    injury = cursor.fetchall()

    for i in range(len(injury)):
        yvalue11 = yvalue11 + 1


    cursor.execute(f"SELECT * FROM Combined_Offensive_Line_Stats WHERE Team = '{rows[0][5]}' and Season = '2022'")
    oline = cursor.fetchall()

    yvalue12 = int(oline[0][1]) # O-Line Rank

    cursor.execute(f"SELECT * FROM snap_counts WHERE player = '{player}' and season = '2022'")
    snaps = cursor.fetchall()
    num_games = 0
    yvalue13 = 0

    for i in range(len(snaps)):
        num_games = num_games + 1
        yvalue13 = yvalue13 + snaps[0][10]
    yvalue13 = yvalue13/num_games # Snap percentage
    """
    xtest.append([yvalue1,yvalue2,yvalue3,yvalue4,yvalue5,yvalue6,yvalue7,yvalue8,yvalue9,yvalue11,yvalue12,yvalue13,yvalue14,yvalue15,yvalue16,yvalue17,yvalue18,yvalue19,yvalue20,yvalue21,yvalue22])
    # print(xtest)
    xtest = np.array(xtest)
    # print(xtest)
    xtest = xtest.astype('float32') 
    # print(xtest)
    return xtest

def GamePredictions():
    print("Select two teams\n")
    team1 = input("Team 1: ")
    team2 = input("Team 2: ")
