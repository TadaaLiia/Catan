import random
from entities import *


class Player:
    """
    - Priority: int 1-4
    - AvailableObjects: {City:4, Village:5, Street:15}
    - ResourceCards: {wheat:0, ore:0, sheep:0, wood:0, clay:0}
    - DevelopmentCards: list

    - updateAvailableObjects: +/- Object
    - updateResourceCard: +/- Card
    - updateDevelopmentCards: +/- Card
    """

    def __init__(self, id):
        self.ID = id
        self.Priority = 0
        self.AvailableObjects = {
            Objects.CITY: 4,
            Objects.VILLAGE: 5,
            Objects.STREET: 15
        }
        self.ResourceCards = dict.fromkeys(Resources, 0)
        self.DevelopmentCards = []
        self.VictoryPoints = 0
        self.PlayedKnightCards = 0

    # ---- update ----
    def updateAvailableObjects(self, object, flag=0):
        # flag = 0: remove Object
        # flag = 1: add Object
        assert object in self.AvailableObjects, "invalid object"
        if flag == 1 and object == Objects.VILLAGE:
            assert self.AvailableObjects[object] < 15, "invalid operation"
            self.AvailableObjects[object] += 1
        else:
            assert self.AvailableObjects[object] > 0, "invalid operation"
            self.AvailableObjects[object] -= 1

    def updateResourceCards(self, card, flag=0):
        # flag = 0: remove card
        # flag = 1: add card
        if flag == 1:
            self.ResourceCards[card] += 1
        else:
            assert self.ResourceCards[card] > 0, "too expensive"
            self.ResourceCards[card] -= 1

    def updateDevelopmentCards(self, card, round, flag=0):
        # flag = 0: add card
        # flag = 1: remove card
        if flag == 1:
            if card not in [x[0] for x in self.DevelopmentCards if x[1] < round]:
                print("you dont own this card")
                return 0
            for developmentCard in self.DevelopmentCards:
                if developmentCard[0] == card:
                    del self.DevelopmentCards[self.DevelopmentCards.index(developmentCard)]
                    return 1
        else:
            self.DevelopmentCards.append((card, round))

    def updateVictoryPoints(self, flag=0):
        # flag = 0: dec Points
        # flag = 1: inc Points
        if flag == 1:
            assert self.VictoryPoints > 0, "0 points"
            self.VictoryPoints -= 1
        else:
            self.VictoryPoints += 1
            if self.VictoryPoints >= 10:
                print(str(self.ID) + "hat gewonnen!")

    # ---- check ----
    def check7(self):
        # number ob resource cards
        sum = 0
        for i in self.ResourceCards.values():
            sum += i
        # remove half of the cards
        if sum > 7:
            for j in range(int(sum / 2)):
                randomCard = self.getRandomResourceCard()
                self.updateResourceCards(randomCard)

    # ---- getter ----
    def getRandomResourceCard(self):
        # number of resource cards
        sum = 0
        for i in self.ResourceCards.values():
            sum += i
        # return random card
        rand = random.randrange(sum)
        for k, v in self.ResourceCards.items():
            if rand > v:
                rand -= v
            else:
                return k

    '''
    def chooseDevCard(self):
        if len(self.DevelopmentCards) != 0:
            print(self.DevelopmentCards)
            print("0 - " + str(len(self.DevelopmentCards)))
            try:
                cardIndex = int(input())
            except ValueError:
                self.chooseDevCard()
            else:
                try:
                    card = self.DevelopmentCards[cardIndex][0]
                except IndexError:
                    self.chooseDevCard
                else:
                    return card
    '''


if __name__ == "__main__":
    jakob = Player(0)
