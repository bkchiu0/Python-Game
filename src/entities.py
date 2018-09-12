from abc import ABC, abstractmethod
from settings import *
import tiles
import pygame
import random
import queue
pygame.init()

class Bot(pygame.sprite.DirtySprite):
    'Represents the bots in the game'
    # Fields
    # int x, int y, int idVal
    # int velX, int velY, int accX, int accY
    def __init__(self, game, coords, team):
        self.groups = game.all_entities
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
        self.directions = []

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
        if(len(self.directions) == 0):
            directions = self.fastFindPath((random.randint(0, MAP_SIZE - 1),
            random.randint(0, MAP_SIZE - 1)))
            self.directions += directions
        if(len(self.directions) != 0):
            if(self.directions[0] == 0):
                self.moveUp()
                del self.directions[0]
            elif(self.directions[0] == 1):
                self.moveDown()
                del self.directions[0]
            elif(self.directions[0] == 2):
                self.moveLeft()
                del self.directions[0]
            elif(self.directions[0] == 3):
                self.moveRight()
                del self.directions[0]
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
        self.cooldown += tile.resistance

    # Harvests the resources of the current tiles
    # Extracts 50% of the tile's resources
    def harvestResources(self):
        currTile = self.game.world[self.y][self.x]
        foodExtract = int(currTile.resources[FOOD] * 0.5)
        waterExtract = int(currTile.resources[WATER] * 0.5)
        woodExtract = int(currTile.resources[WOOD] * 0.5)
        stoneExtract = int(currTile.resources[STONE] * 0.5)
        self.resources[FOOD] += foodExtract
        self.resources[WATER] += waterExtract
        self.resources[WOOD] += woodExtract
        self.resources[STONE] += stoneExtract
        currTile.resources[FOOD] -= foodExtract
        currTile.resources[WATER] -= waterExtract
        currTile.resources[WOOD] -= woodExtract
        currTile.resources[STONE] -= stoneExtract

    # finds the path to a destination
    def fastFindPath(self, destination):
        list = []
        dx = int(destination[0] - self.x)
        dy = int(destination[1] - self.y)
        if(dx > 0):
            horizontalDir = 3
        else:
            horizontalDir = 2
        if(dy > 0):
            verticalDir = 1
        else:
            verticalDir = 0
        if(random.randint(0, 1) == 0):
            for i in range(abs(dx)):
                list.append(horizontalDir)
            for i in range(abs(dy)):
                list.append(verticalDir)
        else:
            for i in range(abs(dy)):
                list.append(verticalDir)
            for i in range(abs(dx)):
                list.append(horizontalDir)
        return list

    # Uses A* pathfinding algorithm to find fastest path to a destination
    # returns a list of directions and a list of coords along the path
    # destination must be a tuple of x and y coords
    # 0 being up
    #1 being down
    #2 being left
    #3 being right
    def findPath(self, destination):
        map = self.game.world
        frontier = queue.PriorityQueue()
        frontier.put((self.x, self.y), 0)
        cameFrom = {}
        costRN = {}
        cameFrom[(self.x, self.y)] = None
        costRN[(self.x, self.y)] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == destination:
                break

            for next in self.getNeighbors(current):
                newCost = costRN[current] + map[next[1]][next[0]].resistance
                if next not in costRN or newCost < costRN[next]:
                    costRN[next] = newCost
                    priority = newCost + self.heuristic(destination, next)
                    frontier.put(next, priority)
                    cameFrom[next] = current
        return self.buildPath(cameFrom, (self.x, self.y), destination)

    # constructs a list of directions
    def buildPath(self, cameFrom, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = cameFrom[current]
        path.append(start)
        path.reverse()
        directions = []
        for i in range(1, len(path)):
            neighbors = self.getNeighbors(path[i - 1])
            for d in range(len(neighbors)):
                if(neighbors[d] == path[i]):
                    directions.append(d)
        return directions, path

    # Calculates the heuristic given two coords tuples
    def heuristic(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # Returns a list of neighboring coords
    # Order is in: top bottom left right
    # coords will be omitted if out of bounds
    def getNeighbors(self, coords):
        list = []
        if(coords[1] != 0):
            list.append((coords[0], coords[1] - 1))
        if(coords[1] != MAP_SIZE - 1):
            list.append((coords[0], coords[1] + 1))
        if(coords[0] != 0):
            list.append((coords[0] - 1, coords[1]))
        if(coords[0] != MAP_SIZE - 1):
            list.append((coords[0] + 1, coords[1]))
        return list
