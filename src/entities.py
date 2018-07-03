from abc import ABC, abstractmethod
from settings import *
from tiles import *
import pygame
import random
pygame.init()

class Bot(pygame.sprite.DirtySprite):
    'Represents the bots in the game'
    # Fields
    # int x, int y, int idVal
    # int velX, int velY, int accX, int accY
    def __init__(self, game, coords, team):
        self.groups = game.all_entities, game.all_alive
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = coords[0]
        self.y = coords[1]
        self.team = team
        self.dirty = 2

    # Moves the bot and updates the bot's coordinates
    def update(self, mapmode):
        if(mapmode == ELEVATION_MAP):
            self.image.fill((0, 0, 0))
        else:
            self.image.fill((200, 200, 200))
        self.action()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Moves the bot in a direction
    def action(self):
        pass


