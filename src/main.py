from abc import ABC, abstractmethod
from opensimplex import OpenSimplex
from settings import *
from tiles import *
from entities import *
import pygame
import random

# --------------- Static Rendering Functions ---------------

def renderGrid(surface) :
    for x in range(0, WIDTH, TILE_SIZE) :
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE) :
        pygame.draw.line(surface, (0, 0, 0), (0, y), (WIDTH, y))    

def limit(n) :
    if(n < 0) :
        return 0
    if(n > MAP_SIZE) :
        return MAP_SIZE
    return n


# --------------- Static World Generation ------------------

# Generates the map which is a 2d list of tiles
def generateMap(heightNoise, resourceNoise) :
    heightMap = generateHeightMap(heightNoise)
    resourceMap = generateResourceMap(resourceNoise)
    tileMap = generateTileMap(heightMap, resourceMap)
    setNeighbors(tileMap)
    return tileMap

# Generates a 2d list of floats
# to represents the map in terms of resource levels
def generateResourceMap(noise) :
    resourceMap = []
    for y in range(0, int(MAP_SIZE)) :
        row = []
        for x in range(0, int(MAP_SIZE)):
            row.append(scale(genResources(x, y, noise)))
        resourceMap.append(row)
    return resourceMap

# Generates a 2d list of floats
# to represent the map in terms of its height
def generateHeightMap(noise) :
    heightMap = []
    for y in range(0, int(MAP_SIZE)) :
        row = []
        for x in range(0, int(MAP_SIZE)):
            row.append(scale(genHeight(x, y, noise)))
        heightMap.append(row)
    return heightMap

# Generates a float using a noise function
# range is [0,1)
def genResources(x, y, noise):
    n1 = 0.65 * (noise.noise2d(FREQUENCY * x, FREQUENCY * y) + 1) / 2
    n2 = 0.35 * (noise.noise2d(1.5 * FREQUENCY * x, 1.5 * FREQUENCY * y) + 1
    ) / 2
    e = n1 + n2
    return pow(e, POW_CONST)

# Generates a float using noise function
# range is [0,1)
def genHeight(x, y, noise):
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
def generateTileMap(heightMap, resourceMap):
    tileMap = []
    for y in range(len(heightMap)):
        tileRow = []
        for x in range(len(heightMap[y])):
            if(heightMap[y][x] <= DEEP_LEVEL):
                tileRow.append(DeepWaterTile((x, y), heightMap[y][x],
                (resourceMap[y][x], 255, 0, 0)))
            elif(heightMap[y][x] <= WATER_LEVEL):
                tileRow.append(WaterTile((x, y), heightMap[y][x],
                (resourceMap[y][x], 255, 0, 0)))
            elif(heightMap[y][x] <= BEACH_LEVEL):
                tileRow.append(BeachTile((x, y), heightMap[y][x],
                (int(resourceMap[y][x] * 0.25), resourceMap[y][x], 0, 0)))
            elif(heightMap[y][x] <= PLAIN_LEVEL):
                tileRow.append(PlainTile((x, y), heightMap[y][x],
                (resourceMap[y][x], int(resourceMap[y][x] * 0.10),
                int(resourceMap[y][x] * 0.15), 0)))
            elif(heightMap[y][x] <= JUNGLE_LEVEL):
                tileRow.append(JungleTile((x, y), heightMap[y][x],
                (int(resourceMap[y][x] * 0.15), int(resourceMap[y][x] * 0.10),
                resourceMap[y][x], 0)))
            elif(heightMap[y][x] <= MOUNTAIN_LEVEL):
                tileRow.append(MountainTile((x, y), heightMap[y][x],
                (0, 0, int(resourceMap[y][x] * 0.25),
                resourceMap[y][x])))
            else :
                tileRow.append(SnowTile((x, y), heightMap[y][x],
                (0, resourceMap[y][x], 0, 0)))
        tileMap.append(tileRow)
    return tileMap

# Sets the neighbors of the each tile
def setNeighbors(cellMap):
    for y in range(len(cellMap)):
        for x in range(len(cellMap[y])):
            if(y == 0):
                cellMap[y][x].setTop(cellMap[y][x])
                cellMap[y][x].setBottom(cellMap[y + 1][x])
            elif(y == len(cellMap) - 1):
                cellMap[y][x].setTop(cellMap[y - 1][x])
                cellMap[y][x].setBottom(cellMap[y][x])
            else:
                cellMap[y][x].setTop(cellMap[y - 1][x])
                cellMap[y][x].setBottom(cellMap[y + 1][x])
            if(x == 0):
                cellMap[y][x].setLeft(cellMap[y][x])
                cellMap[y][x].setRight(cellMap[y][x + 1])
            elif(x == len(cellMap[y]) - 1):
                cellMap[y][x].setLeft(cellMap[y][x - 1])
                cellMap[y][x].setRight(cellMap[y][x])
            else:
                cellMap[y][x].setLeft(cellMap[y][x - 1])
                cellMap[y][x].setRight(cellMap[y][x + 1])
                

# ------------------------- Game Class ----------------------------

class Game():
    # Initialize game object fields
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.enoise = OpenSimplex(ELEVATION_SEED)
        self.rnoise = OpenSimplex(RESOURCE_SEED)
        self.running = True
        self.world = generateMap(self.enoise, self.rnoise)

    # Used of loading any outside information
    def load_data(self):
        pass

    # Starts a new game
    def new(self):
        self.all_entities = pygame.sprite.LayeredDirty()
        self.all_entities.add(Bot((MAP_SIZE / 2, MAP_SIZE / 2), 0))
        self.all_tiles = pygame.sprite.LayeredDirty()
        for row in self.world:
            self.all_tiles.add(row)
        self.run()

    # Game loop
    def run(self):
        self.playing = True
        self.clock.tick(FPS)
        while self.playing:
            self.events()
            self.update()
            self.draw()

    # Game loop update
    def update(self):
        self.all_entities.update()
        self.all_tiles.update()

    # Game loop event handler
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        keys = pygame.key.get_pressed()

    # Game Loop - draw
    def draw(self):
        self.win.fill((255, 255, 255))
        self.all_tiles.draw(self.win)
        rects = self.all_entities.draw(self.win)
        pygame.display.update(rects)

    # Shows the start screen
    def show_start(self):
        pass

    # Shows the end screen
    def show_go(self):
        pass

# --------------------- GAME LOOP ---------------------
# This is the loop that runs the game
# Will loop at FPS amount of times in a second

g = Game()
while g.running:
    g.new()
    g.show_go()
    
# End the game
pygame.quit()
