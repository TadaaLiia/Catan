import random


class CatanMap:
    """
    - BanditPosition: int, tileNumber
    - Adjacency: Matrix(36x36), adjacent tiles
    - AvailableNodes: List, availableNodes(x,y,z)
    - TileList: List, (TileType, value)
    - ObjectList: {player:green, type:a, position:(x,y)}

    - buildStuff: objectList.append
    - setBandit: newTileNumber
    """

    def __init__(self):
        self.BanditPosition = 0
        self.Adjacency = self.generateAdjacency()
        self.AvailableNodes = self.generateNodeList()
        self.TileList = self.generateMap()
        self.ObjectList = self.initializeObjectList()

    # ---- getter ----
    def getBanditPosition(self):
        return self.BanditPosition

    def getAdjacency(self):
        return self.Adjacency

    def getAvailableNodes(self):
        return self.AvailableNodes

    def getTileList(self):
        return self.TileList

    def getObjectList(self):
        return self.ObjectList

    # ---- setter ----
    def setBanditPosition(self, position):
        assert type(position) == int, "invalid Bandit position"
        self.BanditPosition = position

    # ---- generation and initialization ----
    def generateAdjacency(self):
        '''
        returns: Matrix(36x36), adjacent tiles
        '''
        x = []
        for i in range(37):
            x.append([0 for jakob in range(37)])

        TILES_1 = [5, 6, 7]
        for tile in TILES_1:
            nachbar = [tile - 5, tile - 4, tile - 1, tile + 1, tile + 5, tile + 6]
            for n in nachbar:
                x[tile][n] = 1
                x[n][tile] = 1

        TILES_2 = [10, 11, 12, 13]
        for tile in TILES_2:
            nachbar = [tile - 6, tile - 5, tile - 1, tile + 1, tile + 6, tile + 7]
            for n in nachbar:
                x[tile][n] = 1
                x[n][tile] = 1

        TILES_3 = list(range(16, 21))
        for tile in TILES_3:
            nachbar = [tile - 7, tile - 6, tile - 1, tile + 1, tile + 6, tile + 7]
            for n in nachbar:
                x[tile][n] = 1
                x[n][tile] = 1

        TILES_4 = list(range(23, 27))
        for tile in TILES_4:
            nachbar = [tile - 7, tile - 6, tile - 1, tile + 1, tile + 5, tile + 6]
            for n in nachbar:
                x[tile][n] = 1
                x[n][tile] = 1

        TILES_5 = [29, 30, 31]
        for tile in TILES_5:
            nachbar = [tile - 6, tile - 5, tile - 1, tile + 1, tile + 4, tile + 5]
            for n in nachbar:
                x[tile][n] = 1
                x[n][tile] = 1
        return x

    def generateNodeList(self):
        '''
        returns: available, valid nodes
        '''
        nodeList = []

        TILES_1 = [5, 6, 7]
        for tile in TILES_1:
            nodeList.append([tile - 5, tile - 4, tile])
            nodeList.append([tile - 4, tile + 1, tile])
            nodeList.append([tile + 1, tile + 6, tile])
            nodeList.append([tile + 5, tile + 6, tile])
            nodeList.append([tile + 5, tile - 1, tile])
            nodeList.append([tile - 5, tile - 1, tile])

        nodeList.append([4, 9, 10])
        nodeList.append([8, 13, 14])

        TILES_3 = list(range(16, 21))
        for tile in TILES_3:
            nodeList.append([tile - 7, tile - 6, tile])
            nodeList.append([tile - 6, tile + 1, tile])
            nodeList.append([tile + 1, tile + 7, tile])
            nodeList.append([tile + 7, tile + 6, tile])
            nodeList.append([tile + 6, tile - 1, tile])
            nodeList.append([tile - 7, tile - 1, tile])

        nodeList.append([22, 23, 28])
        nodeList.append([26, 27, 32])

        TILES_5 = [29, 30, 31]
        for tile in TILES_5:
            nodeList.append([tile - 6, tile - 5, tile])
            nodeList.append([tile - 5, tile + 1, tile])
            nodeList.append([tile + 1, tile + 5, tile])
            nodeList.append([tile + 5, tile + 4, tile])
            nodeList.append([tile + 4, tile - 1, tile])
            nodeList.append([tile - 6, tile - 1, tile])

        # remove all duplicates and permutations in nested list
        nodeList = list(set(map(lambda x: tuple(sorted(x)), nodeList)))
        return sorted(nodeList)

    def generateMap(self, seed=None):
        AVAILABLE_TILES = {
            "WHEAT": 4,
            "ORE": 3,
            "SHEEP": 4,
            "WOOD": 4,
            "CLAY": 3,
            "DESERT": 1
        }

        # Numbers have to be in that Order
        AVAILABLE_NUMBERS = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

        TILES = [
            ("OCEAN", 0), ("OCEAN", 0), ("OCEAN", 0), ("OCEAN", 0),
            ("OCEAN", 0), (None, "A"), (None, "B"), (None, "C"), ("OCEAN", 0),
            ("OCEAN", 0), (None, "L"), (None, "M"), (None, "N"), (None, "D"), ("OCEAN", 0),
            ("OCEAN", 0), (None, "K"), (None, "O"), (None, "X"), (None, "P"), (None, "E"), ("OCEAN", 0),
            ("OCEAN", 0), (None, "J"), (None, "Q"), (None, "R"), (None, "F"), ("OCEAN", 0),
            ("OCEAN", 0), (None, "I"), (None, "H"), (None, "G"), ("OCEAN", 0),
            ("OCEAN", 0), ("OCEAN", 0), ("OCEAN", 0), ("OCEAN", 0)
        ]

        tileList = []
        for tile in TILES:
            if tile[0] is not None:
                tileList.append(tile)
            else:
                randomTile = random.choice(list(AVAILABLE_TILES.keys()))
                if AVAILABLE_TILES[randomTile] == 1:
                    del AVAILABLE_TILES[randomTile]
                else:
                    AVAILABLE_TILES[randomTile] -= 1
                tileList.append(randomTile)

        tile_order = [5, 6, 7, 13, 20, 26, 31, 30, 29, 23, 16, 10, 11, 12, 19, 25, 24, 17, 18]

        # Shift Tile Order
        shift = random.randint(0, 11)
        sub_tile_order = tile_order[:12]
        for i in range(shift):
            sub_tile_order.append(sub_tile_order.pop(0))

        tile_order = sub_tile_order + tile_order[12:]

        # Inner Part
        shift = int(shift / 2)
        sub_tile_order = tile_order[12:-1]
        for i in range(shift):
            sub_tile_order.append(sub_tile_order.pop(0))

        tile_order = tile_order[:12] + sub_tile_order + [tile_order[-1]]

        # Distribute Numbers
        for tile in tile_order:
            assert tileList[tile][1] != 0
            if tileList[tile] == "DESERT":
                tileList[tile] = ("DESERT", 0)
                self.setBanditPosition(tile)
            else:
                tileList[tile] = (tileList[tile], AVAILABLE_NUMBERS.pop(0))
        return tileList

    def initializeObjectList(self):
        objectList = []
        objectList.append({"player": None, "type": "PORT", "position": (0, 5)})
        objectList.append({"player": None, "type": "PORT", "position": (8, 13)})
        objectList.append({"player": None, "type": "PORT", "position": (20, 21)})
        objectList.append({"player": None, "type": "PORT", "position": (29, 33)})
        objectList.append({"player": None, "type": "SHEEP_PORT", "position": (2, 6)})
        objectList.append({"player": None, "type": "ORE_PORT", "position": (9, 10)})
        objectList.append({"player": None, "type": "WHEAT_PORT", "position": (22, 23)})
        objectList.append({"player": None, "type": "CLAY_PORT", "position": (26, 32)})
        objectList.append({"player": None, "type": "WOOD_PORT", "position": (30, 35)})
        return objectList

    # ---- Objects
    def updateAvailableNodes(self, position):
        # sorted position
        pos = tuple(sorted(position))
        # valid position?
        nodes = self.getAvailableNodes()
        assert pos in nodes, "invalid village position"
        # delete position and 2 or 3 adjacent poitions
        nodes.remove(pos)
        for node in nodes:
            if pos[0] in node and pos[1] in node:
                nodes.remove(node)
            elif pos[1] in node and pos[2] in node:
                nodes.remove(node)
            elif pos[0] in node and pos[2] in node:
                nodes.remove(node)
        self.AvailableNodes = nodes

    def getPlayerShit(self, player):
        objects = [x for x in self.getObjectList() if x["player"] == player]
        buildings = [x["position"] for x in objects if x["type"] != "STREET"]
        streets = [x["position"] for x in objects if x["type"] == "STREET"]
        return objects, buildings, streets

    def getAvailableStreets(self, player):
        # All player Objects
        playerObjects, playerBuildings, playerStreets = self.getPlayerShit(player)
        # Streets
        allStreets = [x["position"] for x in self.getObjectList() if x["type"] == "STREET"]
        # Streets around Cities and Villages
        availableStreets = []
        for b in playerBuildings:
            availableStreets.append((b[0], b[1]))
            availableStreets.append((b[0], b[2]))
            availableStreets.append((b[1], b[2]))
        # street extension
        for street in playerStreets:
            for x in range(37):
                # common neighbors
                if self.getAdjacency()[street[0]][x] == 1 and self.getAdjacency()[street[1]][x] == 1:
                    availableStreets.append((x, street[0]))
                    availableStreets.append((x, street[1]))
        # remove Streets in Oceans or unavailable streets
        final = []
        for street in availableStreets:
            if self.getAdjacency()[street[0]][street[1]] == 1 and street not in allStreets:
                final.append(tuple(sorted(street)))
        final = list(dict.fromkeys(final))
        return sorted(final)

    def getAvailableVillages(self, player, round=1):
        if round == 0:
            return self.getAvailableNodes()
        else:
            playerObjects, playerBuildings, playerStreets = self.getPlayerShit(player)
            availableVillages = []
            for node in self.getAvailableNodes():
                # angrenzende strasse an nodes
                if (node[0], node[1]) in playerStreets or (node[0], node[2]) in playerStreets or (node[1], node[2]) in playerStreets:
                    availableVillages.append(node)
            return sorted(availableVillages)

    def getAvailableCities(self, player, round=1):
        assert round != 0, "you are not allowed to build cities."
        playerObjects, playerBuildings, playerStreets = self.getPlayerShit(player)
        return [x["position"] for x in playerObjects if x["type"] == "VILLAGE"]

    def buildStuff(self, player, type, position, round=1):
        pos = tuple(sorted(position))
        # Street -> (x,y) in available streets(player)
        if type == "STREET":
            assert len(pos) == 2, "invalid position"
            assert pos in self.getAvailableStreets(player), "street not available"
            self.ObjectList.append({"player": player, "type": type, "position": pos})
        # Village -> (x,y,z) in availableNodes
        elif type == "VILLAGE":
            assert len(pos) == 3, "invalid position"
            assert pos in self.getAvailableVillages(player, round), "node not available or two streets required!"
            self.ObjectList.append({"player": player, "type": type, "position": pos})
            self.updateAvailableNodes(pos)
        # City -> {player,village,(x,y,z)} in ObjectList
        elif type == "CITY":
            assert len(pos) == 3, "invalid position"
            assert pos in self.getAvailableCities(player), "no village available"
            self.ObjectList.append({"player": player, "type": type, "position": pos})
            self.ObjectList.remove({"player": player, "type": "VILLAGE", "position": pos})
        else:
            print("incorrect type")
            return

    # ---- Tiles
    def getTilesToValue(self, value):
        tiles = []
        i = 0
        for tile in self.getTileList():
            if tile[1] == value and self.getBanditPosition() != i:
                tiles.append((i, tile[0]))
            i += 1
        return(tiles)

    def getVillagesToTile(self, tile):
        allVillages = [(x["player"], x["position"]) for x in self.getObjectList() if x["type"] == "VILLAGE"]
        villages = []
        for v in allVillages:
            if v[1][0] == tile or v[1][1] == tile or v[1][2] == tile:
                villages.append(v[0])
        return villages

    def getCitiesToTile(self, tile):
        allCities = [(x["player"], x["position"]) for x in self.getObjectList() if x["type"] == "CITY"]
        cities = []
        for c in allCities:
            if c[1][0] == tile or c[1][1] == tile or c[1][2] == tile:
                cities.append(c[0])
        return cities


if __name__ == "__main__":
    cmap = CatanMap()
    print(cmap.getTileList())
    # cmap.buildStuff("jakob", "VILLAGE", (4, 5, 10), 0)
    # cmap.buildStuff("jakob", "CITY", (4, 5, 10))
    # cmap.buildStuff("jakob", "VILLAGE", (2, 6, 1), 0)
    # cmap.buildStuff("jakob", "STREET", (5, 10))
    # cmap.buildStuff("jakob", "STREET", (11, 10))
    # cmap.buildStuff("jakob", "VILLAGE", (10, 11, 17))
    # cmap.buildStuff("lia", "VILLAGE", (13, 19, 20), 0)
    # cmap.buildStuff("jakob", "VILLAGE", (9, 10, 16), 0)
    # print(cmap.getAvailableStreets("jakob"))
    # print(cmap.getTileList())
    # cmap.setBanditPosition(10)
    # for i in range(2, 13):
    #     print(i)
    #     print(cmap.getTilesToValue(i))
