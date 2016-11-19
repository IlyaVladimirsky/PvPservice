# **************MATCH DB STRUCT***************
# 3 tables: matches, match_players, players
#
# matches table fields:
#   1) primary key id
#   2)... some filds containing info about match(data, type etc.)
#
# match_players table fields(implements link one to many, matches table -> players table):
#   1) foreign key match_id which is id from matches table
#   2) foreign key player_id which is id from players table
#   3) int player_unique_id
#
# players table fields:
#   1) primaty key id
#   2)... some filds containing info about player(name, ip and others)

# This class can implement any database!
class MatchDB:
    def __init__(self):
        # connects to db or create it if does not exist
        pass

    def create_match(self, **info):
        # creates match and returns id of a new record using info
        pass

    def get_match(self, match_id):
        # return match by id
        pass

    def register_player(self, **info):
        # registers player if passing nickname has not been registered in players table
        # and returns player_id anyway
        pass

    def get_player(self, nickname):
        # returns player record by nickname
        pass

    def assign_player_to_match(self, match_id, player_id, match_player_id):
        # creates record to match_players table using match_id, unique_player_id, player_id args
        # it means that player(_id) takes part in match(_id)
        pass
