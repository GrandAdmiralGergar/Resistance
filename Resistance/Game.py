'''
Created on Mar 25, 2015

@author: Gregory
'''

import random
from Resistance.GameState import GameState
from Resistance.Mission import GetMissionCount
from Resistance.VotingResult import VotingResult
from Resistance.MissionResult import MissionResult


def ReducePlayerToId(player):
    return player.playerId

class Game:
    '''
    classdocs
    '''

    def __init__(self, players):
        '''
        players - list of Agents to play the game
        '''
        
        self.SPIES_WIN_GAME = 1
        self.SPIES_WIN_ROUND = 2
        self.RESISTANCE_WIN_GAME = 3
        self.RESISTANCE_WIN_ROUND = 4

        self.players = players
        for i in range(0, len(self.players)):
            self.players[i].playerId = i
        self.currentLeader = 0
        
        self.state = GameState(map(ReducePlayerToId,players))
        self.spies = []
        self.resistance = []
        self.winner = None
    
    def AssignLoyalties(self):
        '''Randomly pick the players who are spies / resistance'''
        playerCount = len(self.players)
        
        #Predefined loyalty counters
        if playerCount == 5:
            self.state.spyCount = 2
            self.state.resistanceCount = 3
        if playerCount == 6:
            self.state.spyCount = 2
            self.state.resistanceCount = 4
        if playerCount == 7:
            self.state.spyCount = 3
            self.state.resistanceCount = 4
        if playerCount == 8:
            self.state.spyCount = 3
            self.state.resistanceCount = 5
        if playerCount == 9:
            self.state.spyCount = 3
            self.state.resistanceCount = 6
        if playerCount == 10:
            self.state.spyCount = 4
            self.state.resistanceCount = 6
        
        for player in self.players:
            player.loyalty = self.state.RESISTANCE
        
        #Assign spies - the rest are loyal by default
        self.spies = random.sample(self.players, self.state.spyCount)

        for spy in self.spies:
            spy.loyalty = self.state.SPY
            
        for player in self.players:
            if player.loyalty == self.state.RESISTANCE:
                self.resistance.append(player)
    
    def AntiCheatingMeasure(self, gameCopy, player):
        if not gameCopy.__eq__(self.state):
            print "FRAUD DETECTION ON PLAYER " + str(player.__name__())
            exit()
            
    
    def RevealSpies(self):
        for spy in self.spies:
            spy.Knows(self.spies, self.resistance)
            
        for rebel in self.resistance:
            rebel.Knows([], [rebel])
                
    def NextLeader(self):
        self.currentLeader = (self.currentLeader + 1) % len(self.players) 
        return self.players[self.currentLeader]
    
    def VerifyAnnouncement(self, pid, announcement):
        if len(announcement.targets) != len(self.players):
            return None

        for target in announcement.targets:
            if not target in [self.state.RESISTANCE, self.state.SPY, self.state.UNDECLARED]:
                return None
        
        if announcement.announcer != pid:
            return None
        
        return announcement
        
    def Announcements(self):
        announcements = {}
        gameCopy = self.state.Clone()
        for player in self.players:
            announcement = self.VerifyAnnouncement(player.playerId, player.Announce(gameCopy))
            if announcement:
                announcements[player.playerId] = announcement
            else:
                print "BAD ANNOUNCEMENT"
            self.AntiCheatingMeasure(gameCopy, player)
            
        #Merge new announcements into old announcements
        for playerId in self.state.newAnnouncements:
            if playerId not in self.state.announcements:
                self.state.announcements[playerId] = []
            self.state.announcements[playerId].append(self.state.newAnnouncements[playerId])

        #Update game state with new announcements from above
        for playerId in announcements:
            self.state.newAnnouncements[playerId] = announcements[playerId]
        
        return
        
    def DetermineTeam(self, roundNumber):
        votingResults = []
        for attempt in range(0, 5) :
            votingResult = VotingResult()
            
            leader = self.NextLeader()
            self.state.currentLeader = leader.playerId
            
            #Let players make annoucements
            self.Announcements()
            
            gameCopy = self.state.Clone()
            mission_size = GetMissionCount(len(self.players), roundNumber)
            proposal = leader.ProposeMissionTeam(mission_size,gameCopy)
            
            self.AntiCheatingMeasure(gameCopy, leader)
                        
            #If the player picks the wrong number of proposals, then players are randomly added or removed
            if len(proposal) != mission_size:
                while len(set(proposal)) < mission_size:
                    proposal.append(random.choice(self.players))
                while len(set(proposal)) > mission_size:
                    proposal.remove(random.choice(proposal))
        
            #Prepare for the player voting
            passes = 0
            fails = 0
            votingResult.missionLeader = leader.playerId
            votingResult.proposedTeam = proposal
            votingResult.votes = []

            
            #Iterate through each players' voting step
            for player in self.players:
                playerVote = player.MissionVote(leader.playerId, proposal, attempt, gameCopy)
                self.AntiCheatingMeasure(gameCopy, player)
                #If the agent doesn't return pass or fail, assume pass
                if playerVote is not self.state.PASS and playerVote is not self.state.FAIL:
                    playerVote = self.state.PASS

                if playerVote == self.state.PASS:
                    passes += 1
                else:
                    fails += 1
                
                votingResult.votes.append(playerVote)
            
            votingResults.append(votingResult)
            if passes > fails:
                break
        
        #FAILURE
        if passes <= fails:
            return None
        return votingResults

    def ExecuteMission(self, team, roundNumber):
        result = MissionResult(roundNumber,len(self.players))
        gameCopy = self.state.Clone()
        fails = 0
        passes = 0
        for pid in team:
            playerVote = self.players[pid].MissionAction(team, gameCopy)
            self.AntiCheatingMeasure(gameCopy, self.players[pid])
            
            #If the agent doesn't return pass or fail, assume pass
            if (playerVote is not self.state.PASS and playerVote is not self.state.FAIL) or self.players[pid].loyalty == self.state.RESISTANCE:
                playerVote = self.state.PASS
            
            if playerVote == self.state.FAIL:
                fails += 1
            else:
                passes += 1
        
        result.failCount = fails
        result.passCount = passes
        result.missionTeam = team
        return result
#         if fails >= GetMaxMissionFailCount(len(self.players), roundNumber):
#             return [SPIES_WIN_ROUND, fails]
#         else:
#             return [RESISTANCE_WIN_ROUND, fails]
        
    def DoRound(self, roundNumber):
        self.state.SetCurrentMissionNumber(roundNumber)
        
        voteResults = self.DetermineTeam(roundNumber)
        
        self.state.AddVoteResults(voteResults)
        
        if voteResults is None:
            return self.SPIES_WIN_GAME
        
        result = self.ExecuteMission(voteResults[len(voteResults)-1].proposedTeam, roundNumber)
        
        self.state.AddMissionResults(result)
        
        #Return which side won the round, the fail count doesn't matter for this
        if result.Succeeded():
            return self.RESISTANCE_WIN_ROUND
        else:
            return self.SPIES_WIN_ROUND
        
    def RunGame(self):
               
        self.AssignLoyalties()
        
        resistanceWins = 0
        spyWins = 0
        result = None
        self.state.currentMission = 1
        
        while self.state.currentMission <= 5:
            result = self.DoRound(self.state.currentMission)
            if result == self.RESISTANCE_WIN_ROUND:
                resistanceWins += 1
            elif result == self.SPIES_WIN_ROUND:
                spyWins += 1
            
            if resistanceWins >= 3:
                result = self.RESISTANCE_WIN_GAME
            elif spyWins >= 3:
                result = self.SPIES_WIN_GAME
            
            if result == self.SPIES_WIN_GAME or result == self.RESISTANCE_WIN_GAME:
                break
            
            self.state.currentMission += 1
        
        if result == self.SPIES_WIN_GAME:
            self.winner = self.state.SPY
        elif result == self.RESISTANCE_WIN_GAME:
            self.winner = self.state.RESISTANCE
        #TODO victory actions? Push records to database?
        