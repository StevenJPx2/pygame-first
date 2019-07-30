import datetime
import os
import random
import time

import pygame
import pymunk

import game_objects
from game_objects import Player, Arrow, Enemy

pygame.init()

os.chdir(os.path.dirname(os.path.realpath(__file__)))


# MAIN GLOBAL VARIABLES
FRAMERATE = 24
ENEMY_COUNT = 2
WIN_WIDTH = 700
WIN_HEIGHT = 500
dim = (WIN_WIDTH, WIN_HEIGHT)

win = pygame.display.set_mode(dim)
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()
bg = pygame.image.load("sprites/Background.png")
game_objects.dim = dim



def redraw_game_window():
    man.set_param()
    win.blit(bg, (0,0))
    man.draw(win)
    arrow_list.update()
    arrow_list.draw(win)
    enemy_list.update()
    enemy_list.draw(win)

    pygame.display.update()


arrow_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()


#mainloop
man = Player(200, 410, 64, 64, arrow_list)
for _ in range(ENEMY_COUNT):
    enemy_list.add(Enemy(random.randint(40, 660), 410, 64, 64, arrow_list))
run = True
while run:
    clock.tick(FRAMERATE)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
            
    redraw_game_window()

pygame.quit()
