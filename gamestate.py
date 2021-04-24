from map import CatanMap
from player import Player
import random
from entities import *


class Gamestate:

    def __init__(self, name1, name2, name3, name4=0):
        self.DevelopmentCards = self.initializeDevelopmentCards()
        self.CountDevCards = 25
        self.ResourceCards = self.initializeResourceCards()
        self.Map = CatanMap()
        self.Psuesch1 = Player(name1)  # Player1
        self.Psuesch2 = Player(name2)   # Player2
        self.Psuesch3 = Player(name3)   # Player3
        self.player = 3
        if name4 != 0:
            self.Psuesch4 = Player(name4)
            self.player = 4
        self.PlayerList = self.initializePlayerList(self.player)
        self.Round = 0
        self.Turn = 0
        self.OhHiMarc = self.setCurrentPlayer()  # currentPlayer
        self.PlayedDev = 0
        self.Diced = 0

    def inputCheck(self, type):
        try:
            if type == int:
                i = int(input("> "))
            elif type == tuple:
                i = tuple(int(x) for x in input("> ").split(','))
            elif type == Resources:
                i = int(input("> "))
                return Resources(i)
            else:
                i = None
        except ValueError:
            i = self.inputCheck(type)
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

    def getTurn(self):
        return self.Turn

    def getPlayer(self):
        return self.player

    def getCurrentPlayer(self):
        return self.OhHiMarc

    def getPlayerForName(self, name):
        if self.Psuesch1.getName() == name:
            return self.Psuesch1
        elif self.Psuesch2.getName() == name:
            return self.Psuesch2
        elif self.Psuesch3.getName() == name:
            return self.Psuesch3
        elif self.player == 4 and self.Psuesch4.getName() == name:
            return self.Psuesch4
        else:
            print("no player")

    def getDiced(self):
        return self.Diced

    def getPlayedDev(self):
        return self.PlayedDev

    # ---- setter ----
    def setCurrentPlayer(self):
        for player in self.getPlayerList():
            if self.Turn == player.getPriority():
                self.OhHiMarc = player

    def setDiced(self, i):
        self.Diced = i

    def setPlayedDev(self, i):
        self.PlayedDev = i

    # ---- Initialization ----
    def initializePlayerList(self, player):
        players = [self.Psuesch1, self.Psuesch2, self.Psuesch3]
        if player == 4:
            players.append(self.Psuesch4)
        return players

    def initializeDevelopmentCards(self):
        developmentCards = {
            DevelopmentCards.KNIGHT_CARD: 14,
            DevelopmentCards.VICTORY_POINT_CARD: 5,
            DevelopmentCards.MONOPOLY: 2,
            DevelopmentCards.DEVELOPMENT: 2,
            DevelopmentCards.CONSTRUCTION: 2
        }
        return developmentCards

    def initializeResourceCards(self):
        return dict.fromkeys(Resources, 19)

    # ---- update ----
    def updateDevelopmentCards(self, card):
        jamoinmoritz = card
        assert jamoinmoritz in self.DevelopmentCards, "invalid operation"
        if self.DevelopmentCards[jamoinmoritz] == 1:
            del(self.DevelopmentCards[jamoinmoritz])
        else:
            self.DevelopmentCards[jamoinmoritz] -= 1
        self.decCountDev()

    def updateResourceCards(self, card, flag=0):
        jamoinmoritz = card
        assert jamoinmoritz in self.ResourceCards, "invalid operation"
        if flag == 1:
            assert self.ResourceCards[jamoinmoritz] < 19, "card does not exist"
            self.ResourceCards[jamoinmoritz] += 1
        elif self.ResourceCards[jamoinmoritz] == 0:
            pass
        else:
            self.ResourceCards[jamoinmoritz] -= 1

    def incRound(self):
        self.Round += 1

    def updateTurnPlayer(self):
        self.Turn += 1
        self.Turn = self.getTurn() % self.getPlayer()
        if self.getTurn() == 0:
            self.incRound()
        self.setCurrentPlayer()

    def decCountDev(self):
        self.CountDevCards -= 1

    # ---- Development cards ----
    def KNIGHTCARD(self, playerName, position):
        self.Map.setBanditPosition(position)
        self.getPlayerForName(playerName).updatePlayedKnightCards()

    def VICTORYPOINTCARD(self, playerName):
        self.getPlayerForName(playerName).updateVictoryPoints()

    def CONSTRUCTION(self, playerName, position1, position2):
        self.Map.buildStuff(playerName, Objects.STREET, position1, self.getRound())
        self.Map.buildStuff(playerName, Objects.STREET, position2, self.getRound())

    def MONOPOLY(self, playerName, resourceCard):
        for sum, player in enumerate(self.getPlayerList()):
            i = player.getResourceCards()[resourceCard]
            for j in range(i):
                player.updateResourceCards(resourceCard, 0)
        for i in range(sum):
            self.getPlayerForName(playerName).updateResourceCards(resourceCard, 1)

    def DEVELOPMENT(self, playerName, resourceCard1, resourceCard2):
        self.getPlayerForName(playerName).updateResourceCards(resourceCard1, 1)
        self.getPlayerForName(playerName).updateResourceCards(resourceCard2, 1)

    # ---- trade ----
    def getPortsForPlayer(self, playerName):
        # not working
        availablePorts = []
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        for port in list(Ports):
            nodes = self.Map.getPortDict()[port.name]
            if any(building in nodes for building in buildings) is True:
                availablePorts.append(port)
        print(availablePorts)

    def trade(self, playerName, port):
        objects, buildings, streets = self.Map.getPlayerShit(playerName)
        print("gewünschte Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
        r = self.inputCheck(Resources)
        player = self.getPlayerForName(playerName)
        if port == Ports.NONE:
            print("zu tauschende Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
            r1 = self.inputCheck(Resources)
            if player.getResourceCards()[r1] >= 4:
                self.tradex(playerName, 4, r1, r)
            else:
                print("no resource cards")
        elif port == Ports.PORT:
            nodes = self.Map.getPortDict()[port]
            if any(building in nodes for building in buildings) is False:
                print("no port")
                return
            print("zu tauschende Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
            r1 = self.inputCheck(Resources)
            if player.getResourceCards()[r1] >= 3:
                self.tradex(playerName, 3, r1, r)
            else:
                print("no resource cards")
        else:
            nodes = self.Map.getPortDict()[port]
            if any(building in nodes for building in buildings) is False:
                print("no port")
                return
            res = Resources(port.value)
            if player.getResourceCards()[res] >= 2:
                self.tradex(playerName, 2, res, r)
            else:
                print("no resource cards")

    def tradex(self, playerName, x, card1, card2):
        for i in range(x):
            self.getPlayerForName(playerName).updateResourceCards(card1, 0)
        self.getPlayerForName(playerName).updateResourceCards(card2, 1)


if __name__ == "__main__":
    gs = Gamestate("lia", "jakob", "edgar")
    gs.getPlayerForName("")
