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

    def inputCheck(self):
        try:
            i = int(input("> "))
        except ValueError:
            i = self.inputCheck()
        return i

    # ---- getter ----
    def getDevelopmentCards(self):
        return self.DevelopmentCards

    def getResourceCards(self):
        return self.ResourceCards

    def getCountDev(self):
        return self.CountDevCards

    def getRandomDevCard(self):
        '''
        update wird direkt aufgerufen
        '''
        sum = 0
        for i in self.getDevelopmentCards().values():
            sum += i
        rand = random.randrange(sum)
        for k, v in self.getDevelopmentCards().items():
            if rand > v:
                rand -= v
            else:
                return k

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
            "KNIGHT_CARD": 14,
            "VICTORY_POINT_CARD": 5,
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

    # ---- Development cards
    def KNIGHTCARD(self, playerName):
        print("position:")
        position = self.inputCheck()
        # self.getPlayerToName(playerName).updateDevelopmentCards("KNIGHT_CARD")
        self.Map.setBanditPosition(position)

    def VICTORYPOINTCARD(self, playerName):
        self.getPlayerToName(playerName).updateVictoryPoints()

    def CONSTRUCTION(self, playerName):
        """
        input check, positionen checken
        """
        position1 = input()
        position2 = input()
        self.Map.buildStuff(playerName, "STREET", position1, self.getRound())
        self.Map.buildStuff(playerName, "STREET", position2, self.getRound())

    def MONOPOLY(self, playerName, resourceCard):
        assert resourceCard in self.getResourceCards(), "invalid resourceCard"
        sum = 0
        for player in self.getPlayerList():
            i = player.getResourceCards()[resourceCard]
            sum += i
            for j in range(i):
                player.updateResourceCards(resourceCard, 0)
        for i in range(sum):
            self.getPlayerToName(playerName).updateResourceCards(resourceCard, 1)

    def DEVELOPMENT(self, playerName, resourceCard1, resourceCard2):
        self.getPlayerToName(playerName).updateResourceCards(resourceCard1, 1)
        self.getPlayerToName(playerName).updateResourceCards(resourceCard2, 1)

    # ---- trade ----
    def trade3(self, playerName, card1, card2):
        assert card1 in self.getResourceCards(), "invalid card"
        assert card2 in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()[card1] >= 3, "you need 3 cards"
        nodes = [(0, 1, 5), (0, 4, 5), (7, 8, 13), (8, 13, 14), (14, 20, 21), (20, 21, 27), (28, 29, 33), (29, 33, 34)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(3, card1, card2)
                return
        raise Exception("no 3:1 port")

    def sheepTrade(self, playerName, card):
        assert card in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()["SHEEP"] >= 2, "you need 2 cards"
        nodes = [(1, 2, 6), (2, 6, 7)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(2, "SHEEP", card)
                return
        raise Exception("no sheep port")

    def oreTrade(self, playerName, card):
        assert card in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()["ORE"] >= 2, "you need 2 cards"
        nodes = [(4, 9, 10), (9, 10, 16)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(2, "ORE", card)
                return
        raise Exception("no ore port")

    def wheatTrade(self, playerName, card):
        assert card in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()["WHEAT"] >= 2, "you need 2 cards"
        nodes = [(16, 22, 23), (22, 23, 28)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(2, "WHEAT", card)
                return
        raise Exception("no wheat port")

    def clayTrade(self, playerName, card):
        assert card in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()["CLAY"] >= 2, "you need 2 cards"
        nodes = [(26, 27, 32), (26, 31, 32)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(2, "CLAY", card)
                return
        raise Exception("no clay port")

    def woodTrade(self, playerName, card):
        assert card in self.getResourceCards(), "invalid card"
        assert self.getPlayerToName(playerName).getResourceCards()["WOOD"] >= 2, "you need 2 cards"
        nodes = [(30, 31, 35), (30, 34, 35)]
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for building in buildings:
            if building in nodes:
                self.getPlayerToName(playerName).trade(2, "WOOD", card)
                return
        raise Exception("no wood port")


if __name__ == "__main__":
    lille = Gamestate("lia", "jakob", "edgar")
    print(lille.getRandomDevCard())
