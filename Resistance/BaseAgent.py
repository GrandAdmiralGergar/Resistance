'''
Created on Mar 25, 2015

@author: Gregory
'''
from Resistance.Announcement import Announcement

import random

class BaseAgent(object):
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
        return "DEFAULT_AGENT"
    
     
    def Owner(self):
        '''Returns the name of the bot's creator'''
        return "DEFAULT"
        
    '''DO NOT MODIFY THIS FUNCTION'''
    def AssignLoyalty(self, loyalty):
        self.loyalty = loyalty
    
    def GetName(self):
        return self.name
    
    def RoundUpdate(self, gameState):
        '''Used to generically update a bot before each round begins (including the first round)
        Entirely optional'''
        
        return
    
    def Knows(self, spies, resistance, gameState):
        '''Knowledge given to agent from game that can be absolutely trusted.
        Typically given to spies at the start of the game'''
        
        '''Default action doesn't care, but feel free to add containers for the spies/resistance members'''
        
        
        return
    
    def Announce(self, gameState):
        '''Allows for the agent to make an announcement (see Announcement.py documentation)'''
        '''The agent should return a list of game.state.numPlayers size, containing the assertions against each player (RESISTANCE|SPY|UNDECLARED)'''
        
        announcement = Announcement(self.playerId, gameState)
        
        for pid in gameState.players:
            announcement.targets[pid] = gameState.RESISTANCE
        return None
    
    def ProposeMissionTeam(self, missionSize, gameState):
        '''Decide on a team of <missionSize> people to send on the mission
        Should return a list of Player ids'''
        self.lastGameState = gameState
        proposal = random.sample(self.lastGameState.players, missionSize)
        
        return proposal
        
    def MissionVote(self, leader, proposal, attempt, gameState):
        '''Whether or not the agent approves of the proposal
        leader - player suggesting the proposal
        proposal - list of players to take on the mission
        attempt - 1-5th attempt of voting this round (if 5 fail, the spies win)
        '''
        return gameState.PASS
    
    def MissionAction(self, operativeIds, gameState):
        '''
        The action to take while on the mission (returns PASS or FAIL)
        operatives - List of players on the mission (aliased by player ids)
        '''
        
        #This is always true
        if self.loyalty == gameState.RESISTANCE:
            return gameState.PASS
        else:
            return gameState.FAIL