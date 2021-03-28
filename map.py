import random


class CatanMap:
    """
    - Tile List (Ressource, Number)
    - Adjacency Matrix (NxN - N = Anzahl Tiles)
    - Structure List [
        {"Type":"Village", "Player":"Blue", "Position":"X;Y"}
    ]
        """

    def __init__(self):
        self.BanditPosition = 0
        self.TileList = self.generateMap()
        self.Adjacency = self.generateAdjacency()
        self.ObjectList = self.initializeObjectList()

    def generateAdjacency(self):
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

        for i in range(len(x)):
            for j in x[i]:
                if x[i][j] == 1:
                    x[j][i] = 1

        return x

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
                self.setBandit(tile)
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

    # ----
    def buildStuff(self, player, type, position):
        if type == "STREET":
            assert len(position) == 2, "invalid position"
        elif type == "VILLAGE" or type == "CITY":
            assert len(position) == 3, "invalid position"
        else:
            print("incorrect type")
            return
        self.ObjectList.append({"player": player, "type": type, "position": position})

    def setBandit(self, position):
        assert type(position) == int, "invalid Bandit position"
        self.BanditPosition = position


if __name__ == "__main__":
    lia = CatanMap()
