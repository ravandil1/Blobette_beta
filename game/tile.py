import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class Key(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('./graphics/Props/Keys/key.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
        

class AnimatedTile(Tile):
    def __init__(self, size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()

class Door(AnimatedTile):
    def __init__(self,size,x,y,path):
        
        super().__init__(size,x,y,path)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
    
    def animate(self, index):
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(index)]

    def update(self, index):
        self.animate(index)
        