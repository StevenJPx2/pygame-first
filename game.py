import datetime
import os
import random
import time

import pygame
from pygame.locals import *
from pygame.sprite import spritecollide, groupcollide
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


def collision_detect():
    for enemy in spritecollide(man, enemy_list, 0):
        print(man.health)
        enemy.actions.attack = True

        if man.orientation == "flip-h" and enemy.orientation == "flip-h" and man.x > enemy.x:
            enemy.orientation = "orig"
        elif man.orientation == "orig" and enemy.orientation == "orig" and man.x < enemy.x:
            enemy.orientation = "flip-h"


    # CANNOT DO ARROW-ENEMY COLLISION IN THIS LOOP
    # DOESN'T WORK EVERYTIME

    return 0


def key_press_actions():

    exception_actions = ["crouch", "idle", "draw_bow", "hurt"]

    if (keys[K_LEFT] and keys[K_DOWN]) or (keys[K_a] and keys[K_LSHIFT]):
        man.s_actions.left = True
        man.actions.slide = True

    elif (keys[K_RIGHT] and keys[K_DOWN]) or (keys[K_d] and keys[K_LSHIFT]):
        man.s_actions.right = True
        man.actions.slide = True

    elif keys[K_UP] or keys[K_w]:
        man.s_actions.none = True
        man.actions.jump = True

    elif keys[K_SPACE] and any([keys[K_UP], keys[K_w], man.actions.fall, man.actions.jump]):
        man.s_actions.none = True
        man.actions.jump_draw_bow = True

    elif keys[K_SPACE]:
        man.s_actions.none = True
        man.actions.draw_bow = True
    
    elif keys[K_DOWN] or keys[K_LSHIFT]:
        man.s_actions.none = True
        man.actions.crouch = True

    elif not (man.actions.fall or man.actions.jump):
        man.s_actions.none = True
        man.actions.idle = True

    if_walk = any(filter(lambda x: x in man.actions.__dict__, exception_actions))

    if keys[K_LEFT] or keys[K_a]:
        man.s_actions.left = True
        if if_walk: 
            man.actions.walk = True

    elif keys[K_RIGHT] or keys[K_d]:
        man.s_actions.right = True
        if if_walk:         
            man.actions.walk = True



arrow_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
man_list = pygame.sprite.Group()
sprites_list = pygame.sprite.Group()


#mainloop
man = Player(200, GROUND_LEVEL, 64, 64, arrow_list)
sprites_list.add(man)
man_list.add(man)

for _ in range(ENEMY_COUNT):
    __enemy = Enemy(random.randint(40, 660), GROUND_LEVEL, 64, 64, man_list, arrow_list)
    enemy_list.add(__enemy)
    sprites_list.add(__enemy)
run = True
while run:
    clock.tick(FRAMERATE)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:run = False
        else:
            if not collision_detect():
                key_press_actions()

    redraw_game_window()

pygame.quit()
