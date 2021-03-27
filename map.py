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
            "WHEAT":4,
            "ORE":3,
            "SHEEP":4,
            "WOOD":4,
            "CLAY":3,
            "DESERT":1
        }
        print("helo")

        #Numbers have to be in that Order
        AVAILABLE_NUMBERS = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3]

        TILES = [
            ("OCEAN",0),("OCEAN",0),("OCEAN",0),("OCEAN",0),
            ("OCEAN",0), (None, "A"), (None, "B"), (None, "C"), ("OCEAN",0),
            ("OCEAN",0), (None, "L"), (None, "M"), (None, "N"), (None, "D"), ("OCEAN",0),
            ("OCEAN",0), (None, "K"), (None, "O"), (None, 11), (None, "P"), (None, "E"), ("OCEAN",0),
            ("OCEAN",0), (None, "J"), (None, "Q"), (None, "R"), (None, "F"), ("OCEAN",0),
            ("OCEAN",0), (None, "I"), (None, "H"), (None, "G"), ("OCEAN",0),
            ("OCEAN",0), ("OCEAN",0), ("OCEAN",0), ("OCEAN",0)
        ]

        for tile in TILES:
            if tile[0] is not None:
                self.TileList.append(tile)
            else: 
                randomTile = random.choice(list(AVAILABLE_TILES.keys()))
                if AVAILABLE_TILES[randomTile] == 1:
                    del AVAILABLE_TILES[randomTile]
                else: AVAILABLE_TILES[randomTile] -= 1
                self.TileList.append(randomTile)
            
        for tileNumber in [6,7,8,14,21,27,32,31,30,24,17,11]:
            pass

if __name__ == "__main__":
    lia = CatanMap()
    lia.generateMap()
    print(lia.TileList)