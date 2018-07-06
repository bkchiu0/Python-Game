from abc import ABC, abstractmethod
from settings import *
import entities
import pygame
pygame.init();

# Tile is the grandfather class for all background tiles in the game
class Tile(ABC, pygame.sprite.DirtySprite):
    'Generic tile for building the world'

    #Fields
    # tuple(x, y) coords, float height
    # tuple(food, water, wood, stone) resources
    def __init__(self, game, coords, height, resources):
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.x = coords[0]
        self.y = coords[1]
        self.height = height
        self.dirty = 1
        self.resources = resources
        self.isGreyed = False

    # Updates the tile's properties
    @abstractmethod
    def update(self, mapmode, dirty, time):
        pass

    # Sets the top neighboring tile
    # top is itself if tile is an edge tile
    def setTop(self, tile):
        self.top = tile

    # Sets the bottom neighboring tile
    # is itself if tile is an edge tile
    def setBottom(self, tile):
        self.bottom = tile

    # Sets the left neighboring tile
    # is itself if tile is an edge tile
    def setLeft(self, tile):
        self.left = tile

    # Sets the right neighboring tile
    # is itself if tile is an edge tile
    def setRight(self, tile):
        self.right = tile

class WaterTile(Tile):
    'Shallow ocean tile to mark water'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.water_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = WATER_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((71, 71, 71))
                self.isGreyed = True
            else:
                self.image.fill((0, 66, 146))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[WOOD], self.resources[FOOD],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class DeepWaterTile(Tile):
    'Deep Ocean tile to mark water'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.deep_water_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = DEEP_WATER_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((60, 60, 60))
                self.isGreyed = True
            else:
                self.image.fill((0, 46, 136))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[WOOD], self.resources[FOOD],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class PlainTile(Tile):
    'Land tile to mark plains'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.plains_tiles, game.land_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = PLAINS_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((143, 143, 143))
                self.isGreyed = True
            else:
                self.image.fill((116, 196, 116))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[WOOD], self.resources[FOOD],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class BeachTile(Tile):
    'Land tile to mark beach'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.beach_tiles, game.land_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = BEACH_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((222, 222, 222))
                self.isGreyed = True
            else:
                self.image.fill((255, 238, 173))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[WOOD], self.resources[FOOD],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class JungleTile(Tile):
    'Land tile to mark jungle'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.jungle_tiles, game.land_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = JUNGLE_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((69, 69, 69))
                self.isGreyed = True
            else:
                self.image.fill((45, 116, 45))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[WOOD], self.resources[FOOD],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class MountainTile(Tile):
    'Land tile to mark jungle'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.mountain_tiles, game.land_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = MOUNTAIN_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((43, 43, 43))
                self.isGreyed = True
            else:
                self.image.fill((116, 116, 116))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[STONE],
            self.resources[STONE] - self.resources[WOOD],
            self.resources[STONE] - self.resources[WOOD]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))

class SnowTile(Tile):
    'Land tile to mark jungle'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.snow_tiles, game.land_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        self.resistance = SNOW_COOLDOWN

    # Updates the tile's properties
    def update(self, mapmode, dirty, time):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            if(self.isGreyed or self.game.manhattanDist((self.x, self.y),
            self.game.center) > self.game.currRad):
                self.image.fill((115, 115, 115))
                self.isGreyed = True
            else:
                self.image.fill((255, 255, 255))
        elif(mapmode == RESOURCE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[WATER]))
        elif(mapmode == FOOD_MAP):
            self.image.fill((0, self.resources[FOOD], 0))
        elif(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.resources[WATER]))
        elif(mapmode == WOOD_MAP):
            self.image.fill((self.resources[WOOD], 0, 0))
        elif(mapmode == STONE_MAP):
            self.image.fill((self.resources[STONE], self.resources[STONE],
            self.resources[STONE]))
