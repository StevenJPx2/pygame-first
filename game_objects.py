import pygame
from pygame.color import *
from pygame.locals import *

from create_assist import Animator, GameObject

# PLAYER GLOBAL VARIABLES
JUMP_HEIGHT = 7
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
def set_dim(self, val):
    assert (type(val[0]), type(val[1])) == (int, int)
    self.WIN_WIDTH, self.WIN_HEIGHT = val

@dim.deleter
def del_dim(self):
    del self.WIN_WIDTH
    del self.WIN_HEIGHT

class Player(GameObject):
    def __init__(self, x, y, width, height, arrow_list):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.arrow_list = arrow_list
        self.actions = {
            "jump" : False,
            "left" : False,
            "right" : False,
            "fall" : False,
            "crouch" : False,
            "idle" : False,
            "draw-bow" : False
        }
        self.jump_count = JUMP_HEIGHT
        self.do_shoot = False

        #sprites

        self.walk_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"run3"}, number_of=6, **PLAYER_COMMON_KWARGS)
        self.idle_sprites = Animator("sprites/adventurer-{mul_ent}-0{index}.png", format={"mul_ent":("idle", "idle-2")}, number_of=4, 
                            multiple=True, **PLAYER_COMMON_KWARGS)
        self.jump_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"jump"}, number_of=4, loop=False, **PLAYER_COMMON_KWARGS)
        self.fall_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"fall"}, number_of=2, **PLAYER_COMMON_KWARGS)
        self.crouch_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"crouch"}, number_of=4, **PLAYER_COMMON_KWARGS)
        self.bow_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"bow"}, number_of=9, loop=True, **PLAYER_COMMON_KWARGS)
        self.bow_jump_sprites = Animator("sprites/adventurer-{z}-0{index}.png", format={"z":"bow-jump"}, number_of=6, loop=True, **PLAYER_COMMON_KWARGS)


    def draw(self, window):
        
        
        if self.actions["draw-bow"] and not self.actions["jump"]:
            if self.actions["left"]:
                window.blit(next(self.bow_sprites["flip-h"]), (self.x,self.y))
            else:
                window.blit(next(self.bow_sprites["orig"]), (self.x,self.y))

        elif self.actions["jump"]:
            if self.actions["draw-bow"]:
                if self.actions["left"]:
                    window.blit(next(self.bow_jump_sprites["flip-h"]), (self.x,self.y))
                else:
                    window.blit(next(self.bow_jump_sprites["orig"]), (self.x,self.y))

            else:
                if self.actions["left"]:
                    window.blit(next(self.jump_sprites["flip-h"]), (self.x,self.y))
                else:
                    window.blit(next(self.jump_sprites["orig"]), (self.x,self.y))
            
        elif self.actions["fall"]:
            if self.actions["draw-bow"]:
                if self.actions["left"]:
                    window.blit(next(self.bow_jump_sprites["flip-h"]), (self.x,self.y))
                else:
                    window.blit(next(self.bow_jump_sprites["orig"]), (self.x,self.y))
            else:
                if self.actions["left"]:
                    window.blit(next(self.fall_sprites["flip-h"]), (self.x,self.y))
                else:
                    window.blit(next(self.fall_sprites["orig"]), (self.x,self.y))

        elif self.actions["idle"]:
            if self.actions["left"]:
                window.blit(next(self.idle_sprites["flip-h"]), (self.x,self.y))
            else:
                window.blit(next(self.idle_sprites["orig"]), (self.x,self.y))

        elif self.actions["crouch"]:
            if self.actions["left"]:
                window.blit(next(self.crouch_sprites["flip-h"]), (self.x,self.y))
            else:
                window.blit(next(self.crouch_sprites["orig"]), (self.x,self.y))
        
        elif self.actions["left"]:
            window.blit(next(self.walk_sprites["flip-h"]), (self.x,self.y))

        elif self.actions["right"]:
            window.blit(next(self.walk_sprites["orig"]), (self.x,self.y))

    def set_param(self):

        keys = pygame.key.get_pressed()

        # LEFT

        if (keys[K_LEFT] or keys[K_a]) and self.x > self.vel:
            self.x -= self.vel
            self.actions["left"] = True
            self.actions["right"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["draw-bow"] = False

        # RIGHT

        elif (keys[K_RIGHT] or keys[K_d]) and self.x < WIN_WIDTH - self.width - self.vel:
            self.x += self.vel
            self.actions["right"] = True
            self.actions["left"] = False
            self.actions["idle"] = False
            self.actions["crouch"] = False
            self.actions["draw-bow"] = False


        # CROUCH

        elif (keys[K_DOWN] or keys[K_LSHIFT]) and not (self.actions["jump"] or self.actions["fall"]):
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
                "height" : self.height,
                "arrow_list" : self.arrow_list
            }

            self.actions["draw-bow"] = True

            if (self.bow_jump_sprites.end_of_loop or self.bow_sprites.end_of_loop):
                print("End-of")

                if self.actions["left"]:
                    self.arrow_list.add(Arrow(orientation="flip-h", **temp_kwargs))

                else:
                    self.arrow_list.add(Arrow(orientation="orig", **temp_kwargs))

                self.actions["draw-bow"] = False


        # IDLE

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
            

class Arrow(GameObject):
    def __init__(self, x, y, width, height, arrow_list, orientation):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.arrow_list = arrow_list
        self.orientation = orientation
        self._vel = 5

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
    def set_vel(self, val):
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
            self.arrow_list.remove(self)
