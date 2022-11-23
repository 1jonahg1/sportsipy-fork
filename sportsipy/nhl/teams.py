import pandas as pd
import re
from .constants import PARSING_SCHEME, SEASON_PAGE_URL
from ..decorators import float_property_decorator, int_property_decorator
from .. import utils
from .nhl_utils import _retrieve_all_teams
from .roster import Roster
from .schedule import Schedule


class Team:
    """
    An object containing all of a team's season information.

    Finds and parses all team stat information and identifiers, such as rank,
    name, and abbreviation, and sets them as properties which can be directly
    read from for easy reference.

    If calling directly, the team's abbreviation needs to be passed. Otherwise,
    the Teams class will handle all arguments.

    Parameters
    ----------
    team_name : string (optional)
        The name of the team to pull if being called directly.
    team_data : string (optional)
        A string containing all of the rows of stats for a given team. If
        multiple tables are being referenced, this will be comprised of
        multiple rows in a single string.  Is only used when called directly
        from the Teams class.
    rank : int (optional)
        A team's position in the league based on the number of points they
        obtained during the season.  Is only used when called directly from the
        Teams class.
    year : string (optional)
        The requested year to pull stats from. Is only used when called
        directly from the Teams class.
    season_page : string (optional)
        Optionally specify the filename of a local file to use to pull data
        instead of downloading from sports-reference.com. This file should be
        of the Season page for the designated year.
    """
    def __init__(self, team_name=None, team_data=None, rank=None, year=None,
                 season_page=None):
        self._year = year
        self._rank = rank
        self._abbreviation = None
        self._name = None
        self._average_age = None
        self._games_played = None
        self._wins = None
        self._losses = None
        self._overtime_losses = None
        self._points = None
        self._points_percentage = None
        self._goals_for = None
        self._goals_against = None
        self._simple_rating_system = None
        self._strength_of_schedule = None
        self._total_goals_per_game = None
        self._power_play_goals = None
        self._power_play_opportunities = None
        self._power_play_percentage = None
        self._power_play_goals_against = None
        self._power_play_opportunities_against = None
        self._penalty_killing_percentage = None
        self._short_handed_goals = None
        self._short_handed_goals_against = None
        self._shots_on_goal = None
        self._shooting_percentage = None
        self._shots_against = None
        self._save_percentage = None
        self._pdo_at_even_strength = None

        if team_name:
            team_data = self._retrieve_team_data(year, team_name, season_page)
        self._parse_team_data(team_data)

    def __str__(self):
        """
        Return the string representation of the class.
        """
        return f'{self.name} ({self.abbreviation}) - {self._year}'

    def __repr__(self):
        """
        Return the string representation of the class.
        """
        return self.__str__()

    def _retrieve_team_data(self, year, team_name, season_page):
        """
        Pull all stats for a specific team.

        By first retrieving a dictionary containing all information for all
        teams in the league, only select the desired team for a specific year
        and return only their relevant results.

        Parameters
        ----------
        year : string
            A ``string`` of the requested year to pull stats from.
        team_name : string
            A ``string`` of the team's 3-letter abbreviation, such as 'DET' for
            the Detroit Red Wings.
        season_page : string (optional)
            Optionally specify the filename of a local file to use to pull data
            instead of downloading from sports-reference.com. This file should
            be of the Season page for the designated year.
        """
        teams_list, year = _retrieve_all_teams(year, season_page)
        self._year = year
        # Teams are listed in terms of rank with the first team being #1
        team_data = teams_list[team_name]['data']
        self._rank = teams_list[team_name]['rank']
        return team_data
        # for team_data in teams_list:
        #     name = utils._parse_field(PARSING_SCHEME,
        #                               team_data,
        #                               'abbreviation')
        #     if name == team_name:
        #         self._rank = rank
        #         return team_data
        #     rank += 1

    def _parse_team_data(self, team_data):
        """
        Parses a value for every attribute.

        This function looks through every attribute with the exception of
        '_rank' and retrieves the value according to the parsing scheme and
        index of the attribute from the passed HTML data. Once the value is
        retrieved, the attribute's value is updated with the returned result.

        Note that this method is called directly once Team is invoked and does
        not need to be called manually.

        Parameters
        ----------
        team_data : string
            A string containing all of the rows of stats for a given team. If
            multiple tables are being referenced, this will be comprised of
            multiple rows in a single string.
        """
        for field in self.__dict__:
            # The rank attribute is passed directly to the class during
            # instantiation.
            if field  in ['_rank', '_year']: 
                continue
            value = utils._parse_field(PARSING_SCHEME,
                                       team_data,
                                       str(field)[1:])
            setattr(self, field, value)

    @property
    def dataframe(self):
        """
        Returns a pandas DataFrame containing all other class properties and
        values. The index for the DataFrame is the string abbreviation of the
        team, such as 'DET'.
        """
        fields_to_include = {
            'abbreviation': self.abbreviation,
            'average_age': self.average_age,
            'games_played': self.games_played,
            'goals_against': self.goals_against,
            'goals_for': self.goals_for,
            'losses': self.losses,
            'name': self.name,
            'overtime_losses': self.overtime_losses,
            'pdo_at_even_strength': self.pdo_at_even_strength,
            'penalty_killing_percentage': self.penalty_killing_percentage,
            'points': self.points,
            'points_percentage': self.points_percentage,
            'power_play_goals': self.power_play_goals,
            'power_play_goals_against': self.power_play_goals_against,
            'power_play_opportunities': self.power_play_opportunities,
            'power_play_opportunities_against':
            self.power_play_opportunities_against,
            'power_play_percentage': self.power_play_percentage,
            'rank': self.rank,
            'save_percentage': self.save_percentage,
            'shooting_percentage': self.shooting_percentage,
            'short_handed_goals': self.short_handed_goals,
            'short_handed_goals_against': self.short_handed_goals_against,
            'shots_against': self.shots_against,
            'shots_on_goal': self.shots_on_goal,
            'simple_rating_system': self.simple_rating_system,
            'strength_of_schedule': self.strength_of_schedule,
            'total_goals_per_game': self.total_goals_per_game,
            'wins': self.wins
        }
        return pd.DataFrame([fields_to_include], index=[self._abbreviation])

    @int_property_decorator
    def rank(self):
        """
        Returns an ``int`` of the team's rank based on the number of points
        they obtained in the season.
        """
        return self._rank

    @property
    def abbreviation(self):
        """
        Returns a ``string`` of the team's abbreviation, such as 'DET' for the
        Detroit Red Wings.
        """
        return self._abbreviation

    @property
    def schedule(self):
        """
        Returns an instance of the Schedule class containing the team's
        complete schedule for the season.
        """
        return Schedule(self._abbreviation, self._year)

    @property
    def roster(self):
        """
        Returns an instance of the Roster class containing all players for the
        team during the season with all career stats.
        """
        return Roster(self._abbreviation, self._year)

    @property
    def name(self):
        """
        Returns a ``string`` of the team's full name, such as 'Detroit Red
        Wings'.
        """
        return self._name

    @float_property_decorator
    def average_age(self):
        """
        Returns a ``float`` of the average age of all players on the team,
        weighted by their time on ice.
        """
        return self._average_age

    @int_property_decorator
    def games_played(self):
        """
        Returns an ``int`` of the total number of games the team has played in
        the season.
        """
        return self._games_played

    @int_property_decorator
    def wins(self):
        """
        Returns an ``int`` of the total number of wins the team had in the
        season.
        """
        return self._wins

    @int_property_decorator
    def losses(self):
        """
        Returns an ``int`` of the total number of losses the team had in the
        season.
        """
        return self._losses

    @int_property_decorator
    def overtime_losses(self):
        """
        Returns an ``int`` of the total number of overtime losses the team had
        in the season.
        """
        return self._overtime_losses

    @int_property_decorator
    def points(self):
        """
        Returns an ``int`` of the total number of points the team gained in the
        season.
        """
        return self._points

    @float_property_decorator
    def points_percentage(self):
        """
        Returns a ``float`` denoting the percentage of points gained divided by
        the maximum possible points available during the season. Percentage
        ranges from 0-1.
        """
        return self._points_percentage

    @int_property_decorator
    def goals_for(self):
        """
        Returns an ``int`` of the total number of goals a team scored during
        the season.
        """
        return self._goals_for

    @int_property_decorator
    def goals_against(self):
        """
        Returns an ``int`` of the total number of goals opponents scored
        against the team during the season.
        """
        return self._goals_against

    @float_property_decorator
    def simple_rating_system(self):
        """
        Returns a ``float`` which takes into account the average goal
        differential vs a team's strength of schedule. The league average
        evaluates to 0.0. Teams which have a positive score are comparatively
        stronger than average while teams with a negative score are weaker.
        """
        return self._simple_rating_system

    @float_property_decorator
    def strength_of_schedule(self):
        """
        Returns a ``float`` denoting a team's strength of schedule, based on
        goals scores and conceded. Higher values result in more challenging
        schedules while 0.0 is an average schedule.
        """
        return self._strength_of_schedule

    @float_property_decorator
    def total_goals_per_game(self):
        """
        Returns a ``float`` for the average number of goals scored per game.
        """
        return self._total_goals_per_game

    @int_property_decorator
    def power_play_goals(self):
        """
        Returns an ``int`` of the total number of power play goals scored.
        """
        return self._power_play_goals

    @int_property_decorator
    def power_play_opportunities(self):
        """
        Returns an ``int`` of the total number of power play opportunities for
        a team during the season.
        """
        return self._power_play_opportunities

    @float_property_decorator
    def power_play_percentage(self):
        """
        Returns a ``float`` denoting the percentage of power play opportunities
        where the team has scored. Percentage ranges from 0-100.
        """
        return self._power_play_percentage

    @int_property_decorator
    def power_play_goals_against(self):
        """
        Returns an ``int`` of the total number of power play goals conceded.
        """
        return self._power_play_goals_against

    @int_property_decorator
    def power_play_opportunities_against(self):
        """
        Returns an ``int`` of the total number of power play opportunities for
        the opponents during the season.
        """
        return self._power_play_opportunities_against

    @float_property_decorator
    def penalty_killing_percentage(self):
        """
        Returns a ``float`` denoting the percentage of power plays that have
        been successfully defended without a goal being conceded. Percentage
        ranges from 0-100.
        """
        return self._penalty_killing_percentage

    @int_property_decorator
    def short_handed_goals(self):
        """
        Returns an ``int`` of the number of short handed goals the team has
        scored during the season.
        """
        return self._short_handed_goals

    @int_property_decorator
    def short_handed_goals_against(self):
        """
        Returns an ``int`` of the number of short handed goals the team has
        conceded during the season.
        """
        return self._short_handed_goals_against

    @int_property_decorator
    def shots_on_goal(self):
        """
        Returns an ``int`` of the total number of shots on goal the team made
        during the season.
        """
        return self._shots_on_goal

    @float_property_decorator
    def shooting_percentage(self):
        """
        Returns a ``float`` denoting the percentage of shots to goals during
        the season. Percentage ranges from 0-100.
        """
        return self._shooting_percentage

    @int_property_decorator
    def shots_against(self):
        """
        Returns an ``int`` of the total number of shots on goal the team's
        opponents made during the season.
        """
        return self._shots_against

    @float_property_decorator
    def save_percentage(self):
        """
        Returns a ``float`` denoting the percentage of shots the team has saved
        during the season. Percentage ranges from 0-1.
        """
        return self._save_percentage

    @float_property_decorator
    def pdo_at_even_strength(self):
        """
        Returns a ``float`` of the PDO at even strength which equates to the
        shooting percentage plus the save percentage.
        """
        return self._pdo_at_even_strength


class Teams:
    """
    A list of all NHL teams and their stats in a given year.

    Finds and retrieves a list of all NHL teams from www.hockey-reference.com
    and creates a Team instance for every team that participated in the league
    in a given year. The Team class comprises a list of all major stats and a
    few identifiers for the requested season.

    Parameters
    ----------
    year : string (optional)
        The requested year to pull stats from.
    season_page : string (optional)
        Optionally specify the filename of a local file to use to pull data
        instead of downloading from sports-reference.com. This file should be
        of the Season page for the designated year.
    """
    def __init__(self, year=None, season_page=None):
        self._teams = []

        teams_list, year = _retrieve_all_teams(year, season_page)
        self._instantiate_teams(teams_list, year)

    def __getitem__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation.

        Parameters
        ----------
        abbreviation : string
            An NHL team's three letter abbreviation (ie. 'DET' for Detroit Red
            Wings).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.

        Raises
        ------
        ValueError
            If the requested team is not present within the Teams list.
        """
        for team in self._teams:
            if team.abbreviation.upper() == abbreviation.upper():
                return team
        raise ValueError('Team abbreviation %s not found' % abbreviation)

    def __call__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation. This method is a wrapper for __getitem__.

        Parameters
        ----------
        abbreviation : string
            An NHL team's three letter abbreviation (ie. 'DET' for Detroit Red
            Wings).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.
        """
        return self.__getitem__(abbreviation)

    def __str__(self):
        """
        Return the string representation of the class.
        """
        teams = [f'{team.name} ({team.abbreviation})'.strip()
                 for team in self._teams]
        return '\n'.join(teams)

    def __repr__(self):
        """
        Return the string representation of the class.
        """
        return self.__str__()

    def __iter__(self):
        """Returns an iterator of all of the NHL teams for a given season."""
        return iter(self._teams)

    def __len__(self):
        """Returns the number of NHL teams for a given season."""
        return len(self._teams)

    def _instantiate_teams(self, teams_list, year):
        """
        Create a Team instance for all teams.
        Once all team information has been pulled from the various webpages,
        create a Team instance for each team and append it to a larger list of
        team instances for later use.
        Parameters
        ----------
        teams_list : list
            A ``list`` containing all stats information in HTML format for all
            NHL teams.
        year : string
            A ``string`` of the requested year to pull stats from.
        """
        # Teams are listed in terms of rank with the first team being #1
        rank = 1
        if not teams_list:
            return
        for team_name in teams_list:
            team = Team(team_data=teams_list[team_name]['data'],
                        rank=rank,
                        year=year)
            self._teams.append(team)
            rank += 1

    @property
    def dataframes(self):
        """
        Returns a pandas DataFrame where each row is a representation of the
        Team class. Rows are indexed by the team abbreviation.
        """
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)
