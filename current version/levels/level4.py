import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors
import enemy, items, backgrounds,sounds
import random, pygame, math

class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()
        self.obstacleCoords = {}
        self.obstacles = items.createObstacles(self.obstacleCoords)

        enemyStartX, enemyStartY = random.randrange(w_width),random.randrange(w_height) # give enemies random start points
        wolf = levelEnemy((enemyStartX, enemyStartY),wolfPath,7)
        bear = levelEnemy((enemyStartX, enemyStartY),bearPath,7)
        self.enemies = [wolf,bear]
        self.background = backgrounds.Background(4)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]

        for e in self.enemies:
            crystalList = e.update(keith,self.background,keys,collision,obstacles,crystalList)

            if(e.rectangle.colliderect(keith.rectangle)):

                #self.soundFX.playBloop()
                # NEW SOUND EFFECT!
                e.caughtHim = 1

                # Now enemy drops a crystal, and is stunned
                if(e.crystals > 0):
                    e.crystals -= 1
                    droppedCrystal = pygame.Rect((keith.rectangle.x - 1000 - self.background.x), (keith.rectangle.y -1000 - self.background.y), 41,36)
                    droppedItem = items.Crystal(droppedCrystal)
                    crystalList.append(droppedItem)
                                                 

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

        # If you bump a crystal pick it up
        for crystal in crystals:
            if self.detection.colliderect(crystal.rect):
                del crystals[index]
                self.crystals += 1
            index += 1

        # Invert behaviour, run away!
        if self.detection.colliderect(keith.rectangle):
            self.runAway(bg,keith.rectangle)
        else:
            self.patrol(bg,obstacles)
            self.caughtHim = 0
            self.detection = self.rectangle.inflate(self.inflate,self.inflate)
        return crystals

    def runAway(self,bg,playerRect,ghost=False):

        # increase detection range
        if not ghost:
            self.detection = self.rectangle.inflate(400,300)

        x = (playerRect.x - self.rectangle.x)
        y = (playerRect.y - self.rectangle.y)
        
        length = math.sqrt((x*x)+(y*y))

        headingX = float(x/length)*-1
        headingY = float(y/length)*-1

        newHeading = vector(headingX,headingY)

        nextXPos = self.rectangle.x + (self.speed*headingX)
        nextYPos = self.rectangle.y + (self.speed*headingY)
        
        if nextXPos - bg.x > (bg.resolution[0]-self.rectangle.width):
            newHeading = vector((-1*headingX),headingY)
            #self.heading = newHeading
            nextXPos = (bg.resolution[0]-self.rectangle.width)+bg.x
        if nextXPos - bg.x <= 0:
            newHeading = vector((-1*headingX),headingY)
            #self.heading = newHeading
            nextXPos = bg.x
        if nextYPos - bg.y > (bg.resolution[1]-self.rectangle.height):
            newHeading = vector(headingX,(-1*headingY))
            #self.heading = newHeading
            nextYPos = (bg.resolution[1]-self.rectangle.width)+bg.y
        if nextYPos -bg.y <= 0:
            newHeading = vector(headingX,(-1*headingY))
            #self.heading = newHeading
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
    