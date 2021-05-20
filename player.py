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

    def __init__(self, name):
        self.Name = name
        self.Priority = 0
        self.AvailableObjects = self.initializeAvailableObjects()
        self.ResourceCards = self.initializeResourceCards()
        self.DevelopmentCards = []
        self.VictoryPoints = 0
        self.PlayedKnightCards = 0

    # ---- initialization ----
    def initializeAvailableObjects(self):
        availableObjects = {
            Objects.CITY: 4,
            Objects.VILLAGE: 5,
            Objects.STREET: 15
        }
        return availableObjects

    def initializeResourceCards(self):
        return dict.fromkeys(Resources, 0)

    # ---- update ----
    def updateAvailableObjects(self, object, flag=0):
        assert object in self.AvailableObjects, "invalid object"

        if flag == 1 and object == Objects.VILLAGE:
            assert self.AvailableObjects[object] < 15, "invalid operation"
            self.AvailableObjects[object] += 1
        else:
            assert self.AvailableObjects[object] > 0, "invalid operation"
            self.AvailableObjects[object] -= 1

    def updateResourceCards(self, card, flag=0):
        if flag == 1:
            self.ResourceCards[card] += 1
        else:
            assert self.ResourceCards[card] > 0, "too expensive"
            self.ResourceCards[card] -= 1

    def updateDevelopmentCards(self, card, round, flag=0):
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
        if flag == 1:
            assert self.VictoryPoints > 0, "0 points"
            self.VictoryPoints -= 1
        else:
            self.VictoryPoints += 1
            if self.VictoryPoints >= 10:
                print(self.Name + "hat gewonnen!")

    def updatePlayedKnightCards(self):
        self.playedKnightCards += 1

    # ---- ----
    def check7(self):
        sum = 0
        for card in self.ResourceCards.values():
            sum += card
        if sum > 7:
            for i in range(int(sum / 2)):
                randomCard = self.getRandomResourceCard()
                self.updateResourceCards(randomCard)

    def getRandomResourceCard(self):
        sum = 0
        for i in self.ResourceCards.values():
            sum += i
        rand = random.randrange(sum)
        for k, v in self.ResourceCards.items():
            if rand > v:
                rand -= v
            else:
                return k

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


if __name__ == "__main__":
    jakob = Player("jakob")
    print(jakob.ResourceCards)
