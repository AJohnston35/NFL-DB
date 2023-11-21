# Dropdown menu
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Connection to mysql
import mysql.connector
from sqlalchemy import create_engine

# Team logo
from functools import partial

# Headshot URLs
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Random number
import random

result_label = None
root = tk.Tk()

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

def TeamStats():
    while True:
        selection = input("Team Stats\n Click 'b' to go back or enter to continue: ")
        if selection == 'b':
            break
        else:
            season = input("Select a Season: ")

            week = input("Select a Week: ")

            home_team = input("Select a Team (Enter team abbreviation i.e. 'PIT'): ")

            away_team = input("Select an Opponent (Enter team abbreviation i.e. 'PIT'): ")

            over_under = input("Select O/U line: ")

            user_choices = {'season': season, 'week': week, 'franchise_id': home_team, 'opponent_team_pfr_franchise_code_id': away_team, 'over_under_value': over_under, }

            query = "SELECT * FROM team_data WHERE 1=1"

            for key, value in user_choices.items():
                if value != '':
                    query += f" AND {key} = '{value}'"

            cursor.execute(query)

            rows = cursor.fetchall()

            for i in range(0,len(rows)):
                print(f"Season {rows[i][0]}, Week {rows[i][1]}: {rows[i][2]} {rows[i][20]} - {rows[i][4]} {rows[i][29]}\n")
                print(f"{rows[i][2]} Offense - Pass Yds: {rows[i][68]}, Rush Yds: {rows[i][71]}, Pass TDs: {rows[i][67]}, Rush TDs: {rows[i][70]}, TOs: {rows[i][38]}, 1st Downs: {rows[i][30]}, 2pt Conversions: {rows[i][50]}, Time of Possession: {rows[i][10]}")
                print(f"{rows[i][2]} Defense - Sacks: {rows[i][76]}, Tackles: {rows[i][78]}, TFLs: {rows[i][79]}, INTs: {rows[i][81]}, INT TDs: {rows[i][82]}, FUM: {rows[i][41]}, FUM TDs: {rows[i][44]}")
                print(f"{rows[i][2]} Special Teams - FG Made: {rows[i][47]}, XP Made: {rows[i][49]}, Punt Total: {rows[i][59]}, Punt Return TDs: {rows[i][63]}, Punt Return Yds: {rows[i][64]}, Kick Return TDs: {rows[i][73]}, Kick Return Yds: {rows[i][74]}")
                print(f"{rows[i][4]} Offense - Pass Yds: {rows[i][107]}, Rush Yds: {rows[i][110]}, Pass TDs: {rows[i][39]}, Rush TDs: {rows[i][109]}, TOs: {rows[i][38]}, 1st Downs: {rows[i][30]}, 2pt Conversions: {rows[i][50]}, Time of Possessions: {rows[i][11]}")
                print(f"{rows[i][4]} Defense - Sacks: {rows[i][115]}, Tackles: {rows[i][117]}, TFLs: {rows[i][118]}, INTs: {rows[i][120]}, INT TDs: {rows[i][121]}")
                print(f"{rows[i][4]} Special Teams - FG Made: {rows[i][86]}, XP Made: {rows[i][88]}, Punt Total: {rows[i][98]}, Punt Return TDs: {rows[i][102]}, Punt Return Yds: {rows[i][103]}, Kick Return TDs: {rows[i][112]}, Kick Return Yds: {rows[i][113]}\n")

def Rosters():
        global result_label

        image_label = tk.Label(root)
        image_label.pack()

        season = input("Select a Season: ")
        season_options = []

        team = input("Select a Team (Enter team abbreviation i.e. 'PIT'): ")

        player = input("Select a Player: ")

        jerseyNumber = input("Select a Jersey Number: ")

        position = input("Select a Position: ")

        birthdate = input("Select a Birthdate (yyyy/mm/dd): ")

        college = input("Select a College: ")

        user_choices = {'season': season, 'team': team, 'jerseynumber': jerseyNumber, 'birthdate': birthdate, 'college': college, 'fullname': player, 'position': position}
        
        query = "SELECT * FROM Rosters WHERE 1=1"

        for key, value in user_choices.items():
            if value != '':
                query += f" AND {key} = '{value}'"

        cursor.execute(query)

        rows = cursor.fetchall()



        result_text = Text(root, wrap = "none")
        result_text.pack(fill="both", expand = True)
        result_text.delete("1.0", END)

        # Customize background
        result_text.tag_configure("bold", font = ("Helvetica", 12, "bold"))
        result_text.tag_configure("background", background = "lightgray")

        # Create a header for the results
        header = f"{'Season':<11} {'Team':<11} {'Position':<13} {'Jersey Number':<19} {'Full Name':<30} {'Height':<11} {'Weight':<12} {'College':<20}\n"
        result_text.insert(END, header, "bold background")

        # Create vertical scrollbar
        vsb = Scrollbar(root, orient = "horizontal", command=result_text.yview)
        vsb.pack(side="right", fill = "y")
        result_text.config(yscrollcommand=vsb.set)

        for i in range(0,len(rows)):
            current_result_text = f" {rows[i][0]}   {rows[i][1]}      {rows[i][2]}      #{rows[i][4]}          {rows[i][6]}      {rows[i][10]} in  {rows[i][11]} lbs  {rows[i][12]}\n\n"
            playerid = rows[i][14]
            HeadshotURL(playerid)
            result_text.insert(END, current_result_text)

        result_label.config(text = result_text)

def PlayerStats():
        global result_label
        
        season = input("Select a Season: ")

        week = input("Select a Week: ")

        team = input("Select a Team (Enter team abbreviation i.e. 'PIT'): ")

        player = input("Select a Player: ")

        position = input("Select a Position: ")

        playoff = input("Regular Season or Playoffs (REG or POST): ")

        user_choices = {'season': season, 'week': week, 'recent_team': team, 'season_type': playoff, 'player_display_name': player, 'position': position, }

        query = "SELECT * FROM NFL_player_stats WHERE 1=1"

        if position == 'K':
            query = "SELECT * FROM player_stats_kicking WHERE 1=1"
            user_choices = {'season': season, 'week': week, 'team': team, 'season_type': playoff, 'player_name': player}

        for key, value in user_choices.items():
            if value != '':
                query += f" AND {key} = '{value}'"

        cursor.execute(query)

        rows = cursor.fetchall()

        # Change output of text
        result_text = Text(root, wrap = "none")
        result_text.pack(fill="both", expand = True)
        result_text.delete("1.0", END)

        # Create vertical scrollbar
        vsb = Scrollbar(root, orient = "horizontal", command=result_text.yview)
        vsb.pack(side="right", fill = "y")
        result_text.config(yscrollcommand=vsb.set)

        for i in range(0,len(rows)):
            if rows[i][3] == 'QB':
                current_result_text = f"{rows[i][2]}, {rows[i][3]}, Team: {rows[i][5]}, Season: {rows[i][6]}, Week: {rows[i][7]}, Type: {rows[i][8]}, Comp: {rows[i][9]}, Att: {rows[i][10]}, Pass Yds: {rows[i][11]}, Pass TDs: {rows[i][12]}, INTs: {rows[i][13]}, Sacks Taken: {rows[i][14]}, Sack Yards: {rows[i][15]}, FUM: {rows[i][16]}, Pass Air Yds: {rows[i][18]}, Pass 1st Downs: {rows[i][20]}, EPA: {rows[i][21]}, 2pt Conv: {rows[i][22]}, Car: {rows[i][25]}, Rush Yds: {rows[i][26]}, Rush TDs: {rows[i][27]}, Fantasy Points PPR: {rows[i][50]}\n\n"
                result_text.insert(END, current_result_text)

            elif rows[i][3] == 'RB' or rows[i][3] == 'FB':
                current_result_text = f"{rows[i][2]}, {rows[i][3]}, Team: {rows[i][5]}, Season: {rows[i][6]}, Week: {rows[i][7]}, Type: {rows[i][8]}, Car: {rows[i][25]}, Rush Yds: {rows[i][26]}, Rush TDs: {rows[i][27]}, FUM: {rows[i][29]}, Rush 1st Downs: {rows[i][30]}, Rush EPA: {rows[i][31]}, Rush 2pt Conv: {rows[i][32]}\nRec: {rows[i][33]}, Targ: {rows[i][34]}, Rec Yds: {rows[i][35]}, Rec TDs: {rows[i][36]}, Rec 1st Downs: {rows[i][41]}, Rec EPA: {rows[i][42]}, Rec 2pt Conv: {rows[i][43]}, Targ Share: {rows[i][45]}, Special Teams TDs: {rows[i][48]}, Fantasy Points PPR: {rows[i][50]}\n\n"
                result_text.insert(END, current_result_text)

            elif rows[i][3] == 'WR' or rows[i][3] == 'TE':
                current_result_text = f"{rows[i][2]}, {rows[i][3]}, Team: {rows[i][5]}, Season: {rows[i][6]}, Week: {rows[i][7]}, Type: {rows[i][8]}, Rec: {rows[i][33]}, Targ: {rows[i][34]}, Rec Yds: {rows[i][35]}, Rec TDs: {rows[i][36]}, Rec 1st Downs: {rows[i][41]}, Rec EPA: {rows[i][42]}, Rec 2pt Conv: {rows[i][43]}, Targ Share: {rows[i][45]}\nCar: {rows[i][25]}, Rush Yds: {rows[i][26]}, Rush TDs: {rows[i][27]}, FUM: {rows[i][29]}, Rush 1st Downs: {rows[i][30]}, Rush EPA: {rows[i][31]}, Rush 2pt Conv: {rows[i][32]}, Special Teams TDs: {rows[i][48]}, Fantasy Points PPR: {rows[i][50]}\n\n"
                result_text.insert(END, current_result_text)

            elif position == 'K':
                current_result_text = f"{rows[i][4]}, K, Team: {rows[i][3]}, Season: {rows[i][0]}, Week: {rows[i][1]}, Type: {rows[i][2]}, FG Made: {rows[i][6]}, FG Missed: {rows[i][7]}, FG Blocked: {rows[i][8]}, Long: {rows[i][9]}, PAT Made: {rows[i][12]}, PAT Missed: {rows[i][13]}, PAT Blocked: {rows[i][14]}, Game Winning FGs: {rows[i][22]}\n\n"
                result_text.insert(END, current_result_text)

            else:
                current_result_text = f"{rows[i][2]}, {rows[i][3]}, Team: {rows[i][5]}, Season: {rows[i][6]}, Week: {rows[i][7]}, Type: {rows[i][8]}, Receptions: {rows[i][33]}, Targets: {rows[i][34]}, Receiving Yards: {rows[i][35]}, Receiving TDs: {rows[i][36]}, Receiving First Downs: {rows[i][41]}, Receiving EPA: {rows[i][42]}, Receiving 2pt Conversions: {rows[i][43]}, Target Share: {rows[i][45]}, Special Teams TDs: {rows[i][48]}, Fantasy Points PPR: {rows[i][50]}\n\n"
                result_text.insert(END, current_result_text)


        result_label.config(text = result_text)

def AdvancedStats():
    while True:
        selection = input("Advanced Stats\n Click 'b' to go back or enter to continue: ")
        if selection == 'b':
            break
        else:
            advStats = input("\nMenu\n (1) Defensive\n (2) Passing\n (3) Rushing\n (4) Receiving\n")
            if advStats == '1':
                player = input("Select a Player: ")

                position = input("Select a Position: ")

                year = input("Select a Year: ")

                team = input("Select a Team: ")

                user_choices = {'season': year, 'player_name': player, 'tm': team, 'pos': position}

                query = "SELECT * FROM advstats_season_def WHERE 1=1"

                for key, value in user_choices.items():

                    if value != '':
                        query += f" AND {key} = '{value}'"

                cursor.execute(query)

                column_names = [column[0] for column in cursor.description]

                # Fetch all rows
                rows = cursor.fetchall()

                # Print column values for each row
                for row in rows:
                    for column, value in zip(column_names[:-1], row[:-1]):
                        print(f"{column}: {value}")
                    print()

            elif advStats == '2':
                player = input("Select a Player: ")

                year = input("Select a Year: ")

                team = input("Select a Team: ")

                user_choices = {'season': year, 'player_name': player, 'team': team}

                query = "SELECT * FROM advstats_season_pass WHERE 1=1"

                for key, value in user_choices.items():

                    if value != '':
                        query += f" AND {key} = '{value}'"

                cursor.execute(query)

                column_names = [column[0] for column in cursor.description]

                # Fetch all rows
                rows = cursor.fetchall()

                # Print the column names
                for row in rows:
                    for column, value in zip(column_names[:-1], row[:-1]):
                        print(f"{column}: {value}")
                    print()

            elif advStats == '3':
                player = input("Select a Player: ")

                year = input("Select a Year: ")

                team = input("Select a Team: ")

                user_choices = {'season': year, 'player_name': player, 'tm': team}

                query = "SELECT * FROM advstats_season_rush WHERE 1=1"

                for key, value in user_choices.items():

                    if value != '':
                        query += f" AND {key} = '{value}'"

                cursor.execute(query)

                column_names = [column[0] for column in cursor.description]

                # Print column names
                print('\t '.join(column_names))

                # Fetch all rows
                rows = cursor.fetchall()

                # Print column values for each row
                for row in rows:
                    values = [str(value) for value in row]
                    print('\t'.join(values))

            elif advStats == '4':
                player = input("Select a Player: ")

                position = input("Select a Position: ")

                year = input("Select a Year: ")

                team = input("Select a Team: ")

                user_choices = {'season': year, 'player_name': player, 'tm': team, 'pos': position}

                query = "SELECT * FROM advstats_season_rec WHERE 1=1"

                for key, value in user_choices.items():

                    if value != '':
                        query += f" AND {key} = '{value}'"

                cursor.execute(query)

                column_names = [column[0] for column in cursor.description]

                # Print column names
                print('\t'.join(column_names))

                # Fetch all rows
                rows = cursor.fetchall()

                # Print column values for each row
                for row in rows:
                    values = [str(value) for value in row]
                    print('\t'.join(values))
            
            else:
                print("Invalid selection. Try again.")

def InjuryHistory():
    while True:
        selection = input("Injury History\n Click 'b' to go back or enter to continue: ")
        if selection == 'b':
            break
        else:
            player = input("Select a Player: ")

            position = input("Select a Position: ")

            season = input("Select a Season: ")

            type = input("Select a Type of Injury: ")

            team = input("Select a Team: ")

            user_choices = {'player': player, 'position': position, 'season': season, 'full_name': player, 'team': team, 'report_primary_injury': type}

            query = "SELECT * FROM Injuries WHERE 1=1"

            for key, value in user_choices.items():

                if value != '':
                    query += f" AND {key} = '{value}'"

            cursor.execute(query)

            column_names = [column[0] for column in cursor.description]



            # Fetch all rows
            rows = cursor.fetchall()

            # Print column values for each row
            # Print the column names
            for row in rows:
                for column, value in zip(column_names[:-1], row[:-1]):
                    print(f"{column}: {value}")
                print()

def OffSeasonInfo():
    while True:
        selection = input("Off-Season Information\n Click 'b' to go back or enter to continue: ")
        if selection == 'b':
            break
        else:
            draftChoice = input("\nMenu\n (1) Draft Results\n (2) Combine Results\n")
            if draftChoice == '1':
                year = input("Select a Year: ")

                round = input("Select a Round: ")

                pick = input("Select a Pick: ")

                team = input("Select a Team (Enter team abbreviation i.e. 'PIT' or Enter to skip): ")

                player = input("Select a Player: ")

                position = input("Select a Position: ")

                college = input("Select a College: ")

                side = input("Select a Side (O/D): ")

                user_choices = {'season': year, 'round': round, 'pick': pick, 'team': team, 'pfr_player_name': player, 'position': position, 'college': college, 'side': side}

                query = "SELECT * FROM draft_picks WHERE 1=1"

                for key, value in user_choices.items():

                    if value != '':
                        query += f" AND {key} = '{value}'"

                cursor.execute(query)

                rows = cursor.fetchall()

                for i in range(0,len(rows)):
                    if rows[i][11] == 'O' and rows[i][9] == 'QB':
                        print(f"{rows[i][7]}, {rows[i][3]}: {rows[i][0]}->{rows[i][14]}, Round: {rows[i][1]}, Pick: {rows[i][2]}, Position: {rows[i][9]}, School: {rows[i][12]}\nCareer Stats - Completions: {rows[i][22]}, Attempts: {rows[i][23]}, Passing Yards: {rows[i][24]}, Passing TDs: {rows[i][25]}, Ints: {rows[i][26]}, Rushing Attempts: {rows[i][27]}, Rushing Yards: {rows[i][28]}, Rushing TDs: {rows[i][29]}\nAccolades - All-Pros: {rows[i][15]}, Pro-Bowls: {rows[i][16]}, Seasons Started: {rows[i][17]}, Games: {rows[i][21]}\n")
                    elif rows[i][11] == 'O' and rows[i][9] == 'RB':
                        print(f"{rows[i][7]}, {rows[i][3]}: {rows[i][0]}->{rows[i][14]}, Round: {rows[i][1]}, Pick: {rows[i][2]}, Position: {rows[i][9]}, School: {rows[i][12]}\nCareer Stats - Rushing Attempts: {rows[i][27]}, Rushing Yards: {rows[i][28]}, Rushing TDs: {rows[i][29]}, Receptions: {rows[i][30]}, Receiving Yards: {rows[i][31]}, Receiving TDs: {rows[i][32]}\nAccolades - All-Pros: {rows[i][15]}, Pro-Bowls: {rows[i][16]}, Seasons Started: {rows[i][17]}, Games: {rows[i][21]}\n")
                    elif rows[i][11] == 'O' and rows[i][9] == 'WR' or rows[i][9] == 'TE':
                        print(f"{rows[i][7]}, {rows[i][3]}: {rows[i][0]}->{rows[i][14]}, Round: {rows[i][1]}, Pick: {rows[i][2]}, Position: {rows[i][9]}, School: {rows[i][12]}\nCareer Stats - Receptions: {rows[i][30]}, Receiving Yards: {rows[i][31]}, Receiving TDs: {rows[i][32]}, Rushing Attempts: {rows[i][27]}, Rushing Yards: {rows[i][28]}, Rushing TDs: {rows[i][29]}\nAccolades - All-Pros: {rows[i][15]}, Pro-Bowls: {rows[i][16]}, Seasons Started: {rows[i][17]}, Games: {rows[i][21]}\n")
                    elif rows[i][11] == 'D':
                        print(f"{rows[i][7]}, {rows[i][3]}: {rows[i][0]}->{rows[i][14]}, Round: {rows[i][1]}, Pick: {rows[i][2]}, Position: {rows[i][9]}, School: {rows[i][12]}\nCareer Stats - Solo Tackles: {rows[i][33]}, Interceptions: {rows[i][34]}, Sacks: {rows[i][35]}\nAccolades - All-Pros: {rows[i][15]}, Pro-Bowls: {rows[i][16]}, Seasons Started: {rows[i][17]}, Games: {rows[i][21]}\n")
                    else:
                        print(f"{rows[i][7]}, {rows[i][3]}: {rows[i][0]}->{rows[i][14]}, Round: {rows[i][1]}, Pick: {rows[i][2]}, Position: {rows[i][9]}, School: {rows[i][12]}\nAccolades - All-Pros: {rows[i][15]}, Pro-Bowls: {rows[i][16]}, Seasons Started: {rows[i][17]}, Games: {rows[i][21]}\n")

            elif draftChoice == '2':
                    year = input("Select a Year: ")

                    player = input("Select a Player: ")

                    position = input("Select a Position: ")

                    draft_team = input("Select a Draft Team (Enter full team name i.e. 'Pittsburgh Steelers'): ")

                    round = input("Select a Round: ")

                    pick = input("Select a Pick: ")

                    school = input("Select a College: ")

                    height = input("Select a Height (Feet-Inches format): ")

                    weight = input("Select a Weight: ")

                    moreoptions = input("More Options (y or n): ")

                    if moreoptions == 'y':

                        forty = input("Forty Time: ")

                        vertical = input("Vertical in Inches: ")

                        bench = input("Bench Reps: ")

                        broad_jump = input("Broad Jump in Inches: ")

                        cone = input("Cone Time: ")

                        shuttle = input("Shuttle Time: ")

                        user_choices = {'season': year, 'player_name': player, 'pos': position, 'draft_team': draft_team, 'draft_round': round, 'draft_ovr': pick, 'school': school, 'ht': height, 'wt': weight, 'forty': forty, 'vertical': vertical, 'bench': bench, 'broad_jump': broad_jump, 'cone': cone, 'shuttle': shuttle}

                        query = "SELECT * FROM combine WHERE 1=1"

                        for key, value in user_choices.items():
                            if forty != '':
                                query += f" AND {key} < '{value}'"
                            if value != '':
                                query += f" AND {key} = '{value}'"
                    else:
                        user_choices = {'season': year, 'player_name': player, 'pos': position, 'draft_team': draft_team, 'draft_round': round, 'draft_ovr': pick, 'school': school, 'ht': height, 'wt': weight}

                        query = "SELECT * FROM combine WHERE 1=1"

                        for key, value in user_choices.items():

                            if value != '':
                                query += f" AND {key} = '{value}'"

                    cursor.execute(query)

                    rows = cursor.fetchall()

                    for i in range(0,len(rows)):
                        print(f"{rows[i][7]} - {rows[i][2]} - {rows[i][0]} - Round: {rows[i][3]}, Pick: {rows[i][4]}, Position: {rows[i][8]}, School: {rows[i][9]}, Height: {rows[i][10]}, Weight: {rows[i][11]}\nForty: {rows[i][12]}, Bench: {rows[i][13]}, Vertical: {rows[i][14]}, Broad Jump: {rows[i][15]}, Cone: {rows[i][16]}, Shuttle: {rows[i][17]}\n")

            else:
                print("Invalid selection. Try again.")

def HeadshotURL(playerid, image_label):
    url = "https://a.espncdn.com/i/headshots/nfl/players/full/"
    player = str(playerid) + ".png"
    url += player

    # Fetch image data
    response = requests.get(url)
    if response.status_code == 200:
        # Convert the image data to a PIL Image object
        img = Image.open(BytesIO(response.content))
        img = img.resize((175,160))

        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

    else:
        print("Failed to fetch player headshot")

def load_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    return photo

def search_player():
    search_window = tk.Toplevel(root)
    search_window.title("Search Player")

    search_entry = tk.Entry(search_window)
    search_entry.pack()

    player_name = search_entry.get()
    result_label.config(text=f"Searching for player: {player_name}")

def player_screen():
    print("Player screen")

def search_team():
    search_entry = tk.Entry(root)
    search_entry.pack()

    team_name = search_entry.get()
    result_label.config(text=f"Searching for team: {team_name}")

def TeamScreen():
    print("TeamScreen")

def RandomPlayer():
    query = "SELECT fullname, espnid FROM Rosters ORDER BY RAND() LIMIT 1"
    cursor.execute(query)
    headshot = cursor.fetchall()
    print(headshot)
    return headshot[0][0], headshot[0][1]

def RandomTeam():
    print("RandomTeam")

def main():

    # Adjust size and lock it
    root.geometry("600x800")
    root.resizable(False,False)

    # Create title for dropdown menu 
    root.title("NFL Database")

    # Change the background 
    background = PhotoImage(file='Header.png', master=root)
    background_label = Label(root, image = background)
    background_label.place(x=0,y=0)

    # Create a Frame for team search
    team_frame = tk.Frame(root, bg = 'red')
    team_frame.place(x= 100, y= 200, height = 100, width = 150)

    # Create a Frame to display images
    image_frame = tk.Frame(root)
    image_frame.place(x=300, y= 100, height = 250, width = 250)

    # Create a frame for Search Player
    search_player_frame = tk.Frame(root)
    search_player_frame.place(x=100, y=112, height = 100, width = 150) 

    # Create a search box for Search Player
    search_player_entry = tk.Entry(search_player_frame, fg = "black")
    search_player_entry.place(height = 26, width=150)

    # Create a search button for Search Player
    search_player_button = tk.Button(search_player_frame, text="Search Player", command=search_player)
    search_player_button.place(y=38,height = 50, width=150)

    # Create a dropdown menu for selecting teams
    team_var = tk.StringVar()

    team_logos = {
        "Arizona Cardinals": tk.PhotoImage(file="TeamLogos/thumbs_arizona-cardinals-logo-present Background Removed.png"),
        "Atlanta Falcons": tk.PhotoImage(file="TeamLogos/thumbs_atlanta-falcons-logo-present Background Removed.png"),
        "Baltimore Ravens": tk.PhotoImage(file="TeamLogos/thumbs_baltimore-ravens-logo-present Background Removed.png"),
        "Buffalo Bills": tk.PhotoImage(file="TeamLogos/thumbs_buffalo-bills-logo-present Background Removed.png"),
        "Carolina Panthers": tk.PhotoImage(file="TeamLogos/thumbs_carolina-panthers-logo-present Background Removed.png"),
        "Chicago Bears": tk.PhotoImage(file="TeamLogos/thumbs_chicago-bears-logo-present Background Removed.png"),
        "Cincinnati Bengals": tk.PhotoImage(file="TeamLogos/thumbs_cincinnati-bengals-logo-present Background Removed.png"),
        "Cleveland Browns": tk.PhotoImage(file="TeamLogos/thumbs_cleveland-browns-logo-present Background Removed.png"),
        "Dallas Cowboys": tk.PhotoImage(file="TeamLogos/thumbs_dallas-cowboys-logo-present Background Removed.png"),
        "Denver Broncos": tk.PhotoImage(file="TeamLogos/thumbs_denver-broncos-logo-present Background Removed.png"),
        "Detroit Lions": tk.PhotoImage(file="TeamLogos/thumbs_detroit-lions-logo-present Background Removed.png"),
        "Green Bay Packers": tk.PhotoImage(file="TeamLogos/thumbs_green-bay-packers-logo-present Background Removed.png"),
        "Houston Texans": tk.PhotoImage(file="TeamLogos/thumbs_houston-texans-logo-present Background Removed.png"),
        "Indianapolis Colts": tk.PhotoImage(file="TeamLogos/thumbs_indianapolis-colts-logo-present Background Removed.png"),
        "Jacksonville Jaguars": tk.PhotoImage(file="TeamLogos/thumbs_jacksonville-jaguars-logo-present Background Removed.png"),
        "Kansas City Chiefs": tk.PhotoImage(file="TeamLogos/thumbs_kansas-city-chiefs-logo-present Background Removed.png"),
        "Las Vegas Raiders": tk.PhotoImage(file="TeamLogos/thumbs_oakland-raiders-logo-present Background Removed.png"),
        "Los Angeles Chargers": tk.PhotoImage(file="TeamLogos/thumbs_san-diego-chargers-logo-present Background Removed.png"),
        "Los Angeles Rams": tk.PhotoImage(file="TeamLogos/thumbs_st-louis-rams-logo-present Background Removed.png"),
        "Miami Dolphins": tk.PhotoImage(file="TeamLogos/thumbs_miami-dolphins-logo-present Background Removed.png"),
        "Minnesota Vikings": tk.PhotoImage(file="TeamLogos/thumbs_minnesota-vikings-logo-present Background Removed.png"),
        "New England Patriots": tk.PhotoImage(file="TeamLogos/thumbs_new-england-patriots-logo-present Background Removed.png"),
        "New Orleans Saints": tk.PhotoImage(file="TeamLogos/thumbs_new-orleans-saints-logo-present Background Removed.png"),
        "New York Giants": tk.PhotoImage(file="TeamLogos/thumbs_new-york-giants-logo-present Background Removed.png"),
        "New York Jets": tk.PhotoImage(file="TeamLogos/thumbs_new-york-jets-logo-present Background Removed.png"),
        "Philadelphia Eagles": tk.PhotoImage(file="TeamLogos/thumbs_philadelphia-eagles-logo-present Background Removed.png"),
        "Pittsburgh Steelers": tk.PhotoImage(file="TeamLogos/thumbs_pittsburgh-steelers-logo Background Removed.png"),
        "San Francisco 49ers": tk.PhotoImage(file="TeamLogos/thumbs_san-francsico-49ers-logo-peresent Background Removed.png"),
        "Seattle Seahawks": tk.PhotoImage(file="TeamLogos/thumbs_seattle-seahawks-logo-present Background Removed.png"),
        "Tampa Bay Buccaneers": tk.PhotoImage(file="TeamLogos/thumbs_tampa-bay-buccaneers-logo-present Background Removed.png"),
        "Tennessee Titans": tk.PhotoImage(file="TeamLogos/thumbs_tennese-titans-logo-present Background Removed.png"),
        "Washington Commanders": tk.PhotoImage(file="TeamLogos/thumbs_Washington-Commanders-Logo 2 Background Removed.png")
    }

    def team_selected(*args):
        selected_team = team_var.get()
        selected_team_label.config(image=team_logos.get(selected_team, None))

    team_dropdown = tk.OptionMenu(team_frame, team_var, *list(team_logos.keys()))
    team_dropdown.place(height = 50, width=150)

    selected_team_label = tk.Label(image_frame, image=None)
    selected_team_label.place(width = 250, height = 250)

    # Bind a callback to the <Enter> event to show the logo
    def enter_event(event):
        selected_team = team_var.get()
        selected_team_label.config(image=team_logos.get(selected_team, None))

    team_dropdown.bind("<Enter>", enter_event)

    # Create a search button for Search Team
    search_team_button = tk.Button(team_frame, text="Search Team", command=search_team)
    search_team_button.place(y=50, width = 150, height=50)

    # Create a frame for Random Player
    random_player_frame = tk.Label(root, bg="lightgray")
    random_player_frame.place(x = 100, y = 350, width = 150, height = 175)
    returnvalues = RandomPlayer()
    playerid = returnvalues[1]
    playername = returnvalues[0]
    HeadshotURL(playerid, random_player_frame)
    random_player_button = tk.Button(random_player_frame, text = playername, command = search_player)
    random_player_button.place(x=-2,y = 150, width=150, height = 25)


    # Create a frame for Random Team
    random_team_frame = tk.Frame(root, bg = "lightgray")
    random_team_frame.place(x = 350, y = 350, width = 150, height = 175)
    teamindex = random.randint(0,32)
    teamnames = list(team_logos.keys())
    teamname = teamnames[teamindex]
    teamlogo = team_logos[teamnames[teamindex]]
    random_team_logo = tk.Label(random_team_frame, image = teamlogo)
    random_team_logo.place(width = 150, height = 150)
    random_team_button = tk.Button(random_team_frame, text = teamname, command = search_team)
    random_team_button.place(y = 150, width = 150, height = 25)

    # Create a frame for Combine Data
    combine_data_frame = tk.Frame(root, bg="blue")
    combine_data_frame.place(x = 100, y = 600, width = 150, height = 100)

    # Create a frame for Draft Data
    draft_data_frame = tk.Frame(root, bg="blue")
    draft_data_frame.place(x = 350, y = 600, width = 150, height = 100)

    # Execute tkinter
    root.mainloop()

if __name__ == "__main__":
    main()