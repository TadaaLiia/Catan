from map import Map
from player import Player
import random
from entities import *


class Gamestate:

    def __init__(self, player=4):
        self.Map = Map()

        self.Player = player
        self.Psuesch1 = Player(1)  # Player1
        self.Psuesch2 = Player(2)  # Player2
        self.Psuesch3 = Player(3)  # Player3
        self.PlayerList = [self.Psuesch1, self.Psuesch2, self.Psuesch3]
        if self.Player == 4:
            self.Psuesch4 = Player(4)
            self.PlayerList.append(self.Psuesch4)

        self.DevelopmentCards = {
            DevelopmentCards.KNIGHT_CARD: 14,
            DevelopmentCards.VICTORY_POINT_CARD: 5,
            DevelopmentCards.MONOPOLY: 2,
            DevelopmentCards.DEVELOPMENT: 2,
            DevelopmentCards.CONSTRUCTION: 2
        }
        self.CountDevCards = 25
        self.ResourceCards = dict.fromkeys(Resources, 19)

        self.Round = 0
        self.Turn = 0

        self.PlayedDev = 0
        self.Diced = 0
        self.Roll7 = 0

    # ---- cards ----
    def updateDevelopmentCards(self, card):
        jamoinmoritz = card
        assert jamoinmoritz in self.DevelopmentCards, "invalid operation"
        if self.DevelopmentCards[jamoinmoritz] == 1:
            del(self.DevelopmentCards[jamoinmoritz])
        else:
            self.DevelopmentCards[jamoinmoritz] -= 1
        self.CountDevCards -= 1

    def getRandomDevCard(self):
        # number of cards
        sum = 0
        for i in self.DevelopmentCards.values():
            sum += i
        # return random card
        rand = random.randrange(sum)
        for k, v in self.DevelopmentCards.items():
            if rand > v:
                rand -= v
            else:
                return k

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

    # ---- trade ----
    """
    def getPortsForPlayer(self, id):
        # not working
        availablePorts = []
        objects, buildings, streets = self.Map.getPlayerShit(id)
        for port in list(Ports):
            nodes = self.Map.PortDict[port.name]
            if any(building in nodes for building in buildings) is True:
                availablePorts.append(port)
        print(availablePorts)

    def trade(self, id, port):
        objects, buildings, streets = self.Map.getPlayerShit(id)
        print("gewünschte Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
        r = self.inputCheck(Resources)
        player = self.getPlayerForID(id)
        if port == Ports.NONE:
            print("zu tauschende Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
            r1 = self.inputCheck(Resources)
            if player.ResourceCards[r1] >= 4:
                self.tradex(id, 4, r1, r)
            else:
                print("no resource cards")
        elif port == Ports.PORT:
            nodes = self.Map.PortDict[port]
            if any(building in nodes for building in buildings) is False:
                print("no port")
                return
            print("zu tauschende Ressource: " + ", ".join([str(x.name) + ":" + str(x.value) for x in Resources]))
            r1 = self.inputCheck(Resources)
            if player.ResourceCards[r1] >= 3:
                self.tradex(id, 3, r1, r)
            else:
                print("no resource cards")
        else:
            nodes = self.Map.getPortDict()[port]
            if any(building in nodes for building in buildings) is False:
                print("no port")
                return
            res = Resources(port.value)
            if player.ResourceCards[res] >= 2:
                self.tradex(id, 2, res, r)
            else:
                print("no resource cards")

    def tradex(self, id, x, card1, card2):
        for i in range(x):
            self.getPlayerForID(id).updateResourceCards(card1, 0)
        self.getPlayerForID(id).updateResourceCards(card2, 1)
    """

if __name__ == "__main__":
    gs = Gamestate(3)

    # ---- Player Interaction ----

"""
    # ---- check ----
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
    """
