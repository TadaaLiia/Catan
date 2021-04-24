import enum


class Resources(enum.Enum):
    WOOD = 1
    CLAY = 2
    SHEEP = 3
    WHEAT = 4
    ORE = 5

    def __eq__(self, other):
        if isinstance(other, Resources):
            return self is other
        elif isinstance(other, Ports) or isinstance(other, Tiles):
            return self.value == other.value
        else:
            return False

    def __hash__(self):
        return self.value


class Tiles(enum.Enum):
    WOOD = Resources.WOOD.value
    CLAY = Resources.CLAY.value
    SHEEP = Resources.SHEEP.value
    WHEAT = Resources.WHEAT.value
    ORE = Resources.ORE.value
    DESERT = 6
    OCEAN = 7

    def __eq__(self, other):
        if isinstance(other, Tiles):
            return self is other
        elif isinstance(other, Resources):
            return self.value == other.value
        else:
            return False

    def __hash__(self):
        return self.value


class Ports(enum.Enum):
    NONE = 0
    WOOD = Resources.WOOD.value
    CLAY = Resources.CLAY.value
    SHEEP = Resources.SHEEP.value
    WHEAT = Resources.WHEAT.value
    ORE = Resources.ORE.value
    PORT = 6

    def __eq__(self, other):
        if isinstance(other, Ports):
            return self is other
        elif isinstance(other, Resources):
            return self.value == other.value
        else:
            return False

    def __hash__(self):
        return self.value


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


class PlayerColor(enum.Enum):
    ORANGE = 0
    BLUE = 1
    WHITE = 2
    RED = 3
