import pygame
from constants import w_width,w_height
import os

class Background():
    def __init__(self,level):

        # these should be updated relative to the level
        self.resolution = (3000,3000)
        self.offset = 1000
        self.x = -1000
        self.y = -1000
        self.disabled = []
        self.collides = 0

        if level == 1:
            self.pic = pygame.image.load('assets/images/levelOne/LevelOneBG.png').convert()
        elif level == 2:
            self.pic = pygame.image.load('assets/images/levelTwo/GroundAndOutline.png').convert()
        elif level == 3:
            self.pic = pygame.image.load('assets/images/levelThree/GroundAndOutline.png').convert()
        elif level == 4:
            self.pic = pygame.image.load('assets/images/levelFour/GroundAndOutline.png').convert()
        elif level == 5:
            self.pic = pygame.image.load('assets/images/space.jpg').convert()
            self.resolution = (3000,3000)
            self.offset = 1000
            self.x = -1000
            self.y = -1000

        self.previousPos = (self.x,self.y)
        self.level = level

    def handle(self,keys,keith,level):
        diffX = abs(self.x - self.previousPos[0])
        diffY = abs(self.y - self.previousPos[1])

        collisions = collision(level,keith)
        if len(collisions):
            # hitting an obstacle
            if self.disabled == []:

                self.collides = len(collisions)
                # nothing set, so set something
                if keys[pygame.K_a]:
                    self.disabled.append(pygame.K_a)
                if keys[pygame.K_s]:
                    self.disabled.append(pygame.K_s)
                if keys[pygame.K_w]:
                    self.disabled.append(pygame.K_w)
                if keys[pygame.K_d]:
                    self.disabled.append(pygame.K_d)
            else:
                if len(collisions) > self.collides:
                    if keys[pygame.K_a]:
                        self.disabled.append(pygame.K_a)
                    if keys[pygame.K_s]:
                        self.disabled.append(pygame.K_s)
                    if keys[pygame.K_w]:
                        self.disabled.append(pygame.K_w)
                    if keys[pygame.K_d]:
                        self.disabled.append(pygame.K_d)
                    self.collides = len(collisions)
                    
                # something set
                for pressed in self.disabled:
                    if keys[pressed]:
                    # if we tried to move in the disabled direction
                        return self.disabled
               
                # we are moving in a new direction, so allow it
                if self.level == 5:
                    keith.playerMove(keys)
                else:
                    self.move(keys,keith)
        else:
            #if (diffX > 10) and (diffY > 10):
            self.disabled = []
            self.collides = 0
            if self.level == 5:
                keith.playerMove(keys)
            else:
                self.move(keys,keith)

        return self.disabled


    def move(self,keys,keith):

        self.previousPos = (self.x, self.y)

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


def collision(level,keith):
    colliders = []
    for obstacle in level.obstacles:
        if obstacle.rect.colliderect(keith.rectangle):
            colliders.append(obstacle)
            #return True
    return colliders
