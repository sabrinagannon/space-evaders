import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors, blobPath
import enemy, items, backgrounds,sounds
import random, pygame

class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()
        self.obstacleCoords = {'obst1': {'x':100 ,'y':500 , 'width':376 , 'height':296, 'path':'assets/images/suck.png' },'obst2':{'x':1500,'y':-200 , 'width':376, 'height':296, 'path':'assets/images/suck.png'}}
        self.obstacles = items.createObstacles(self.obstacleCoords)

        # top left
        blob1 = enemy.Enemy((-1000,-1000),blobPath,3,0)
        # top right
        blob2 = enemy.Enemy((2000,-1000),blobPath,3,0)
        # bottom left
        blob3 = enemy.Enemy((-1000,2000),blobPath,3,0)
        # bottom right
        blob4 = enemy.Enemy((2000,2000),blobPath,3,0)

        self.enemies = [blob1,blob2,blob3,blob4]
        self.background = backgrounds.Background(3)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):

        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]

        chasers = keith.itemsHeld//2
        
        for e in self.enemies:
            if chasers > 0:
                e.update3(keith,self.background,keys,collision,obstacles,True)
                chasers -= 1
            else:
                e.update3(keith,self.background,keys,collision,obstacles,False)

            if(e.rectangle.colliderect(keith.rectangle)):

                self.soundFX.playBloop()

                if(keith.itemsHeld > 0):
                    keith.itemsHeld -= 1
                    keith.updateSpeed()
                    droppedBox = pygame.Rect((keith.rectangle.x - 1000 - self.background.x), (keith.rectangle.y -1000 - self.background.y), 41,36)
                    droppedItem = items.Crystal(droppedBox)
                    crystalList.append(droppedItem)

    def draw(self,crystalList,sink,keith):
        self.screen.fill(colors['black'])
        self.background.draw(self.screen)
        self.drawItems(crystalList,sink,self.background)
        self.drawObstacles(self.obstacles,self.background)
        self.drawEnemies(self.enemies)
        self.drawText(keith)
        self.screen.blit(keith.image, keith.rectangle)
