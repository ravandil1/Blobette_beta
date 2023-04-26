import pygame
from tile import Tile, StaticTile, Key, Door
from settings import tile_size, screen_width, screen_height
from player import Player
from support import import_csv_layout, import_cut_graphics
from game_data import *


class Level:
    def __init__(self,current_level,surface, level_complete, try_again):
       self.reset_level(current_level,surface, level_complete, try_again)
        

    def reset_level(self,current_level,surface, level_complete, try_again):
        # general setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.level_complete = level_complete
        self.try_again = try_again
        
        # audio
        self.death_sound = pygame.mixer.Sound('./audio/sfx/death.wav')
        self.open_sound = pygame.mixer.Sound('./audio/sfx/dooropen.wav')

        #background
        self.background = pygame.image.load('./graphics/Backgrounds/background.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        
        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        #keys setup
        keys_layout = import_csv_layout(level_data['keys'])
        self.keys_sprites = self.create_tile_group(keys_layout, 'keys')
        self.key_index = 0
        
        #door setup
        doors_layout = import_csv_layout(level_data['doors'])
        self.door_sprites = self.create_tile_group(doors_layout, 'doors')
        
        self.current_x = 0
    
    
    
    def create_tile_group(self, layout,type):
        self.sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/Tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size,x,y, tile_surface) 
                    elif type == 'keys':
                        sprite = Key(tile_size,x,y)
                    elif type == 'doors':
                        sprite = Door(tile_size,x,y, './graphics/door')
                        
                        
                    self.sprite_group.add(sprite)

        return self.sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left    
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right
                    

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.rect.y += player.direction.y
        player.apply_gravity()
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if  player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.direction.x = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        

    def key_interaction(self):
        collided_keys = pygame.sprite.spritecollide(self.player.sprite, self.keys_sprites, True)
        if collided_keys:
            self.open_sound.play()
            self.key_index += 1

    def door_interaction(self):
        collided_doors = pygame.sprite.spritecollide(self.player.sprite, self.door_sprites, False)
        if collided_doors and self.key_index == 1:
            self.key_index = 0
            self.level_complete()
            
            
            
    
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
                self.death_sound.play()
                self.try_again()

    def run(self):
        #level tiles
        self.display_surface.blit(self.background,(0,0))
        self.terrain_sprites.draw(self.display_surface)

        #key
        self.keys_sprites.draw(self.display_surface)
        self.key_interaction()

        #door
        self.door_sprites.draw(self.display_surface)
        self.door_interaction()
        self.door_sprites.update(self.key_index)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.check_death()
        