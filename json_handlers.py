import json
from player import Player
from team import Team

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

