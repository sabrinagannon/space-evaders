import random, pygame
from constants import itemPath

from constants import w_width,w_height,colors

class Sink():
    def __init__(self,size,font,capacity):
        self.dims = size
        self.xpos = (w_width/2)-100
        self.ypos = (w_height/2)-50
        self.itemsHeld = 0
        self.capacity = capacity
        self.font = font
        self.rect = pygame.Rect(self.xpos,self.ypos,self.dims,self.dims)
        self.image = pygame.image.load('assets/sprites/items/timemachineBig.png')

    def draw(self,screen,relX, relY, offset):
        self.rect = pygame.Rect(self.xpos+(relX+offset),self.ypos+(relY+offset),self.dims,self.dims)
        #pygame.draw.rect(screen,colors['red'],self.rect,3)

        # dispString = 'Collect: '+str(self.itemsHeld)+'/'+str(self.capacity)
        # label = self.font.render(dispString, 1, colors['blue'])

        #screen.blit(label,(100,0))
        screen.blit(self.image,self.rect)

    def take(self):
        self.itemsHeld += 1

class Crystal():
    def __init__(self,rect):
        self.sheet = pygame.image.load(itemPath[0] + itemPath[1])
        self.rect = rect
        self.origX = rect.x
        self.origY = rect.y

    def isCoin(self):
        return False

class Coin():
    def __init__(self,rect):
        self.sheet = pygame.image.load(itemPath[0] + 'goldCoin.png')
        self.rect = rect
        self.origX = rect.x
        self.origY = rect.y

    def isCoin(self):
        return True
        

def createRandomRect( w_Width, w_Height , rectWidth , rectHeight , playerRect, sinkRect):
    goodCoords = False
    x = 0
    y = 0

    while not goodCoords:
        x = random.randint(0, (2000 - rectWidth))
        y = random.randint(0,(2000 - rectHeight))
        if(not playerRect.collidepoint(x,y)) and (not sinkRect.collidepoint(x,y)):
           # print "x: " + str(x)
           # print 'y: ' + str(y)
            goodCoords = True

    itemRect=pygame.Rect(x,y,41,36)
    crystal = Crystal(itemRect)

    return crystal


class Obstacle:
    
    def __init__(self,rect,path):
        self.sheet = pygame.image.load(path)
        self.rect = rect
        self.path = path
        self.origX = rect.x
        self.origY = rect.y

    

def createObstacles(obstacleDict):

    obstacles = []

    for obstacle in obstacleDict:
        x = obstacleDict[obstacle]['x']
        y = obstacleDict[obstacle]['y']
        width = obstacleDict[obstacle]['width']
        height = obstacleDict[obstacle]['height']

        clip_area = pygame.Rect(x,y,width,height)
            
        obstacles.append(Obstacle(clip_area,obstacleDict[obstacle]['path']))
        

        # self.sheet.set_clip(clip_area)
        # self.image = self.sheet.subsurface(self.sheet.get_clip())
        # self.rectangle = self.image.get_rect()
        # self.rectangle.topleft = startingPos


    return obstacles
