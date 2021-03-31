class Player:
    """
    - Priority: int 1-4
    - AvailableObjects: {City:4, Village:5, Street:15}
    - ResourceCards: {wheat:0, ore:0, sheep:0, wood:0, clay:0}
    - DevelopmentCards: list

    - updateAvailableObjects: +/- Object
    - updateResourceCard: +/- Card
    - pdateDevelopmentCards: +/- Card
    """

    def __init__(self, name):
        self.Name = name
        self.Priority = 0
        self.AvailableObjects = self.initializeAvailableObjects()
        self.ResourceCards = self.initializeResourceCards()
        self.DevelopmentCards = []

    # ---- getter ----
    def getName(self):
        return self.Name

    def getPriority(self):
        return self.Priority

    def getAvailableObjects(self):
        return self.AvailableObjects

    def getResourceCards(self):
        return self.ResourceCards

    def getDevelopmentCards(self):
        return self.DevelopmentCards

    # ---- setter ----
    def setName(self, name):
        self.Name = name

    def setPriority(self, prio):
        self.Priority = prio

    # ---- initialization ----
    def initializeAvailableObjects(self):
        availableObjects = {
            "CITY": 4,
            "VILLAGE": 5,
            "STREET": 15
        }
        return availableObjects

    def initializeResourceCards(self):
        resourceCards = {
            "WHEAT": 0,
            "ORE": 0,
            "SHEEP": 0,
            "WOOD": 0,
            "CLAY": 0
        }
        return resourceCards

    # ---- update ----
    def updateAvailableObjects(self, object, flag=0):
        assert object in self.AvailableObjects, "invalid object"

        if flag == 1 and object == "VILLAGE":
            assert self.AvailableObjects[object] < 15, "invalid operation"
            self.AvailableObjects[object] += 1
        else:
            assert self.AvailableObjects[object] > 0, "invalid operation"
            self.AvailableObjects[object] -= 1

    def updateResourceCards(self, card, flag=0):
        assert card in self.ResourceCards, "invalid card"

        if flag == 1:
            self.ResourceCards[card] += 1
        else:
            assert self.ResourceCards[card] > 0, "too expensive"
            self.ResourceCards[card] -= 1

    def updateDevelopmentCards(self, card, round, flag=0):
        if flag == 1:
            assert card in [x[0] for x in self.DevelopmentCards if x[1] < round], "you dont own this card"
            for developmentCard in self.DevelopmentCards:
                if developmentCard[0] == card:
                    del self.DevelopmentCards[self.DevelopmentCards.index(developmentCard)]
                    break
        else:
            self.getDevelopmentCards().append((card, round))


if __name__ == "__main__":
    jakob = Player()
