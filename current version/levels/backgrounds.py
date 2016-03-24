import pygame
from constants import w_width,w_height
import os

class Background():
    def __init__(self,level):

        # these should be updated relative to the level
        self.resolution = (1000,1000)
        self.offset = 0
        self.x = 0
        self.y = 0
        self.disabled = None

        if level == 1:
            self.pic = pygame.image.load('assets/images/LevelOneBG.png').convert()
            self.resolution = (3000,3000)
            self.offset = 1000
            self.x = -1000
            self.y = -1000

        elif level == 2:
            self.pic = pygame.image.load('assets/images/space.jpg').convert()
            self.resolution = (3000,3000)
            self.offset = 1000
            self.x = -1000
            self.y = -1000

         elif level == 3:
            self.pic = pygame.image.load('assets/images/background.png').convert()
            self.resolution = (3000,3000)
            self.offset = 1000
            self.x = -1000
            self.y = -1000

        self.level = level

    def handle(self,keys,keith,level):

        if checkForCollisions(level,keith):
            #hitting an obstacle
            if self.disabled == None:
                #nothing set, so set something
                if keys[pygame.K_a]:
                    self.disabled = pygame.K_a
                elif keys[pygame.K_s]:
                    self.disabled = pygame.K_s
                elif keys[pygame.K_w]:
                    self.disabled = pygame.K_w
                elif keys[pygame.K_d]:
                    self.disabled = pygame.K_d
            else:
                #something set
                if keys[self.disabled]:
                    return self.disabled
                else:
                    self.move(keys,keith)
        else:
            self.disabled = None
            self.move(keys,keith)
        
        return self.disabled
            
    def move(self,keys,keith):
        if keys[pygame.K_a]:
            self.x += keith.speed
            if self.x >= (w_width/2):
                self.x = (w_width/2)

        if keys[pygame.K_d]:
            self.x -= keith.speed
            if self.x <= (-self.resolution[0])+(w_width/2):
                self.x = (-self.resolution[0])+(w_width/2)

        if keys[pygame.K_w]:
            self.y += keith.speed
            if self.y >= (w_height/2):
                self.y = (w_height/2)

        if keys[pygame.K_s]:
            self.y -= keith.speed
            if self.y <= -self.resolution[1] + (w_height/2):
                self.y = -self.resolution[1] + (w_height/2)       

    def draw(self,screen):
        screen.blit(self.pic, (self.x,self.y))


def checkForCollisions(level,keith):
    for obstacle in level.obstacles:
        if obstacle.rect.colliderect(keith.rectangle):
            return True
        
