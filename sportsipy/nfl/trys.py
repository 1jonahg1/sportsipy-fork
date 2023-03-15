from sportsipy.nfl.boxscore2 import Boxscore
from sportsipy.nfl.boxscore2 import Boxscores
from sportsipy.nfl.player import AbstractPlayer
from sportsipy.nfl.roster import Roster
from sportsipy.nfl.teams import Team
from sportsipy.nfl.schedule import Schedule
import time
import pandas as pd



"""
kan_roster = Roster('KAN')
print(kan_roster.players)
boxscore1 = Boxscore('202209150kan')
print(boxscore1.summary)
player1 = AbstractPlayer('HopkDu00', 'Dustin Hopkins','202209150kan')
print(player1.name)
try_team = Team('CHI')
print(try_team.rank)


df_list = pd.read_html("https://www.pro-football-reference.com")
print(df_list[0])

phili = Team("PHI")
if('*' == df_list[1]['Tm'][1][3]):
    print("hhh")


boxscore1 = Boxscore('202209150kan')
print(boxscore1.winning_abbr)

phili = Team("KAN")
def findConferences(team1):
        url = "https://www.pro-football-reference.com"
        teamOneConf = 'AFC'
        df_list = pd.read_html(url)
        for i in range(0,len(df_list[1]['Tm'])):
            if team1.abbreviation == df_list[1]['Tm'][i][0:3]:
                teamOneConf = 'NFC'
        print(teamOneConf)

findConferences(phili)


houston_schedule = Schedule('HTX')
for game in houston_schedule:
    print(game.date)  # Prints the date the game was played
    print(game.quarterback_rating)  # Prints whether the team won or lost
    # Creates an instance of the Boxscore class for the game.
    boxscore = game.boxscore
"""

boxscore1 = Boxscore('202209150kan')
print(boxscore1.away_time_of_possession)
print(boxscore1.home_time_of_possession)
print(int(boxscore1.away_time_of_possession[0:2]) + int(boxscore1.home_time_of_possession[0:2]))