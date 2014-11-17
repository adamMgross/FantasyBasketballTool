#TODO: in no particular order
# 1) Incorporate API use to make it so user only has to input name of player, and stats are pulled from online
# 2) Create structure for points system, no opponent
# 3) Incorporate API to make games per week update automatically

from playerObj import Player
from Team import Team
import json
num_of_statistical_categories = 13
players_on_team = 13

#simulation functions-------------------------------------------------------------------------------------------------

#runs a simulation for a week with @param team1 versus @param team2
def simulate(team1, team2):
    print '\nYour Team:\n'
    team1.print_team_by_individual()
    play_week(team1, team2)
    team1.reset_totals()
    team2.reset_totals()

#finds the difference in stat output
#in one particular category between two teams
#@returns the difference with a + or - in front ot it
def find_difference(my_team, opponent, category):
    dif = my_team.totals[category] - opponent.totals[category]
    sign = ''

    if dif >= 0:
        sign = '+'
    
    return sign + str(round(dif,3))

#determines the final score between my_team and opponent
def get_score(my_team, opponent):

    count = {'wins': 0, 'losses': 0, 'ties': 0}
    for key in my_team.stats:
        if key is 'TO':
            if my_team.stats[key] > opponent.stats[key]:
                count['losses'] += 1
            elif my_team.stats[key] == opponent.stats[key]:
                count['ties'] += 1
            else:
                count['wins'] += 1
        else:
            if my_team.stats[key] > opponent.stats[key]:
                count['wins'] += 1
            elif my_team.stats[key] == opponent.stats[key]:
                count['ties'] += 1
            else:
                count['losses'] += 1

    return count

#calculates the totals in @param key stat category by summing each individual player's output
#for both @param my_team and @param opponent
#returns total in @param key category for my_team
def run_totals(my_team, opponent, key):
    my_total = 0
    opponent_total = 0
    if str.find(key, '%') >= 0:
        for player in my_team.team:
            my_total += player.stats[key]
        my_total /= players_on_team

        for player in opponent.team:
            opponent_total += player.stats[key]
        opponent_total /= players_on_team

    else:
        for player in my_team.team:
            my_total += player.stats[key]*player.num_of_games

        for player in opponent.team:
            opponent_total += player.stats[key]*player.num_of_games

    my_team.totals[key] = my_total
    opponent.totals[key] = opponent_total

    return round(my_total,3)

#simulates a week's worth of play for @param my_team and @param opponent
#and prints out the results to the screen
def play_week(my_team, opponent):
    print ''

    for key in my_team.stats:
        print str(key) + ':\t ' + str(run_totals(my_team, opponent, key)) + '\t ' + find_difference(my_team, opponent, key)

    print '\nResult: '

    score = get_score(my_team, opponent)
    print str(score['wins']) + ' - ' + str(score['losses']) + ' - ' + str(score['ties'])


#modifiers-------------------------------------------------------------------------------------------------------------

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
    player.set_num_of_games(float(take_num_input('Input how many games he will play this week: ')))
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

#JSON functions--------------------------------------------------------------------------------------------------------
def decode(player_array_of_dicts):
    team = []
    for dct in player_array_of_dicts:
        player = Player()
        player.set_num_of_games(float(dct['num_of_games']))
        player.set_name(dct['name'])
        player.set_stats(dct['stats'])
        team.append(player)
    return team

def dump_to_json(team, is_users_team):

    if is_users_team:
        output = json.dumps(team.__dict__, default=lambda obj: obj.__dict__)
        with open('myTeam.json', 'w') as outfile:
            outfile.write(output)
            outfile.close()
    else:
        output2 = json.dumps(team.__dict__, default=lambda obj: obj.__dict__)
        with open('opponent.json', 'w') as outfile:
            outfile.write(output2)
            outfile.close()

def load_from_json(is_users_team):

    if is_users_team:
        with open('myTeam.json') as infile:
                json_data = json.load(infile)
                team1 = Team(decode(json_data['team']))
                return team1
    else:
        with open('opponent.json') as infile2:
            json_data2 = json.load(infile2)
            team2 = Team(decode(json_data2['team']))
            return team2

#main-----------------------------------------------------------------------------------------------------------------

#runs whole simulation
def run_main():
    team1 = Team([])
    team2 = Team([])
    answer = take_str_input('Do you want to load your team, edit your team or create a new one or stop? (answer: load or edit or new or stop) ')

    if answer == 'stop':
        print '\nDone.\n'
        return

    while answer == 'edit':
        update_players(load_from_json(True))
        answer = take_str_input('Type "edit" to make another edit, "load" to load your team, or "new" to make a new team. ')

    if answer == 'new':
        print 'Team 1: '
        team1 = Team(getTeam())
        dump_to_json(team1, True)
    else:
        team1 = load_from_json(True)

    answer = take_str_input('Do you want to load your opponents team or create a new one? (answer: load or new) ')

    if answer == 'new':
        print 'Team 2: '
        team2 = Team(getTeam())
        dump_to_json(team2, False)
    else:
        team2 = load_from_json(False)

    simulate(team1, team2)
    substitute = take_str_input('Do you want to substitute in a new player for an active one (to test the difference)? (y|n) ')
    if substitute == 'y':
        make_changes(team1)
        simulate(team1, team2)

    run_main()

run_main()

