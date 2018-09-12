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
def generateMap(game, heightNoise, resourceNoise):
    heightMap = generateHeightMap(heightNoise)
    resourceMap = generateResourceMap(resourceNoise)
    tileMap = generateTileMap(game, heightMap, resourceMap)
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
def generateTileMap(g, heightMap, resourceMap):
    tileMap = []
    for y in range(len(heightMap)):
        tileRow = []
        for x in range(len(heightMap[y])):
            if(heightMap[y][x] <= DEEP_LEVEL):
                tileRow.append(DeepWaterTile(g, (x, y), heightMap[y][x],
                [resourceMap[y][x], 255, 0, 0]))
            elif(heightMap[y][x] <= WATER_LEVEL):
                tileRow.append(WaterTile(g, (x, y), heightMap[y][x],
                [resourceMap[y][x], 255, 0, 0]))
            elif(heightMap[y][x] <= BEACH_LEVEL):
                tileRow.append(BeachTile(g, (x, y), heightMap[y][x],
                [int(resourceMap[y][x] * 0.25), resourceMap[y][x], 0, 0]))
            elif(heightMap[y][x] <= PLAIN_LEVEL):
                tileRow.append(PlainTile(g, (x, y), heightMap[y][x],
                [resourceMap[y][x], int(resourceMap[y][x] * 0.10),
                int(resourceMap[y][x] * 0.15), 0]))
            elif(heightMap[y][x] <= JUNGLE_LEVEL):
                tileRow.append(JungleTile(g, (x, y), heightMap[y][x],
                [int(resourceMap[y][x] * 0.15), int(resourceMap[y][x] * 0.10),
                resourceMap[y][x], 0]))
            elif(heightMap[y][x] <= MOUNTAIN_LEVEL):
                tileRow.append(MountainTile(g, (x, y), heightMap[y][x],
                [0, 0, int(resourceMap[y][x] * 0.25), 255]))
            else:
                tileRow.append(SnowTile(g, (x, y), heightMap[y][x],
                [0, resourceMap[y][x], 0, resourceMap[y][x]]))
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
        self.running = True
        pygame.init()
        pygame.mixer.init()

        self.all_entities = pygame.sprite.LayeredDirty()
        self.all_tiles = pygame.sprite.LayeredDirty()
        self.land_tiles = pygame.sprite.Group()
        self.deep_water_tiles = pygame.sprite.Group()
        self.water_tiles = pygame.sprite.Group()
        self.beach_tiles = pygame.sprite.Group()
        self.plains_tiles = pygame.sprite.Group()
        self.jungle_tiles = pygame.sprite.Group()
        self.mountain_tiles = pygame.sprite.Group()
        self.snow_tiles = pygame.sprite.Group()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.enoise = OpenSimplex(ELEVATION_SEED)
        self.rnoise = OpenSimplex(RESOURCE_SEED)
        self.new()

    # Used of loading any outside information
    def load_data(self):
        pass

    # Calculates the manhattan distance between two coords
    def manhattanDist(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    # Starts a new game
    def new(self):
        self.mapmode = ELEVATION_MAP
        self.all_entities.empty()
        self.all_tiles.empty()
        self.land_tiles.empty()
        self.deep_water_tiles.empty()
        self.water_tiles.empty()
        self.beach_tiles.empty()
        self.plains_tiles.empty()
        self.jungle_tiles.empty()
        self.mountain_tiles.empty()
        self.snow_tiles.empty()
        self.world = generateMap(self, self.enoise, self.rnoise)
        self.redraw = 1
        self.time = 0
        self.center = (MAP_SIZE / 2, MAP_SIZE / 2)
        self.radius = MAP_SIZE + 1
        self.currRad = MAP_SIZE + 1
        self.nextCenter = self.getNewCenter()
        self.addPlayers()

    # adds all the players in the world
    # all players spawn on beach tiles
    def addPlayers(self):
        for ctr in range(NUM_PLAYERS):
            beachList = self.beach_tiles.sprites()
            tile = beachList[random.randint(0, len(beachList))]
            x = tile.x
            y = tile.y
            while(not self.isValidSpawn(x, y)):
                tile = beachList[random.randint(0, len(beachList))]
                x = tile.x
                y = tile.y
            self.all_entities.add(Bot(self, (x, y), ctr))

    def isValidSpawn(self, x, y):
        for bot in self.all_entities.sprites():
            if(bot.x == x and bot.y == y):
                return False
        return True

    # Game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.time += 1
            self.redraw = 1
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # Game loop update
    def update(self):
        if(self.time % ACTION_RATE == 0 and self.currRad > self.radius):
            self.currRad -= 1
            self.redraw = 1
        self.all_entities.update(self.mapmode, self.time)
        self.killOutside()
        self.all_tiles.update(self.mapmode, self.redraw, self.time)
        self.redraw = 0

    # Game loop event handler
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_0]):
            self.mapmode = ELEVATION_MAP
            self.redraw = 1
        if(keys[pygame.K_1]):
            self.mapmode = RESOURCE_MAP
            self.redraw = 1
        if(keys[pygame.K_2]):
            self.mapmode = FOOD_MAP
            self.redraw = 1
        if(keys[pygame.K_3]):
            self.mapmode = WATER_MAP
            self.redraw = 1
        if(keys[pygame.K_4]):
            self.mapmode = WOOD_MAP
            self.redraw = 1
        if(keys[pygame.K_5]):
            self.mapmode = STONE_MAP
            self.redraw = 1

        if(self.time % DAY_LENGTH == 0 and (self.time // DAY_LENGTH) % 3 == 1):
            self.center = self.nextCenter
            self.radius //= 2
            self.nextCenter = self.getNewCenter()

    # Kills all the sprites that are outside of the circle
    def killOutside(self):
        for sprite in self.all_entities:
            if self.manhattanDist((sprite.x, sprite.y),
            self.center) > self.currRad:
                print("Bot " + str(sprite.team) + 
                " has died outside the playzone.")
                sprite.kill()


    # Randomly generates a new centerTile for the next iteration
    def getNewCenter(self):
        tiles = self.land_tiles.sprites()
        centerTile = tiles[random.randint(0, len(tiles) - 1)]
        while(self.manhattanDist((centerTile.x, centerTile.y),
        self.center) > self.radius // 2):
            centerTile = tiles[random.randint(0, len(tiles) - 1)]
        return (centerTile.x, centerTile.y)

    # Game Loop - draw
    def draw(self):
        self.win.fill((255, 255, 255))
        rects = self.all_tiles.draw(self.win)
        rects += self.all_entities.draw(self.win)
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
    g.run()
    g.show_go()

# End the game
pygame.quit()
