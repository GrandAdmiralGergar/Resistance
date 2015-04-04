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


#Define list of bots to choose from (class names only)
bots = [SimpleBot]



def ReduceClassToInstance(someType):
    return someType()

def main(argv):
    dbFile = 'dummy.db'
    iterations = 10
    
    try:
        opts, args = getopt.getopt(argv, "", ["iterations=", "dbFile="])
    except getopt.GetoptError:
        print 'main.py --iterations <int> --dbFile <database filename>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("--iterations"):
            iterations = int(arg)
        elif opt in ("--dbFile"):
            dbFile = arg
    

    #Database set up
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS GameResults(game_id, bot_name, won, side, player_count)")
    
    for x in range(0, iterations):
        game_size = random.randint(5, 10)
        
        botSelection = []
        if len(bots) < game_size:
            for y in range(0, game_size):
                botSelection.append(random.choice(bots))
        else:
            botSelection = random.sample(bots, game_size)
    
        game = Game(map(ReduceClassToInstance, botSelection))
        game.RunGame()
        
        for bot in game.players:
            
            botName = bot.__name__()
            win = int((bot.loyalty == game.winner))
            side = None
            if bot.loyalty == game.state.RESISTANCE:
                side = "\"RESISTANCE\""
            else:
                side = "\"SPY\""
            num_players = len(game.players)
            
            query = "INSERT INTO GameResults(game_id, bot_name, won, side, player_count) VALUES(" + str(x) + ", \"" + botName + "\", " + str(win) + ", " + side + ", " + str(num_players) + ")"
            cur.execute(query) 
    con.commit()
    con.close()
    #game = Game([SimpleBot(), SimpleBot(), SimpleBot(), SimpleBot(),SimpleBot(),SimpleBot(),SimpleBot()])
        

if __name__ == '__main__':
    main(sys.argv[1:])