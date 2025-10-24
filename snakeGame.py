import pygame
import random

pygame.init()

class SnakeGame:
    def __init__(self, w = 960, h = 720):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()


game = SnakeGame()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    game.clock.tick(60)

pygame.quit()