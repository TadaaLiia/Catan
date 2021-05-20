import random
from gamestate import *
from entities import *
import pickle


class Simulation:

    def __init__(self, player=4):
        self.JarvisVision = Gamestate("a", "b", "c", "d")

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
            self.JarvisVision.Roll7 = 1
            # self.roll7(self.getCurrentPlayer())
        self.JarvisVision.Diced = 1

    def endOfTurn(self):
        '''
        increments turn and round, updates CurrentPlayer
        '''
        self.JarvisVision.updateTurnPlayer()
        self.JarvisVision.PlayedDev = 0
        self.JarvisVision.Diced = 0

    def roll7(self, position=0):
        self.bandit(position)
        villages = self.JarvisVision.Map.getVillagesForTile(position)
        cities = self.JarvisVision.Map.getCitiesForTile(position)
        players = list(dict.fromkeys(villages + cities))
        for player in players:
            card = player.getRandomResourceCard()
            self.removeResourceCards(player, card)
            self.giveResourceCards(self.getCurrentPlayer().Name, card)
        self.JarvisVision.Roll7 == 0

    # ---- Interaction with JarvisVision

    def getRound(self):
        return self.JarvisVision.Round

    def getCurrentPlayer(self):
        return self.JarvisVision.OhHiMarc

    # ---- Interaction with Map ----
    def getObjectList(self):
        return self.JarvisVision.Map.ObjectList

    def getAvailableStreetPositions(self):
        return self.JarvisVision.Map.getAvailableStreets(self.getCurrentPlayer().Name)

    def getAvailableVillagePositions(self):
        return self.JarvisVision.Map.getAvailableVillages(self.getCurrentPlayer().Name, self.getRound())

    def getAvailableCityPositions(self):
        return self.JarvisVision.Map.getAvailableCities(self.getCurrentPlayer().Name, self.getRound())

    def buildObject(self, type, position):
        playerName = self.getCurrentPlayer().Name
        player = self.getCurrentPlayer()
        assert type in Objects, "invalid type"
        if type == Objects.STREET:
            assert player.ResourceCards[Resources.WOOD] != 0, "street: missing wood"
            assert player.ResourceCards[Resources.CLAY] != 0, "street: missing clay"
            self.JarvisVision.Map.buildStuff(
                playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
        elif type == Objects.VILLAGE:
            assert player.ResourceCards[Resources.WOOD] != 0, "village: missing wood"
            assert player.ResourceCards[Resources.CLAY] != 0, "village: missing clay"
            assert player.ResourceCards[Resources.SHEEP] != 0, "village: missing sheep"
            assert player.ResourceCards[Resources.WHEAT] != 0, "village: missing wheat"
            self.JarvisVision.Map.buildStuff(
                playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.WOOD)
            self.removeResourceCards(playerName, Resources.CLAY)
            self.removeResourceCards(playerName, Resources.SHEEP)
            self.removeResourceCards(playerName, Resources.WHEAT)
        elif type == Objects.CITY:
            assert player.ResourceCards[Resources.ORE] >= 3, "city: missing ore"
            assert player.ResourceCards[Resources.WHEAT] >= 2, "city: missing wheat"
            self.JarvisVision.Map.buildStuff(
                playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.ORE)
            self.removeResourceCards(playerName, Resources.WHEAT)
            self.removeResourceCards(playerName, Resources.WHEAT)

    def getLegalBanditPositions(self):
        pos = []
        for count, tile in enumerate(self.JarvisVision.Map.TileList):
            if tile[0] != Tiles.OCEAN and tile[0] != Tiles.DESERT:
                pos.append(count)
        if self.JarvisVision.Map.BanditPosition in pos:
            pos.remove(self.JarvisVision.Map.BanditPosition)
        return pos

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
        self.JarvisVision.nextCurrentPlayer()

    def giveResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.JarvisVision.getPlayerForName(
                playerName).updateResourceCards(card, 1)

    def removeResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.JarvisVision.getPlayerForName(
                playerName).updateResourceCards(card, 0)

    def handOutCards(self, roll):
        tiles = self.JarvisVision.Map.getTilesForValue(roll)
        players = self.JarvisVision.PlayerList
        for tile in tiles:
            villages = self.JarvisVision.Map.getVillagesForTile(tile[0])
            cities = self.JarvisVision.Map.getCitiesForTile(tile[0])
            for player in players:
                for v in villages:
                    if v == player.Name:
                        self.giveResourceCards(player.Name, tile[1])
                for c in cities:
                    if c == player.Name:
                        self.giveResourceCards(player.Name, tile[1], 2)

    def drawDevelopmentCard(self):
        playerName = self.getCurrentPlayer().Name
        assert self.getCurrentPlayer().ResourceCards[
            Resources.SHEEP] != 0, "missing sheep"
        assert self.getCurrentPlayer().ResourceCards[
            Resources.ORE] != 0, "missing ore"
        assert self.getCurrentPlayer().ResourceCards[
            Resources.WHEAT] != 0, "missing wheat"
        card = self.JarvisVision.getRandomDevCard()
        self.removeResourceCards(playerName, Resources.SHEEP)
        self.removeResourceCards(playerName, Resources.ORE)
        self.removeResourceCards(playerName, Resources.WHEAT)
        self.JarvisVision.OhHiMarc.updateDevelopmentCards(card, self.getRound())

    def playDevelopmentCard(self, devCard):
        playerName = self.getCurrentPlayer().Name
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

    def getPlayerForName(self, name):
        return self.JarvisVision.getPlayerForName(name)

    # ---- interaction with Bot ----

    def getLegalMoves(self):
        methods = {
            "playDevCard": self.playDevelopmentCard,
            "roll": self.roll,
            "roll7": self.roll7,
            "buildObject": self.buildObject,
            "drawDevCard": self.drawDevelopmentCard,
            "endOfTurn": self.endOfTurn
        }
        legalMoves = []
        player = self.getCurrentPlayer()

        devCards = []
        if self.JarvisVision.PlayedDev == 0:
            for card in player.DevelopmentCards:
                if card[1] != self.getRound():
                    devCards.append(card[0])

        legalMoves.extend([(methods["playDevCard"], [card]) for card in devCards if (
            card == DevelopmentCards.KNIGHT_CARD or self.JarvisVision.Diced != 0)])

        if self.JarvisVision.Diced == 0:
            legalMoves.append((methods["roll"], []))
        # elif self.JarvisVision.Roll7 == 1:
        #    positions = self.getLegalBanditPositions()
        #    rand = random.randrange(len(positions))
        #    legalMoves.append((methods["roll7"], positions[rand]))
        else:
            legalMoves.append((methods["endOfTurn"], []))
            # build
            if player.ResourceCards[Resources.WOOD] != 0 and player.ResourceCards[Resources.CLAY] != 0:
                streets = self.getAvailableStreetPositions()
                for street in streets:
                    legalMoves.append((methods["buildObject"], [Objects.STREET, street]))

            if player.ResourceCards[Resources.WOOD] != 0 and player.ResourceCards[Resources.CLAY] != 0 and player.ResourceCards[Resources.SHEEP] != 0 and player.ResourceCards[Resources.WHEAT] != 0:
                villages = self.getAvailableVillagePositions()
                for village in villages:
                    legalMoves.append((methods["buildObject"], [Objects.VILLAGE, village]))

            if player.ResourceCards[Resources.ORE] >= 3 and player.ResourceCards[Resources.WHEAT] >= 2:
                cities = self.getAvailableCityPositions()
                for city in cities:
                    legalMoves.append((methods["buildObject"], [Objects.CITY, city]))
            # draw dev
            if player.ResourceCards[Resources.ORE] != 0 and player.ResourceCards[Resources.WHEAT] != 0 and player.ResourceCards[Resources.SHEEP] != 0:
                legalMoves.append((methods["drawDevCard"], []))
            # trade
        return legalMoves

    def getRandomLegalMove(self):
        legalMoves = self.getLegalMoves()
        rand = random.randrange(len(legalMoves))
        return legalMoves[rand]

    def getNextGamestate(self, legalMove):
        legalMove[0](*legalMove[1])
        # return self.JarvisVision

if __name__ == "__main__":
    sim = Simulation()

    sim.priorityRoll(3)
    # round 0
    res = [(Resources.WOOD, 10), (Resources.CLAY, 10), (Resources.WHEAT, 10), (Resources.SHEEP, 10), (Resources.ORE, 10)]
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().Name, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (10, 11, 17))
    sim.buildObject(Objects.VILLAGE, (18, 24, 25))
    sim.buildObject(Objects.STREET, (10, 17))
    sim.buildObject(Objects.STREET, (24, 25))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().Name, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (23, 24, 29))
    sim.buildObject(Objects.VILLAGE, (12, 13, 19))
    sim.buildObject(Objects.STREET, (13, 19))
    sim.buildObject(Objects.STREET, (23, 24))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().Name, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (29, 33, 34))
    sim.buildObject(Objects.VILLAGE, (30, 34, 35))
    sim.buildObject(Objects.STREET, (29, 33))
    sim.buildObject(Objects.STREET, (30, 34))
    sim.endOfTurn()
    sim.save("saves/gs1")
    print(sim.JarvisVision.Diced)


    sim.load("saves/gs1")

    print("Round:" + str(sim.getRound()))
    sim.drawDevelopmentCard()
    sim.drawDevelopmentCard()
    sim.getNextGamestate(sim.getRandomLegalMove())
    #print(sim.getLegalMoves())

    sim.endOfTurn()
    sim.getRandomLegalMove()
    # sim.JarvisVision.getPortsForPlayer(sim.getCurrentPlayer().getName())
    sim.endOfTurn()
    sim.getRandomLegalMove()
    # sim.JarvisVision.getPortsForPlayer(sim.getCurrentPlayer().getName())
    sim.endOfTurn()
    sim.getRandomLegalMove()
    # sim.JarvisVision.getPortsForPlayer(sim.getCurrentPlayer().getName())
    #print(sim.getLegalMoves())
    sim.roll()
    sim.getRandomLegalMove()
    # print(sim.getLegalMoves())
    sim.endOfTurn()
    # print(sim.getLegalMoves())
