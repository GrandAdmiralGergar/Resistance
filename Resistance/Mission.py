'''
Created on Mar 25, 2015

@author: Gregory
'''

def GetMaxMissionFailCount(playerCount, missionNumber):
    if playerCount >= 7 and missionNumber == 4:
        return 2
    else:
        return 1

def GetMissionCount(playerCount, missionNumber):
    '''
    Constructor
    '''        
    operativeCount = 0
    if missionNumber == 1:
        if playerCount == 5:
            operativeCount = 2
        if playerCount == 6:
            operativeCount = 2
        if playerCount == 7:
            operativeCount = 2
        if playerCount == 8:
            operativeCount = 3
        if playerCount == 9:
            operativeCount = 3
        if playerCount == 10:
            operativeCount = 3
    if missionNumber == 2:
        if playerCount == 5:
            operativeCount = 3
        if playerCount == 6:
            operativeCount = 3
        if playerCount == 7:
            operativeCount = 3
        if playerCount == 8:
            operativeCount = 4
        if playerCount == 9:
            operativeCount = 4
        if playerCount == 10:
            operativeCount = 4
    if missionNumber == 3:
        if playerCount == 5:
            operativeCount = 2
        if playerCount == 6:
            operativeCount = 4
        if playerCount == 7:
            operativeCount = 3
        if playerCount == 8:
            operativeCount = 4
        if playerCount == 9:
            operativeCount = 4
        if playerCount == 10:
            operativeCount = 4
    if missionNumber == 4:
        if playerCount == 5:
            operativeCount = 3
        if playerCount == 6:
            operativeCount = 3
        if playerCount == 7:
            operativeCount = 4
        if playerCount == 8:
            operativeCount = 5
        if playerCount == 9:
            operativeCount = 5
        if playerCount == 10:
            operativeCount = 5
    if missionNumber == 5:
        if playerCount == 5:
            operativeCount = 3
        if playerCount == 6:
            operativeCount = 4
        if playerCount == 7:
            operativeCount = 4
        if playerCount == 8:
            operativeCount = 5
        if playerCount == 9:
            operativeCount = 5
        if playerCount == 10:
            operativeCount = 5
    
    if operativeCount == 0:
        print "MISSION GENERATION ERROR"
    return operativeCount