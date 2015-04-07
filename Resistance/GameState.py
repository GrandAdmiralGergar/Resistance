'''
Created on Mar 25, 2015

@author: Gregory
'''

import copy

class GameState:
    '''
    classdocs
    '''

    def __init__(self, players):
        '''
        Constructor
        '''
        #Constants for pass and fail
        self.PASS=True
        self.FAIL=False
        
        #Constants for teams
        self.RESISTANCE=0
        self.SPY=1
        self.UNDECLARED=2
        
        self.num_players = len(players)
        
        '''List of Player's. By default, their loyalties are all set to be RESISTANCE'''
        self.players = players
        
        self.currentLeader = 0
        
        '''Keep track of total spies and resistance members in a given game'''
        self.spyCount = 0
        self.resistanceCount = 0
        
        '''Mission counter '''
        self.currentMission = 1
        
        '''Voting results are a list of lists of pairs, 
        [Mission Number[Vote attempt[VotingResult]]]
        containing the voting results of player x in a given round'''
        self.voteResults = []
        
        '''Mission results are a list of lists, the latter containing a MissionResult object'''
        self.missionResults = []
                
        '''Announcements are a dictionary of 'name:[list of announcements]' '''
        self.announcements = {}
        
        '''These represent the announcements made in the last round'''
        self.newAnnouncements = {}
        
        
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def Clone(self):
        '''Make sure any local modifications on the game state don't affect the host game. Because I know what you are up to, Norm'''
        return copy.deepcopy(self)
    
    def SetCurrentMissionNumber(self, missionNumber):
        self.currentMission = missionNumber
        
    def GetCurrentMissionNumber(self):
        return self.currentMission
    
    def AddVoteResults(self, voteResults):
        '''Adds voting results to the top of the stack'''
        self.voteResults.append(voteResults)
    
    def AddMissionResults(self, missionResults):
        '''Adds mission results to the top of the stack'''
        self.missionResults.append(missionResults)
    
    def GetVoteResults(self, missionNumber):
        '''Returns the voting results of the given mission number'''
        if missionNumber > len(self.voteResults) :
            return []
        else:
            return self.voteResults[missionNumber-1]
        
    def GetMissionResults(self, missionNumber):
        '''Returns the voting results of the given mission number'''
        if missionNumber > len(self.missionResults) :
            return []
        else:
            return self.missionResults[missionNumber-1]
    
    def GetResistanceRoundWins(self):
        wins = 0
        for round in self.missionResults:
            if round.Succeeded():
                wins += 1
        return wins
    
    def GetSpyRoundWins(self):
        wins = 0
        for round in self.missionResults:
            if not round.Succeeded():
                wins += 1
        return wins