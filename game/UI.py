import pygame



class UI:
    def __init__(self, surface, current_health):
        self.update_health(surface, current_health)

    def show_health(self):
        self.display_surface.blit(self.health_bar, (70,10))

    def update_health(self, surface, current_health):
        #setup
        self.display_surface = surface
        self.current_health = current_health

        #health
        self.health = [
            './graphics/UI/0.png',
            './graphics/UI/1.png',
            './graphics/UI/2.png',
            './graphics/UI/3.png',
        ]
        self.health_bar = pygame.image.load(self.health[self.current_health]).convert_alpha()
        self.health_bar = pygame.transform.scale(self.health_bar, (108,34))

    
    def update(self):
        self.show_health()