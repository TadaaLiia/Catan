import enum


class Tiles(enum.Enum):
    WOOD = 1
    CLAY = 2
    SHEEP = 3
    WHEAT = 4
    ORE = 5
    DESERT = 6
    OCEAN = 7


class Resources(enum.Enum):
    WOOD = 1
    CLAY = 2
    SHEEP = 3
    WHEAT = 4
    ORE = 5


class Ports(enum.Enum):
    NONE = 0
    WOOD = Resources.WOOD.value
    CLAY = Resources.CLAY.value
    SHEEP = Resources.SHEEP.value
    WHEAT = Resources.WHEAT.value
    ORE = Resources.ORE.value
    PORT = 6


class DevelopmentCards(enum.Enum):
    KNIGHT_CARD = 1
    VICTORY_POINT_CARD = 2
    MONOPOLY = 3
    DEVELOPMENT = 4
    CONSTRUCTION = 5


class Objects(enum.Enum):
    STREET = 1
    VILLAGE = 2
    CITY = 3
