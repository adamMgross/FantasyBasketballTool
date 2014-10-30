#TODO: in no particular order
# 1) organize
# 1b) fix tie category problem
# 1c) account for mistakes in user input
# 1d) account for percentages in stat runs
# 2) Incorporate API use to make it so user only has to input name of player, and stats are pulled from online
# 3) Create team structure where positions are filled accordingly
# 4) Create structure for points system, no opponent

import json
num_of_statistical_categories = 13
players_on_team = 1

#PLAYER CLASS ------------------------------------------------------------------------
class Player(object):

    #default constructor
    def __init__(self):
        self.name = ''
        self.position = ''
        self.num_of_games = 0
        self.stats = {'FGM': 0.0, 'FG%': 0.0, 'FTM': 0.0, 'FT%': 0.0, '3PM': 0.0, 'TP%': 0.0, 'REB': 0.0, 'AST': 0.0, 'STL': 0.0, 'BLK': 0.0, 'TO': 0.0, 'DD': 0.0, 'PTS': 0.0}

    def alt_ctor(self, name, position, num_of_games, stats):
        self.name = name
        self.position = position
        self.num_of_games = num_of_games
        self.stats = stats
        return self

    #sets player's name to @param name
    def set_name(self, name):
        self.name = name

    #sets player's position to @param position
    def set_position(self, position):
        self.position = position

    #sets player's num_of_games to @param num
    def set_num_of_games(self, num):
        self.num_of_games = num

    #sets player's average in @param category to @param num
    def set_average(self, category, number):
        self.stats[category] = number

    #sets player's stats to @param stat_dict
    def set_stats(self, stat_dict):
        self.stats = stat_dict

    #prints player's name and position
    def print_player(self):
        print self.name + ', ' + self.position



