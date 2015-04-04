'''
Created on Mar 30, 2015

@author: Gregory
'''

class VotingResult:
    ''' Simple container to hold voting results '''

    def __init__(self):
        '''List of player numbers on the proposed team'''
        self.proposedTeam = []
        
        '''List of votes, indexed by player number'''
        self.votes = []
        
        '''Mission leader player id'''
        self.missionLeader = -1
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    def __ne__(self, other):
        return not self.__eq__(other)