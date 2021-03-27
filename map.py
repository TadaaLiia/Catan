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
        self.TileList = []
        self.Adjacency = self.generateAdjacency()

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

        for tile in TILES:
            if tile[0] is not None:
                self.TileList.append(tile)
            else:
                randomTile = random.choice(list(AVAILABLE_TILES.keys()))
                if AVAILABLE_TILES[randomTile] == 1:
                    del AVAILABLE_TILES[randomTile]
                else:
                    AVAILABLE_TILES[randomTile] -= 1
                self.TileList.append(randomTile)

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
            assert self.TileList[tile][1] != 0
            if self.TileList[tile] == "DESERT":
                self.TileList[tile] = ("DESERT", 0)
            else:
                self.TileList[tile] = (self.TileList[tile], AVAILABLE_NUMBERS.pop(0))


if __name__ == "__main__":
    lia = CatanMap()
    lia.generateMap()
    print(lia.TileList)
