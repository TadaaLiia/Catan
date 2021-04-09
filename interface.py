# import the pygame module
import pygame
 
# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *
import pygame.freetype

BLUE = pygame.Color(0, 0, 128)
WHITE = pygame.Color(255, 255, 255)
GREEN = (0, 200, 0 )
MIDPOINT = (400, 400)
FONT_PATH = "data/RobotoMono-Regular.ttf"

class Hex(pygame.sprite.Sprite):
    def __init__(self, color, size=20, number=None, offset=(0, 0)):
        super(Hex, self).__init__()
        self.color = color
        self.size = size
        # Offset soll immer in relation zu einer Hex-Breite bzw Länge sein
        self.offset = (offset[0] * 3, offset[1] * 4)
        self.number = number

    def calcHexCoordinates(self):
        coordinates = [
            ((MIDPOINT[0] - int(1.5 * self.size) + (self.offset[0] * self.size * 1.5)), (MIDPOINT[1]  + int(1 * self.size)) + (self.offset[1] * self.size)),
            (MIDPOINT[0] + (self.offset[0] * self.size), (MIDPOINT[1] + int(2 * self.size)) + (self.offset[1] * self.size)),
            ((MIDPOINT[0] + int(1.5 * self.size) + (self.offset[0] * self.size * 1.5)), (MIDPOINT[1] + int(1 * self.size)) + (self.offset[1] * self.size)),
            ((MIDPOINT[0] + int(1.5 * self.size) + (self.offset[0] * self.size * 1.5)), (MIDPOINT[1] - int(1 * self.size)) + (self.offset[1] * self.size)),
            (MIDPOINT[0] + (self.offset[0] * self.size), (MIDPOINT[1] - int(2 * self.size)) + (self.offset[1] * self.size)),
            ((MIDPOINT[0] - int(1.5 * self.size) + (self.offset[0] * self.size * 1.5)), (MIDPOINT[1] - int(1 * self.size)) + (self.offset[1] * self.size))]
        print(coordinates)
        return coordinates
 
    def _drawNum(self, screen, game_font):
        if not self.number: return
        coordinates = (MIDPOINT[0] + (self.offset[0] * self.size), MIDPOINT[1] + (self.offset[1] * self.size))
        game_font.render_to(screen, coordinates, str(self.number), WHITE)

    def _drawHex(self, screen):
        pygame.draw.polygon(screen, self.color, self.calcHexCoordinates())

    def draw(self, screen, game_font):
        self._drawHex(screen)
        self._drawNum(screen, game_font)




class CatanBoard():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.running = True
        self.game_font = pygame.freetype.Font(FONT_PATH, 24)
        blue_hex = Hex(BLUE, number=5)
        blue_hex.draw(self.screen, self.game_font)
        # x-Achsen Berechnung ist kinda bugged
        green_hex = Hex(GREEN, number=9, offset=(0,1))
        green_hex.draw(self.screen, self.game_font)

        self.gameloop()

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

