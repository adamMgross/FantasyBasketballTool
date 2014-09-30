
num_of_statistical_categories = 3
default_games_per_week = 4
players_on_team = 1


#PLAYER CLASS ------------------------------------------------------------------------
class Player(object):

    #default constructor
    def __init__(self):
        self.name = ''
        self.position = ''
        self.num_of_games = 0
        self.stats = {'Pts': 0.0, 'Reb': 0.0, 'Ast': 0.0}

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


#TEAM CLASS ------------------------------------------------------------------------
class Team(object):

    #default constructor
    def __init__(self, players):
        self.team = players
        self.stats = {'Pts': 0.0, 'Reb': 0.0, 'Ast': 0.0}
        self.totals = {'Pts': 0.0, 'Reb': 0.0, 'Ast': 0.0}
        self.set_total_avgs()

    #sets team's averages to sum of all of its players' averages
    def set_total_avgs(self):
        for key in self.stats:
            self.set_category_avg(key)

    #sets team's average in a particular category
    #to sum of each player's average in that category
    def set_category_avg(self, category):
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



#MAIN DRIVER ------------------------------------------------------------------------

#finds the difference in stat output
#in one particular category between two teams
#@returns the difference with a + or - in front ot it
def find_difference(my_team, opponent, category):
    dif = my_team.totals[category] - opponent.totals[category]
    sign = ''

    if dif >= 0:
        sign = '+'

    return sign + str(dif)

#determines whether @param my_team beat @param opponent
#@return true or false
def assert_win(my_team, opponent):
    count = 0

    for key in my_team.stats:
        count += int(my_team.stats[key] > opponent.stats[key])
    return count >= (num_of_statistical_categories/2) + 1

#determines the final score between my_team and opponent
def get_score(my_team, opponent):
    count = 0
    for key in my_team.stats:
        if my_team.stats[key] > opponent.stats[key]:
            count += 1

    return count

#calculates the totals in @param key stat category by summing each individual player's output
#for both @param my_team and @param opponent
#returns total in @param key category for my_team
def run_totals(my_team, opponent, key):
    my_total = 0
    opponent_total = 0

    for player in my_team.team:
        my_total += player.stats[key]*player.num_of_games

    for player in opponent.team:
        opponent_total += player.stats[key]*player.num_of_games

    my_team.totals[key] = my_total
    opponent.totals[key] = opponent_total

    return my_total

#simulates a week's worth of play for @param my_team and @param opponent
#and prints out the results to the screen
def play_week(my_team, opponent):
    print ''

    for key in my_team.stats:
        print str(key) + ': ' + str(run_totals(my_team, opponent, key)) + ' ' + find_difference(my_team, opponent, key)

    print '\nResult: '

    score = get_score(my_team, opponent)
    if assert_win(my_team, opponent):
        print 'Win, with a score of ' + str(score) + ' to ' + str(num_of_statistical_categories-score)
    else:
        print 'Lose, with a score of ' + str(num_of_statistical_categories-score) + ' to ' + str(score)

#prompts the user to input data for @param key category
def input_data(category_name):
    num = int(raw_input('Input ' + category_name + ' avg: '))
    answer = ''
    if num > 39:
        answer = raw_input('Are you sure that was the right number? (y|n) ')
        if answer == 'n':
            num = int(raw_input('Input ' + category_name + ' avg: '))
    return num

#prompts the user to input data for all member variables in @param player
def player_query(player):
    player.set_name(raw_input('Input player name: '))
    player.set_position(raw_input('Input player position: '))
    player.set_num_of_games(int(raw_input('Input how many games he will play this week: ')))
    for key in player.stats:
        player.set_average(key, input_data(key))

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

#runs a simulation for a week with @param team1 versus @param team2
def simulate (team1, team2) :
    print '\nYour Team:\n'
    team1.print_team_by_individual()
    play_week(team1, team2)
    team1.reset_totals()
    team2.reset_totals()

#prompts the user if he wants to make any substitutions to his team
#and if so, prompts the user to input new player information.
#replaces old player with new player in @param my_team
def make_changes(my_team):
    substitute = raw_input('Do you want to substitute in a new player for an active one? (y|n) ')
    while substitute == 'y':
        player_new = Player()
        to_remove = raw_input('Whom do you want to remove? ')
        found = False
        while (not found):
            for i, player in enumerate(my_team.team):
                if (player.name == to_remove):
                    my_team.team[i] = player_new
                    print 'Who is the new player?'
                    player_query(my_team.team[i])
                    found = True
            if not found:
                to_remove = raw_input('Couldnt find him, try different spelling or pick a different player: ')

        my_team.set_total_avgs()

        substitute = raw_input('Do you want to sub in another player? (y|n) ')

#runs whole simulation
def run_main():

    print 'Team 1: '
    team1 = Team(getTeam())

    print 'Team 2: '
    team2 = Team(getTeam())

    simulate(team1, team2)

    user_response = raw_input('Run again? (y|n) ')
    while (user_response is not 'n'):
        make_changes(team1)
        simulate(team1, team2)
        user_response = raw_input('Run again? (y|n) ')

    print 'DONE. \n'

run_main()


