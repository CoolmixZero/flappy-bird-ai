import os
import neat
import pygame

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", f"bird{x}.png"))) for x in range(1, 4)
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

STATS_FONT = pygame.font.SysFont("comicsans", 40)
