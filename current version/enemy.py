import pygame, sys, random, math
from constants import w_width, w_height,playerSpeed
import json

class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def negateX(self):
        self.x *= -1

    def negateY(self):
        self.y *= -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self,startingPos,imagePath,speed = 10):
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
        self.speed = speed
        
        self.heading = self.createRandomHeading()
        self.direction = 'left'
        self.detection = self.rectangle.inflate(60,60)

    def update(self,playerRect):

        if self.detection.colliderect(playerRect):
            self.chase(playerRect)
        else:
            self.patrol()
            self.detection = self.rectangle.inflate(60,60)
        
    def patrol(self):
        nextXPos = self.rectangle.x + (self.speed*self.heading.x)
        nextYPos = self.rectangle.y + (self.speed*self.heading.y)

        if nextXPos > (w_width-self.rectangle.width):
            newHeading = vector((-1*self.heading.x),self.heading.y)
            self.heading = newHeading
        if nextXPos <= 0:
            newHeading = vector((-1*self.heading.x),self.heading.y)
            self.heading = newHeading
        if nextYPos > (w_height-self.rectangle.height):
            newHeading = vector(self.heading.x,(-1*self.heading.y))
            self.heading = newHeading
        if nextYPos <= 0:
            newHeading = vector(self.heading.x,(-1*self.heading.y))
            self.heading = newHeading

        self.rectangle.x = nextXPos
        self.rectangle.y = nextYPos

        if nextYPos > nextXPos: # animate vertical
            if self.heading.y > 0:        # moving down
                self.move(self.down_states)
            else:
                self.move(self.up_states)
        else:                   # animate hroizontal
            if self.heading.x > 0:        # moving right
                self.move(self.right_states)
            else:
                self.move(self.left_states)

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def patrolBorder(self):
        if self.direction == 'left':
            if (self.rectangle.x > self.speed):
                self.rectangle.x -= self.speed
                self.move(self.left_states)
            else:
                self.direction = 'down'
                
        if self.direction == 'right':
            if (self.rectangle.x < w_width - self.rectangle.width):
                self.rectangle.x += self.speed
                self.move(self.right_states)
            else:
                self.direction = 'up'

        if self.direction == 'up':
            if (self.rectangle.y > self.speed):
                self.rectangle.y -= self.speed
                self.move(self.up_states)
            else:
                self.direction = 'left'
        if self.direction == 'down':
            if (self.rectangle.y < w_height-self.rectangle.height):
                self.rectangle.y += self.speed
                self.move(self.down_states)
            else:
                self.direction = 'right'

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def chase(self,playerRect):
        # increase detection range
        self.detection = self.rectangle.inflate(400,300)

        # using integer division to get the floor
        x = (playerRect.x - self.rectangle.x)//(playerSpeed+5)
        y = (playerRect.y - self.rectangle.y)//(playerSpeed+5)
        self.rectangle.x += x
        self.rectangle.y += y

        if y > 0:             # player below
            self.move(self.down_states)
        elif y < 0:             # player above
            self.move(self.up_states)
        elif x > 0:               # player to right
            self.move(self.right_states)
        elif x < 0:             # player to left
            self.move(self.left_states)
   

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

    def createRandomHeading(self):
        angle = random.randint(0,360)
        angle = angle * (3.14159/180)
        
        x = math.cos(angle)
        y = math.sin(angle)
        v = vector(x,y)
        return v