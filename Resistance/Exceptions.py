'''
Created on Apr 4, 2015

@author: Gregory
'''

class Cheater(Exception):
    def __init__(self, player, reason):
        self.cheater = player
        self.reason = reason
    def __str__(self):
        return "Player " + self.cheater.__name__() + " was caught: " + self.reason