'''
Created on Mar 30, 2015

@author: Gregory
'''

class Announcement:
    ''' Simple container to hold an announcement
    Announcements take the form of:
    "PLAYER X SUGGESTS PLAYER Y OF BEING <RESISTANCE / SPY>"
    Where:
    PLAYER X = ANNOUNCER
    PLAYER Y = TARGET
    <RESISTANCE/SPY/UNDECLARED> = LOYALTY  
    '''


    def __init__(self, announcerId, gameState):
        '''
        Constructor
        '''
        self.announcer = announcerId
        self.targets = []
        for id in gameState.players:
            self.targets.append(gameState.UNDECLARED)

    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    