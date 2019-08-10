import pygame
from pygame.color import *
from math import pow
import os

from create_assist import Animator, Action



# PLAYER GLOBAL VARIABLES
JUMP_HEIGHT = 7
SLIDE_COUNT = 10
PLAYER_COMMON_KWARGS = {
    "flip_h" : True,
    "scale" : "2x"
}

WIN_WIDTH = 700
WIN_HEIGHT = 500

@property
def dim(self):
    return (WIN_WIDTH, WIN_HEIGHT)

@dim.setter
def dim(self, val):
    'setting'
    assert (type(val[0]), type(val[1])) == (int, int)
    self.WIN_WIDTH, self.WIN_HEIGHT = val

@dim.deleter
def del_dim(self):
    del self.WIN_WIDTH
    del self.WIN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, arrow_list):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.arrow_list = arrow_list

        self.vel = 7
        self.health = 20
        self.score = 0

        self.actions = Action()
        self.s_actions = Action()

        self.jump_count = JUMP_HEIGHT
        self.slide_count = SLIDE_COUNT

        self.orientation = "orig"

        #sprites

        self.walk_sprites = Animator("sprites/adventurer-{z}-0{index}-1.3.png", format={"z":"run"}, number_of=6, **PLAYER_COMMON_KWARGS)
        self.idle_sprites = Animator("sprites/adventurer-{mul_ent}-0{index}.png", format={"mul_ent":("idle", "idle-2")}, number_of=4, 
                            multiple=True, **PLAYER_COMMON_KWARGS)
        self.jump_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"jump"}, number_of=4, loop=False, **PLAYER_COMMON_KWARGS)
        self.fall_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"fall"}, number_of=2, **PLAYER_COMMON_KWARGS)
        self.slide_sprites = Animator("sprites/adventurer-{z}-0{index}-1.3.png", format={"z":"slide"}, number_of=2, **PLAYER_COMMON_KWARGS)
        self.crouch_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"crouch"}, number_of=4, **PLAYER_COMMON_KWARGS)
        self.smrslt_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"smrslt"}, number_of=4, **PLAYER_COMMON_KWARGS)
        self.stand_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"stand"}, number_of=3, **PLAYER_COMMON_KWARGS)
        self.bow_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"bow"}, number_of=9, **PLAYER_COMMON_KWARGS)
        self.bow_jump_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"bow-jump"}, number_of=6, **PLAYER_COMMON_KWARGS)
        self.hurt_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"hurt"}, number_of=2, loop=True, **PLAYER_COMMON_KWARGS)
        self.die_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"die"}, number_of=7, loop=False, **PLAYER_COMMON_KWARGS)

        self.health_sprite = Animator("sprites/health-bar.png", scale="2x")
        self.health_bar_sprite = Animator("sprites/health-bar-back.png", scale="2x")

    @property
    def image(self):

        if self.actions.hurt:
            return next(self.hurt_sprites[self.orientation])

        if self.actions.dead:
            return next(self.die_sprites[self.orientation])

        if self.actions.draw_bow:
            return next(self.bow_sprites[self.orientation])

        elif self.actions.jump_draw_bow:
            return next(self.bow_jump_sprites[self.orientation])

        elif self.actions.jump:
            if self.jump_sprites.end_of_loop:
                if self.smrslt_sprites.end_of_loop:
                    self.jump_sprites.refresh()
                else:
                    return next(self.smrslt_sprites[self.orientation])
            return next(self.jump_sprites[self.orientation])
            
        elif self.actions.fall:
            return next(self.fall_sprites[self.orientation])

        elif self.actions.idle:
            return next(self.idle_sprites[self.orientation])

        elif self.actions.crouch:
            return next(self.crouch_sprites[self.orientation])

        elif self.actions.stand:
            return next(self.stand_sprites[self.orientation])

        elif self.actions.slide:
            return next(self.slide_sprites[self.orientation])

        else:
            return next(self.walk_sprites[self.orientation])

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def display_health(self):
        health_block = next(self.health_sprite["orig"])
        health_bar_sprite = next(self.health_bar_sprite["orig"]).copy()
        width = health_block.get_width()
        full_width = width * self.health

        health_bar_sprite.blits([(health_block, (8+i, 20)) for i in range(0, full_width, width)], 0)
        return health_bar_sprite

    def display_score(self):
        font = pygame.font.Font("fonts/visitor1.ttf", 30)
        font_surface = font.render(f"SCORE: {self.score}", 0, (0,0,0))
        return (font_surface, font_surface.get_width())

    def update(self):
        if self.health <= 0:
            self.actions.dead = True
            self.s_actions.none = True
            return

        if self.s_actions.left:
            if self.x > self.vel:
                self.x -= self.vel
                self.orientation = "flip-h"

        elif self.s_actions.right:
            if self.x < WIN_WIDTH - self.width - self.vel:
                self.x += self.vel
                self.orientation = "orig"

        if any([self.actions.fall, self.actions.jump_draw_bow, self.actions.jump]):
            if self.jump_count >= -JUMP_HEIGHT:
                if self.jump_count < 0:
                    neg = -1
                    if not self.actions.jump_draw_bow:
                        self.actions.fall = True
                else:
                    neg = 1
                self.y -= pow(self.jump_count, 2) * 0.5 * neg
                self.jump_count -= 1

            else:
                self.s_actions.none = True
                self.actions.idle = True
                self.jump_count = JUMP_HEIGHT

        if self.actions.jump_draw_bow or self.actions.draw_bow:
            if (self.bow_jump_sprites.end_of_loop or self.bow_sprites.end_of_loop):
                temp_kwargs = {
                    "x" : self.x,
                    "y" : self.y,
                    "width" : self.width,
                    "height" : self.height,
                    "orientation" : self.orientation
                }
                self.arrow_list.add(Arrow(**temp_kwargs))
                if self.jump_count != JUMP_HEIGHT:
                    if self.jump_count > 0: self.actions.jump = True
                    else: self.actions.fall = True
                else:
                    self.actions.idle = True

        

        if self.actions.hurt and self.hurt_sprites.end_of_loop:
            self.actions.idle = True

        if self.actions.slide:
            if self.slide_count <= 0:
               self.slide_count = SLIDE_COUNT
               self.actions.stand = True
               self.s_actions.none = True
            else:
                self.slide_count -= 1

        if self.actions.stand:
            self.s_actions.none = True
            if self.stand_sprites.end_of_loop:
                self.actions.idle = True


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, orientation):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self._vel = 10
        self.damage = 3

        # SPRITES

        self.sprites = Animator('sprites/adventurer-arrow-00.png', **PLAYER_COMMON_KWARGS)

    @property
    def vel(self):
        if self.orientation == "flip-h" and self._vel > 0:
            self._vel = self._vel * -1
        else:
            self._vel = self._vel
        
        return self._vel

    @vel.setter
    def vel(self, val):
        'setting'
        if self.orientation == "flip-h" and self._vel > 0:
            self._vel = val * -1
        else:
            self._vel = val

    @property
    def image(self):
        return next(self.sprites[self.orientation])

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        if self.x < WIN_WIDTH and self.x > 0:
            self.x += self.vel 
        else:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, mc_list, arrow_list):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height+4

        self.mc_list = mc_list
        self.arrow_list = arrow_list

        self.actions = Action()
        self.actions.walk = True

        self.damage = 5
        self._orientation = "orig"
        self._vel = 3

        self.health = 10

        # SPRITES

        self.walk_sprites = Animator("sprites/Skeleton Walk.png", number_of=13, sheet=True, **PLAYER_COMMON_KWARGS)
        self.attack_sprites = Animator("sprites/Skeleton Attack.png", number_of=18, sheet=True, **PLAYER_COMMON_KWARGS)
        self.dead_sprites = Animator("sprites/Skeleton Dead.png", number_of=15, sheet=True, **PLAYER_COMMON_KWARGS)
        self.hit_sprites = Animator("sprites/Skeleton Hit.png", number_of=8, sheet=True, **PLAYER_COMMON_KWARGS)

        self.health_sprite = Animator("sprites/health-bar.png")

    @property
    def vel(self):
        if (self.orientation == "flip-h" and self._vel > 0) or (self.orientation == "orig" and self._vel < 0):
            self._vel = self._vel * -1
        else:
            self._vel = self._vel
        
        return self._vel

    @vel.setter
    def vel(self, val):
        'setting'
        if (self.orientation == "flip-h" and self._vel > 0) or (self.orientation == "orig" and self._vel < 0):
            self._vel = val * -1
        else:
            self._vel = val

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        'setting'
        params = ["orig", "flip-h"]

        if val == 1:
            if self._orientation == "orig":
                self._orientation = "flip-h"
            elif self._orientation == "flip-h":
                self._orientation = "orig"

        elif val in params:
            self._orientation = val


    @property
    def image(self):
        if self.actions.dead:
            image = next(self.dead_sprites[self.orientation])

        elif self.actions.attack:
            image = next(self.attack_sprites[self.orientation])

        elif self.actions.walk:
            image = next(self.walk_sprites[self.orientation])
        
        elif self.actions.hit:
            image = next(self.hit_sprites[self.orientation])

        image = image.copy()
        health = next(self.health_sprite["orig"])
        width = health.get_width()
        full_width = width * (self.health)
        image.blits([(health, (10+i, -4)) for i in range(0, full_width, width)], 0)
        return image


    @property
    def rect(self):
        if self.actions.attack:
            return pygame.Rect(self.x-10, self.y-9, self.width+8, self.height)
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        if not (self.x < WIN_WIDTH-self.width and self.x > self.width):
            if self.x > WIN_WIDTH-self.width:
                self.orientation = "flip-h"

            if self.x < self.width:
                self.orientation = "orig"

            self.actions.walk = True
            self.actions.attack = False

        for arrow in pygame.sprite.spritecollide(self, self.arrow_list, 1):
            if self.health > 0:
                self.actions.hit = True
                self.health -= arrow.damage
                if self.health < 0 : self.actions.dead = True

            self.actions.walk = False 

        if self.actions.walk:
            self.x += self.vel

        if self.dead_sprites.end_of_loop:
            self.mc_list.sprites()[0].score += 5
            self.kill()

        if self.hit_sprites.end_of_loop:
            self.actions.walk = True

        if self.attack_sprites.end_of_loop:
            mc_list = pygame.sprite.spritecollide(self, self.mc_list, 0)
            
            if not mc_list:
                self.actions.walk = True

            else:
                mc = mc_list[0]
                mc.health -= self.damage
                if not any([mc.actions.jump, mc.actions.fall, mc.actions.dead]):
                    mc.actions.hurt = True
            
            
            


        
