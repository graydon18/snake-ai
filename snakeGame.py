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

GAME_BG = '#74c365'
SNAKE_COLOUR = '#6495ed'
HEAD_COLOUR = '#1b61e4'
FOOD_COLOUR = '#ed2939'

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
GRID_SIZE = 20
VEL = 20

class SnakeGame:
    def __init__(self):  
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake AI")
        self.screen.fill(GAME_BG)
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(SCREEN_WIDTH / 4, SCREEN_HEIGHT /2)
        self.snake = [self.head, Point(self.head.x - GRID_SIZE, self.head.y), Point(self.head.x - (2 * GRID_SIZE), self.head.y)]
        
        self.score = 0
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.placeFood()

    def updateUI(self):  
        for point in self.snake:
            pygame.draw.circle(self.screen, SNAKE_COLOUR, [point.x + (GRID_SIZE // 2), point.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))
        
        pygame.draw.circle(self.screen, HEAD_COLOUR, [self.head.x + (GRID_SIZE // 2), self.head.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))  
        pygame.draw.circle(self.screen, FOOD_COLOUR, [self.food.x + (GRID_SIZE // 2), self.food.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))

        pygame.display.flip()
    

game = SnakeGame()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    game.updateUI()
    game.clock.tick(60)

pygame.quit()