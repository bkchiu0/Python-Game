from abc import ABC, abstractmethod
from settings import *
from entities import *
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
        self.food = resources[FOOD]
        self.water = resources[WATER]
        self.wood = resources[WOOD]
        self.stone = resources[STONE]

    # Updates the tile's properties
    def update(self, mapmode, dirty):
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

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((0, 66, 146))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((0, self.food, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, self.food, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))

class DeepWaterTile(Tile):
    'Deep Ocean tile to mark water'

    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.deep_water_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((0, 46, 136))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((0, self.food, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, self.food, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))

class PlainTile(Tile):
    'Land tile to mark plains'
    
    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.plains_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((116, 196, 116))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((self.wood, self.food, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, self.food, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((self.wood, self.wood, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))

class BeachTile(Tile):
    'Land tile to mark beach'
    
    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.beach_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((255, 238, 173))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((0, self.food, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, self.food, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))

class JungleTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.jungle_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((45, 116, 45))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((self.wood, self.food, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, self.food, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((self.wood, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))

class MountainTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.mountain_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((116, 116, 116))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((self.stone, self.stone - self.wood, self.stone -
            self.wood))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == WOOD_MAP):
            self.image.fill((self.wood, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((self.stone, self.stone, self.stone))

class SnowTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, game, coords, height, resources):
        self.groups = game.all_tiles, game.snow_tiles
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        Tile.__init__(self, game, coords, height, resources)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Updates the tile's properties
    def update(self, mapmode, dirty):
        self.dirty = dirty
        if(mapmode == ELEVATION_MAP):
            self.image.fill((255, 255, 255))
        if(mapmode == RESOURCE_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == FOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == WATER_MAP):
            self.image.fill((0, 0, self.water))
        if(mapmode == WOOD_MAP):
            self.image.fill((0, 0, 0))
        if(mapmode == STONE_MAP):
            self.image.fill((0, 0, 0))
