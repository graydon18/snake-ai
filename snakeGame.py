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
BODY_COLOUR = '#6495ed'
HEAD_COLOUR = '#1b61e4'
FOOD_COLOUR = '#ed2939'

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
GRID_SIZE = 40
VEL = 10

class SnakeAI:
    def __init__(self):  
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(SCREEN_WIDTH / 4, SCREEN_HEIGHT /2)
        self.body = [self.head, Point(self.head.x - GRID_SIZE, self.head.y), Point(self.head.x - (2 * GRID_SIZE), self.head.y)]
        
        self.score = 0
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.food = Point(x, y)
        if self.food in self.body:
            self.placeFood()
    
    def incHead(self, direction):
        if direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - GRID_SIZE)
        elif direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y + GRID_SIZE)
        elif direction == Direction.LEFT:
            self.head = Point(self.head.x - GRID_SIZE, self.head.y)
        elif direction == Direction.RIGHT:
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

    def handleMove(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Final score:', self.score)
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
    
        self.incHead(self.direction)
        self.body.insert(0, self.head) # fill in the space where the head was moved

        if self.checkGameOver():
            return True

        if self.head == self.food:
            self.score += 1
            self.placeFood() # no pop, the fill in acts as the growth
        else:
            self.body.pop()

        self.updateUI()
        self.clock.tick(VEL)

        return False

ai = SnakeAI()

running = True
while running:
    gameOver = ai.handleMove()
        
    if gameOver == True:
        running = False

print('GAME OVER\nFinal score:', ai.score)

pygame.quit()