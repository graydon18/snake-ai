import pygame
import random

from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

Point = namedtuple('Point', 'x, y')

GRID_SIZE = 20
VEL = 20

class SnakeGame:
    def __init__(self, w = 960, h = 720):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w/4, self.h/2)
        self.snake = [self.head, Point(self.head.x - GRID_SIZE, self.head.y), Point(self.head.x - (2 * GRID_SIZE), self.head.y)]
        
        self.score = 0
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (self.w - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (self.h - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.placeFood()

game = SnakeGame()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    game.clock.tick(60)

pygame.quit()