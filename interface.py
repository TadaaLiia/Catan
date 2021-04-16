# import the pygame module
import pygame
import map
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

MIDPOINT = (400, 50)
FONT_PATH = "data/RobotoMono-Regular.ttf"


class Hex(pygame.sprite.Sprite):
    def __init__(self, color, size=70, number=None, offset=(0, 0)):
        super(Hex, self).__init__()
        self.color = color
        self.size = size
        # Offset soll immer in relation zu einer Hex-Breite bzw Länge sein
        self.number = number
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
        return coordinates

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

    def _drawHex(self, screen, points):
        pygame.draw.polygon(screen, self.color, points)

    def _drawOutline(self, screen, points):
        pygame.draw.lines(screen, DARK_GRAY, closed=True,
                          points=points, width=1)

    def draw(self, screen, game_font):
        hex_coordinates = self.calcHexCoordinates()
        self._drawHex(screen, hex_coordinates)
        self._drawNum(screen, game_font)
        self._drawOutline(screen, hex_coordinates)


class CatanBoard():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 1200))
        self.running = True
        self.game_font = pygame.freetype.Font(FONT_PATH, 24)
        self.hexes = []
        # blue_hex = Hex(BLUE, number=5)
        # blue_hex.draw(self.screen, self.game_font)
        # Hex mit Offset = (1,0) ist dann rechts neben dem Center-Hex
        # Hex mit offset = (0.5, 3/4) ist rechts unten neben dem Center-Hex
        # green_hex = Hex(GREEN, number=9, offset=(1,0))
        # green_hex.draw(self.screen, self.game_font)
        catanMap = map.CatanMap()
        self.generateBoard(catanMap.generateMap())
        self.gameloop()

    def buildGrid(self):
        # Layers is a number representing the number of rings
        # Layers = 1
        #    [x][x]
        #   [x][x][x]
        #    [x][x]
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
        # (0,0) -> (0,0)
        # (1,0) -> (- 0.5, 3/4)
        horizontal_offsets = [0, -0.5, -1, -1.5, -1, -0.5, 0]
        base_offset = (0, 0)
        for row in range(len(offsets)):
            base_offset = (horizontal_offsets[row], base_offset[1] + 3 / 4)
            for column in range(len(offsets[row])):
                result.append((base_offset[0] + column, base_offset[1]))
        return result

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
        i = 0
        for Tile in TileList:
            newHex = Hex(mapping[Tile[0]], number=Tile[1], offset=offsets[i])
            newHex.draw(self.screen, self.game_font)
            self.hexes.append(newHex)
            i += 1

    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # If the Backspace key has been pressed set
                    # running to false to exit the main loop
                    if event.key == K_BACKSPACE:
                        gameOn = False
                elif event.type == QUIT:
                    running = False

                # Update the Display
                pygame.display.flip()


if __name__ == "__main__":
    board = CatanBoard()
    board.buildGrid()
