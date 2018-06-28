from abc import ABC, abstractmethod
from opensimplex import OpenSimplex
import pygame
pygame.init();

# --------------- Event Handling Functions ------------

# handles all the keys events
def keyHandler(keys):
    if keys[pygame.K_w] :
        player.velY = -10
    elif keys[pygame.K_s] :
        player.velY = 10
    else :
        player.velY = 0
    if keys[pygame.K_a] :
        player.velX = -10
    elif keys[pygame.K_d] :
        player.velX = 10
    else :
        player.velX = 0

# --------------- Rendering Functions ---------------

# Limits the view only to a certain section of the map
#def renderTerrain() :
#    screenWidth = int(WIDTH * 1.25 / TILE_SIZE)
#    screenHeight = int(HEIGHT * 1.25 / TILE_SIZE)
#    topLX = limit(int(player.x / TILE_SIZE) - int(screenWidth / 2))
#    topLY = limit(int(player.y / TILE_SIZE) - int(screenHeight / 2))
#    bottomRX = limit(int(player.x / TILE_SIZE) + int(screenWidth / 2))
#    bottomRY = limit(int(player.y / TILE_SIZE) + int(screenHeight / 2))
#    for y in range(topLY, bottomRY) :
#        for x in range(topLX, bottomRX) :
#            world[y][x].render(topLX, topLY)

def renderTerrain() :
    for row in world :
        for tile in row :
            tile.render(0, 0)

def limit(n) :
    if(n < 0) :
        return 0
    if(n > MAP_SIZE) :
        return MAP_SIZE
    return n


# --------------- World Generation ------------------

# Generates the map which is a 2d list of tiles
def generateMap() :
    heightMap = generateHeightMap()
    return generateTileMap(heightMap)

# Generates a 2d list of floats all 0.0
# to represent the map in terms of its height
def generateHeightMap() :
    heightMap = []
    for y in range(0, int(MAP_SIZE)) :
        row = []
        for x in range(0, int(MAP_SIZE)):
            row.append(scale(genHeight(x, y)))
        heightMap.append(row)
    return heightMap

# Generates a float using noise function
# range is from MIN_SCALE to MAX_SCALE inclusive
def genHeight(x, y):
    n1 = 0.75 * (noise.noise2d(FREQUENCY * x, FREQUENCY * y) + 1) / 2
    n2 = 0.20 * (noise.noise2d(2 * FREQUENCY * x, 2 * FREQUENCY * y) + 1) / 2
    n3 = 0.05 * (noise.noise2d(4 * FREQUENCY * x, 4 * FREQUENCY * y) + 1) / 2
    e = (n1 + n2 + n3) + LAND_CONST - (WATER_CONST * pow(dist(x, y) /
    MANHATTAN_DIST, DROP_CONST))
    return pow(e, POW_CONST)

# Calculates the manhattan distance given the x and y
def dist(x, y):
    return abs((MAP_SIZE / 2) - x) + abs((MAP_SIZE / 2) - y)

# Scales a value from MIN_SCALE to MAX_SCALE
def scale(val):
    return int(val * (MAX_SCALE - MIN_SCALE) + MIN_SCALE)

# Generates a 2d list of tile objects based on
# the height map given as a parameter
def generateTileMap(heightMap) :
    tileMap = []
    for y in range(len(heightMap)) :
        tileRow = []
        for x in range(len(heightMap[y])) :
            if(heightMap[y][x] <= WATER_LEVEL) :
                tileRow.append(OceanTile(x, y, heightMap[y][x]))
            elif(heightMap[y][x] <= BEACH_LEVEL) :
                tileRow.append(BeachTile(x, y, heightMap[y][x]))
            elif(heightMap[y][x] <= PLAIN_LEVEL) :
                tileRow.append(PlainTile(x, y, heightMap[y][x]))
            elif(heightMap[y][x] <= JUNGLE_LEVEL) :
                tileRow.append(JungleTile(x, y, heightMap[y][x]))
            elif(heightMap[y][x] <= MOUNTAIN_LEVEL) :
                tileRow.append(MountainTile(x, y, heightMap[y][x]))
            else :
                tileRow.append(SnowTile(x, y, heightMap[y][x]))
        tileMap.append(tileRow)
    return tileMap

# --------------- Class definitions -----------------

# Entity is the grandfather class of all things in the game
class Entity(ABC):
    'Common base class for all game entities'

    # Fields
    # int x, int y, int idVal
    # int velX, int velY, int accX, int accY
    def __init__(self, x, y, velX, velY, accX, accY, idVal):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.accX = accX
        self.accY = accY
        self.idVal = idVal

    @abstractmethod
    def render(self):
        pass

    def update(self):
        self.x += self.velX
        self.y += self.velY
        self.velX += self.accX
        self.velY += self.accY

class Player(Entity):
    'Represents the player in the game'
    def __init__(self, x, y, velX, velY, accX, accY, idVal):
        Entity.__init__(self, x, y, velX, velY, accX, accY, idVal)

    def render(self):
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y, 30, 30))

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
    def xPixels(self, offX):
        return (self.x * TILE_SIZE) - (player.x % TILE_SIZE) - (offX *
        TILE_SIZE)

    # Returns an int that indicates the y position of the tile in pixels
    def yPixels(self, offY):
        return (self.y * TILE_SIZE) - (player.y % TILE_SIZE) - (offY *
        TILE_SIZE)

    # draws this tile on the main canvas
    @abstractmethod
    def render(self, offX, offY):
        pass

class OceanTile(Tile):
    'Ocean tile to mark water'

    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas
    def render(self, offX, offY):
        pygame.draw.rect(win, (0, 66, 146), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

class PlainTile(Tile):
    'Land tile to mark plains'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, offX, offY):
        pygame.draw.rect(win, (116, 196, 116), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

class BeachTile(Tile):
    'Land tile to mark beach'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, offX, offY):
        pygame.draw.rect(win, (255, 238, 173), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

class JungleTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, offX, offY):
        pygame.draw.rect(win, (45, 116, 45), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

class MountainTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, offX, offY):
        pygame.draw.rect(win, (116, 116, 116), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

class SnowTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, offX, offY):
        pygame.draw.rect(win, (255, 255, 255), (Tile.xPixels(self, offX),
            Tile.yPixels(self, offY), TILE_SIZE, TILE_SIZE))

# ------------------------- Game LOOP ----------------------------

# Constants for the window display
WIDTH = 800
HEIGHT = 800
FPS = 200
TILE_SIZE = 5

# Constants for map generation
SEED = 574421234
MAP_SIZE = 800 / TILE_SIZE

# Elevation Constants
WATER_LEVEL = 100
BEACH_LEVEL = 120
PLAIN_LEVEL = 170
JUNGLE_LEVEL = 210
MOUNTAIN_LEVEL = 230
SNOW_LEVEL = 240
MAX_SCALE = 255
MIN_SCALE = 0
FREQUENCY = 0.05
POW_CONST = 1.0

# Island generation constants
MANHATTAN_DIST = int((2.5 * MAP_SIZE) / 4)
LAND_CONST = 0.15
WATER_CONST = 0.75
DROP_CONST = 3.0

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# GAME LOOP
# This is the loop that runs the game
# Will loop at FPS amount of times in a second
run = True
noise = OpenSimplex(SEED)
world = generateMap()
player = Player(MAP_SIZE * TILE_SIZE / 2, MAP_SIZE * TILE_SIZE / 2, 0, 0, 0,
0, 0)
while run:
    pygame.time.delay(int(1000/FPS))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keyHandler(pygame.key.get_pressed())
    win.fill((0, 0, 0))
    renderTerrain()
    pygame.display.flip()
    
# End the game
pygame.quit()    
