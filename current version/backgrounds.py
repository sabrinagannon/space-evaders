import pygame
from constants import w_width,w_height

class Background():
    def __init__(self,level):
        self.level1 = pygame.image.load('assets/background.png').convert()
        self.resolution = (3000,3000)
        self.level = level
        self.offset = 1000
        self.x = -1000
        self.y = -1000

    def handle(self,keys,keith):

        if keys[pygame.K_a]:
            self.x += keith.speed
            if self.x >= 120:
                self.x = 120
        if keys[pygame.K_d]:
            self.x -= keith.speed
            if self.x <= (-self.resolution[0])+120: # probably shouldn't be hardcoded
                self.x = (-self.resolution[0])+120
        if keys[pygame.K_w]:
            self.y += keith.speed
            if self.y >= 120:
                self.y = 120
        if keys[pygame.K_s]:
            self.y -= keith.speed
            if self.y <= -self.resolution[1] + 120:
                self.y = -self.resolution[1] + 120

    def draw(self,screen):
        if self.level == 1:
            screen.blit(self.level1, (self.x,self.y))
        
