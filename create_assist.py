import datetime
import random

import pygame

DELAY_FOR_MULTIPLE = 20

class Animator(object):

    def __init__(self, file_desc, format=None, number_of=1, start_from=0, flip_h=False, flip_v=False, 
    multiple=False, loop=True, scale=None, sheet=False, random=True):
 
        self.multiple = multiple
        self.selected_delay = datetime.datetime.now()
        self.loop = loop
        self.orientation = "orig"
        self.len = number_of
        self.random = random

        if format:
            if self.multiple:
                mul_ent = format["mul_ent"]
                format["mul_ent"] = "{mul_ent}"

            if r"{index}" in file_desc:
                format["index"] = "{index}"

            self.full_file_desc = file_desc.format(**format)
        else: 
            self.full_file_desc = file_desc

        if self.multiple:
            if not sheet:
                self.sprite_objects = {
                    "orig" : [[pygame.image.load(self.full_file_desc.format(mul_ent=ent, index=index)) \
                        for index in range(start_from, number_of)] for ent in mul_ent]
                    }

            else:
                self.sprite_objects = {"orig": []}
                for ent in mul_ent:
                    temp_sprite_list = []
                    sprite_sheet = pygame.image.load(self.full_file_desc.format(mul_ent=ent))
                    sprite_width = sprite_sheet.get_width() // number_of
                    sprite_height = sprite_sheet.get_height()
                    x = 0
                    for _ in range(number_of):
                        sprite_collect = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA, 32)
                        sprite_collect.blit(sprite_sheet, (x, 0))
                        temp_sprite_list.append(sprite_collect.copy())
                        x -= sprite_width
                    
                    self.sprite_objects["orig"].append(temp_sprite_list)
                        

            if scale == "2x": 
                self.sprite_objects["orig"] = [list(map(pygame.transform.scale2x, l)) for l in self.sprite_objects["orig"]]
            
            elif type(scale) is tuple and len(scale) == 2:
                self.sprite_objects["orig"] = [list(map(lambda x: pygame.transform.scale(x, scale), l)) for l in self.sprite_objects["orig"]]

            if flip_h:
                self.sprite_objects["flip-h"] = [[pygame.transform.flip(image, True, False) for image in l] for l in self.sprite_objects["orig"]]
            
            if flip_v:
                self.sprite_objects["flip-v"] = [[pygame.transform.flip(image, False, True) for image in l] for l in self.sprite_objects["orig"]]

            if flip_h and flip_v:
                self.sprite_objects["flip-all"] = [[pygame.transform.flip(image, True, True) for image in l] for l in self.sprite_objects["orig"]]
                
            self.selected = 0

            
        else:

            if "{index}" in self.full_file_desc:
                self.sprite_objects = {
                    "orig" : [pygame.image.load(self.full_file_desc.format(index=index)) for index in range(start_from, number_of)]
                    }            
            else:
                if not sheet:
                    self.sprite_objects = {
                        "orig" : [pygame.image.load(self.full_file_desc) for index in range(start_from, number_of)]
                    }
                
                else:
                    self.sprite_objects = {
                        "orig" : []
                    }
                    sprite_sheet = pygame.image.load(self.full_file_desc)
                    sprite_width = sprite_sheet.get_width() // number_of
                    sprite_height = sprite_sheet.get_height()
                    x = 0
                    for _ in range(number_of):
                        sprite_collect = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA, 32)
                        sprite_collect.blit(sprite_sheet, (x, 0))
                        self.sprite_objects["orig"].append(sprite_collect.copy())
                        x -= sprite_width

            if scale == "2x": 
                self.sprite_objects["orig"] = list(map(pygame.transform.scale2x, self.sprite_objects["orig"])) 

            elif type(scale) is tuple and len(scale) == 2:            
                self.sprite_objects["orig"] = list(map(lambda x: pygame.transform.scale(x, scale), self.sprite_objects["orig"])) 

            if flip_h:
                self.sprite_objects["flip-h"] = [pygame.transform.flip(image, True, False) for image in self.sprite_objects["orig"]]

            if flip_v:
                self.sprite_objects["flip-v"] = [pygame.transform.flip(image, False, True) for image in self.sprite_objects["orig"]]

            if flip_h and flip_v:
                self.sprite_objects["flip-all"] = [pygame.transform.flip(image, True, True) for image in self.sprite_objects["orig"]]
        
        self.sprite_orientation = typed_list(self.sprite_objects["orig"], type="orig")     
        self.sprite_objects_iterate = self.__return_iter()

    
    def __next__(self):
        try:
            if self.multiple:   

                if self.sprite_objects_iterate[self.selected].type == self.orientation:
                    return next(self.sprite_objects_iterate[self.selected])  
                else:
                    raise StopIteration
            else: 
                if self.sprite_objects_iterate.type == self.orientation:
                    return next(self.sprite_objects_iterate)
                else:
                    raise StopIteration
                
        except StopIteration:
            if self.loop:
                self.sprite_objects_iterate = self.__return_iter()
                return next(self.sprite_objects_iterate[self.selected]) if self.multiple else next(self.sprite_objects_iterate)
            
            else:
                return self.sprite_orientation[self.selected][-1] if self.multiple else self.sprite_orientation[-1]

            
    def __getitem__(self, param):
        self.orientation = param
        self.sprite_orientation = typed_list(self.sprite_objects[param], type=param)
        return self

    def __return_iter(self):
        if self.multiple:
            if self.random and (datetime.datetime.now() - self.selected_delay).seconds >= DELAY_FOR_MULTIPLE:
                self.selected = random.randint(0, len(self.sprite_objects)-1)
                self.selected_delay = datetime.datetime.now()
            
            elif not self.random:
                if self.selected < len(self.sprite_objects)-1: self.selected += 1
                else: self.selected = 0

            return typed_list([iter(typed_list(i, type=self.orientation)) for i in self.sprite_orientation], type=self.orientation)
        
        else:
            return iter(self.sprite_orientation)

    def refresh(self): self.sprite_objects_iterate = self.__return_iter()
        
    @property
    def end_of_loop(self):
        if not self.sprite_objects_iterate.list:
            if self.loop: self.sprite_objects_iterate = self.__return_iter()
            return True  
        else: 
            return False

    @property
    def pos(self):
        if not self.sprite_objects_iterate.list:
            return self.sprite_objects_iterate.pos
        else: 
            return False
            

class Action(object):
    def __getattribute__(self, attr):
        __dict__ = super(Action, self).__getattribute__('__dict__')
        if attr == "__dict__":
            return __dict__
        return attr in __dict__
    def __setattr__(self, attr, value):
        if value:
            super(Action, self).__setattr__('__dict__', {attr: value})



class Background(object):
    def __init__(self, dim=(500,500), caption='', image=None):
        self.dim = dim
        self.WIN_WIDTH = dim[0]
        self.WIN_HEIGHT = dim[1]
        self.caption = caption
        self.image = image

    @property
    def dim(self):
        return (self.WIN_WIDTH, self.WIN_HEIGHT)

    @dim.setter
    def set_dim(self, val):
        assert (type(val[0]), type(val[1])) == (int, int)
        self.WIN_WIDTH, self.WIN_HEIGHT = val
        

class typed_list(list):
    def __init__(self, elements, type=None):
        super().__init__(elements)
        self.elements = elements
        self.type = type
        self.iter_obj = iter(elements)

    @property
    def list(self):
        iter_obj_list = list(self.iter_obj)
        self.iter_obj = iter(iter_obj_list)
        return iter_obj_list

    @property
    def pos(self):
        return self.elements.index(self.list[0])

    
    def __iter__(self):
        super().__iter__()
        self.iter_obj = iter(self.elements)
        return self

    def __next__(self):
        return next(self.iter_obj)
