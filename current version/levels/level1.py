import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors
import enemy, items, backgrounds, sounds
import random, pygame

class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()
        self.obstacleCoords = {'obst1': {'x':10 ,'y':500 , 'width':376 , 'height':296, 'path':'assets/images/suck.png' },'obst2':{'x':1500,'y':-200 , 'width':376, 'height':296, 'path':'assets/images/suck.png'}}
        self.obstacles = items.createObstacles(self.obstacleCoords)
        # where the enemies will start on this level
        enemyStartX, enemyStartY = random.randrange(w_width),random.randrange(w_height) # give enemies random start points
        wolf = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,7)
        bear = enemy.Enemy((enemyStartX, enemyStartY),bearPath,9)
        wolf2 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,10)
        bear2 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,11)
        wolf3 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,3)
        bear3 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,12)

        self.enemies = [wolf,bear,wolf2,bear2,bear3,wolf3]
        self.background = backgrounds.Background(1)

    def updateEnemies(self,keith,keys,crystalList):
        for e in self.enemies:
            e.update(keith,self.background,keys)

            if(e.rectangle.colliderect(keith.rectangle)):

                self.soundFX.playBloop()
                e.caughtHim = 1

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
        self.drawEnemies(self.enemies)
        self.drawText(keith)
        self.drawObstacles(self.obstacles,self.background)
        self.screen.blit(keith.image, keith.rectangle)
