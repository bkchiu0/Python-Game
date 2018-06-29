from abc import ABC, abstractmethod
from settings import *
from entities import *
import pygame
pygame.init();

# Tile is the grandfather class for all background tiles in the game
class Tile(ABC, pygame.sprite.DirtySprite):
    'Generic tile for building the world'

    #Fields
    # tuple coords, float height
    def __init__(self, coords, height):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.x = coords[0]
        self.y = coords[1]
        self.height = height
        self.dirty = 1

    # Updates the tile's properties
    def update(self):
        pass

class WaterTile(Tile):
    'Shallow ocean tile to mark water'

    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((0, 66, 146))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class DeepWaterTile(Tile):
    'Deep Ocean tile to mark water'

    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((0, 46, 136))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class PlainTile(Tile):
    'Land tile to mark plains'
    
    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((116, 196, 116))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class BeachTile(Tile):
    'Land tile to mark beach'
    
    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((255, 238, 173))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class JungleTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((45, 116, 45))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class MountainTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((116, 116, 116))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

class SnowTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, coords, height):
        Tile.__init__(self, coords, height)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
