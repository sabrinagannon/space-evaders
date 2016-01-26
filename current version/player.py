import pygame, sys
from constants import w_width, w_height
import pickle

class Player(pygame.sprite.Sprite):
    def __init__(self,startingPos,imagePath, speed = 5.5):
        pygame.sprite.Sprite.__init__(self) # calls the parent class constructor
        
        self.sheet = pygame.image.load(imagePath[0] + imagePath[1]) # load and assign spritesheet

        # using with to load clip co-ordinates ensures the files
        # are closed
        with open(imagePath[0] + 'ls.dat', "rb") as ls,\
             open(imagePath[0] + 'us.dat', "rb") as us,\
             open(imagePath[0] + 'rs.dat', "rs") as rs,\
             open(imagePath[0] + 'ds.dat', "rb") as ds:
                    self.left_states = pickle.load(ls)
                    self.up_states = pickle.load(us)
                    self.right_states = pickle.load(rs)
                    self.down_states = pickle.load(ds)
        
        clip_area = pygame.Rect(self.left_states[0]) # this is the size of a frame
        self.sheet.set_clip(clip_area)

        
        # create a rectangle that is the player sprite
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = startingPos        
        
        # used to cycle through frames
        self.frame = 0  
        self.speed = speed
        
    
    def handle(self,event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                self.update('left')
            if event.key == pygame.K_d:
                self.update('right')
            if event.key == pygame.K_w:
                self.update('up')
            if event.key == pygame.K_s:
                self.update('down')
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:  

            if event.key == pygame.K_a:
                self.update('stand_left')            
            if event.key == pygame.K_d:
                self.update('stand_right')
            if event.key == pygame.K_w:
                self.update('stand_up')
            if event.key == pygame.K_s:
                self.update('stand_down')

    def update(self, direction):
        if direction == 'left':
            if (self.rectangle.x > self.speed):
                self.rectangle.x -= self.speed 
                self.move(self.left_states)
        if direction == 'right':
            if (self.rectangle.x < w_width - self.rectangle.width):
                self.rectangle.x += self.speed
                self.move(self.right_states)
        if direction == 'up':
            if (self.rectangle.y > self.speed):
                self.rectangle.y -= self.speed
                self.move(self.up_states)
        if direction == 'down':
            if (self.rectangle.y < w_height-self.rectangle.height):
                self.rectangle.y += self.speed 
                self.move(self.down_states)
 
        if direction == 'stand_left':
            self.move(self.left_states[0])
        if direction == 'stand_right':
            self.move(self.right_states[0])
        if direction == 'stand_up':
            self.move(self.up_states[0])
        if direction == 'stand_down':
            self.move(self.down_states[0])

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
        return movement         # not sure why we return this
