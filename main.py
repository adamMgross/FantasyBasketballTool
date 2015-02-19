from player import Player
from team import Team
import api_interface
import input_handlers
import json_handlers
import json

# global variables
num_of_statistical_categories = 13
players_on_team = 1

#simulation functions-------------------------------------------------------------------------------------------------

# runs a simulation for a week with @param team1 versus @param team2
def simulate(team1, team2):
    print '\nYour Team:\n'
    team1.print_team_by_individual()
    play_week(team1, team2)
    team1.reset_totals()
    team2.reset_totals()

# finds the difference in stat output
# in one particular category between two teams
# and returns the difference with a + or - in front ot it
def find_difference(my_team, opponent, category):
    dif = my_team.totals[category] - opponent.totals[category]
    sign = ''

    if dif >= 0:
        sign = '+'
    
    return sign + str(round(dif,3))

# determines the final score between my_team and opponent
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

# calculates the totals in @param key stat category by summing each individual player's output
# for both @param my_team and @param opponent
# returns total in @param key category for my_team
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

# simulates a week's worth of play for @param my_team and @param opponent
# and prints out the results to the screen
def play_week(my_team, opponent):
    print ''

    for key in my_team.stats:
        print str(key) + ':\t ' + str(run_totals(my_team, opponent, key)) + '\t ' + find_difference(my_team, opponent, key)

    print '\nResult: '

    score = get_score(my_team, opponent)
    print str(score['wins']) + ' - ' + str(score['losses']) + ' - ' + str(score['ties'])

#main-----------------------------------------------------------------------------------------------------------------

#runs whole simulation
def main():
    team1 = Team([])
    team2 = Team([])
    answer = input_handlers.take_str_input('Do you want to load your team, edit your team or create a new one or stop? (answer: load or edit or new or stop) ')

    if answer == 'stop':
        print '\nDone.\n'
        return

    while answer == 'edit':
        update_players(json_handlers.load_from_json(True))
        answer = input_handlers.take_str_input('Type "edit" to make another edit, "load" to load your team, or "new" to make a new team. ')

    if answer == 'new':
        print 'Team 1: '
        team1 = Team(input_handlers.getTeam())
        json_handlers.dump_to_json(team1, True)
    else:
        team1 = json_handlers.load_from_json(True)

    answer = input_handlers.take_str_input('Do you want to load your opponents team or create a new one? (answer: load or new) ')

    if answer == 'new':
        print 'Team 2: '
        team2 = Team(input_handlers.getTeam())
        json_handlers.dump_to_json(team2, False)
    else:
        team2 = json_handlers.load_from_json(False)

    simulate(team1, team2)
    substitute = input_handlers.take_str_input('Do you want to substitute in a new player for an active one (to test the difference)? (y|n) ')
    if substitute == 'y':
        input_handlers.make_changes(team1)
        simulate(team1, team2)

    main()

main()

