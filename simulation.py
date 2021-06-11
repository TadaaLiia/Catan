import random
from gamestate import *
from entities import *
import pickle


class Simulation:

    def __init__(self, player=4):
        self.GS = Gamestate(player)
        self.priorityRoll()

    # ---- initialisation ----
    def priorityRoll(self):
        player = self.GS.Player
        begin = random.randrange(player)
        self.GS.Psuesch1.Priority = (1 + begin) % player
        self.GS.Psuesch2.Priority = (2 + begin) % player
        self.GS.Psuesch3.Priority = (3 + begin) % player
        if player == 4:
            self.GS.Psuesch4.Priority = (4 + begin) % player

    # ---- load, safe Gamestate ----
    def save(self, filename):
        # create a pickle file
        picklefile = open(filename, 'wb')
        # pickle the dictionary and write it to file
        pickle.dump(self.GS, picklefile)
        # close the file
        picklefile.close()

    def load(self, filename):
        # read the pickle file
        picklefile = open(filename, 'rb')
        # unpickle the dataframe
        self.GS = pickle.load(picklefile)
        # close file
        picklefile.close()

    # ---- round ----
    def getRound(self):
        return self.GS.Round

    def getCurrentPlayer(self):
        # current player <=> turn == priority
        for player in self.GS.PlayerList:
            if self.GS.Turn == player.Priority:
                return player

    def endOfTurn(self):
        '''
        increments turn and round, updates CurrentPlayer
        '''
        self.GS.Turn = (self.GS.Turn + 1) % self.GS.Player
        if self.GS.Turn == 0:
            # inc Round
            self.GS.Round += 1
        self.GS.PlayedDev = 0
        self.GS.Diced = 0
        self.GS.Roll7 = 0

    # ---- turn ----
    def roll(self):
        r = random.randrange(1, 7) + random.randrange(1, 7)
        print(r)
        if r != 7:
            self.handOutCards(r)
        else:
            self.GS.Roll7 = 1
            # self.roll7(self.getCurrentPlayer())
        self.GS.Diced = 1

    def roll7(self, position=0):
        self.setBanditPosition(position)
        villages = self.GS.Map.getVillagesForTile(position)
        cities = self.GS.Map.getCitiesForTile(position)
        players = list(dict.fromkeys(villages + cities))
        for id in players:
            card = self.getPlayerForID(id).getRandomResourceCard()
            self.removeResourceCards(id, card)
            self.giveResourceCards(self.getCurrentPlayer().ID, card)
        self.GS.Roll7 == 0

    # ---- Interaction with Map ----
    def getObjectList(self):
        return self.GS.Map.ObjectList

    def getAvailableStreetPositions(self):
        return self.GS.Map.getAvailableStreets(self.getCurrentPlayer().ID)

    def getAvailableVillagePositions(self):
        return self.GS.Map.getAvailableVillages(self.getCurrentPlayer().ID, self.getRound())

    def getAvailableCityPositions(self):
        return self.GS.Map.getAvailableCities(self.getCurrentPlayer().ID, self.getRound())

    def buildObject(self, type, position):
        id = self.getCurrentPlayer().ID
        player = self.getCurrentPlayer()
        assert type in Objects, "invalid type"
        if type == Objects.STREET:
            assert player.ResourceCards[Resources.WOOD] != 0, "street: missing wood"
            assert player.ResourceCards[Resources.CLAY] != 0, "street: missing clay"
            self.GS.Map.buildStuff(
                id, type, position, self.getRound())
            self.removeResourceCards(id, Resources.WOOD)
            self.removeResourceCards(id, Resources.CLAY)
        elif type == Objects.VILLAGE:
            assert player.ResourceCards[Resources.WOOD] != 0, "village: missing wood"
            assert player.ResourceCards[Resources.CLAY] != 0, "village: missing clay"
            assert player.ResourceCards[Resources.SHEEP] != 0, "village: missing sheep"
            assert player.ResourceCards[Resources.WHEAT] != 0, "village: missing wheat"
            self.GS.Map.buildStuff(
                id, type, position, self.getRound())
            self.removeResourceCards(id, Resources.WOOD)
            self.removeResourceCards(id, Resources.CLAY)
            self.removeResourceCards(id, Resources.SHEEP)
            self.removeResourceCards(id, Resources.WHEAT)
        elif type == Objects.CITY:
            assert player.ResourceCards[Resources.ORE] >= 3, "city: missing ore"
            assert player.ResourceCards[Resources.WHEAT] >= 2, "city: missing wheat"
            self.GS.Map.buildStuff(
                id, type, position, self.getRound())
            self.removeResourceCards(id, Resources.ORE)
            self.removeResourceCards(id, Resources.ORE)
            self.removeResourceCards(id, Resources.ORE)
            self.removeResourceCards(id, Resources.WHEAT)
            self.removeResourceCards(id, Resources.WHEAT)

    def getLegalBanditPositions(self):
        pos = []
        for count, tile in enumerate(self.GS.Map.TileList):
            if tile[0] != Tiles.OCEAN and tile[0] != Tiles.DESERT:
                pos.append(count)
        if self.GS.Map.BanditPosition in pos:
            pos.remove(self.GS.Map.BanditPosition)
        return pos

    def setBanditPosition(self, position):
        self.GS.Map.setBanditPosition(position)

    # ---- Interaction with Player ----
    def getPlayerForID(self, id):
        if self.GS.Psuesch1.ID == id:
            return self.GS.Psuesch1
        elif self.GS.Psuesch2.ID == id:
            return self.GS.Psuesch2
        elif self.GS.Psuesch3.ID == id:
            return self.GS.Psuesch3
        elif self.GS.Player == 4 and self.GS.Psuesch4.ID == id:
            return self.GS.Psuesch4
        else:
            print(str(id))

    def giveResourceCards(self, id, card, count=1):
        for i in range(count):
            self.getPlayerForID(
                id).updateResourceCards(card, 1)

    def removeResourceCards(self, id, card, count=1):
        for i in range(count):
            self.getPlayerForID(
                id).updateResourceCards(card, 0)

    def handOutCards(self, roll):
        tiles = self.GS.Map.getTilesForValue(roll)
        players = self.GS.PlayerList
        for tile in tiles:
            villages = self.GS.Map.getVillagesForTile(tile[0])
            cities = self.GS.Map.getCitiesForTile(tile[0])
            for player in players:
                for v in villages:
                    if v == player.ID:
                        self.giveResourceCards(player.ID, tile[1])
                for c in cities:
                    if c == player.ID:
                        self.giveResourceCards(player.ID, tile[1], 2)

    def drawDevelopmentCard(self):
        id = self.getCurrentPlayer().ID
        assert self.getCurrentPlayer().ResourceCards[
            Resources.SHEEP] != 0, "missing sheep"
        assert self.getCurrentPlayer().ResourceCards[
            Resources.ORE] != 0, "missing ore"
        assert self.getCurrentPlayer().ResourceCards[
            Resources.WHEAT] != 0, "missing wheat"
        card = self.GS.getRandomDevCard()
        self.removeResourceCards(id, Resources.SHEEP)
        self.removeResourceCards(id, Resources.ORE)
        self.removeResourceCards(id, Resources.WHEAT)
        self.getCurrentPlayer().updateDevelopmentCards(card, self.getRound())

    def playDevelopmentCard(self, devCard, arg1=0, arg2=0):
        id = self.getCurrentPlayer().ID
        r = self.getCurrentPlayer().updateDevelopmentCards(devCard, self.getRound(), 1)
        if r == 1:
            if devCard == DevelopmentCards.KNIGHT_CARD:
                self.KNIGHTCARD(id, arg1)
            elif devCard == DevelopmentCards.VICTORY_POINT_CARD:
                self.VICTORYPOINTCARD(id)
            elif devCard == DevelopmentCards.MONOPOLY:
                self.MONOPOLY(id, arg1)
            elif devCard == DevelopmentCards.DEVELOPMENT:
                self.DEVELOPMENT(id, arg1, arg2)
            elif devCard == DevelopmentCards.CONSTRUCTION:
                self.CONSTRUCTION(id, arg1, arg2)

    # ---- Development cards ----
    def KNIGHTCARD(self, id, position):
        # BanditPosition
        self.GS.Map.setBanditPosition(position)
        # Increment played knights
        self.getPlayerForID(id).PlayedKnightCards += 1

    def VICTORYPOINTCARD(self, id):
        # increments VictoryPoints
        self.getPlayerForID(id).updateVictoryPoints()

    def CONSTRUCTION(self, id, position1, position2):
        # builds two streets
        self.GS.Map.buildStuff(id, Objects.STREET, position1, self.getRound())
        self.GS.Map.buildStuff(id, Objects.STREET, position2, self.getRound())

    def MONOPOLY(self, id, resourceCard):
        # all players
        for sum, player in enumerate(self.GS.PlayerList):
            # resourceCards[card] = 0
            i = player.ResourceCards[resourceCard]
            for j in range(i):
                player.updateResourceCards(resourceCard, 0)
        for i in range(sum):
            # resourceCards[card] = x
            self.getPlayerForID(id).updateResourceCards(resourceCard, 1)

    def DEVELOPMENT(self, id, resourceCard1, resourceCard2):
        # adds two resource cards
        self.getPlayerForID(id).updateResourceCards(resourceCard1, 1)
        self.getPlayerForID(id).updateResourceCards(resourceCard2, 1)

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
        if self.GS.PlayedDev == 0:
            for card in player.DevelopmentCards:
                if card[1] != self.getRound():
                    devCards.append(card[0])

        # legalMoves.extend([(methods["playDevCard"], [card]) for card in devCards if (
        #    card == DevelopmentCards.KNIGHT_CARD or self.GS.Diced != 0)])

        if self.GS.Diced == 0:
            legalMoves.append((methods["roll"], []))
        # elif self.GS.Roll7 == 1:
        #    positions = self.getLegalBanditPositions()
        #    rand = random.randrange(len(positions))
        #    legalMoves.append((methods["roll7"], positions[rand]))
        elif self.GS.Roll7 == 1:
            for pos in self.getLegalBanditPositions():
                legalMoves.append((methods["roll7"], [pos]))
            self.GS.Roll7 = 0
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

            for card in devCards:
                if (card == DevelopmentCards.KNIGHT_CARD):
                    for pos in self.getLegalBanditPositions():
                        legalMoves.append((methods["playDevCard"], [card, pos]))
                elif (card == DevelopmentCards.VICTORY_POINT_CARD):
                    legalMoves.append((methods["playDevCard"], [card]))
                elif (card == DevelopmentCards.CONSTRUCTION):
                    for street in self.getAvailableStreetPositions():
                        s = self.getAvailableStreetPositions()
                        s.remove(street)
                        for street2 in self.getAvailableStreetPositions():
                            legalMoves.append((methods["playDevCard"], [card, street, street2]))
                elif (card == DevelopmentCards.DEVELOPMENT):
                    for res in Resources:
                        for res2 in Resources:
                            legalMoves.append((methods["playDevCard"], [card, res, res2]))
                elif (card == DevelopmentCards.MONOPOLY):
                    for res in Resources:
                        legalMoves.append((methods["playDevCard"], [card, res]))
        return legalMoves

    def getRandomLegalMove(self):
        legalMoves = self.getLegalMoves()
        return random.choice(legalMoves)

    def getNextGamestate(self, legalMove):
        legalMove[0](*legalMove[1])
        # return self.GS


if __name__ == "__main__":
    sim = Simulation(3)
# round 0
    res = [(Resources.WOOD, 10), (Resources.CLAY, 10), (Resources.WHEAT, 10), (Resources.SHEEP, 10), (Resources.ORE, 10)]
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().ID, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (10, 11, 17))
    sim.buildObject(Objects.VILLAGE, (18, 24, 25))
    sim.buildObject(Objects.STREET, (10, 17))
    sim.buildObject(Objects.STREET, (24, 25))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().ID, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (23, 24, 29))
    sim.buildObject(Objects.VILLAGE, (12, 13, 19))
    sim.buildObject(Objects.STREET, (13, 19))
    sim.buildObject(Objects.STREET, (23, 24))
    sim.endOfTurn()
    for i in res:
        sim.giveResourceCards(sim.getCurrentPlayer().ID, i[0], i[1])
    sim.buildObject(Objects.VILLAGE, (29, 33, 34))
    sim.buildObject(Objects.VILLAGE, (30, 34, 35))
    sim.buildObject(Objects.STREET, (29, 33))
    sim.buildObject(Objects.STREET, (30, 34))
    sim.endOfTurn()
    sim.save("saves/gs1")

    sim.load("saves/gs1")

    for i in range(21):
        print("Round:" + str(sim.getRound()))
        print("turn:" + str(sim.GS.Turn))
        x = sim.getRandomLegalMove()
        print(x)
        sim.getNextGamestate(x)
        print("-------------------")
    """
    sim.drawDevelopmentCard()
    sim.drawDevelopmentCard()
    sim.getNextGamestate(sim.getRandomLegalMove())
    print(sim.getAvailableStreetPositions())
    sim.endOfTurn()
    sim.getNextGamestate(sim.getRandomLegalMove())
    sim.endOfTurn()
    sim.getNextGamestate(sim.getRandomLegalMove())
    sim.endOfTurn()

    sim.getNextGamestate(sim.getRandomLegalMove())
    sim.getNextGamestate(sim.getRandomLegalMove())
    sim.endOfTurn()
    print(sim.getRound())
    """

    # ---- turn ----
    """
    def inputCheck(self):
        try:
            i = int(input("> "))
        except ValueError:
            i = self.inputCheck()
        return i
    """


    '''
    
    '''