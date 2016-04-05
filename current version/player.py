import pygame, sys, items, time
from constants import w_width, w_height
import json

class Player(pygame.sprite.Sprite):
    def __init__(self,startingPos,imagePath, speed = 10):
        pygame.sprite.Sprite.__init__(self) # calls the parent class constructor

        self.sheet = pygame.image.load(imagePath[0] + imagePath[1]) # load and assign spritesheet

        # using with to load clip co-ordinates ensures the files
        # are closed
        with open(imagePath[0] + 'ls.json', "rb") as ls,\
             open(imagePath[0] + 'us.json', "rb") as us,\
             open(imagePath[0] + 'rs.json', "rb") as rs,\
             open(imagePath[0] + 'ds.json', "rb") as ds:
            self.left_states = {int(key):tuple(value) for key, value in json.load(ls).items()}
            self.up_states = {int(key):tuple(value) for key, value in json.load(us).items()}
            self.right_states = {int(key):tuple(value) for key, value in json.load(rs).items()}
            self.down_states = {int(key):tuple(value) for key, value in json.load(ds).items()}

        clip_area = pygame.Rect(self.left_states[0]) # this is the size of a frame
        self.sheet.set_clip(clip_area)


        # create a rectangle that is the player sprite
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = startingPos

        # used to cycle through frames
        self.frame = 0

        # state attributes
        self.initialSpeed = speed
        self.speed = speed
        self.itemsHeld = 0
        self.coinsHeld = 0
        self.score = 0
        self.lives = 3
        self.isInvincible = False
        self.startInvinc = 0

    def handle(self,keys,bg):

        if keys[pygame.K_a]:
            self.update('left')
        if keys[pygame.K_d]:
            self.update('right')
        if keys[pygame.K_w]:
            self.update('up')
        if keys[pygame.K_s]:
            self.update('down')

        if (keys[pygame.K_k]) and (self.itemsHeld > 0) :
            self.itemsHeld -= 1
            self.updateSpeed()
            droppedItem = pygame.Rect((self.rectangle.x -1000 - bg.x), (self.rectangle.y -1000 - bg.y), 50,50)
            droppedCrystal = items.Crystal(droppedItem)
            return droppedCrystal

        if keys[pygame.K_ESCAPE]:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        
        return None

    def update(self, direction):
        if direction == 'left':
            if (self.rectangle.x > self.speed):
                self.move(self.left_states)
        if direction == 'right':
            if (self.rectangle.x < w_width - self.rectangle.width):
                self.move(self.right_states)
        if direction == 'up':
            if (self.rectangle.y > self.speed):
                self.move(self.up_states)
        if direction == 'down':
            if (self.rectangle.y < w_height-self.rectangle.height):
                self.move(self.down_states)

        # what actually updates the image
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def move(self, movement):
        if type(movement) is dict:
            # regular case, where we call self.move with our dictionary
            # of coordinates
            self.frame += 1     # cycle through
            if self.frame > (len(movement) -1):
                self.frame = 0
            coords = movement[self.frame]
        else:
            # in the case we want to stop moving, and pass in
            # a single stand frame
            coords =  movement
        new_rect =  pygame.Rect(coords)

        self.sheet.set_clip(new_rect)
        return movement   

    
    def updateSpeed(self):
        update = self.initialSpeed - (2*self.itemsHeld)
        if update < 5:
            update = 5
        self.speed = update

    def onEnemyCollision(self):
        self.isInvincible = True
        self.startInvinc = pygame.time.get_ticks()

    def updateInvincible(self):
        newTime = pygame.time.get_ticks()
        if (newTime - self.startInvinc ) >= 1000 :
            
            self.isInvincible = False
