# import the pygame module
import pygame
import map
# import simulation
import entities
import gamestate

from entities import *

# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *
import pygame.freetype
import math

BLUE = pygame.Color("#78e3fd")
WHITE = pygame.Color("#F8F7F9")
DARK_GREEN = pygame.Color("#082d0f")
GREEN = pygame.Color("#7FB800")
GRAY = pygame.Color("#8B8982")
YELLOW = pygame.Color("#FED766")
BROWN = pygame.Color("#7A4419")
DARK_GRAY = pygame.Color("#3C3C3C")
BRIGHT_RED = pygame.Color("#AE0700")
DARK_RED = pygame.Color("#800000")



MIDPOINT = (400, 50)
FONT_PATH = "data/RobotoMono-Regular.ttf"


class Node(pygame.sprite.Sprite):

    def __init__(self):
        self.state = 0  # 1 = village, 2 = city
        self.position = list()
        self.coords = (0, 0)
        self.villageImg = pygame.image.load('textures/villageblue.png')
        self.cityImg = pygame.image.load('textures/cityblue.png')

    def updatePos(self, pos):
        if len(self.position) + len(pos) <= 3:
            self.position.extend(pos)

    def getPos(self):
        return self.position

    def setCoords(self, coords):
        if type(coords) == tuple:
            self.coords = coords

    def buildVillage(self, screen):
        if self.state == 0:
            self.state = 1
            imgSize = self.villageImg.get_rect().size
            imgCoords = (self.coords[0] - imgSize[0]/2,
                         self.coords[1] - imgSize[1])
            screen.blit(self.villageImg, imgCoords)
        else:
            raise ValueError("Village or City already present")

    def buildCity(self, screen):
        if self.state == 1:
            self.state = 2
            imgSize = self.cityImg.get_rect().size
            imgCoords = (self.coords[0] - imgSize[0]/2,
                         self.coords[1] - imgSize[1])
            screen.blit(self.cityImg, imgCoords)
        else:
            raise ValueError("No village on this node")

class Hex(pygame.sprite.Sprite):
    def __init__(self, _id, color, size=70, number=None, offset=(0, 0)):
        super(Hex, self).__init__()
        self.id = _id
        self.color = color
        self.size = size
        self.number = number
        self.adjacentNodes = {}
        # Offset soll immer in relation zu einer Hex-Breite bzw Länge sein
        self.offset = (offset[0] * self.size, offset[1] * self.size)

    def calcHexCoordinates(self):
        # In the pointy orientation, a hexagon has width w = sqrt(3) * size
        # and height h = 2 * size. The sqrt(3) comes from sin(60°).
        hex_MIDPOINT = (MIDPOINT[0] + (self.offset[0] *
                        math.sqrt(3)), MIDPOINT[1] + (self.offset[1] * 2))
        x_width = self.size * math.sqrt(3)
        y_height = self.size * 2
        coordinates = [
            ((hex_MIDPOINT[0] - (x_width * 0.5)),
             (hex_MIDPOINT[1] + (0.25 * y_height))),
            (hex_MIDPOINT[0], (hex_MIDPOINT[1] + (0.5 * y_height))),
            ((hex_MIDPOINT[0] + (x_width * 0.5),
             (hex_MIDPOINT[1] + (0.25 * y_height)))),
            ((hex_MIDPOINT[0] + (x_width * 0.5),
             (hex_MIDPOINT[1] - (0.25 * y_height)))),
            (hex_MIDPOINT[0], (hex_MIDPOINT[1] - (0.5 * y_height))),
            ((hex_MIDPOINT[0] - (x_width * 0.5)), (hex_MIDPOINT[1] - (0.25 * y_height)))]
        return [(int(coords[0]),int(coords[1])) for coords in coordinates]

    def _drawNum(self, screen, game_font):
        if not self.number:
            return
        hex_MIDPOINT = (MIDPOINT[0] + (self.offset[0] *
                        math.sqrt(3)), MIDPOINT[1] + (self.offset[1] * 2))
        coordinates = (hex_MIDPOINT[0], hex_MIDPOINT[1])
        number, number_rect = game_font.render(
            str(self.number), WHITE)
        number_rect.center = coordinates
        screen.blit(number, number_rect)

    def _drawId(self, screen):
        _font = pygame.freetype.Font(FONT_PATH, 12)
        hex_MIDPOINT = (MIDPOINT[0] + (self.offset[0] *
                        math.sqrt(3)), MIDPOINT[1] + (self.offset[1] * 2))
        coordinates = (hex_MIDPOINT[0], hex_MIDPOINT[1] - self.size * .8)
        number, number_rect = _font.render(
            str(self.id), DARK_GRAY)
        number_rect.center = coordinates
        screen.blit(number, number_rect)

    def _drawHex(self, screen, points):
        pygame.draw.polygon(screen, self.color, points)

    def _drawOutline(self, screen, points):
        pygame.draw.lines(screen, DARK_GRAY, closed=True,
                          points=points, width=1)

    def _indexNodes(self, hex_coordinates):
        for node in hex_coordinates:
            tmpNode = Node()
            tmpNode.updatePos([self.id])
            tmpNode.setCoords(node)
            # floor coordinates because point calculation is not accurate enough to be used for comparison
            key = tuple((math.floor(coord) for coord in node))
            self.adjacentNodes[key] = tmpNode

    def getNodes(self):
        return self.adjacentNodes

    def getNumber(self):
        return self.number

    def draw(self, screen, game_font):
        hex_coordinates = self.calcHexCoordinates()
        self._drawHex(screen, hex_coordinates)
        self._drawNum(screen, game_font)
        self._drawId(screen)
        self._drawOutline(screen, hex_coordinates)
        self._indexNodes(hex_coordinates)


class CatanBoard():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 1200))
        self.running = True
        self.game_font = pygame.freetype.Font(FONT_PATH, 24)
        self.hexes = []
        self.nodes = {}
        catanMap = map.CatanMap()
        self.generateBoard(catanMap.generateMap())
        self.gamestate = gamestate.Gamestate("p1", "p2", "p3", "p4")
        # self.simulation = simulation.Simulation(gamestate)
        self.getColorForName("p1")
        self.buildStreet((7,13), WHITE)
        self.buildVillage((7,12,13), WHITE)
        self.buildCity((18,12,19), WHITE)
        self.drawBandit(12)
        self.gameloop()

    def buildStreet(self, pos, color):
        assert type(pos) == tuple and len(pos) == 2, "Invalid Position"
        width = 6
        height_offset = 3
        
        #find coordinates for pos
        hexes = [hex for hex in self.hexes if hex.id in pos]
        intersecting_coordinates = list(set(hexes[0].calcHexCoordinates()) & set(hexes[1].calcHexCoordinates()))
        print(intersecting_coordinates)
        
        #draw the Street
        pygame.draw.line(self.screen, WHITE, intersecting_coordinates[0], intersecting_coordinates[1], width=6)

    def buildVillage(self, pos, color):
        assert type(pos) == tuple and len(pos) == 3, "Invalid Position"
        size = 12

        #find coordinates for pos
        hexes = [hex for hex in self.hexes if hex.id in pos]
        intersecting_coordinates = list(set(hexes[0].calcHexCoordinates()) & set(hexes[1].calcHexCoordinates()) & set(hexes[2].calcHexCoordinates()))
        print(intersecting_coordinates)
        
        #draw the Village
        points = [
            (intersecting_coordinates[0][0],intersecting_coordinates[0][1] - (size)),
            (intersecting_coordinates[0][0] - size,intersecting_coordinates[0][1] + (size)),
            (intersecting_coordinates[0][0] + size,intersecting_coordinates[0][1] + (size)),
        ]
        pygame.draw.polygon(self.screen, color, points)
        
        #draw Outline
        pygame.draw.lines(self.screen, DARK_GRAY, closed=True, points=points, width=1)
        
    def buildCity(self, pos, color):
        assert type(pos) == tuple and len(pos) == 3, "Invalid Position"
        size = 15

        #find coordinates for pos
        hexes = [hex for hex in self.hexes if hex.id in pos]
        print([hex.calcHexCoordinates() for hex in hexes])
        intersecting_coordinates = list(set(hexes[0].calcHexCoordinates()) & set(hexes[1].calcHexCoordinates()) & set(hexes[2].calcHexCoordinates()))
        print(intersecting_coordinates)
        
        #draw the Village
        points = [
            (intersecting_coordinates[0][0] - size,intersecting_coordinates[0][1] - (size)),
            (intersecting_coordinates[0][0] - size,intersecting_coordinates[0][1] + (size)),
            (intersecting_coordinates[0][0] + size,intersecting_coordinates[0][1] + (size)),
            (intersecting_coordinates[0][0] + size,intersecting_coordinates[0][1] - (size))
        ]
        pygame.draw.polygon(self.screen, color, points)
        
        #draw Outline
        pygame.draw.lines(self.screen, DARK_GRAY, closed=True, points=points, width=1)
        
    def drawBandit(self, pos):
        assert type(pos) == int, "Invalid Position"
        
        #Get Coordinates for Hex
        hexes = [hex for hex in self.hexes if hex.id == pos]
        coordinates = [hex.calcHexCoordinates() for hex in hexes][0]
        
        #draw red x
        pygame.draw.line(self.screen, DARK_RED, coordinates[0], coordinates[3], width=6)
        pygame.draw.line(self.screen, DARK_RED, coordinates[2], coordinates[5], width=6)

    def buildGrid(self):
        offsets = [
            [0, 1, 2, 3],
            [4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19, 20, 21],
            [22, 23, 24, 25, 26, 27],
            [28, 29, 30, 31, 32],
            [33, 34, 35, 36]
        ]
        result = []
        horizontal_offsets = [0, -0.5, -1, -1.5, -1, -0.5, 0]
        base_offset = (0, 0)
        for row in range(len(offsets)):
            base_offset = (horizontal_offsets[row], base_offset[1] + 3 / 4)
            for column in range(len(offsets[row])):
                result.append((base_offset[0] + column, base_offset[1]))
        return result

    def _updateNodes(self, nodeDict):
        for key in nodeDict.keys():
            if key in self.nodes.keys():
                self.nodes[key].updatePos(nodeDict[key].getPos())
            else:
                self.nodes[key] = nodeDict[key]

    def _cleanNodes(self):
        newNodes = {}
        for key in self.nodes.keys():
            pos = tuple(sorted(self.nodes[key].getPos()))
            if len(pos) == 3:
                newNodes[pos] = self.nodes[key]
        self.nodes = newNodes

    def generateBoard(self, TileList):
        offsets = self.buildGrid()
        mapping = {
            Tiles.WHEAT: YELLOW,
            Tiles.ORE: GRAY,
            Tiles.SHEEP: GREEN,
            Tiles.WOOD: DARK_GREEN,
            Tiles.CLAY: BROWN,
            Tiles.DESERT: WHITE,
            Tiles.OCEAN: BLUE
        }
        for i, Tile in enumerate(TileList):
            newHex = Hex(i, mapping[Tile[0]],
                         number=Tile[1], offset=offsets[i])
            newHex.draw(self.screen, self.game_font)
            self.hexes.append(newHex)
            self._updateNodes(newHex.getNodes())
        self._cleanNodes()

    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        # reset board
                        pass
                    elif event.key == K_RIGHT:
                        # show next step
                        firstNode = list(self.nodes.keys())[0]
                        print(firstNode)
                        self.nodes[firstNode].buildVillage(
                            self.screen)
                        pass
                    elif event.key == K_LEFT:
                        # show previous step
                        pass
                elif event.type == QUIT:
                    self.running = False

                pygame.display.flip()

    # Playerinteraction
    def getColorForName(self, playerName):
        prio = self.gamestate.getPlayerForName(playerName).getPriority()
        return PlayerColor(prio).name


if __name__ == "__main__":
    board = CatanBoard()
