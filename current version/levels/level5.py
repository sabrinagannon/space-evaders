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
        self.obstacleCoords = {}
        self.obstacles = items.createObstacles(self.obstacleCoords)

        enemyStartX, enemyStartY = random.randrange(300),random.randrange(600) # give enemies random start points
        wolf = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,10)
        bear = enemy.Enemy((enemyStartX, enemyStartY),bearPath,9)
        blob = enemy.Enemy((enemyStartX, enemyStartY),blobPath,3,0)

        self.enemies = [wolf, bear, blob]
        self.background = backgrounds.Background(5)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        chasers = keith.itemsHeld//2
        if disabled == None:
            collision = False
        else:
            collision = keys[disabled]
        #self.enemies[0].update(keith,self.background,keys,collision,obstacles)
        #self.enemies[1].update2(keith,self.background,keys,collision,obstacles)
        #if chasers > 0:
            #self.enemies[2].update3(keith,self.background,keys,collision,obstacles,True)
            #chasers -= 1
        #else:
            #self.enemies[2].update3(keith,self.background,keys,collision,obstacles,False)

        for e in self.enemies:
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
