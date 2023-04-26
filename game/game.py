import pygame
import sys
from settings import *
from level import Level
from player import Player
from UI import UI
from tutorial import tutorial, tutorial2, tutorial3, tutorial4
from game_data import levels

# Pygame setup
pygame.init()

class Game:
    def __init__(self, current_health):
        self.level = Level(current_level, screen, self.level_complete, self.try_again)
        self.current_health = current_health
        self.status = 'tutorial'
    
        #audio
        self.bg_music = pygame.mixer.music.load('./audio/bg_music.wav')
        pygame.mixer.music.set_volume(0.1)
        
        

        #UI
        self.ui = UI(screen, self.current_health)
    
    def level_complete(self):
        self.status = 'complete'

    def try_again(self):
        if self.current_health <= 1:
            self.status = 'game over'
        else:
            self.status = 'try again'

    
    def run(self):
        self.level.run()
        self.ui.update()
        
        

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blobette")
clock = pygame.time.Clock()
current_level = 0
current_health = 3
game = Game(current_health)

test_font = pygame.font.Font(None, 50)
test_font2 = pygame.font.Font(None, 25)
complete_level = test_font.render('Level complete', False, 'White')
try_again = test_font.render('Try again', False, 'White')
game_over = test_font.render('Game Over', False, 'White')
press = test_font2.render('Press left mouse button to continue', False, 'White')
how_to_play = test_font.render('How to play', False, 'White')
tutorial_msg = test_font2.render(tutorial, False, 'White')
tutorial_msg2 = test_font2.render(tutorial2, False, 'White')
tutorial_msg3 = test_font2.render(tutorial3, False, 'White')
tutorial_msg4 = test_font2.render(tutorial4, False, 'White')


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if game.status == 'run':
        game.run()

    elif game.status == 'tutorial':
        mouse_keys = pygame.mouse.get_pressed()
        key_pressed = False
        pygame.mixer.music.play(loops = - 1)
        if mouse_keys[0] and key_pressed == False:
            key_pressed = True
            game.status = 'run'

        screen.fill('black')
        screen.blit(how_to_play, (screen_width //2 - 150, 100))
        screen.blit(tutorial_msg, (150, 200))
        screen.blit(tutorial_msg2, (150, 220))
        screen.blit(tutorial_msg3, (150, 240))
        screen.blit(tutorial_msg4, (150, 260))
        screen.blit(press, (screen_width //2 - 150, screen_height // 2))     
        
    elif game.status == 'complete':
        mouse_keys = pygame.mouse.get_pressed()
        key_pressed = False
        if mouse_keys[0] and key_pressed == False:
            key_pressed = True
            current_level += 1
            if current_level > 4:
                current_level = 0
                game.current_health = 3
                game.ui.update_health(screen, game.current_health)
            game.level.reset_level(current_level, screen, game.level_complete, game.try_again)
            game.status = 'run'
        screen.fill('black')
        screen.blit(complete_level, (screen_width //2 - 150, screen_height // 2 - 50))
        screen.blit(press, (screen_width //2 - 150, screen_height // 2))
    
    elif game.status == 'try again' and game.current_health > 0:
        mouse_keys = pygame.mouse.get_pressed()
        key_pressed = False
        if mouse_keys[0] and key_pressed == False:
            key_pressed = True
            game.current_health += -1
            game.level.reset_level(current_level, screen, game.level_complete, game.try_again)
            game.ui.update_health(screen, game.current_health)
            game.status = 'run'
        screen.fill('black')
        screen.blit(try_again, (screen_width //2 - 150, screen_height // 2 - 50))
        screen.blit(press, (screen_width //2 - 150, screen_height // 2))
    
    elif game.status == 'game over':
        mouse_keys = pygame.mouse.get_pressed()
        key_pressed = False
        game.current_health = 3
        pygame.mixer.music.stop()
        
        if mouse_keys[0] and key_pressed == False:
            key_pressed = True
            current_level = 0
            game.level.reset_level(current_level, screen, game.level_complete, game.try_again)
            game.ui.update_health(screen, game.current_health)
            game.status = 'run'
            pygame.mixer.music.play(loops = -1)

        screen.fill('black')
        screen.blit(game_over, (screen_width //2 - 150, screen_height // 2 - 50))
        screen.blit(press, (screen_width //2 - 150, screen_height // 2))

      

        
    pygame.display.update()
       

    
    clock.tick(60)

    
    


