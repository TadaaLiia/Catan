from gamestate import Gamestate
import random
from entities import *
import pickle


class Simulation:

    def __init__(self, gamestate, player=4):
        self.JarvisVision = gamestate
        self.methods = self.initializeMethodMapping()

    def save(self, filename):
        # create a pickle file
        picklefile = open(filename, 'wb')
        # pickle the dictionary and write it to file
        pickle.dump(self.JarvisVision, picklefile)
        # close the file
        picklefile.close()

    def load(self, filename):
        # read the pickle file
        picklefile = open(filename, 'rb')
        # unpickle the dataframe
        self.JarvisVision = pickle.load(picklefile)
        # close file
        picklefile.close()

    # ---- turn ----

    def inputCheck(self):
        try:
            i = int(input("> "))
        except ValueError:
            i = self.inputCheck()
        return i

    def roll(self):
        r = random.randrange(1, 7) + random.randrange(1, 7)
        if r != 7:
            self.handOutCards(r)
        else:
            self.roll7(self.getCurrentPlayer())
        self.JarvisVision.setDiced(1)

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
        '''
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
        self.JarvisVision.setPlayedDev(0)
        self.JarvisVision.setDiced(0)

    def roll7(self, position=0):
        # print("bandit position")
        # position = self.inputCheck()
        self.bandit(position)
        villages = self.JarvisVision.Map.getVillagesToTile(position)
        cities = self.JarvisVision.Map.getCitiesToTile(position)
        players = list(dict.fromkeys(villages + cities))
        for player in players:
            card = player.getRandomResourceCard()
            self.removeResourceCards(player, card)
            self.giveResourceCards(self.getCurrentPlayer().getName(), card)

    # ---- Interaction with JarvisVision

    def getRound(self):
        return self.JarvisVision.getRound()

    def getCurrentPlayer(self):
        return self.JarvisVision.getCurrentPlayer()

    # ---- Interaction with CatanMap ----
    def getObjectList(self):
        return self.JarvisVision.Map.getObjectList()

    def getAvailableStreetPositions(self):
        return self.JarvisVision.Map.getAvailableStreets(self.getCurrentPlayer().getName())

    def getAvailableVillagePositions(self):
        return self.JarvisVision.Map.getAvailableVillages(self.getCurrentPlayer().getName(), self.getRound())

    def getAvailableCityPositions(self):
        return self.JarvisVision.Map.getAvailableCities(self.getCurrentPlayer().getName(), self.getRound())

    def buildObject(self, type, position):
        playerName = self.getCurrentPlayer().getName()
        player = self.getCurrentPlayer()
        assert type in Objects, "invalid type"
        if type == Objects.STREET:
            assert player.getResourceCards()[Resources.WOOD] != 0, "street: missing wood"
            assert player.getResourceCards()[Resources.CLAY] != 0, "street: missing clay"
            self.JarvisVision.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
        elif type == Objects.VILLAGE:
            assert player.getResourceCards()[Resources.WOOD] != 0, "village: missing wood"
            assert player.getResourceCards()[Resources.CLAY] != 0, "village: missing clay"
            assert player.getResourceCards()[Resources.SHEEP] != 0, "village: missing sheep"
            assert player.getResourceCards()[Resources.WHEAT] != 0, "village: missing wheat"
            self.JarvisVision.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
            self.removeResourceCards(playerName, Resources.SHEEP)
            self.removeResourceCards(playerName, Resources.WHEAT)
        elif type == Objects.CITY:
            assert player.getResourceCards()[Resources.ORE] >= 3, "city: missing ore"
            assert player.getResourceCards()[Resources.WHEAT] >= 2, "city: missing wheat"
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
        begin = random.randrange(player)
        self.JarvisVision.Psuesch1.Priority = (1 + begin) % player
        self.JarvisVision.Psuesch2.Priority = (2 + begin) % player
        self.JarvisVision.Psuesch3.Priority = (3 + begin) % player
        if player == 4:
            self.JarvisVision.Psuesch4.Priority = (4 + begin) % player
        self.JarvisVision.setCurrentPlayer()

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

    def drawDevelopmentCard(self):
        playerName = self.getCurrentPlayer().getName()
        assert self.getCurrentPlayer().getResourceCards()[Resources.SHEEP] != 0, "missing sheep"
        assert self.getCurrentPlayer().getResourceCards()[Resources.ORE] != 0, "missing ore"
        assert self.getCurrentPlayer().getResourceCards()[Resources.WHEAT] != 0, "missing wheat"
        card = self.JarvisVision.getRandomDevCard()
        self.removeResourceCards(playerName, Resources.SHEEP)
        self.removeResourceCards(playerName, Resources.ORE)
        self.removeResourceCards(playerName, Resources.WHEAT)
        self.JarvisVision.getCurrentPlayer().updateDevelopmentCards(card, self.getRound())

    def playDevelopmentCard(self, devCard):
        playerName = self.getCurrentPlayer().getName()
        r = self.getCurrentPlayer().updateDevelopmentCards(devCard, self.getRound(), 1)
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

    # ---- interaction with Bot ----

    def initializeMethodMapping(self):
        methods = {
            "playDevCard": self.playDevelopmentCard,
            "roll": self.roll,
            "buildObject": self.buildObject,
            "drawDevCard": self.drawDevelopmentCard
        }
        return methods

    def getLegalMoves(self):
        legalMoves = []
        player = self.getCurrentPlayer()

        devCards = []
        if self.JarvisVision.getPlayedDev() == 0:
            for card in player.getDevelopmentCards():
                if card[1] != self.getRound():
                    devCards.append(card[0])

        legalMoves.extend([(self.methods["playDevCard"], card) for card in devCards if (card == DevelopmentCards.KNIGHT_CARD or self.JarvisVision.getDiced() != 0)])

        if self.JarvisVision.getDiced() == 0:
            legalMoves.append((self.methods["roll"], None))
        else:
            # build
            if player.getResourceCards()[Resources.WOOD] != 0 and player.getResourceCards()[Resources.CLAY] != 0:
                streets = self.getAvailableStreetPositions()
                for street in streets:
                    legalMoves.append((self.methods["buildObject"], street))

            if player.getResourceCards()[Resources.WOOD] != 0 and player.getResourceCards()[Resources.CLAY] != 0 and player.getResourceCards()[Resources.SHEEP] != 0 and player.getResourceCards()[Resources.WHEAT] != 0:
                villages = self.getAvailableVillagePositions()
                for village in villages:
                    legalMoves.append((self.methods["buildObject"], village))

            if player.getResourceCards()[Resources.ORE] >= 3 and player.getResourceCards()[Resources.WHEAT] >= 2:
                cities = self.getAvailableCityPositions()
                for city in cities:
                    legalMoves.append((self.methods["buildObject"], city))
            # draw dev
            if player.getResourceCards()[Resources.ORE] != 0 and player.getResourceCards()[Resources.WHEAT] != 0 and player.getResourceCards()[Resources.SHEEP] != 0:
                legalMoves.append((self.methods["drawDevCard"], None))
            # trade
        return legalMoves


if __name__ == "__main__":
    gs = Gamestate("maxspdcbr", "jamoinmoritz", "edgar")
    sim = Simulation(gs)

    sim.load("gs1")

    print("Round:" + str(sim.getRound()))
    sim.drawDevelopmentCard()
    sim.drawDevelopmentCard()
    print(sim.getLegalMoves())

    sim.endOfTurn()
    # sim.JarvisVision.getPortsToPlayer(sim.getCurrentPlayer().getName())
    sim.endOfTurn()
    # sim.JarvisVision.getPortsToPlayer(sim.getCurrentPlayer().getName())
    sim.endOfTurn()
    # sim.JarvisVision.getPortsToPlayer(sim.getCurrentPlayer().getName())
    print(sim.getLegalMoves())
    sim.roll()
    print(sim.getLegalMoves())
    sim.endOfTurn()
    print(sim.getLegalMoves())



'''
Code zu GS1:
    sim.priorityRoll(3)
    # round 0
    res = [(Resources.WOOD, 10), (Resources.CLAY, 10), (Resources.WHEAT, 10), (Resources.SHEEP, 10), (Resources.ORE, 10)]
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().getName(), i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (10, 11, 17))
    sim.buildObject(Objects.VILLAGE, (18, 24, 25))
    sim.buildObject(Objects.STREET, (10, 17))
    sim.buildObject(Objects.STREET, (24, 25))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().getName(), i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (23, 24, 29))
    sim.buildObject(Objects.VILLAGE, (12, 13, 19))
    sim.buildObject(Objects.STREET, (13, 19))
    sim.buildObject(Objects.STREET, (23, 24))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().getName(), i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (29, 33, 34))
    sim.buildObject(Objects.VILLAGE, (30, 34, 35))
    sim.buildObject(Objects.STREET, (29, 33))
    sim.buildObject(Objects.STREET, (30, 34))
    sim.endOfTurn()
    sim.save("gs1")
    print(sim.JarvisVision.Diced)
'''

"""


"""
