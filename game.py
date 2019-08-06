import datetime
import os
import random
import time

import pygame
from pygame.locals import *
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
GROUND_LEVEL = 390
dim = (WIN_WIDTH, WIN_HEIGHT)

win = pygame.display.set_mode(dim)
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()
bg = pygame.transform.scale(pygame.image.load("sprites/Background.png"), dim)
game_objects.dim = dim



def redraw_game_window():
    win.blit(bg, (0,0))
    sprites_list.update()
    sprites_list.draw(win)
    arrow_list.update()
    arrow_list.draw(win)

    pygame.display.update()


arrow_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
mc_list = pygame.sprite.Group()
sprites_list = pygame.sprite.Group()


#mainloop
man = Player(200, GROUND_LEVEL, 64, 64, arrow_list, enemy_list)
sprites_list.add(man)
mc_list.add(man)

for _ in range(ENEMY_COUNT):
    __enemy = Enemy(random.randint(40, 660), GROUND_LEVEL, 64, 64, arrow_list, mc_list)
    enemy_list.add(__enemy)
    sprites_list.add(__enemy)
run = True
while run:
    clock.tick(FRAMERATE)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
        else:
            if all([keys[K_LEFT], keys[K_DOWN]]) or all([keys[K_a], keys[K_LSHIFT]]):
                man.actions.slide = True
                man.orientation = "flip-h"

            elif all([keys[K_RIGHT], keys[K_DOWN]]) or all([keys[K_d], keys[K_LSHIFT]]):
                man.actions.slide = True
                man.orientation = "orig"

            elif keys[K_LEFT] or keys[K_a]:
                man.actions.walk = True
                man.orientation = "orig"

            elif keys[K_RIGHT] or keys[K_d]:
                man.actions.walk = True
                man.orientation = "flip-h"
                
            
            elif keys[K_DOWN] or keys[K_LSHIFT]:
                man.actions.crouch = True

            elif keys[K_SPACE] and (keys[K_UP] or keys[K_w]):
                man.jump_draw_bow = True

            elif keys[K_SPACE]:
                man.draw_bow = True

            elif keys[K_UP] or keys[K_w]:
                man.jump = True

            else:
                man.idle = True

            
            
    redraw_game_window()

pygame.quit()
