from player import Player
from team import Team
import json

num_of_statistical_categories = 13
players_on_team = 1

#input handlers--------------------------------------------------------------------------------------------------------

def take_str_input(str):
    answer = raw_input(str)
    words = answer.split(' ')
    toReturn = ''
    for word in words:
        if word.isalpha() is False:
            return take_str_input('Invalid input. \n' + str)
        else:
            toReturn += word + ' '
    return toReturn[:-1]    

def take_num_input(str):
    answer = raw_input(str)
    if not answer.isalpha():
        return answer
    take_num_input('Invalid input. \n' + str)


#prompts the user to input data for @param key category
def input_data(category_name):
    num = float(take_num_input('Input ' + category_name + ' avg: '))
    answer = ''
    if num > 39:
        answer = take_str_input('Are you sure that was the right number? (y|n) ')
        if answer == 'n':
            num = float(take_num_input('Input ' + category_name + ' avg: '))
    return num

#prompts the user to input data for all member variables in @param player
def player_query(player):
    player.set_name(take_str_input('Input player name: '))
    player.team = take_str_input('What team is he on? ')
    set_averages_by_array(player, take_num_input('Input averages in the following order separated by commas and with no spaces: FGM, FG%, FTM, FT%, 3PM, TP%, REB, AST, STL, BLK, TO, DD, PTS: '))

#prompts the user to input each player in a team along with their individual stats
#@return team_arr, an array of all of the players that were input
def getTeam():
        team_arr = []
        players = 0
        while players < players_on_team:
            player_new = Player()
            player_query(player_new)
            team_arr.append(player_new)
            players += 1

        return team_arr

#prompts the user if he wants to make any substitutions to his team
#and if so, prompts the user to input new player information.
#replaces old player with new player in @param my_team
def make_changes(my_team):
    substitute = 'y'
    while substitute == 'y':
        player_new = Player()
        to_remove = take_str_input('Whom do you want to remove? ')
        found = False
        while (not found):
            for i, player in enumerate(my_team.team):
                if (player.name == to_remove):
                    my_team.team[i] = player_new
                    print 'Who is the new player?'
                    player_query(my_team.team[i])
                    found = True
            if not found:
                to_remove = take_str_input('Couldnt find him, try different spelling or pick a different player: ')

        my_team.set_total_avgs()
        substitute = take_str_input('Do you want to sub in another player? (y|n) ')

def edit_player(player):
    answer = take_str_input('Type name of category to edit, "games" to change # of games, or "all" to change all ')

    if answer == 'all':
        player.set_name((take_str_input('Input player name: ')))
        player.set_num_of_games(float(take_num_input('Input how many games he will play this week: ')))
        set_averages_by_array(player, take_num_input('Input averages in the following order separated by commas and with no spaces: FGM, FG%, FTM, FT%, 3PM, TP%, REB, AST, STL, BLK, TO, DD, PTS: '))

    elif answer == 'games':
        player.num_of_games = float(take_num_input('Input number of games: '))

    else:
        player.set_average(answer, float(take_num_input('Input ' + answer + ' avg: ')))


def update_players(my_team):

        to_edit = take_str_input('Whom do you want to edit? ')
        found = False
        while (not found):
            for i, player in enumerate(my_team.team):
                if (player.name == to_edit):
                    edit_player(player)
                    found = True
            if not found:
                to_edit = take_str_input('Couldnt find him, try different spelling or pick a different player: ')

        my_team.set_total_avgs()
        dump_to_json(my_team, True)

# handles setting a player's averages
# when the input is copy & pasted from
# the ESPN Fantasy Basketball website
def set_averages_by_array(player, array):
    array = array.split('\t')
    fgs = float(array[0][:array[0].index('/')])
    fts = float(array[2][:array[2].index('/')])
    tps = float (array[4][:array[4].index('/')])
    player.set_average('FGM', fgs)
    player.set_average('FG%', float(array[1]))
    player.set_average('FTM', fts)
    player.set_average('FT%', float(array[3]))
    player.set_average('3PM', tps)
    player.set_average('TP%', float(array[5]))
    player.set_average('REB', float(array[6]))
    player.set_average('AST', float(array[7]))
    player.set_average('STL', float(array[8]))
    player.set_average('BLK', float(array[9]))
    player.set_average('TO', float(array[10]))
    player.set_average('DD', float(array[11]))
    player.set_average('PTS', float(array[12]))
