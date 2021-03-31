from gamestate import Gamestate
import random

class Simulation:

    def __init__(self, gamestate, player=4):
        self.gamestate = gamestate

    # ---- turn ----
    def roll(self):
        return random.randrange(1, 7) + random.randrange(1, 7)

    def turn(self, player):
        r = self.roll()
        if r != 7:
            self.handOutCards(r)
        print(r)

    # ---- Interaction with gamestate
    def getRound(self):
        return self.gamestate.getRound()

    def incRound(self):
        self.gamestate.incRound()

    # ---- Interaction with CatanMap ----
    def getObjectList(self):
        return self.gamestate.Map.getObjectList()

    def getAvailableStreetPositions(self, player):
        return self.gamestate.Map.getAvailableStreets(player)

    def getAvailableVillagePositions(self, player):
        return self.gamestate.Map.getAvailableVillages(player, self.getRound())

    def getAvailableCityPositions(self, player):
        return self.gamestate.Map.getAvailableCities(player, self.getRound())

    def buildObject(self, player, type, position):
        self.gamestate.Map.buildStuff(player, type, position, self.getRound())

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

    def giveResourceCards(self, playerName, card):
        self.gamestate.getPlayerToName(playerName).updateResourceCards(card, 1)

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
                        self.giveResourceCards(player.getName(), tile[1])
                        self.giveResourceCards(player.getName(), tile[1])

    def drawDevelopmentCard(self, playerName):
        card = self.gamestate.getRandomDevCard()
        self.gamestate.getPlayerToName(playerName).updateDevelopmentCards(card, self.getRound())


if __name__ == "__main__":
    gs = Gamestate("lia", "jakob", "edgar")
    sim = Simulation(gs)

    sim.buildObject("jakob", "VILLAGE", (4, 5, 10))
    sim.buildObject("jakob", "CITY", (4, 5, 10))
    sim.buildObject("jakob", "VILLAGE", (2, 6, 1))
    sim.buildObject("jakob", "STREET", (5, 10))
    sim.buildObject("jakob", "STREET", (11, 10))
    sim.buildObject("lia", "VILLAGE", (13, 19, 20))
    sim.buildObject("lia", "VILLAGE", (25, 30, 31))
    sim.incRound()
    sim.drawDevelopmentCard("lia")
    sim.incRound()
    sim.drawDevelopmentCard("lia")
    print(sim.gamestate.getPlayerToName("lia").getDevelopmentCards())
# liste der moves
# nächster gamestate nach move
# simulate random game: 1 gewonnen
