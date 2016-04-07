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
    def __init__(self,startingPos,imagePath,speed = 10, inflate = 100,bearDex = 0):
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

        # This is hacky but it's to stop the carnage
        self.caughtHim = 0

        # for level 2
        self.rampage = 0
        self.stepCounter = 50
        self.headingX = 0
        self.headingY = 0 

        # for level 3
        self.chasing = False

        # for level4
        self.crystals = 2
        self.inInterval = 0
        self.bearID = bearDex
        self.bearLims = {0:{'left':150,'right':750,'up':150,'down':650},1:{'left':1700,'right':2300,'up':150,'down':650},2:{'left':1700,'right':2300,'up':1700,'down':2250},3:{'left':150,'right':750,'up':1700,'down':2250}}
      
        
        self.heading = self.createRandomHeading()
        self.direction = 'left'
        self.inflate = inflate
        self.detection = self.rectangle.inflate(self.inflate,self.inflate)

    def update(self,keith,bg,keys,collision,obstacles):
        if not collision:
            if keys[pygame.K_a]:
                self.rectangle.x += keith.speed
            if keys[pygame.K_d]:
                self.rectangle.x -= keith.speed
            if keys[pygame.K_w]:
                self.rectangle.y += keith.speed
            if keys[pygame.K_s]:
                self.rectangle.y -= keith.speed

        if self.detection.colliderect(keith.rectangle):
            self.chase(keith.rectangle)
        else:
            self.patrol(bg,obstacles)
            self.caughtHim = 0
            self.detection = self.rectangle.inflate(self.inflate,self.inflate)

    def patrol(self,bg,obstacles,ghost=False):
        # Have to check for collisions here
        nextXPos = self.rectangle.x + (self.speed*self.heading.x)
        nextYPos = self.rectangle.y + (self.speed*self.heading.y)

        fnxt = math.floor(nextXPos)
        fnyt = math.floor(nextYPos)
        
        if not ghost:
            for obstacle in obstacles:
                x = obstacle.rect.x
                y = obstacle.rect.y
                width = obstacle.rect.width
                height = obstacle.rect.height
                if (nextXPos > x-self.rectangle.width-6) and (nextXPos < x +width+6) and (nextYPos > y-self.rectangle.height-6) and (nextYPos < y+height+6):

                    if fnxt in range(x-self.rectangle.width-5,x-self.rectangle.width+5):
                        # send back east
                        newHeading = vector((-1*self.heading.x),self.heading.y)
                        self.heading = newHeading
                        nextXPos = x-self.rectangle.width
                    elif fnxt in range(x + width-5,x+width+5):
                        # send back west
                        newHeading = vector((-1*self.heading.x),self.heading.y)
                        self.heading = newHeading
                        nextXPos = x+width
                    elif fnyt in range(y-self.rectangle.height-5,y-self.rectangle.height+5):
                        # send back north
                        newHeading = vector(self.heading.x,(-1*self.heading.y))
                        self.heading = newHeading
                        nextYPos = y-self.rectangle.height
                    elif fnyt in range(y+height-5,y+height+5):
                        # send back south
                        newHeading = vector(self.heading.x,(-1*self.heading.y))
                        self.heading = newHeading
                        nextYPos = y+height

        if nextXPos - bg.x > (bg.resolution[0]-self.rectangle.width):
            newHeading = vector((-1*self.heading.x),self.heading.y)
            self.heading = newHeading
            nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        if nextXPos - bg.x <= 0:
            newHeading = vector((-1*self.heading.x),self.heading.y)
            self.heading = newHeading
            nextXPos = bg.x
        if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
            newHeading = vector(self.heading.x,(-1*self.heading.y))
            self.heading = newHeading
            nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        if nextYPos -bg.y <= 0:
            newHeading = vector(self.heading.x,(-1*self.heading.y))
            self.heading = newHeading
            nextYPos = bg.y

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


    def chase(self,playerRect,ghost=False):

        if self.caughtHim == 1:
            self.detection = self.rectangle.inflate(400,300)
            return

        # increase detection range
        if not ghost:
            self.detection = self.rectangle.inflate(400,300)

        x = (playerRect.x - self.rectangle.x)
        y = (playerRect.y - self.rectangle.y)
        
        length = math.sqrt((x*x)+(y*y))

        if length == 0:
            length = 1

        headingX = float(x/length)
        headingY = float(y/length)

        nextXPos = self.rectangle.x + (self.speed*headingX)
        nextYPos = self.rectangle.y + (self.speed*headingY)

        self.rectangle.x = nextXPos
        self.rectangle.y = nextYPos

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
            # regular case, where we call self.move with our dictionary of coordinates
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

 
    def createRandomHeading(self):
        angle = random.randint(0,360)
        angle = angle * (3.14159/180)

        x = math.cos(angle)
        y = math.sin(angle)
        v = vector(x,y)
        return v
