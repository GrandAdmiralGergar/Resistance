'''
Created on Mar 30, 2015

@author: Gregory
'''
from Resistance.Mission import GetMaxMissionFailCount

class MissionResult:
    ''' Simple container for the mission results for a given mission '''

    def __init__(self, missionNumber, playerCount):
        self.missionTeam =[]
        self.passCount=0
        self.failCount=0
        self.missionNumber =missionNumber
        self.playerCount = playerCount
    
    def Succeeded(self):
        if self.failCount >= GetMaxMissionFailCount(self.playerCount,self.missionNumber):
            return False
        else:
            return True
        
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    def __ne__(self, other):
        return not self.__eq__(other)