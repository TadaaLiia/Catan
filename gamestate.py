from map import CatanMap
from player import Player
import random

class Gamestate:

    def __init__(self, name1, name2, name3, name4=0):
        self.DevelopmentCards = self.initializeDevelopmentCards()
        self.CountDevCards = 25
        self.ResourceCards = self.initializeResourceCards()
        self.Map = CatanMap()
        self.Player1 = Player(name1)
        self.Player2 = Player(name2)
        self.Player3 = Player(name3)
        self.player = 3
        if name4 != 0:
            self.Player4 = Player(name4)
            self.player = 4
        self.PlayerList = self.initializePlayerList(self.player)
        self.Round = 0

    # ---- getter ----
    def getDevelopmentCards(self):
        return self.DevelopmentCards

    def getResourceCards(self):
        return self.ResourceCards

    def getCountDev(self):
        return self.CountDevCards

    def getRandomDevCard(self):
        '''
        update wird direkt aufgerufen, noch nicht random
        '''
        dev = list(self.getDevelopmentCards().keys())
        rand = random.randrange(len(dev))
        self.updateDevelopmentCards(dev[rand])
        return dev[rand]

    def getPlayerList(self):
        return self.PlayerList

    def getRound(self):
        return self.Round

    def getPlayerToName(self, name):
        if self.Player1.getName() == name:
            return self.Player1
        elif self.Player2.getName() == name:
            return self.Player2
        elif self.Player3.getName() == name:
            return self.Player3
        elif self.player == 4 and self.Player4.getName() == name:
            return self.Player4
        else:
            print("no player")

    # ---- Initialization ----
    def initializePlayerList(self, player):
        players = [self.Player1, self.Player2, self.Player3]
        if player == 4:
            players.append(self.Player4)
        return players

    def initializeDevelopmentCards(self):
        developmentCards = {
            "KNIGHT_CARDS": 14,
            "VICTORY_POINT_CARDS": 5,
            "MONOPOLY": 2,
            "DEVELOPMENT": 2,
            "CONSTRUCTION": 2
        }
        return developmentCards

    def initializeResourceCards(self):
        resourceCards = {
            "WHEAT": 19,
            "ORE": 19,
            "SHEEP": 19,
            "WOOD": 19,
            "CLAY": 19
        }
        return resourceCards

    # ---- update ----
    def updateDevelopmentCards(self, card):
        assert card in self.DevelopmentCards, "invalid operation"
        if self.DevelopmentCards[card] == 1:
            del(self.DevelopmentCards[card])
        else:
            self.DevelopmentCards[card] -= 1
        self.decCountDev()

    def updateResourceCards(self, card, flag=0):
        assert card in self.ResourceCards, "invalid operation"
        if flag == 1:
            assert self.ResourceCards[card] < 19, "card does not exist"
            self.ResourceCards[card] += 1
        elif self.ResourceCards[card] == 0:
            pass
        else:
            self.ResourceCards[card] -= 1

    def incRound(self):
        self.Round += 1

    def decCountDev(self):
        self.CountDevCards -= 1


if __name__ == "__main__":
    lille = Gamestate("lia", "jakob", "edgar")
    print(lille.getRandomDevCard())
