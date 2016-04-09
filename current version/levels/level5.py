import pygame, sys, random, math, json
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath, colors, blobPath, armBearPath
import enemy, items, backgrounds,sounds


class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()
        self.obstacleCoords = {}
        #with open('assets/images/levelFive/levelfiveobstacles.json','rb') as obstacles:
            #self.obstacleCoords = json.load(obstacles)
        self.obstacleCoords['tm']= {"x": 500, "y": 300, "height": 150, "width": 150, "path": 'DNR'}

        self.obstacles = items.createObstacles(self.obstacleCoords)
        self.sink = items.getSink(self.obstacles)
        

        enemyStartX, enemyStartY = random.randrange(300),random.randrange(600) # give enemies random start points
        wolf = level1Enemy((enemyStartX, enemyStartY),wolfPath,10)
        bear = level2Enemy((enemyStartX, enemyStartY),bearPath,9)
        blob = level3Enemy((enemyStartX, enemyStartY),blobPath,3,0)
        bear2 = level4Enemy((enemyStartX, enemyStartY),bearPath,7)
        coolBear = levelBear((enemyStartX,enemyStartY),armBearPath,4,100,0)

        self.enemies = [wolf, bear, blob, bear2, coolBear]
        self.background = backgrounds.Background(5)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        chasers = keith.itemsHeld//2
        if disabled == None:
            collision = False
        else:
            collision = False
            for pressed in disabled:
                if keys[pressed]:
                    collision = True

        for e in self.enemies:

            if e.rectangle.colliderect(self.sink.rect):
                e.reverseHeading(self.sink)
            
            if chasers > 0:
                e.update(keith,self.background,keys,collision,obstacles,True,crystalList)
                chasers -= 1
            else:
                e.update(keith,self.background,keys,collision,obstacles,False,crystalList)

            if(e.rectangle.colliderect(keith.rectangle) and keith.isInvincible == False):

                self.soundFX.playBloop()
                e.caughtHim = 1
                keith.onEnemyCollision()

                if(keith.itemsHeld > 0):
                    keith.itemsHeld -= 1
                    keith.updateSpeed()
                    droppedBox = pygame.Rect((keith.rectangle.x - 1000 - self.background.x), (keith.rectangle.y -1000 - self.background.y), 41,36)
                    droppedItem = items.Crystal(droppedBox)
                    crystalList.append(droppedItem)
                else:
                    keith.lives -= 1

    def draw(self,crystalList,sink,keith):
        self.screen.fill(colors['black'])
        self.background.draw(self.screen)
        self.drawItems(crystalList,sink,self.background)
        self.drawEnemies(self.enemies)
        self.drawText(keith,sink)
        self.drawObstacles(self.obstacles,self.background)
        self.screen.blit(keith.image, keith.rectangle)
class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def negateX(self):
        self.x *= -1

    def negateY(self):
        self.y *= -1

class level1Enemy(enemy.Enemy):

    def update(self,keith,bg,keys,collision,obstacles,chaser,crystalList):

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

class level2Enemy(enemy.Enemy):

    def update(self,keith,bg,keys,collision,obstacles,chaser,crystalList):


        if self.detection.colliderect(keith.rectangle):
            self.chase(keith.rectangle)
        else:
            self.patrol(bg,obstacles)
            self.caughtHim = 0
            self.detection = self.rectangle.inflate(200,200)


    def chase(self,playerRect):

        if self.caughtHim == 1:
            self.rampage = 0
            self.detection = self.rectangle.inflate(400,300)
            return

        if self.rampage == 0:
        # increase detection range
            self.detection = self.rectangle.inflate(400,300)

            x = (playerRect.x - self.rectangle.x)
            y = (playerRect.y - self.rectangle.y)

            length = math.sqrt((x*x)+(y*y))
            try:
                self.headingX = float(x/length)
            except ZeroDivisionError:
                self.headingX = float(x/(length+1))
            try:
                self.headingY = float(y/length)
            except ZeroDivisionError:
                self.headingY = float(y/(length + 1))

            self.rampage = 1

        else:
            self.detection = self.rectangle.inflate(400,300)
            x = (playerRect.x - self.rectangle.x)
            y = (playerRect.y - self.rectangle.y)
            rampageSpeed = self.speed*1.7
            self.stepCounter-=1
            nextXPos = self.rectangle.x + (rampageSpeed*self.headingX)
            nextYPos = self.rectangle.y + (rampageSpeed*self.headingY)

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

        if self.stepCounter <= 0:

            self.rampage = 0
            self.stepCounter = 50
            return

        self.image = self.sheet.subsurface(self.sheet.get_clip())

class level3Enemy(enemy.Enemy):
    def update(self,keith,bg,keys,collision,obstacles,chaser,crystalList):

        if (bg.previousPos == (bg.x,bg.y)) and (not chaser):
            # not moving, so move away
            if self.chasing:
                playerRect = keith.rectangle
                x = (playerRect.x - self.rectangle.x)
                y = (playerRect.y - self.rectangle.y)

                length = math.sqrt((x*x)+(y*y))

                headingX = float(x/length)
                headingY = float(y/length)

                newHeading = vector(-1*headingX,-1*headingY)
                self.heading = newHeading
                self.chasing = False
            self.patrol(bg,obstacles,ghost=True)
        else:
            # move towards player
            self.chase(keith.rectangle)
            if not self.chasing:
                self.chasing = True
class level4Enemy(enemy.Enemy):
    def isBear(self):
        return False

    def update(self,keith,bg,keys,collision,obstacles,chaser,crystals):

        index = 0

        # Invert behaviour, run away!
        if self.detection.colliderect(keith.rectangle):
            if not self.inInterval:
                update = True
            else:
                update = False
            self.runAway(bg,keith.rectangle,update)
        else:
            self.patrol(bg,obstacles)
            self.caughtHim = 0
            self.detection = self.rectangle.inflate(self.inflate,self.inflate)
        return crystals

    def runAway(self,bg,playerRect,update,ghost=False,):


        # increase detection range
        if not ghost:
            self.detection = self.rectangle.inflate(400,300)

        if update:
            self.inInterval = 5
            x = (playerRect.x - self.rectangle.x)
            y = (playerRect.y - self.rectangle.y)

            length = math.sqrt((x*x)+(y*y))

            headingX = float(x/length)*-1
            headingY = float(y/length)*-1

            newHeading = vector(headingX,headingY)
        else:
            self.inInterval -= 1
            x = self.rectangle.x
            y = self.rectangle.y
            newHeading = self.heading
            headingX = self.heading.x
            headingY = self.heading.y

        nextXPos = self.rectangle.x + (self.speed*headingX)
        nextYPos = self.rectangle.y + (self.speed*headingY)

        if nextXPos - bg.x > (bg.resolution[0]-self.rectangle.width):
            newHeading = vector((-1*headingX),headingY)
            nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        if nextXPos - bg.x <= 0:
            newHeading = vector((-1*headingX),headingY)
            nextXPos = bg.x
        if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
            newHeading = vector(headingX,(-1*headingY))
            nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        if nextYPos -bg.y <= 0:
            newHeading = vector(headingX,(-1*headingY))
            nextYPos = bg.y

        self.rectangle.x = nextXPos
        self.rectangle.y = nextYPos
        self.heading = newHeading

        if y > 0:             # player below
            self.move(self.down_states)
        elif y < 0:             # player above
            self.move(self.up_states)
        elif x > 0:               # player to right
            self.move(self.right_states)
        elif x < 0:             # player to left
            self.move(self.left_states)

        self.image = self.sheet.subsurface(self.sheet.get_clip())



class levelBear(enemy.Enemy):
    def isBear(self):
        return True

    def update(self,keith,bg,keys,collision,obstacles,chaser,crystals):
        keith.updateInvincible()

        index = 0

        self.patrol(bg,obstacles)
            # self.caughtHim = 0
            # self.detection = self.rectangle.inflate(self.inflate,self.inflate)
        return crystals

    def runAway(self,bg,playerRect,update,ghost=False,):
        # increase detection range
        if not ghost:
            self.detection = self.rectangle.inflate(400,300)

        if update:
            self.inInterval = 5
            x = (playerRect.x - self.rectangle.x)
            y = (playerRect.y - self.rectangle.y)

            length = math.sqrt((x*x)+(y*y))

            headingX = float(x/length)*-1
            headingY = float(y/length)*-1

            newHeading = vector(headingX,headingY)
        else:
            self.inInterval -= 1
            x = self.rectangle.x
            y = self.rectangle.y
            newHeading = self.heading
            headingX = self.heading.x
            headingY = self.heading.y

        nextXPos = self.rectangle.x + (self.speed*headingX)
        nextYPos = self.rectangle.y + (self.speed*headingY)

        if nextXPos - bg.x > (bg.resolution[0]-self.rectangle.width):
            newHeading = vector((-1*headingX),headingY)
            nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        if nextXPos - bg.x <= 0:
            newHeading = vector((-1*headingX),headingY)
            nextXPos = bg.x
        if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
            newHeading = vector(headingX,(-1*headingY))
            nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        if nextYPos -bg.y <= 0:
            newHeading = vector(headingX,(-1*headingY))
            nextYPos = bg.y

        self.rectangle.x = nextXPos
        self.rectangle.y = nextYPos
        self.heading = newHeading

        if y > 0:             # player below
            self.move(self.down_states)
        elif y < 0:             # player above
            self.move(self.up_states)
        elif x > 0:               # player to right
            self.move(self.right_states)
        elif x < 0:             # player to left
            self.move(self.left_states)

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def patrol(self,bg,obstacles,ghost=False):

        if self.direction == 'left':
            if (self.rectangle.x - bg.x > self.bearLims.get(self.bearID)['left']):
                self.rectangle.x -= self.speed
                self.move(self.left_states)
            else:
                self.direction = 'down'

        if self.direction == 'right':
            if (self.rectangle.x - bg.x <  self.bearLims.get(self.bearID)['right']):
                self.rectangle.x += self.speed
                self.move(self.right_states)
            else:
                self.direction = 'up'

        if self.direction == 'up':
            if (self.rectangle.y - bg.y >  self.bearLims.get(self.bearID)['up']):
                self.rectangle.y -= self.speed
                self.move(self.up_states)
            else:
                self.direction = 'left'
        if self.direction == 'down':
            if (self.rectangle.y-bg.y< self.bearLims.get(self.bearID)['down']):
                self.rectangle.y += self.speed
                self.move(self.down_states)
            else:
                self.direction = 'right'

        self.image = self.sheet.subsurface(self.sheet.get_clip())
