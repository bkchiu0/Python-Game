from abc import ABC, abstractmethod
from settings import *
from entities import *
import pygame
pygame.init();

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
        return (self.x * TILE_SIZE)

    # Returns an int that indicates the y position of the tile in pixels
    def yPixels(self):
        return (self.y * TILE_SIZE)

    # draws this tile on the main canvas
    @abstractmethod
    def render(self, surface):
        pass

class WaterTile(Tile):
    'Shallow ocean tile to mark water'

    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas
    def render(self, surface):
        pygame.draw.rect(surface, (0, 66, 146), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class DeepWaterTile(Tile):
    'Deep Ocean tile to mark water'

    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas
    def render(self, surface):
        pygame.draw.rect(surface, (0, 46, 136), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class PlainTile(Tile):
    'Land tile to mark plains'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, surface):
        pygame.draw.rect(surface, (116, 196, 116), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class BeachTile(Tile):
    'Land tile to mark beach'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, surface):
        pygame.draw.rect(surface, (255, 238, 173), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class JungleTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, surface):
        pygame.draw.rect(surface, (45, 116, 45), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class MountainTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, surface):
        pygame.draw.rect(surface, (116, 116, 116), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))

class SnowTile(Tile):
    'Land tile to mark jungle'
    
    def __init__(self, x, y, height):
        Tile.__init__(self, x, y, height)

    # draws this tile on the main canvas    
    def render(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (Tile.xPixels(self),
            Tile.yPixels(self), TILE_SIZE, TILE_SIZE))
