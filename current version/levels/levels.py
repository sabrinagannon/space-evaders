from constants import colors, w_width, w_height
import pygame, cutscenes, cutsceneText

class levels():

    def __init__(self,screen):
        self.screen = screen
        self.music = ["assets/music/keithDenial.mp3","assets/music/realKeithAnger.mp3","assets/music/keithDepression.mp3","assets/music/BargainingKeith.mp3","keithAcceptance.mp3"]
        self.font =  pygame.font.SysFont("monospace", 25)
        self.crystal = pygame.image.load("assets/sprites/items/crystal.png")
        self.heart = pygame.image.load("assets/sprites/items/HeartContainer.png")
        self.smallHeart = pygame.image.load("assets/sprites/items/HeartContainerSmall.png")
        self.sinkIcon = pygame.image.load('assets/sprites/items/timemachineIcon.png')

    def drawEnemies(self,enemies):
        for enemy in enemies:
            #if enemy.inflate:
                #pygame.draw.rect(self.screen,colors['blue'],enemy.detection,3)
            self.screen.blit(enemy.image, enemy.rectangle)

    def drawItems(self,crystalList,sink,bg):
        sink.draw(self.screen,bg.x,bg.y,bg.offset)

        for crystal in crystalList:
            crystal.rect.x = crystal.origX + (bg.x + bg.offset)
            crystal.rect.y = crystal.origY + (bg.y + bg.offset)
            #pygame.draw.rect(self.screen,colors['green'],crystal.rect,3)
            self.screen.blit(crystal.sheet, crystal.rect)

    def drawObstacles(self,obstacleList,bg):

        for obstacle in obstacleList:
            obstacle.rect.x = obstacle.origX + (bg.x + bg.offset)
            obstacle.rect.y = obstacle.origY + (bg.y + bg.offset)
            self.screen.blit(obstacle.sheet,obstacle.rect)

    def playLvlMusic(self,lvlNumber):
        pygame.mixer.music.load(self.music[lvlNumber-1]) # change to lvlNumber-1
        pygame.mixer.music.play(-1)

    def drawText(self,keith):

        #backgroundBar
        bgRect = pygame.Rect(0,0,1200,39)
        pygame.draw.rect(self.screen,colors['black'],bgRect)

        #crystals
        text = self.font.render(str(keith.itemsHeld), 1,colors['blue'])
        textpos = pygame.Rect(185,5,w_width/2,w_height/2)
        crystalDisplay = pygame.Rect(140,0,41,36)

        #sink
        

        self.screen.blit(text, textpos)
        pygame.draw.rect(self.screen,colors['blue'],crystalDisplay)
        self.screen.blit(self.crystal,crystalDisplay)
        self.screen.blit(text, textpos)

        for life in range(0,keith.lives):
            self.screen.blit(self.smallHeart,(5+(life*41),0,41,36))

    def playCutscene(self,level):
        cutsceneArray = "level" + str(level) + "_cutscene"
        cutscenes.playCutscene(self.screen, cutsceneText.text[cutsceneArray])
