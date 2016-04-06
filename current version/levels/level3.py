import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors, blobPath
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

        with open('assets/images/levelThree/level3obstacles.json','rb') as obstacles:
            self.obstacleCoords = json.load(obstacles)

        self.obstacles = items.createObstacles(self.obstacleCoords)

        # top left
        blob1 = levelEnemy((-100,-100),blobPath,3,0)
        # top right
        blob2 = levelEnemy((1100,-100),blobPath,3,0)
        # bottom left
        blob3 = levelEnemy((-100,1100),blobPath,3,0)
        # bottom right
        blob4 = levelEnemy((1100,1100),blobPath,3,0)
          # top left
        blob5 = levelEnemy((-500,-600),blobPath,3,0)
        # top right
        blob6 = levelEnemy((600,2000),blobPath,3,0)
        # bottom left
        blob7 = levelEnemy((-400,1000),blobPath,3,0)
        # bottom right
        blob8 = levelEnemy((400,400),blobPath,3,0)

        self.enemies = [blob1,blob2,blob3,blob4,blob5,blob6,blob7,blob8]
        self.background = backgrounds.Background(3)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]

        chasers = keith.itemsHeld//2
        
        for e in self.enemies:
            if chasers > 0:
                e.update(keith,self.background,keys,collision,obstacles,True)
                chasers -= 1
            else:
                e.update(keith,self.background,keys,collision,obstacles,False)

            if(e.rectangle.colliderect(keith.rectangle)):

                self.soundFX.playBloop()

                if(keith.itemsHeld > 0):
                    keith.itemsHeld -= 1
                    keith.onEnemyCollision()
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
        self.drawObstacles(self.obstacles,self.background)
        self.drawEnemies(self.enemies)
        self.screen.blit(keith.image, keith.rectangle)
        self.drawText(keith)

class vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def negateX(self):
        self.x *= -1

    def negateY(self):
        self.y *= -1


class levelEnemy(enemy.Enemy):

    
    def update(self,keith,bg,keys,collision,obstacles,chaser):
        # Houskeeping
        if not collision:
            if keys[pygame.K_a]:
                self.rectangle.x += keith.speed
            if keys[pygame.K_d]:
                self.rectangle.x -= keith.speed
            if keys[pygame.K_w]:
                self.rectangle.y += keith.speed
            if keys[pygame.K_s]:
                self.rectangle.y -= keith.speed

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
