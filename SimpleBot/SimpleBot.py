'''
Created on Apr 1, 2015

@author: Gregory
'''

from Resistance.Announcement import Announcement
import random
from Resistance.BaseAgent import BaseAgent

class SimpleBot(BaseAgent):
    '''
    The simplest of bots. Does everything randomly if possible.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        BaseAgent.__init__(self)
        self.knownSpies = []
        self.knownResistance = []
        self.lastGameState = None 
        
    def __name__(self):
        return "SimpleBot"
    
    def Knows(self, spies, resistance):
        '''Knowledge given to agent from game that can be absolutely trusted.
        Typically given to spies at the start of the game'''
        
        '''Default action doesn't care, but feel free to add containers for the spies/resistance members'''
        self.knownResistance = resistance
        self.knownSpies = spies
        
        return
    
    def Announce(self, gameState):
        '''Allows for the agent to make an announcement (see Announcement.py documentation)'''
        '''The agent should return a list of game.state.numPlayers size, containing the assertions against each player (RESISTANCE|SPY|UNDECLARED)'''
        
        announcement = Announcement(self.playerId, gameState)
        
        for pid in gameState.players:
            announcement.targets[pid] = gameState.UNDECLARED
            if pid == self.playerId:
                announcement.targets[pid] = gameState.RESISTANCE
                
        return announcement
    
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
        self.lastGameState = gameState
        
        return random.choice([gameState.PASS, gameState.FAIL])
    
    def MissionAction(self, operativeIds, gameState):
        '''
        The action to take while on the mission (returns PASS or FAIL)
        operatives - List of players on the mission (aliased by player ids)
        '''
        self.lastGameState = gameState
        
        if self.loyalty == gameState.RESISTANCE:
            return gameState.PASS
        else:
            return gameState.FAIL