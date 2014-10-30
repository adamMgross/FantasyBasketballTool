#TODO: in no particular order
# 1) organize
# 1b) fix tie category problem
# 1c) account for mistakes in user input
# 1d) account for percentages in stat runs
# 2) Incorporate API use to make it so user only has to input name of player, and stats are pulled from online
# 3) Create team structure where positions are filled accordingly
# 4) Create structure for points system, no opponent

from playerObj import Player
import json
num_of_statistical_categories = 13
players_on_team = 1

#TEAM CLASS ------------------------------------------------------------------------
class Team(object):

    #default constructor
    def __init__(self, players):
        self.team = players
        self.stats = {'FGM': 0.0, 'FG%': 0.0, 'FTM': 0.0, 'FT%': 0.0, '3PM': 0.0, 'TP%': 0.0, 'REB': 0.0, 'AST': 0.0, 'STL': 0.0, 'BLK': 0.0, 'TO': 0.0, 'DD': 0.0, 'PTS': 0.0}
        self.totals = {'FGM': 0.0, 'FG%': 0.0, 'FTM': 0.0, 'FT%': 0.0, '3PM': 0.0, 'TP%': 0.0, 'REB': 0.0, 'AST': 0.0, 'STL': 0.0, 'BLK': 0.0, 'TO': 0.0, 'DD': 0.0, 'PTS': 0.0}
        self.set_total_avgs()

    def alt_ctor(self, players, stats, totals):
        self.team = players
        self.stats = stats
        self.totals = totals

    #sets team's averages to sum of all of its players' averages
    def set_total_avgs(self):
        for key in self.stats:
            self.set_category_avg(key)

    #sets team's average in a particular category
    #to sum of each player's average in that category
    def set_category_avg(self, category):
        if str.find(category, '%') >= 0:
            for player in self.team:
                self.stats[category] += player.stats[category]
            self.stats[category] /= players_on_team
        else:
            for player in self.team:
                self.stats[category] += player.stats[category]

    #prints out team's stat averages
    def print_team_overall_stats(self):
        print self.stats

    #prints out the team, player by player
    def print_team_by_individual(self):
        for player in self.team:
            player.print_player()

    #resets team's totals to 0 in each category
    def reset_totals(self):
        for key in self.totals:
            self.totals[key] = 0


