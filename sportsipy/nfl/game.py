import datetime
import pandas as pd
from pyquery import PyQuery as pq
from lxml.etree import ParserError
import requests
import calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sportsipy.nfl.boxscore import Boxscore
from sportsipy.nfl.boxscore import Boxscores
from sportsipy.nfl.schedule import Schedule
from sportsipy.nfl.schedule import Game
from sportsipy.nfl.teams import Team

BOXSCORE_URL = 'https://www.pro-football-reference.com/boxscores/%s.htm'

class GameData:
    """
    class that colleects all the data from the game.
    this data includes the boxScore details, stats from the game and the players inside the game
    Furtermore, the game will add in the future additional information about the game and will calculate the 'Value' of the game according to the Parameters the game checks out.
    """

    def __init__(self, boxscoreString, game_data, game_type, year, team_name1, team_name2, team_data1, team_data2, rank1, rank2, season_page1, season_page2):
        self.boxscore = Boxscore(boxscoreString)
        self.game = Game(game_data, game_type, year)
        self.team1 = Team(team_name1, team_data1, rank1, year, season_page1)
        self.team2 = Team(team_name2, team_data2, rank2, year, season_page2)
        self.gameValue = None
        self.gameSummery = None
        self.homePoints = None
        self.awayPoints = None
        self.totalPoints = None
        self.thirdQuarterAway = None
        self.thirdQuarterHome = None
        self.diffThird = None
        self.diffPoints = None
        self.isOvertime = None
        self.lastMinWin = None
        self.counterChangeLead = None
        self.isTeamOneWinning = None
        self.isTeamTwoWinning = None

        self.setGameValue(boxscoreString)

    

    def calGameScores(self, boxscoreString):
        url = BOXSCORE_URL % boxscoreString
        lastMinWin = False
        counterLeadChanges = 0 
        lastScoreWin = 0
        lastScoreLose = 0
        winningTeam = self.boxscore.winning_abbr
        losingTeam = self.boxscore.losing_abbr
        df_list = pd.read_html(url)
        quarter = 'nan'
        for i in range(0,len(df_list[1]['Quarter'])):
            diffBefore = lastScoreWin - lastScoreLose 
            diffNow = int(df_list[1][winningTeam][i]) - int(df_list[1][losingTeam][i])
            if(diffBefore < 0 and diffNow >= 0) or (diffBefore > 0 and diffNow <= 0):
                counterLeadChanges+= 1
            if(str(df_list[1]['Quarter'][i]) != 'nan'):
                quarter = str(df_list[1]['Quarter'][i])
            timePlay = str(df_list[1]['Time'][i])
            if(quarter == "4.0" and  (int(timePlay[0]) < 3) and timePlay[1] == ':'):
                if(lastScoreWin - lastScoreLose < 0) and (int(df_list[1][winningTeam][i]) - int(df_list[1][losingTeam][i]) > 0):
                    lastMinScore = True
            lastScoreLose = int(df_list[1][losingTeam][i])
            lastScoreWin = int(df_list[1][winningTeam][i])    
        return lastMinScore, counterLeadChanges


    def setGameValue(self, boxscoreString):
        """
        Calculates the value of the game according to the algorithem.
        """
        counterValue = 0.0
        self.gameSummary = self.boxscore.summary
        self.homePoints = self.boxscore.home_points
        self.awayPoints = self.boxscore.away_points
        self.totalPoints = self.homePoints + self.awayPoints
        self.thirdQuarterAway = sum(self.gameSummary['away'][:3])
        self.thirdQuarterHome = sum(self.gameSummary['home'][:3])
        self.diffThird = abs(self.thirdQuarterHome - self.thirdQuarterAway)
        self.diffPoints = abs(self.homePoints - self.awayPoints)
        self.isOvertime = self.game.overtime
        self.lastMinWin, self.counterChangeLead = self.calGameScores(boxscoreString)
        self.isTeamOneWinning = (self.team1.wins / (self.team1.losses + self.team1.wins) >= 0.65)
        self.isTeamTwoWinning = (self.team2.wins / (self.team2.losses + self.team2.wins) >= 0.65)


        "first parameter"
        if (self.totalPoints / self.diffPoints) <= 6:
            counterValue += 2
        
        "second parameter"
        if(self.diffThird <= 6):
            counterValue += 1

        "third parameter"
        if self.isOvertime:
            counterValue += 2

        "forth parameter"
        if self.lastMinWin:
            counterValue += 3

        "fifth parameter"
        counterValue += self.counterChangeLead / 2

        "sixth parameter"
        #can be canged to win_percentage parameter
        if ((self.isTeamOneWinning or (self.team1.rank <= 10)) and (self.isTeamTwoWinning or (self.team2.rank <= 10))):
            counterValue += 3

        "seventh parameter"
        

        

        
        
