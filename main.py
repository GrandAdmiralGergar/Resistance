'''
Created on Mar 25, 2015

@author: Gregory
'''
from Resistance.Game import Game
from SimpleBot.SimpleBot import SimpleBot
import sqlite3

import sys
import getopt
import random
import time
from Resistance.Exceptions import Cheater


#Define list of bots to choose from (class names only)
bots = [SimpleBot]



def ReduceClassToInstance(someType):
    return someType()

def main(argv):
    dbFile = 'dummy.db'
    iterations = sys.maxint
    seconds = sys.maxint
    
    try:
        opts, args = getopt.getopt(argv, "", ["iterations=", "seconds=", "dbFile="])
    except getopt.GetoptError:
        print 'main.py --iterations <int> --seconds <int (seconds)> --dbFile <database filename>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("--iterations"):
            iterations = int(arg)
        elif opt in ("--dbFile"):
            dbFile = arg
        elif opt in ("--seconds"):
            seconds = int(arg)
    
    if seconds == sys.maxint and iterations == sys.maxint:
        iterations = 10
    

    #Database set up
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Game(game_id, winning_side, player_count, resistance_round_wins, spy_round_wins)")
    cur.execute("CREATE TABLE IF NOT EXISTS BotResults(game_id, bot_name, side, player_id)")
    cur.execute("CREATE TABLE IF NOT EXISTS Disqualifications(game_id, bot_name, reason)")
    #cur.execute("CREATE TABLE IF NOT EXISTS Announcements(game_id, bot_name, player_id, round, target, declaration)")
    cur.execute("CREATE TABLE IF NOT EXISTS MissionResults(game_id, round, mission_success, pass_votes, fail_votes, team_member_1, team_member_2, team_member_3, team_member_4, team_member_5)")
    cur.execute("CREATE TABLE IF NOT EXISTS VoteResults(game_id, round, vote_attempt, vote_success, leader, pass_votes, fail_votes, proposed_team_member_1, proposed_team_member_2, proposed_team_member_3, proposed_team_member_4, proposed_team_member_5, player_1_vote, player_2_vote, player_3_vote, player_4_vote, player_5_vote, player_6_vote, player_7_vote, player_8_vote, player_9_vote, player_10_vote)")
    
    iteration = 0
    start = time.time()
    while iteration < iterations and (time.time() - start) < seconds:
        iteration += 1
        game_size = random.randint(5, 10)
        
        botSelection = []
        if len(bots) < game_size:
            if len(bots) == 0:
                print "No bots or all bots have been disqualified"
                CloseDBConnection(con)
                exit()
                
            for y in range(0, game_size):
                botSelection.append(random.choice(bots))
        else:
            botSelection = random.sample(bots, game_size)
    
        game = Game(map(ReduceClassToInstance, botSelection))
        try:
            game.RunGame()
        
        except Cheater as e:
            print e
            for x in range(0, len(bots)):
                botName = bots[x]().__name__()
                if botName == e.cheater.__name__():
                    query = "INSERT INTO Disqualifications(game_id, bot_name, reason) VALUES(" + str(x) + ", \"" + botName + "\",\"" + e.reason + "\")"
                    cur.execute(query) 
                    bots.pop(x)
                    break

        PushGameToDB(cur, game, iteration)
    CloseDBConnection(con)
    print "Ran " + str(iteration) + " iterations in " + str(time.time()-start) + " seconds"
    #game = Game([SimpleBot(), SimpleBot(), SimpleBot(), SimpleBot(),SimpleBot(),SimpleBot(),SimpleBot()])
        
def PushGameToDB(cur, game, iteration):
    winningSide = ""
    if game.winner == game.state.RESISTANCE:
        winningSide = "\"RESISTANCE\""
    else:
        winningSide = "\"SPY\""
        
    query = "INSERT INTO Game(game_id, winning_side, player_count, resistance_round_wins, spy_round_wins) VALUES(" + str(iteration) + ", " + winningSide + ", " + str(game.state.num_players) + ", " + str(game.state.GetResistanceRoundWins()) + ", " + str(game.state.GetSpyRoundWins()) + ")"
    cur.execute(query) 
    
    for bot in game.players:
        
        botName = bot.__name__()
        win = int((bot.loyalty == game.winner))
        side = None
        if bot.loyalty == game.state.RESISTANCE:
            side = "\"RESISTANCE\""
        else:
            side = "\"SPY\""
        
        query = "INSERT INTO BotResults(game_id, bot_name, side, player_id) VALUES(" + str(iteration) + ", \"" + botName + "\", " + side + ", " + str(bot.playerId) + ")"            
        cur.execute(query) 
    
    for missionResult in game.state.missionResults:
        query  = "INSERT INTO MissionResults(game_id, round, mission_success, pass_votes, fail_votes "
        for x in range(0, len(missionResult.missionTeam)):
            query += ", team_member_" + str(x+1)
        query += ") "
        missionSuccess = ""
        if not missionResult.Succeeded():
            missionSuccess = "\"MISSION_FAILED\""
        else:
            missionSuccess = "\"MISSION_SUCCESS\""
        query += "VALUES(" + str(iteration) + "," + str(missionResult.missionNumber) + ", " + missionSuccess + "," + str(missionResult.passCount) + ", " + str(missionResult.failCount)
        for playerId in missionResult.missionTeam:
            query += ", " + str(playerId)
        query += ")"
        cur.execute(query)
    
    voteRound = 0
    for roundVoteResult in game.state.voteResults:
        voteRound += 1
        voteAttempt = 0
        for voteResultAttempt in roundVoteResult:
            voteAttempt += 1
            query = "INSERT INTO VoteResults(game_id, round, vote_attempt, vote_success, leader, pass_votes, fail_votes"
            for x in range(0, len(voteResultAttempt.proposedTeam)):
                query += ", proposed_team_member_" + str(x+1)
            for x in range(0, game.state.num_players):
                query += ", player_" + str(x+1) + "_vote "
            query += ") "
            voteSuccess = ""
            if voteResultAttempt.PassVotes() <= voteResultAttempt.FailVotes():
                voteSuccess = "\"VOTE_FAILED\""
            else:
                voteSuccess = "\"VOTE_PASSED\""
            query += "VALUES(" + str(iteration) + ", " + str(voteRound) + ", " + str(voteAttempt) + ", " + voteSuccess + ", " + str(voteResultAttempt.missionLeader) + ", " + str(voteResultAttempt.PassVotes()) + ", " + str(voteResultAttempt.FailVotes())
            for playerId in voteResultAttempt.proposedTeam:
                query += ", " + str(playerId)
            for x in range(0, game.state.num_players):
                if voteResultAttempt.votes[x] == True:
                    query += ", \"PASS\""
                else:
                    query += ", \"FAIL\""
            query += ")"
            cur.execute(query)
def CloseDBConnection(connection):
    connection.commit()
    connection.close()
    
if __name__ == '__main__':
    main(sys.argv[1:])