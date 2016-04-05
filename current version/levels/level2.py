import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors
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
 
        with open('assets/images/levelTwo/level2obstacles.json','rb') as obstacles:
            self.obstacleCoords = json.load(obstacles)

        # self.obstacleCoords = {'obst1': {'x':100 ,'y':500 , 'width':376 , 'height':296, 'path':'assets/images/suck.png' },'obst2':{'x':1500,'y':-200 , 'width':376, 'height':296, 'path':'assets/images/suck.png'}}
        self.obstacles = items.createObstacles(self.obstacleCoords)
        
        enemyStartX, enemyStartY = random.randrange(w_width),random.randrange(w_height) # give enemies random start points
        wolf = levelEnemy((enemyStartX, enemyStartY),wolfPath,10)
        wolf1 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,7)
        bear = enemy.Enemy((enemyStartX, enemyStartY),bearPath,9)
        wolf2 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,10)
        bear2 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,11)
        wolf3 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,3)
        bear3 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,12)
        
        self.enemies = [wolf,wolf1,bear,wolf2,wolf3,bear,bear2,bear3]
        self.background = backgrounds.Background(2)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]
        for e in self.enemies:
            e.update(keith,self.background,keys,collision,obstacles)

            if(e.rectangle.colliderect(keith.rectangle)):

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
        self.drawText(keith)
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

class levelEnemy(enemy.Enemy):

    def update(self,keith,bg,keys,collision,obstacles):
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

            self.headingX = float(x/length)
            self.headingY = float(y/length)

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

