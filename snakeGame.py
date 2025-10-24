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
GRID_SIZE = 40
VEL = 5

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
        for point in self.snake:
            pygame.draw.circle(self.screen, SNAKE_COLOUR, [point.x + (GRID_SIZE // 2), point.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))
        
        pygame.draw.circle(self.screen, HEAD_COLOUR, [self.head.x + (GRID_SIZE // 2), self.head.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))  
        pygame.draw.circle(self.screen, FOOD_COLOUR, [self.food.x + (GRID_SIZE // 2), self.food.y + (GRID_SIZE // 2)], (GRID_SIZE // 2))

        pygame.display.flip()

    def handleMove(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        self.snake.insert(0, self.head) # fill in the space where the head was moved

        self.updateUI()
        self.clock.tick(VEL)

        return False

game = SnakeGame()

running = True
while running:
    game_over = game.handleMove()
        
    if game_over == True:
        running = False

print('Final Score', game.score)

pygame.quit()