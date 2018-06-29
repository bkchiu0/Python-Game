from abc import ABC, abstractmethod
from settings import *
from tiles import *
import pygame
import random
pygame.init()

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

    def render(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, 30, 30))
