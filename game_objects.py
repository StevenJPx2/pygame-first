import pygame
from pygame.color import *
from pygame.locals import *

from create_assist import Animator

# PLAYER GLOBAL VARIABLES
JUMP_HEIGHT = 10
SLIDE_COUNT = 20
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
    def __init__(self, x, y, width, height, arrow_list, enemy_list):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._vel = 7
        self.arrow_list = arrow_list
        self.enemy_list = enemy_list
        self.health = 20
        self.actions = {
            "jump" : False,
            "left" : False,
            "right" : False,
            "fall" : False,
            "stand" : False,
            "slide" : False,
            "crouch" : False,
            "idle" : False,
            "draw-bow" : False
        }
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


    @property
    def vel(self):
        if (self.actions["left"] and self._vel > 0) or (self.actions["right"] and self._vel < 0):
            self._vel = self._vel * -1
        else:
            self._vel = self._vel
        
        return self._vel

    @vel.setter
    def vel(self, val):
        'setting'
        if (self.actions["left"] and self._vel > 0) or (self.actions["right"] and self._vel < 0):
            self._vel = val * -1
        else:
            self._vel = val

    @property
    def image(self):
        if self.actions["draw-bow"] and not self.actions["jump"]:
            return next(self.bow_sprites[self.orientation])

        elif self.actions["jump"]:
            if self.actions["draw-bow"]:
                return next(self.bow_jump_sprites[self.orientation])

            else:
                if self.jump_sprites.end_of_loop:
                    return next(self.smrslt_sprites[self.orientation])
                return next(self.jump_sprites[self.orientation])
            
        elif self.actions["fall"]:
            if self.actions["draw-bow"]:
                return next(self.bow_jump_sprites[self.orientation])
            else:
                return next(self.fall_sprites[self.orientation])

        elif self.actions["idle"]:
            return next(self.idle_sprites[self.orientation])

        elif self.actions["crouch"]:
            return next(self.crouch_sprites[self.orientation])

        elif self.actions["slide"]:
            return next(self.slide_sprites[self.orientation])

        elif self.actions["stand"]:
            return next(self.stand_sprites[self.orientation])
        
        else:
            return next(self.walk_sprites[self.orientation])

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):

        keys = pygame.key.get_pressed()
        
        
        # SLIDE LEFT

        if (all([keys[K_LEFT], keys[K_DOWN]]) or all([keys[K_a], keys[K_LSHIFT]])) and self.x > self.vel \
             and not (self.actions["jump"] or self.actions["fall"]):
            self.actions["slide"] = True
            self.orientation = "flip-h"
            self.actions["left"] = True
            self.x += self.vel
            self.actions["right"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["draw-bow"] = False


        # LEFT

        elif (keys[K_LEFT] or keys[K_a]) and self.x > self.vel:
            self.actions["left"] = True
            self.x += self.vel
            self.orientation = "flip-h"
            self.actions["right"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["slide"] = False
            self.actions["draw-bow"] = False


        # SLIDE RIGHT


        elif (all([keys[K_RIGHT], keys[K_DOWN]]) or all([keys[K_d], keys[K_LSHIFT]])) and self.x < WIN_WIDTH - self.width - self.vel \
            and not (self.actions["jump"] or self.actions["fall"]):
            self.actions["slide"] = True
            self.actions["right"] = True
            self.x += self.vel
            self.orientation = "orig"
            self.actions["left"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["draw-bow"] = False

        # RIGHT

        elif (keys[K_RIGHT] or keys[K_d]) and self.x < WIN_WIDTH - self.width - self.vel:
            self.actions["right"] = True
            self.x += self.vel
            self.orientation = "orig"
            self.actions["left"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["slide"] = False
            self.actions["draw-bow"] = False




        # CROUCH

        elif (keys[K_DOWN] or keys[K_LSHIFT]) and not (self.actions["jump"] or self.actions["fall"]):
            if not self.actions["stand"]:
                self.actions["crouch"] = True

            self.actions["jump"] = False
            self.actions["idle"] = False
            self.actions["draw-bow"] = False


        # DRAW-BOW 


        elif keys[K_SPACE]:
            temp_kwargs = {
                "x" : self.x,
                "y" : self.y,
                "width" : self.width,
                "height" : self.height
            }

            self.actions["draw-bow"] = True

            if (self.bow_jump_sprites.end_of_loop or self.bow_sprites.end_of_loop):

                self.arrow_list.add(Arrow(orientation=self.orientation, **temp_kwargs))

                self.actions["draw-bow"] = False


        # IDLE

        elif self.actions["stand"] and self.stand_sprites.end_of_loop:
            self.actions["stand"] = False
            self.actions["idle"] = True

        elif not (self.actions["jump"] or self.actions["fall"]):
            self.actions["idle"] = True
            self.actions["draw-bow"] = False

        
        else: 
            self.actions["idle"] = True
            self.actions["draw-bow"] = False



        # FALL
        # NEED TO IMPROVE THE ALGORITHM
        
        if self.actions["fall"]:
            if self.jump_count >= -JUMP_HEIGHT:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                    self.actions["fall"] = True
                    self.actions["jump"] = False
                    self.actions["crouch"] = False
                    self.actions["idle"] = False
                    self.actions["draw-bow"] = False



                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.actions["fall"] = False

                self.jump_count = JUMP_HEIGHT
        
        # JUMP

        elif not self.actions["jump"]:
            if keys[K_UP] or keys[K_w]:
                self.actions["jump"] = True
                self.actions["crouch"] = False
                self.actions["idle"] = False
                # self.actions["draw-bow"] = False

                
        else:
            if self.jump_count >= -JUMP_HEIGHT:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                    self.actions["fall"] = True
                    self.actions["jump"] = False
                    self.actions["crouch"] = False
                    self.actions["idle"] = False
                    self.actions["draw-bow"] = False

                    
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1

            else:
                self.actions["fall"] = False
                self.actions["idle"] = False
                self.actions["crouch"] = False
                self.actions["draw-bow"] = False



                self.jump_count = JUMP_HEIGHT
            

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, orientation):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self._vel = 6
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
    def __init__(self, x, y, width, height, arrow_list, mc_list):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.arrow_list = arrow_list
        self.mc_list = mc_list
        self.actions = {
            "dead" : False,
            "walk" : True,
            "attack" : False,
            "hit" : False
        }
        self.damage = 5
        self._orientation = "orig"
        self._vel = 3
        self.health = 10

        # SPRITES

        self.walk_sprites = Animator("sprites/Skeleton Walk.png", number_of=13, sheet=True, **PLAYER_COMMON_KWARGS)
        self.attack_sprites = Animator("sprites/Skeleton Attack.png", number_of=18, sheet=True,**PLAYER_COMMON_KWARGS)
        self.dead_sprites = Animator("sprites/Skeleton Dead.png", number_of=15, sheet=True, **PLAYER_COMMON_KWARGS)
        self.hit_sprites = Animator("sprites/Skeleton Hit.png", number_of=8, sheet=True, **PLAYER_COMMON_KWARGS)


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
        if self.actions["dead"]:
            return next(self.dead_sprites[self.orientation])

        elif self.actions["attack"]:
            return next(self.attack_sprites[self.orientation])

        elif self.actions["walk"]:
            return next(self.walk_sprites[self.orientation])
        
        elif self.actions["hit"]:
            return next(self.hit_sprites[self.orientation])


    @property
    def rect(self):
        if self.actions["attack"]:
            return pygame.Rect(self.x-10, self.y-9, self.width+8, self.height)
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        if not (self.x < WIN_WIDTH-self.width and self.x > self.width):
            if self.x > WIN_WIDTH-self.width:
                self.orientation = "flip-h"

            if self.x < self.width:
                self.orientation = "orig"

            self.actions["walk"] = True
            self.actions["attack"] = False


        if self.actions["walk"]:
            self.x += self.vel

        for arrow in pygame.sprite.spritecollide(self, self.arrow_list, 1):
            
            if self.health > 0:
                self.actions["hit"] = True
                self.actions["dead"] = False
                self.health -= arrow.damage
            else:
                self.actions["dead"] = True
                self.actions["hit"] = False

            self.actions["walk"] = False

        for mc in pygame.sprite.spritecollide(self, self.mc_list, 0):
            print(mc.health)
            self.actions["attack"] = True
            self.actions["dead"] = False
            self.actions["walk"] = False
            self.actions["hit"] = False

            if mc.actions["left"] and self.orientation == "flip-h" and mc.x > self.x:
                self.orientation = "orig"
            elif mc.actions["right"] and self.orientation == "orig" and mc.x < self.x:
                self.orientation = "flip-h"


        if self.dead_sprites.end_of_loop:
            self.kill()

        if self.hit_sprites.end_of_loop:
            self.actions["hit"] = False
            self.actions["walk"] = True

        if self.attack_sprites.end_of_loop:
            mc_list = pygame.sprite.spritecollide(self, self.mc_list, 0)
            if not mc_list:
                self.actions["attack"] = False
                self.actions["walk"] = True

            else:
                mc_list[0].health -= self.damage
            
            
            


        
