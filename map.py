import random
from entities import *
from player import *


class Map:
    """
    Representation and generation of the board
    - BanditPosition: int, tileNumber
    - Adjacency: Matrix(36x36), adjacent tiles
    - AvailableNodes: List, availableNodes(x,y,z)
    - TileList: List, (TileType, value)
    - ObjectList: {player:name, type:a, position:(x,y)}

    - buildStuff: objectList.append
    - setBandit: newTileNumber
    """

    def __init__(self):
        self.BanditPosition = 0
        self.Adjacency = self.generateAdjacency()
        self.AvailableNodes = self.generateNodeList()
        self.TileList = self.generateTileList()
        self.PortDict = self.initializePortDict()
        self.ObjectList = []

    # ---- setter ----
    def setBanditPosition(self, position):
        assert type(position) == int, "invalid Bandit position"
        self.BanditPosition = position

    # ---- generation and initialization ----
    def generateAdjacency(self):
        '''
        returns: Matrix(36x36), adjacent tiles
        '''
        #     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
        x = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
             [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
             [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
             [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
             [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
             [0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
             [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
             [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
             [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
             [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 16
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 20
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 21
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 22
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 23
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 24
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # 25
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # 26
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 27
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 28
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0],  # 29
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0],  # 30
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],  # 31
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 32
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 33
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 34
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # 35
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]  # 36

        # x = [[0] * 37] * 37
        '''
        x = []
        for i in range(37):
            x.append([0 for jakob in range(37)])

        TILES_1 = [5, 6, 7]
        for tile in TILES_1:
            nachbar = [tile - 5, tile - 4, tile - 1, tile + 1, tile + 5, tile + 6]
            for n in nachbar:
                x[tile][n] = 1

        TILES_2 = [10, 11, 12, 13]
        for tile in TILES_2:
            nachbar = [tile - 6, tile - 5, tile - 1, tile + 1, tile + 6, tile + 7]
            for n in nachbar:
                x[tile][n] = 1

        TILES_3 = list(range(16, 21))
        for tile in TILES_3:
            nachbar = [tile - 7, tile - 6, tile - 1, tile + 1, tile + 6, tile + 7]
            for n in nachbar:
                x[tile][n] = 1

        TILES_4 = list(range(23, 27))
        for tile in TILES_4:
            nachbar = [tile - 7, tile - 6, tile - 1, tile + 1, tile + 5, tile + 6]
            for n in nachbar:
                x[tile][n] = 1

        TILES_5 = [29, 30, 31]
        for tile in TILES_5:
            nachbar = [tile - 6, tile - 5, tile - 1, tile + 1, tile + 4, tile + 5]
            for n in nachbar:
                x[tile][n] = 1

        for i in range(37):
            for j in x[i]:
                if x[i][j] == 1:
                    x[j][i] = 1
        '''

        return x

    def generateNodeList(self):
        '''
        returns: List of valid nodes
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

    def generateTileList(self, seed=None):
        """
        returns TileList: TileType and Number
        """
        AVAILABLE_TILES = {
            Tiles.WHEAT: 4,
            Tiles.ORE: 3,
            Tiles.SHEEP: 4,
            Tiles.WOOD: 4,
            Tiles.CLAY: 3,
            Tiles.DESERT: 1
        }

        # Numbers have to be in that Order
        MAXSPDCBR = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

        TILES = [
            (Tiles.OCEAN, 0), (Tiles.OCEAN, 0), (Tiles.OCEAN, 0), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (None, "A"), (None, "B"), (None, "C"), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (None, "L"), (None, "M"), (None, "N"), (None, "D"), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (None, "K"), (None, "O"), (None, "X"), (None, "P"), (None, "E"), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (None, "J"), (None, "Q"), (None, "R"), (None, "F"), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (None, "I"), (None, "H"), (None, "G"), (Tiles.OCEAN, 0),
            (Tiles.OCEAN, 0), (Tiles.OCEAN, 0), (Tiles.OCEAN, 0), (Tiles.OCEAN, 0)
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
            if tileList[tile] == Tiles.DESERT:
                tileList[tile] = (Tiles.DESERT, 0)
                self.setBanditPosition(tile)
            else:
                tileList[tile] = (tileList[tile], MAXSPDCBR.pop(0))
        return tileList

    def initializePortDict(self):
        """
        returns PortDict
        """
        portDict = {
            Ports.PORT: [(0, 1, 5), (0, 4, 5), (7, 8, 13), (8, 13, 14), (14, 20, 21), (20, 21, 27), (28, 29, 33), (29, 33, 34)],
            Ports.SHEEP: [(1, 2, 6), (2, 6, 7)],
            Ports.ORE: [(4, 9, 10), (9, 10, 16)],
            Ports.WOOD: [(30, 31, 35), (30, 34, 35)],
            Ports.CLAY: [(26, 27, 32), (26, 31, 32)],
            Ports.WHEAT: [(16, 22, 23), (22, 23, 28)]
        }
        return portDict

    # ---- Board ----
    def updateAvailableNodes(self, position):
        """
        updates available nodes depending on input position, deletes up to 3 adjacent nodes to position
        """
        # sorted position
        pos = tuple(sorted(position))
        # valid position?
        nodes = self.AvailableNodes
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

    def getTilesForValue(self, value):
        tiles = []
        i = 0
        for tile in self.TileList:
            if tile[1] == value and self.BanditPosition != i:
                tiles.append((i, tile[0]))
            i += 1
        return(tiles)

    def getVillagesForTile(self, tile):
        allVillages = [(x["player"], x["position"]) for x in self.ObjectList if x["type"] == Objects.VILLAGE]
        villages = []
        for v in allVillages:
            if v[1][0] == tile or v[1][1] == tile or v[1][2] == tile:
                villages.append(v[0])
        return villages

    def getCitiesForTile(self, tile):
        allCities = [(x["player"], x["position"]) for x in self.ObjectList if x["type"] == Objects.CITY]
        cities = []
        for c in allCities:
            if c[1][0] == tile or c[1][1] == tile or c[1][2] == tile:
                cities.append(c[0])
        return cities

    # ---- Player ----
    def getPlayerShit(self, id):
        """
        returns objects of player
        """
        objects = [x for x in self.ObjectList if x["player"] == id]
        buildings = [x["position"] for x in objects if x["type"] != Objects.STREET]
        streets = [x["position"] for x in objects if x["type"] == Objects.STREET]
        return objects, buildings, streets

    def getAvailableStreets(self, id):
        # All player Objects
        playerObjects, playerBuildings, playerStreets = self.getPlayerShit(id)
        # Streets
        allStreets = [x["position"] for x in self.ObjectList if x["type"] == Objects.STREET]
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
                if self.Adjacency[street[0]][x] == 1 and self.Adjacency[street[1]][x] == 1:
                    availableStreets.append((x, street[0]))
                    availableStreets.append((x, street[1]))
        # print(availableStreets)
        # remove Streets in Oceans or unavailable streets
        final = []
        for street in availableStreets:
            if self.Adjacency[street[0]][street[1]] == 1 and street not in allStreets:
                final.append(tuple(sorted(street)))
        final = list(dict.fromkeys(final))
        return sorted(final)

    def getAvailableVillages(self, id, round=1):
        if round == 0:
            return self.AvailableNodes
        else:
            playerObjects, playerBuildings, playerStreets = self.getPlayerShit(id)
            availableVillages = []
            for node in self.AvailableNodes:
                # angrenzende strasse an nodes
                if (node[0], node[1]) in playerStreets or (node[0], node[2]) in playerStreets or (node[1], node[2]) in playerStreets:
                    availableVillages.append(node)
            return sorted(availableVillages)

    def getAvailableCities(self, id, round=1):
        assert round != 0, "you are not allowed to build cities."
        playerObjects, playerBuildings, playerStreets = self.getPlayerShit(id)
        return [x["position"] for x in playerObjects if x["type"] == Objects.VILLAGE]

    def buildStuff(self, id, type, position, round=1):
        pos = tuple(sorted(position))
        # Street -> (x,y) in available streets(id)
        if type == Objects.STREET:
            assert len(pos) == 2, "invalid position"
            assert pos in self.getAvailableStreets(id), "street not available"
            self.ObjectList.append({"player": id, "type": type, "position": pos})
        # Village -> (x,y,z) in availableNodes
        elif type == Objects.VILLAGE:
            assert len(pos) == 3, "invalid position"
            assert pos in self.getAvailableVillages(id, round), "node not available or two streets required!"
            self.ObjectList.append({"player": id, "type": type, "position": pos})
            self.updateAvailableNodes(pos)
        # City -> {player,village,(x,y,z)} in ObjectList
        elif type == Objects.CITY:
            assert len(pos) == 3, "invalid position"
            assert pos in self.getAvailableCities(id), "no village available"
            self.ObjectList.append({"player": id, "type": type, "position": pos})
            self.ObjectList.remove({"player": id, "type": Objects.VILLAGE, "position": pos})
        else:
            print("incorrect type")
            return


if __name__ == "__main__":
    cmap = Map()
    # print(cmap.TileList)
    # print(cmap.Adjacency)
    print(cmap.AvailableNodes)
    cmap.buildStuff(0, Objects.VILLAGE, (10, 11, 17), 0)
    cmap.buildStuff(0, Objects.VILLAGE, (18, 24, 25), 0)
    cmap.buildStuff(0, Objects.STREET, (10, 17), 0)
    cmap.buildStuff(0, Objects.STREET, (24, 25), 0)
    cmap.buildStuff(1, Objects.VILLAGE, (23, 24, 29), 0)
    cmap.buildStuff(1, Objects.VILLAGE, (12, 13, 19), 0)
    cmap.buildStuff(1, Objects.STREET, (13, 19), 0)
    cmap.buildStuff(1, Objects.STREET, (23, 24), 0)
    print("-----")
    print(cmap.AvailableNodes)
    # print(cmap.getAvailableStreets(0))
    # print(cmap.getPlayerShit(0))
