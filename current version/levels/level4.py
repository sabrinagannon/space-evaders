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
        wolf2 = levelEnemy((enemyStartX, enemyStartY),wolfPath,7)
        bear2 = levelEnemy((enemyStartX, enemyStartY),bearPath,7)
        coolBear = levelBear((-350,-800),armBearPath,4,100,0)
        coolBear2 = levelBear((1290,-800),armBearPath,4,100,1)
        coolBear3 = levelBear((1290,700),armBearPath,4,100,2)
        coolBear4 = levelBear((-350,700),armBearPath,4,100,3)
        self.enemies = [wolf,bear,coolBear,coolBear2,coolBear3,coolBear4,wolf2,bear2]
        self.background = backgrounds.Background(4)

        self.timer = (30*60)*2  # 2 minutes at 30 fps
        self.timerMin = 2
        self.timerSec = 0

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        if self.timer%(30*60)== 0:
            self.timerMin -= 1

        if self.timer%30 == 0:
            self.timerSec -= 1
            if self.timerSec == -1 and self.timerMin != -1:
                self.timerSec = 59
            elif self.timerSec == -1:
                self.timerSec = 0

        self.timer -= 1
        
        if disabled == []:
            collision = False
        else:
            collision = False
            for pressed in disabled:
                if keys[pressed]:
                    collision = True
        
        index = 0
        for e in self.enemies:
            crystalList = e.update(keith,self.background,keys,collision,obstacles,crystalList)

            if(e.rectangle.colliderect(keith.rectangle) and keith.isInvincible == False):

                #self.soundFX.playBloop()
                # NEW SOUND EFFECT?
                e.caughtHim = 1
                keith.onEnemyCollision()

                # Now enemy drops a crystal, and dies
                if(e.crystals > 0) and (keith.coinsHeld > 0) and (not e.isBear()):
                    self.soundFX.playChime()
                    e.crystals -= 1
                    droppedCrystal = pygame.Rect((keith.rectangle.x - 1000 - self.background.x), (keith.rectangle.y -1000 - self.background.y), 41,36)
                    droppedItem = items.Crystal(droppedCrystal)
                    crystalList.append(droppedItem)
                    del self.enemies[index]
                    index -= 1
                    keith.coinsHeld -= 1
                else:
                    self.soundFX.playBloop()
                    keith.lives -= 1
            index += 1
            

    def draw(self,crystalList,sink,keith):
        self.screen.fill(colors['black'])
        self.background.draw(self.screen)
        self.drawItems(crystalList,sink,self.background)
        self.drawObstacles(self.obstacles,self.background)
        self.drawEnemies(self.enemies)
        self.screen.blit(keith.image, keith.rectangle)
        self.drawText(keith,sink)
        self.drawDisplay(crystalList,sink,self.background,4)
      

    def drawText(self,keith,sink):
        # background bar
        bgRect = pygame.Rect(0,0,1200,39)
        pygame.draw.rect(self.screen,colors['black'],bgRect)

        # crystals
        text = self.font.render(str(keith.itemsHeld), 1,colors['blue'])
        textpos = pygame.Rect(185,5,w_width/2,w_height/2)
        crystalDisplay = pygame.Rect(140,0,41,36)
        self.screen.blit(text, textpos)
        pygame.draw.rect(self.screen,colors['blue'],crystalDisplay)
        self.screen.blit(self.crystal,crystalDisplay)
        self.screen.blit(text, textpos)

        # timer
        timerText = self.font.render('Time Remaining: ' + str(self.timerMin)+':'+str(self.timerSec),True,colors['white'])
        
        if self.timerSec < 10:
            timerText = self.font.render('Time Remaining: ' + str(self.timerMin)+':0'+str(self.timerSec),True,colors['white'])

        timerPos = pygame.Rect(875,5,w_width/2,w_height/2)
        self.screen.blit(timerText, timerPos)
    
        #sink
        icon = pygame.Rect(220,0,41,36)
        amt = (36-(9*(sink.itemsHeld)))
        sinkpos = pygame.Rect(220,amt,41,(9*sink.itemsHeld))
        if sink.itemsHeld != 0:
            pygame.draw.rect(self.screen,colors['green'],sinkpos)
        self.screen.blit(self.sinkIcon,icon)

        for life in range(0,keith.lives):
            self.screen.blit(self.smallHeart,(5+(life*41),0,41,36))
        
      

class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def negateX(self):
        self.x *= -1

    def negateY(self):
        self.y *= -1


class levelEnemy(enemy.Enemy):
    def isBear(self):
        return False
    
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
    def isBear(self):
        return True

    def update(self,keith,bg,keys,collision,obstacles,crystals):
        keith.updateInvincible()
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
        # if self.detection.colliderect(keith.rectangle):
        #     if not self.inInterval:
        #         update = True
        #     else:
        #         update = False
        #     self.runAway(bg,keith.rectangle,update)
            
        
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
