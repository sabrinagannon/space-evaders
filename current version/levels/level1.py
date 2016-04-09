import sys
sys.path.insert(0,'../')
from levels import levels
from constants import w_width, w_height, wolfPath, bearPath,colors
import enemy, items, backgrounds, sounds
import random, pygame, json

class level(levels):

    def __init__(self, screen):
        levels.__init__(self,screen)
        self.screen = screen
        # where the player will start on this level
        self.startingPosX = 600
        self.startingPosY = 350
        self.soundFX = sounds.SoundFX()
        with open('assets/images/levelOne/level1obstacles.json','rb') as obstacles:
            self.obstacleCoords = json.load(obstacles)
        self.obstacleCoords['tm']= {"x": 500, "y": 300, "height": 150, "width": 150, "path": 'DNR'}

        self.obstacles = items.createObstacles(self.obstacleCoords)
        self.sink = items.getSink(self.obstacles)
        # where the enemies will start on this level
        enemyStartX, enemyStartY = enemy.createPoints()

        wolf = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,7)
        bear = enemy.Enemy((enemyStartX, enemyStartY),bearPath,9)
        wolf2 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,10)
        bear2 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,11)
        wolf3 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,3)
        bear3 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,12)

        self.enemies = [wolf,bear,wolf2,bear2,bear3,wolf3]
        self.background = backgrounds.Background(1)

    def updateEnemies(self,keith,keys,crystalList,disabled,obstacles):
        keith.updateInvincible()
        if disabled == []:
            collision = False
        else:
            collision = False
            for pressed in disabled:
                if keys[pressed]:
                    collision = True

        for e in self.enemies:

            if e.rectangle.colliderect(self.sink.rect):
                e.reverseHeading(self.sink)
                bumped = True
            else:
                bumped = False

            e.update(keith,self.background,keys,collision,obstacles,bumped)
        
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
        self.drawEnemies(self.enemies)
        self.drawObstacles(self.obstacles,self.background)
        self.drawItems(crystalList,sink,self.background)
        self.drawText(keith,sink)
        self.drawDisplay(crystalList,sink,self.background)
        self.screen.blit(keith.image, keith.rectangle)
