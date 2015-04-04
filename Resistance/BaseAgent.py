'''
Created on Mar 25, 2015

@author: Gregory
'''
import Player
from Resistance.Announcement import Announcement


class BaseAgent(Player.Player):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #Maintain this default loyalty
        Player.Player.__init__(self)
        self.loyalty = 0
        
    def __name__(self):
        return "DEFAULT_AGENT"
    
     
        
    '''DO NOT MODIFY THIS FUNCTION'''
    def AssignLoyalty(self, loyalty):
        self.loyalty = loyalty
    
    def GetName(self):
        return self.name
    
    def Knows(self, spies, resistance):
        '''Knowledge given to agent from game that can be absolutely trusted.
        Typically given to spies at the start of the game'''
        
        '''Default action doesn't care, but feel free to add containers for the spies/resistance members'''
        
        return
    def Thinks(self, spies, resistance):
        '''Recommended place holder for player-given knowledge'''
        
        '''Write this function generally so that singular bits of knowledge can be added by passing in partial lists of spies or resistance members, 
        either by the game or the bot itself if it deducts something'''
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