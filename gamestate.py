from map import CatanMap
from player import Player

class Gamestate:

    def __init__(self, player=4):
        self.DevelopmentCards = self.initializeDevelopmentCards()
        self.ResourceCards = self.initializeResourceCards()
        self.Map = CatanMap()
        self.Player1 = Player()
        self.Player2 = Player()
        self.Player3 = Player()
        if player == 4:
            self.Player4 = Player()

    def initializeDevelopmentCards(self):
        developmentCards = {
            "KNIGHT_CARDS": 14,
            "VICTORY_POINT_CARDS": 5,
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

    # ----
    def updateDevelopmentCards(self, card):
        assert card in self.DevelopmentCards, "invalid operation"
        if self.DevelopmentCards[card] == 1:
            del(self.DevelopmentCards[card])
        else:
            self.DevelopmentCards[card] -= 1

    def updateResourceCards(self, card, flag=0):
        assert card in self.ResourceCards, "invalid operation"
        if flag == 1:
            assert self.ResourceCards[card] < 19, "card does not exist"
            self.ResourceCards[card] += 1
        elif self.ResourceCards[card] == 0:
            pass
        else:
            self.ResourceCards[card] -= 1


if __name__ == "__main__":
    lille = Gamestate()
