from gamestate import Gamestate
import random

class Simulation:

    def __init__(self, gamestate, player=4):
        self.gamestate = gamestate

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
        for card in self.gamestate.getPlayerToName(playerName).getDevelopmentCards():
            if "KNIGHT_CARD" == card[0]:
                print("1: play knight card, 0: skip")
                answer = self.inputCheck()
                if answer == 1:
                    self.playDevelopmentCard(playerName, "KNIGHT_CARD")
                break
        r = self.roll()
        print("roll " + str(r))
        if r != 7:
            self.handOutCards(r)
        elif r == 7:
            self.roll7(playerName)
        # option1: devcard speilen
        # option2: traden
        # option3:bauen
        # option4: exit
        exit = False
        while not exit:
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
                exit = True
            else:
                print("invalid input")

    def roll7(self, playerName):
        print("bandit position")
        position = self.inputCheck()
        self.bandit(position)
        villages = self.gamestate.Map.getVillagesToTile(position)
        cities = self.gamestate.Map.getCitiesToTile(position)
        players = list(dict.fromkeys(villages + cities))
        for player in players:
            card = self.getPlayerToName(player).getRandomResourceCard()
            self.removeResourceCards(player, card)
            self.giveResourceCards(playerName, card)

    # ---- Interaction with gamestate

    def getRound(self):
        return self.gamestate.getRound()

    def incRound(self):
        self.gamestate.incRound()

    # ---- Interaction with CatanMap ----
    def getObjectList(self):
        return self.gamestate.Map.getObjectList()

    def getAvailableStreetPositions(self, playerName):
        return self.gamestate.Map.getAvailableStreets(playerName)

    def getAvailableVillagePositions(self, playerName):
        return self.gamestate.Map.getAvailableVillages(playerName, self.getRound())

    def getAvailableCityPositions(self, playerName):
        return self.gamestate.Map.getAvailableCities(playerName, self.getRound())

    def buildObject(self, playerName, type, position):
        assert type in ["STREET", "VILLAGE", "CITY"], "invalid type"
        if type == "STREET":
            assert self.getPlayerToName(playerName).getResourceCards()["WOOD"] != 0, "street: missing wood"
            assert self.getPlayerToName(playerName).getResourceCards()["CLAY"] != 0, "street: missing clay"
            self.gamestate.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, "WOOD")
            self.removeResourceCards(playerName, "CLAY")
        elif type == "VILLAGE":
            assert self.getPlayerToName(playerName).getResourceCards()["WOOD"] != 0, "village: missing wood"
            assert self.getPlayerToName(playerName).getResourceCards()["CLAY"] != 0, "village: missing clay"
            assert self.getPlayerToName(playerName).getResourceCards()["SHEEP"] != 0, "village: missing sheep"
            assert self.getPlayerToName(playerName).getResourceCards()["WHEAT"] != 0, "village: missing wheat"
            self.gamestate.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, "WOOD")
            self.removeResourceCards(playerName, "CLAY")
            self.removeResourceCards(playerName, "SHEEP")
            self.removeResourceCards(playerName, "WHEAT")
        elif type == "CITY":
            assert self.getPlayerToName(playerName).getResourceCards()["ORE"] >= 3, "city: missing ore"
            assert self.getPlayerToName(playerName).getResourceCards()["WHEAT"] >= 2, "city: missing wheat"
            self.gamestate.Map.buildStuff(playerName, type, position, self.getRound())
            self.removeResourceCards(playerName, "ORE")
            self.removeResourceCards(playerName, "ORE")
            self.removeResourceCards(playerName, "ORE")
            self.removeResourceCards(playerName, "WHEAT")
            self.removeResourceCards(playerName, "WHEAT")

    def bandit(self, position):
        self.gamestate.Map.setBanditPosition(position)

    # ---- Interaction with Player ----
    def priorityRoll(self, player=4):
        begin = random.randrange(player) + 1
        self.gamestate.Player1.Priority = (1 + begin) % player + 1
        self.gamestate.Player2.Priority = (2 + begin) % player + 1
        self.gamestate.Player3.Priority = (3 + begin) % player + 1
        if player == 4:
            self.gamestate.Player4.Priority = (4 + begin) % player + 1

    def giveResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.gamestate.getPlayerToName(playerName).updateResourceCards(card, 1)

    def removeResourceCards(self, playerName, card, count=1):
        for i in range(count):
            self.gamestate.getPlayerToName(playerName).updateResourceCards(card, 0)

    def handOutCards(self, roll):
        tiles = self.gamestate.Map.getTilesToValue(roll)
        players = self.gamestate.getPlayerList()
        for tile in tiles:
            villages = self.gamestate.Map.getVillagesToTile(tile[0])
            cities = self.gamestate.Map.getCitiesToTile(tile[0])
            for player in players:
                for v in villages:
                    if v == player.getName():
                        self.giveResourceCards(player.getName(), tile[1])
                for c in cities:
                    if c == player.getName():
                        self.giveResourceCards(player.getName(), tile[1], 2)

    def drawDevelopmentCard(self, playerName):
        assert self.getPlayerToName(playerName).getResourceCards()["SHEEP"] != 0, "missing sheep"
        assert self.getPlayerToName(playerName).getResourceCards()["ORE"] != 0, "missing ore"
        assert self.getPlayerToName(playerName).getResourceCards()["WHEAT"] != 0, "missing wheat"
        card = self.gamestate.getRandomDevCard()
        self.gamestate.getPlayerToName(playerName).updateDevelopmentCards(card, self.getRound())

    def playDevelopmentCard(self, playerName, devCard):
        r = self.getPlayerToName(playerName).updateDevelopmentCards(devCard, self.getRound(), 1)
        if r == 1:
            if devCard == "KNIGHT_CARD":
                self.gamestate.KNIGHTCARD(playerName)
            elif devCard == "VICTORY_POINT_CARD":
                self.gamestate.VICTORYPOINTCARD(playerName)
            elif devCard == "MONOPOLY":
                self.gamestate.MONOPOLY(playerName)
            elif devCard == "DEVELOPMENT":
                self.gamestate.DEVELOPMENT(playerName)
            elif devCard == "CONSTRUCTION":
                self.gamestate.CONSTRUCTION(playerName)

    def getPlayerToName(self, name):
        return self.gamestate.getPlayerToName(name)

    def getLegalMoves(self, playerName):
        pass


if __name__ == "__main__":
    gs = Gamestate("lia", "jakob", "edgar")
    sim = Simulation(gs)
    sim.giveResourceCards("jakob", "WOOD", 10)
    sim.giveResourceCards("jakob", "CLAY", 10)
    sim.giveResourceCards("jakob", "WHEAT", 10)
    sim.giveResourceCards("jakob", "SHEEP", 10)
    sim.giveResourceCards("jakob", "ORE", 10)
    sim.giveResourceCards("lia", "ORE", 10)
    sim.gamestate.MONOPOLY("jakob", "ORE")
    sim.giveResourceCards("edgar", "WOOD", 10)
    sim.giveResourceCards("edgar", "CLAY", 10)
    sim.giveResourceCards("edgar", "WHEAT", 10)
    sim.giveResourceCards("edgar", "ORE", 10)
    sim.giveResourceCards("edgar", "SHEEP", 10)
    # print(sim.gamestate.getPlayerToName("jakob").getResourceCards())
    # print(sim.gamestate.getPlayerToName("jakob").check7())
    sim.buildObject("jakob", "VILLAGE", (4, 5, 10))
    sim.buildObject("jakob", "CITY", (4, 5, 10))
    sim.buildObject("jakob", "VILLAGE", (2, 6, 1))
    sim.buildObject("jakob", "STREET", (5, 10))
    sim.buildObject("jakob", "STREET", (11, 10))
    sim.buildObject("edgar", "VILLAGE", (7, 8, 13))
    sim.incRound()
    sim.drawDevelopmentCard("jakob")
    sim.drawDevelopmentCard("jakob")
    sim.drawDevelopmentCard("jakob")
    sim.incRound()
    sim.drawDevelopmentCard("jakob")
    sim.drawDevelopmentCard("jakob")
    # print(sim.gamestate.getPlayerToName("jakob").getResourceCards())
    # print(sim.gamestate.getPlayerToName("lia").getResourceCards())
    sim.turn("jakob")
    # print(sim.gamestate.getPlayerToName("jakob").getResourceCards())
    # sim.getPlayerToName("jakob").trade4("WOOD", "ORE")
    # print(sim.gamestate.getPlayerToName("edgar").getResourceCards())
    # sim.gamestate.trade3("edgar", "WOOD", "ORE")
    # print(sim.gamestate.getPlayerToName("edgar").getResourceCards())
    # print(sim.gamestate.getPlayerToName("jakob").getDevelopmentCards())
    # sim.turn("jakob")
    # sim.buildObject("lia", "VILLAGE", (13, 19, 20))
    # sim.buildObject("lia", "VILLAGE", (25, 30, 31))

    # print(sim.getObjectList())
    # sim.incRound()
    # print(sim.gamestate.Map.getAvailableStreets("jakob"))
    # print(sim.getAvailableStreetPositions("jakob"))
    # sim.drawDevelopmentCard("lia")
    # sim.incRound()
    # sim.buildObject("jakob", "VILLAGE", (10, 11, 17))
    # print(sim.gamestate.getPlayerToName("jakob").getResourceCards())

    # sim.drawDevelopmentCard("lia")
    # print(sim.gamestate.getPlayerToName("lia").getDevelopmentCards())
# liste der moves
# naechster gamestate nach move
# simulate random game: 1 gewonnen
