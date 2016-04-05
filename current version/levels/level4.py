import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,armBearPath,colors
import enemy, items, backgrounds,sounds
import random, pygame, math, json

class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()

        
        with open('assets/images/levelFour/level4obstacles.json','rb') as obstacles:
            self.obstacleCoords = json.load(obstacles)

        self.obstacles = items.createObstacles(self.obstacleCoords)

        enemyStartX, enemyStartY = random.randrange(w_width),random.randrange(w_height) # give enemies random start points
        wolf = levelEnemy((enemyStartX, enemyStartY),wolfPath,7)
        bear = levelEnemy((enemyStartX, enemyStartY),bearPath,7)
        coolBear = levelBear((0,0),armBearPath,3)
        self.enemies = [wolf,bear,coolBear]
        self.background = backgrounds.Background(4)

        self.timer = (30*60)*2  # 2 minutes at 30 fps
        self.timerMin = 1
        self.timerSec = 60

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        if self.timer%(30*60)== 0:
            self.timerMin -= 1

        if self.timer%30 == 0:
            self.timerSec -= 1
            if self.timerSec == -1 and self.timerMin != 0:
                self.timerSec = 59

        self.timer -= 1
        
        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]

        index = 0
        for e in self.enemies:
            crystalList = e.update(keith,self.background,keys,collision,obstacles,crystalList)

            if(e.rectangle.colliderect(keith.rectangle)):

                #self.soundFX.playBloop()
                # NEW SOUND EFFECT!
                e.caughtHim = 1
                keith.onEnemyCollision()

                # Now enemy drops a crystal, and is stunned
                if(e.crystals > 0) and (keith.coinsHeld > 0):
                    e.crystals -= 1
                    droppedCrystal = pygame.Rect((keith.rectangle.x - 1000 - self.background.x), (keith.rectangle.y -1000 - self.background.y), 41,36)
                    droppedItem = items.Crystal(droppedCrystal)
                    crystalList.append(droppedItem)
                    del self.enemies[index]
                    index -= 1
                else:
                    keith.lives -= 1
            index += 1
            

    def draw(self,crystalList,sink,keith):
        self.screen.fill(colors['black'])
        self.background.draw(self.screen)
        self.drawItems(crystalList,sink,self.background)
        self.drawEnemies(self.enemies)
        self.drawObstacles(self.obstacles,self.background)
        self.screen.blit(keith.image, keith.rectangle)
        self.drawText(keith)

    def drawText(self,keith):
        text = self.font.render('You are carrying '+str(keith.itemsHeld)+' crystals', 1,colors['blue'])
        textpos = pygame.Rect(10,10,w_width/2,w_height/2)

        if self.timerSec == 0:
            timerText = self.font.render('Time Remaining: ' + str(self.timerMin)+':00',True,colors['black'])
        else:
            timerText = self.font.render('Time Remaining: ' + str(self.timerMin)+':'+str(self.timerSec),True,colors['black'])
        self.font =  pygame.font.SysFont("monospace", 56)
        timerPos = pygame.Rect(1000,10,w_width/2,w_height/2)
        self.screen.blit(text, textpos)
        self.screen.blit(timerText, timerPos)
        self.font =  pygame.font.SysFont("monospace", 15)

class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def negateX(self):
        self.x *= -1

    def negateY(self):
        self.y *= -1


class levelEnemy(enemy.Enemy):
    
    def update(self,keith,bg,keys,collision,obstacles,crystals):
        if not collision:
            if keys[pygame.K_a]:
                self.rectangle.x += keith.speed
            if keys[pygame.K_d]:
                self.rectangle.x -= keith.speed
            if keys[pygame.K_w]:
                self.rectangle.y += keith.speed
            if keys[pygame.K_s]:
                self.rectangle.y -= keith.speed

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

    def update(self,keith,bg,keys,collision,obstacles,crystals):
        if not collision:
            if keys[pygame.K_a]:
                self.rectangle.x += keith.speed
            if keys[pygame.K_d]:
                self.rectangle.x -= keith.speed
            if keys[pygame.K_w]:
                self.rectangle.y += keith.speed
            if keys[pygame.K_s]:
                self.rectangle.y -= keith.speed

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

    def patrol(self,bg,obstacles,ghost=False):
        
        if self.direction == 'left':
            if (self.rectangle.x - bg.x > self.speed):
                self.rectangle.x -= self.speed
                self.move(self.left_states)
            else:
                self.direction = 'down'

        if self.direction == 'right':
            if (self.rectangle.x - bg.x < w_width - self.rectangle.width):
                self.rectangle.x += self.speed
                self.move(self.right_states)
            else:
                self.direction = 'up'

        if self.direction == 'up':
            if (self.rectangle.y - bg.y > self.speed):
                self.rectangle.y -= self.speed
                self.move(self.up_states)
            else:
                self.direction = 'left'
        if self.direction == 'down':
            if (self.rectangle.y -bg.y< w_height-self.rectangle.height):
                self.rectangle.y += self.speed
                self.move(self.down_states)
            else:
                self.direction = 'right'

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        # Have to check for collisions here
        # nextXPos = self.rectangle.x + (self.speed*self.heading.x)
        # nextYPos = self.rectangle.y + (self.speed*self.heading.y)

        # fnxt = math.floor(nextXPos)
        # fnyt = math.floor(nextYPos)
        
        # if not ghost:
        #     for obstacle in obstacles:
        #         x = obstacle.rect.x
        #         y = obstacle.rect.y
        #         width = obstacle.rect.width
        #         height = obstacle.rect.height
        #         if (nextXPos > x-self.rectangle.width-6) and (nextXPos < x +width+6) and (nextYPos > y-self.rectangle.height-6) and (nextYPos < y+height+6):

        #             if fnxt in range(x-self.rectangle.width-5,x-self.rectangle.width+5):
        #                 # send back east
        #                 newHeading = vector((-1*self.heading.x),self.heading.y)
        #                 self.heading = newHeading
        #                 nextXPos = x-self.rectangle.width
        #             elif fnxt in range(x + width-5,x+width+5):
        #                 # send back west
        #                 newHeading = vector((-1*self.heading.x),self.heading.y)
        #                 self.heading = newHeading
        #                 nextXPos = x+width
        #             elif fnyt in range(y-self.rectangle.height-5,y-self.rectangle.height+5):
        #                 # send back north
        #                 newHeading = vector(self.heading.x,(-1*self.heading.y))
        #                 self.heading = newHeading
        #                 nextYPos = y-self.rectangle.height
        #             elif fnyt in range(y+height-5,y+height+5):
        #                 # send back south
        #                 newHeading = vector(self.heading.x,(-1*self.heading.y))
        #                 self.heading = newHeading
        #                 nextYPos = y+height

        # if nextXPos - bg.x > (bg.resolution[0]-self.rectangle.width):
        #     newHeading = vector((-1*self.heading.x),self.heading.y)
        #     self.heading = newHeading
        #     nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        # if nextXPos - bg.x <= 0:
        #     newHeading = vector((-1*self.heading.x),self.heading.y)
        #     self.heading = newHeading
        #     nextXPos = bg.x
        # if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
        #     newHeading = vector(self.heading.x,(-1*self.heading.y))
        #     self.heading = newHeading
        #     nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        # if nextYPos -bg.y <= 0:
        #     newHeading = vector(self.heading.x,(-1*self.heading.y))
        #     self.heading = newHeading
        #     nextYPos = bg.y

        #  if nextXPos - bg.x > 1200 and nextYPos - bg.y > 
        #     newHeading = vector((-1*self.heading.x),self.heading.y)
        #     self.heading = newHeading
        #     nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        # if nextXPos - bg.x <= 0:
        #     newHeading = vector((-1*self.heading.x),self.heading.y)
        #     self.heading = newHeading
        #     nextXPos = bg.x
        # if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
        #     newHeading = vector(self.heading.x,(-1*self.heading.y))
        #     self.heading = newHeading
        #     nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        # if nextYPos -bg.y <= 0:
        #     newHeading = vector(self.heading.x,(-1*self.heading.y))
        #     self.heading = newHeading
        #     nextYPos = bg.y

        # self.rectangle.x = nextXPos
        # self.rectangle.y = nextYPos

        # if nextYPos > nextXPos: # animate vertical
        #     if self.heading.y > 0:        # moving down
        #         self.move(self.down_states)
        #     else:
        #         self.move(self.up_states)
        # else:                   # animate hroizontal
        #     if self.heading.x > 0:        # moving right
        #         self.move(self.right_states)
        #     else:
        #         self.move(self.left_states)

        # self.image = self.sheet.subsurface(self.sheet.get_clip())
