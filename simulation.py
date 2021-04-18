from gamestate import Gamestate
import random
from entities import *

class Simulation:

    def __init__(self, gamestate, player=4):
        self.JarvisVision = gamestate

    # ---- turn ----
    def inputCheck(self):
        try:
            i = int(input("> "))
        except ValueError:
            i = self.inputCheck()
        return i

    def roll(self):
        return random.randrange(1, 7) + random.randrange(1, 7)

    def turn(self, playerName):
        """
        for card in self.JarvisVision.getPlayerToName(playerName).getDevelopmentCards():
            if DevelopmentCards.KNIGHT_CARD == card[0]:
                print("1: play knight card, 0: skip")
                answer = self.inputCheck()
                if answer == 1:
                    self.playDevelopmentCard(playerName, DevelopmentCards.KNIGHT_CARD)
                break
        """
        r = self.roll()
        print("roll " + str(r))
        if r != 7:
            self.handOutCards(r)
        else:
            self.roll7(playerName)
        '''
        # option1: devcard speilen
        # option2: traden
        # option3:bauen
        # option4: exit
        while True:
            print("1: DevCard, 2: Trade, 3: Build, 4: exit")
            option = input("> ")
            if option == str(1):
                card = self.getPlayerToName(playerName).chooseDevCard()
                self.playDevelopmentCard(playerName, card)
            elif option == str(2):
                pass
            elif option == str(3):
                pass
            elif option == str(4):
                break
            else:
                print("invalid input")
        '''

    def endOfTurn(self):
        '''
        increments turn and round, updates CurrentPlayer
        '''
        self.JarvisVision.updateTurnPlayer()

    def roll7(self, playerName, position):
        # print("bandit position")
        # position = self.inputCheck()
        self.bandit(position)
        villages = self.JarvisVision.Map.getVillagesToTile(position)
        cities = self.JarvisVision.Map.getCitiesToTile(position)
        players = list(dict.fromkeys(villages + cities))
        for player in players:
            card = self.getPlayerToName(player).getRandomResourceCard()
            self.removeResourceCards(player, card)
            self.giveResourceCards(playerName, card)

    # ---- Interaction with JarvisVision

    def getRound(self):
        return self.JarvisVision.getRound()

    def getCurrentPlayer(self):
        return self.JarvisVision.getCurrentPlayer()

    # ---- Interaction with CatanMap ----
    def getObjectList(self):
        return self.JarvisVision.Map.getObjectList()

    def getAvailableStreetPositions(self, playerName):
        return self.JarvisVision.Map.getAvailableStreets(playerName)

    def getAvailableVillagePositions(self, playerName):
        return self.JarvisVision.Map.getAvailableVillages(playerName, self.getRound())

    def getAvailableCityPositions(self, playerName):
        return self.JarvisVision.Map.getAvailableCities(playerName, self.getRound())

    def buildObject(self, playerName, type, position):
        assert type in Objects, "invalid type"
        if type == Objects.STREET:
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.WOOD] != 0, "street: missing wood"
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.CLAY] != 0, "street: missing clay"
            self.JarvisVision.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
        elif type == Objects.VILLAGE:
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.WOOD] != 0, "village: missing wood"
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.CLAY] != 0, "village: missing clay"
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.SHEEP] != 0, "village: missing sheep"
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.WHEAT] != 0, "village: missing wheat"
            self.JarvisVision.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
            self.removeResourceCards(playerName, Resources.SHEEP)
            self.removeResourceCards(playerName, Resources.WHEAT)
        elif type == Objects.CITY:
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.ORE] >= 3, "city: missing ore"
            assert self.getPlayerToName(playerName).getResourceCards()[Resources.WHEAT] >= 2, "city: missing wheat"
            self.JarvisVision.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.WHEAT)
            self.removeResourceCards(playerName, Resources.WHEAT)

    def bandit(self, position):
        self.JarvisVision.Map.setBanditPosition(position)

    # ---- Interaction with Player ----
    def priorityRoll(self, player=4):
        begin = random.randrange(player) + 1
        self.JarvisVision.Player1.Priority = (1 + begin) % player + 1
        self.JarvisVision.Player2.Priority = (2 + begin) % player + 1
        self.JarvisVision.Player3.Priority = (3 + begin) % player + 1
        if player == 4:
            self.JarvisVision.Player4.Priority = (4 + begin) % player + 1

    def giveResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.JarvisVision.getPlayerToName(playerName).updateResourceCards(card, 1)

    def removeResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.JarvisVision.getPlayerToName(playerName).updateResourceCards(card, 0)

    def handOutCards(self, roll):
        tiles = self.JarvisVision.Map.getTilesToValue(roll)
        players = self.JarvisVision.getPlayerList()
        for tile in tiles:
            villages = self.JarvisVision.Map.getVillagesToTile(tile[0])
            cities = self.JarvisVision.Map.getCitiesToTile(tile[0])
            for player in players:
                for v in villages:
                    if v == player.getName():
                        self.giveResourceCards(player.getName(), tile[1])
                for c in cities:
                    if c == player.getName():
                        self.giveResourceCards(player.getName(), tile[1], 2)

    def drawDevelopmentCard(self, playerName):
        assert self.getPlayerToName(playerName).getResourceCards()[Resources.SHEEP] != 0, "missing sheep"
        assert self.getPlayerToName(playerName).getResourceCards()[Resources.ORE] != 0, "missing ore"
        assert self.getPlayerToName(playerName).getResourceCards()[Resources.WHEAT] != 0, "missing wheat"
        card = self.JarvisVision.getRandomDevCard()
        self.JarvisVision.getPlayerToName(playerName).updateDevelopmentCards(card, self.getRound())

    def playDevelopmentCard(self, playerName, devCard):
        r = self.getPlayerToName(playerName).updateDevelopmentCards(devCard, self.getRound(), 1)
        if r == 1:
            if devCard == DevelopmentCards.KNIGHT_CARD:
                self.JarvisVision.KNIGHTCARD(playerName)
            elif devCard == DevelopmentCards.VICTORY_POINT_CARD:
                self.JarvisVision.VICTORYPOINTCARD(playerName)
            elif devCard == DevelopmentCards.MONOPOLY:
                self.JarvisVision.MONOPOLY(playerName)
            elif devCard == DevelopmentCards.DEVELOPMENT:
                self.JarvisVision.DEVELOPMENT(playerName)
            elif devCard == DevelopmentCards.CONSTRUCTION:
                self.JarvisVision.CONSTRUCTION(playerName)

    def getPlayerToName(self, name):
        return self.JarvisVision.getPlayerToName(name)

    def getLegalMoves(self, playerName):
        # Developmentcards spielen
        # 1x roll
        


if __name__ == "__main__":
    gs = Gamestate("maxspdcbr", "jamoinmoritz", "edgar")
    sim = Simulation(gs)
    sim.giveResourceCards("jamoinmoritz", Resources.WOOD, 10)
    sim.giveResourceCards("jamoinmoritz", Resources.CLAY, 10)
    sim.giveResourceCards("jamoinmoritz", Resources.WHEAT, 10)
    sim.giveResourceCards("jamoinmoritz", Resources.SHEEP, 10)
    sim.giveResourceCards("jamoinmoritz", Resources.ORE, 10)
    sim.giveResourceCards("maxspdcbr", Resources.WOOD, 10)
    sim.giveResourceCards("maxspdcbr", Resources.CLAY, 10)
    sim.giveResourceCards("maxspdcbr", Resources.WHEAT, 10)
    sim.giveResourceCards("maxspdcbr", Resources.SHEEP, 10)
    sim.giveResourceCards("maxspdcbr", Resources.ORE, 10)
    sim.giveResourceCards("edgar", Resources.WOOD, 10)
    sim.giveResourceCards("edgar", Resources.CLAY, 10)
    sim.giveResourceCards("edgar", Resources.WHEAT, 10)
    sim.giveResourceCards("edgar", Resources.SHEEP, 10)
    sim.giveResourceCards("edgar", Resources.ORE, 10)
    sim.buildObject("jamoinmoritz", Objects.VILLAGE, (10, 11, 17))
    sim.buildObject("jamoinmoritz", Objects.VILLAGE, (18, 24, 25))
    sim.buildObject("jamoinmoritz", Objects.STREET, (10, 17))
    sim.buildObject("jamoinmoritz", Objects.STREET, (24, 25))
    sim.buildObject("maxspdcbr", Objects.VILLAGE, (23, 24, 29))
    sim.buildObject("maxspdcbr", Objects.VILLAGE, (12, 13, 19))
    sim.buildObject("maxspdcbr", Objects.STREET, (13, 19))
    sim.buildObject("maxspdcbr", Objects.STREET, (23, 24))
    sim.buildObject("edgar", Objects.VILLAGE, (29, 33, 34))
    sim.buildObject("edgar", Objects.VILLAGE, (30, 34, 35))
    sim.buildObject("edgar", Objects.STREET, (29, 33))
    sim.buildObject("edgar", Objects.STREET, (30, 34))
    sim.incRound()
    # print(sim.JarvisVision.getPlayerToName("edgar").getResourceCards())
    # sim.JarvisVision.trade("edgar", Ports.CLAY)
    # print(sim.JarvisVision.getPlayerToName("edgar").getResourceCards())
# liste der moves
# naechster JarvisVision nach move
# simulate random game: 1 gewonnen
