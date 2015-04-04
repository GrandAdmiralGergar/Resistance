'''
Created on Mar 30, 2015

@author: Gregory
'''


class Player:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        '''Tracked by Game, so don't bother trying to change it (NORM)'''
        self.loyalty = 0
        
        '''Identifies players within a game, also denotes position around the table
        E.g: player 0 is next to player 1 and player 10 (if 10 players), player 3 is next to 2 and 4.
        Used to track next leader'''
        self.playerId = -1
    
    def __name__(self):
        return "DEFAULT"