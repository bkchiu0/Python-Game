from abc import ABC, abstractmethod
from settings import *
import tiles
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
        self.cooldown = 0
        self.resources = [0, 0, 0, 0]
        self.dirty = 2

    # Moves the bot and updates the bot's coordinates
    def update(self, mapmode, time):
        if(mapmode == ELEVATION_MAP):
            self.image.fill((0, 0, 0))
        else:
            self.image.fill((200, 200, 200))

        if(time % ACTION_RATE == 0):
            self.cooldown = max(0, self.cooldown - 1)
            if(self.cooldown == 0):
                self.action()


        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)

    # Moves the bot in a direction
    def action(self):
        d = random.randint(0, 3)
        if(d == 0):
            self.moveUp()
        elif(d == 1):
            self.moveDown()
        elif(d == 2):
            self.moveRight()
        elif(d == 3):
            self.moveLeft()
        else:
            self.harvestResources()

    # Moves the bot up
    def moveUp(self):
        self.y = int(max(0, self.y - 1))
        self.assignMoveCooldown()

    # Moves the bot up
    def moveDown(self):
        self.y = int(min(MAP_SIZE - 1, self.y + 1))
        self.assignMoveCooldown()

    # Moves the bot up
    def moveLeft(self):
        self.x = int(max(0, self.x - 1))
        self.assignMoveCooldown()

    # Moves the bot up
    def moveRight(self):
        self.x = int(min(MAP_SIZE - 1, self.x + 1))
        self.assignMoveCooldown()

    # Assigns the cooldown time for moving to the given tile
    def assignMoveCooldown(self):
        tile = self.game.world[self.y][self.x]
        if(type(tile) is tiles.WaterTile):
            self.cooldown += WATER_COOLDOWN
        elif(type(tile) is tiles.DeepWaterTile):
            self.cooldown += DEEP_WATER_COOLDOWN
        elif(type(tile) is tiles.BeachTile):
            self.cooldown += BEACH_COOLDOWN
        elif(type(tile) is tiles.PlainTile):
            self.cooldown += PLAINS_COOLDOWN
        elif(type(tile) is tiles.JungleTile):
            self.cooldown += JUNGLE_COOLDOWN
        elif(type(tile) is tiles.MountainTile):
            self.cooldown += MOUNTAIN_COOLDOWN
        else:
            self.cooldown += SNOW_COOLDOWN

    # Harvests the resources of the current tiles
    # Extracts 50% of the tile's resources
    def harvestResources(self):
        pass
