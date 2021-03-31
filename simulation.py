from gamestate import Gamestate
import random

class Simulation:

    def __init__(self, gamestate, player=4):
        self.gamestate = gamestate

    # ---- new Game ----
    def priorityRoll(self, player=4):
        begin = random.randrange(player) + 1
        self.gamestate.Player1.Priority = (1 + begin) % player + 1
        self.gamestate.Player2.Priority = (2 + begin) % player + 1
        self.gamestate.Player3.Priority = (3 + begin) % player + 1
        if player == 4:
            self.gamestate.Player4.Priority = (4 + begin) % player + 1

    # ---- turn ----
    def roll(self):
        return random.randrange(1, 7) + random.randrange(1, 7)

    def turn(self, player):
        # ereigniskarte ausspielen
        # ja nein
        # würfeln
        num = self.roll()
        # karten bekommen
        self.handOutCards(num)
        # ereigniskarte auspielen
        # kaufen
        # bauen
        # ereigniskarte ausspielen
        # zug beenden

    def handOutCards(self, roll):
        pass

    # ---- Board ----

    def getavailableStreetPositions(self):
        pass

    def getAvailableVillagePositions(self, round=1):
        pass

    def getavailableCityPositions(self):
        pass

    def buildObject(self, player, object, position):
        pass


if __name__ == "__main__":
    lille = Gamestate()
    edgar = Simulation(lille)

# liste der moves
# nächster gamestate nach move
# simulate random game: 1 gewonnen
