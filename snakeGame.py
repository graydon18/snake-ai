import pygame
import random
import numpy

from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

Point = namedtuple('Point', 'x, y')

GAME_BG = '#74c365'
BODY_COLOUR = '#6495ed'
HEAD_COLOUR = '#1b61e4'
FOOD_COLOUR = '#ed2939'

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
GRID_SIZE = 40
VEL = 10

class SnakeGame:
    def __init__(self):  
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(SCREEN_WIDTH / 4, SCREEN_HEIGHT /2)
        self.body = [self.head, Point(self.head.x - GRID_SIZE, self.head.y), Point(self.head.x - (2 * GRID_SIZE), self.head.y)]
        self.score = 0
        self.placeFood()

        self.sameState = 0

    def placeFood(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.food = Point(x, y)
        if self.food in self.body:
            self.placeFood()
    
    def incHead(self, action):
        # [1, 0, 0] - straight
        # [0, 1, 0] - left
        # [0, 0, 1] - right

        if numpy.array_equal(action, [0, 1, 0]):
            self.direction = Direction((self.direction - 1) % 4)
        elif numpy.array_equal(action, [0, 0, 1]):
            self.direction = Direction((self.direction + 1) % 4)

        if self.direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - GRID_SIZE)
        elif self.direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y + GRID_SIZE)
        elif self.direction == Direction.LEFT:
            self.head = Point(self.head.x - GRID_SIZE, self.head.y)
        elif self.direction == Direction.RIGHT:
            self.head = Point(self.head.x + GRID_SIZE, self.head.y)

    def updateUI(self):  
        self.screen.fill(GAME_BG) # resets UI so that old snake parts are drawn over

        for point in self.body:
            pygame.draw.circle(self.screen, BODY_COLOUR, [point.x + (GRID_SIZE // 2), point.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))
        
        pygame.draw.circle(self.screen, HEAD_COLOUR, [self.head.x + (GRID_SIZE // 2), self.head.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))  
        pygame.draw.circle(self.screen, FOOD_COLOUR, [self.food.x + (GRID_SIZE // 2), self.food.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))

        pygame.display.flip()
    
    def checkGameOver(self):
        if self.head.x < 0 or self.head.x > (SCREEN_WIDTH - GRID_SIZE) or self.head.y < 0 or self.head.y > (SCREEN_HEIGHT - GRID_SIZE):
            return True
        
        if self.head in self.body[1:]:
            return True
        
        return False

    def handleMove(self, action):
        self.sameState += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        self.incHead(action)
        self.body.insert(0, self.head) # fill in the space where the head was moved

        reward = 0
        if self.checkGameOver() or self.sameState > 100*len(self.body): # scales to allow time for long times between growth for longer snakes
            reward = -1
            return reward, True

        if self.head == self.food:
            reward = 1
            self.score += 1
            self.placeFood() # no pop, the fill in acts as the growth
        else:
            self.body.pop()

        self.updateUI()
        self.clock.tick(VEL)

        return reward, False