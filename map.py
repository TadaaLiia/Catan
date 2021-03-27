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
        print(tile_order)

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
