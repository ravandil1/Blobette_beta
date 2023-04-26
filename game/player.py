import pygame, tile, level
from support import import_player_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.20
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # audio
        self.jump_sound = pygame.mixer.Sound('./audio/sfx/jump.wav')
        
        self.jump_sound.set_volume(0.2)
        
        #power animation
        self.import_power_animation()
        self.power_frame_index = 0
        self.power_animation_speed = 0.15
        self.display_surface = surface
        
        # player movement
        self.power_index = 0
        self.move_x = 0
        self.move_y = 0
        self.gravity = 0.8
        self.direction = pygame.math.Vector2(0,0)

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        

    def import_character_assets(self):
        character_path = './graphics/player/'
        self.animations = {'idle':[], 'jump':[], 'falling':[], 'dying':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_player_folder(full_path)

    def import_power_animation(self):
        self.power = import_player_folder('./graphics/power')

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image


    def power_animation(self):
        if self.power_index > 0:
            self.power_frame_index += self.power_animation_speed
            if self.power_index < 25 and self.power_frame_index > 3:
                self.power_frame_index = 3
            elif self.power_index < 50 and self.power_frame_index > 7:
                self.power_frame_index = 7
            elif self.power_index >= 50 and self.power_frame_index > 11:
                self.power_frame_index = 11
            power_animation = self.power[int(self.power_frame_index)]
            pos = self.rect.topright
            self.display_surface.blit(power_animation, pos)
    
    def get_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_keys = pygame.mouse.get_pressed()
        
        if mouse_keys[0] == True and self.on_ground == True:       
            self.power_index += 1
        elif mouse_keys[0] == False and self.power_index > 0 and self.on_ground == True:
            self.jump_sound.play()
            self.move_x = (mouse_pos[0] - self.rect.x)
            self.move_y = (mouse_pos[1] - self.rect.y)
            if self.power_index < 25:
                if self.move_x > 60:
                    self.move_x = 60
                elif self.move_x < -60:
                    self.move_x = -60
                if self.move_y > 60:
                    self.move_y = 60
                elif self.move_y < -60:
                    self.move_y = -60        
            elif self.power_index < 50:
                if self.move_x > 90:
                    self.move_x = 90
                elif self.move_x < -90:
                    self.move_x = -90
                if self.move_y > 90:
                    self.move_y = 90
                elif self.move_y < -90:
                    self.move_y = -90    
            else:
                if self.move_x > 120:
                    self.move_x = 120
                elif self.move_x < -120:
                    self.move_x = -120
                if self.move_y > 120:
                    self.move_y = 120
                elif self.move_y < -120:
                    self.move_y = -120
                
            self.power_index = 0
            self.power_frame_index = 0
            self.direction.x += self.move_x * 0.105
            self.direction.y += self.move_y * 0.105
    
    def get_status(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_pos[0] < self.rect.x:
            self.facing_right = False
        else:
            self.facing_right = True
        
        if self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x == 0:
                self.status = 'idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        
    def update(self):        
        self.get_status()
        self.animate()
        self.power_animation()
        self.get_input()
        
        
        
        
        
        
        

