from abc import ABC, abstractmethod
import pygame
pygame.init();

# --------------- Event Handling Functions ------------




# --------------- World Generation ------------------

# Generates the map which is a 2d list of tiles
def generateMap() :
    heightMap = generateHeightMap()
    return generateTileMap(heightMap)

# Generates a 2d list of floats all 0.0
# to represent the map in terms of its height
def generateHeightMap() :
    heightMap = []
    for y in range(0, int(HEIGHT / TILE_SIZE)) :
        row = []
        for x in range(0, int(WIDTH / TILE_SIZE)):
            row.append(0.0)
        heightMap.append(row)
    return heightMap

# Generates a 2d lisst of tile objects based on
# the height map given as a parameter
def generateTileMap(heightMap) :
    tileMap = []
    for y in range(len(heightMap)) :
        tileRow = []
        for x in range(len(heightMap[y])) :
            if(heightMap[y][x] > 0.0) :
                tileRow.append(LandTile(x, y, heightMap[y][x]))
            else :
                tileRow.append(OceanTile(x, y, heightMap[y][x]))
        tileMap.append(tileRow)
    return tileMap

# --------------- Class definitions -----------------

# Entity is the grandfather class of all things in the game
class Entity(ABC):
    'Common base class for all game entities'

    # Fields
    # int x, int y, int idVal
    # float velX, float velY, float accX, float accY
    def __init__(self, x, y, velX, velY, accX, accY, idVal):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.accX = accX
        self.accY = accY
        self.idVal = idVal

# Tile is the grandfather class for all background tiles in the game
class Tile(ABC):
    'Generic tile for building the world'

    #Fields
    # int x, int y, float height
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    # Returns an int that indicates the x position of the tile in pixels
    def xPixels(self):
        return self.x * TILE_SIZE

    # Returns an int that indicates the y position of the tile in pixels
    def yPixels(self):
        return self.y * TILE_SIZE

    # draws this tile on the main canvas
    @abstractmethod
    def render(self):
        pass

class OceanTile(Tile):
    'Ocean tile to mark water'

    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas
    def render(self):
        pygame.draw.rect(win, (0, 66, 146),
            (Tile.xPixels(self), Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class LandTile(Tile):
    'Land tile to mark land'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self):
        pygame.draw.rect(win, (0, 196, 116),
            (Tile.xPixels(self), Tile.yPixels(self), TILE_SIZE, TILE_SIZE))
    


# ------------------------- Game LOOP ----------------------------

# Constants for the window display
WIDTH = 800
HEIGHT = 800
FPS = 60
TILE_SIZE = 10

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# GAME LOOP
# This is the loop that runs the game
# Will loop at FPS amount of times in a second
run = True
world = generateMap()
while run:
    pygame.time.delay(int(1000/FPS))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for row in world :
        for tile in row :
            tile.render()
    
    pygame.display.update()
    
# End the game
pygame.quit()    
