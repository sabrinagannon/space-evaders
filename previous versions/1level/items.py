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

    def draw(self,screen,relX, relY, offset):
        self.rect = pygame.Rect(self.xpos+(relX+offset),self.ypos+(relY+offset),self.dims,self.dims)
        pygame.draw.rect(screen,colors['red'],self.rect,3)
        dispString = 'Collect: '+str(self.itemsHeld)+'/'+str(self.capacity)
        label = self.font.render(dispString , 1, colors['blue'])

        if self.itemsHeld > 9:  # not digit
            screen.blit(label,(self.rect.x+12,self.rect.y+5))
        else:
            screen.blit(label,(self.rect.x+14,self.rect.y+5))

    def take(self):
        self.itemsHeld += 1

class Crystal():
    def __init__(self,rect):
        self.sheet = pygame.image.load(itemPath[0] + itemPath[1])
        self.rect = rect
        self.origX = rect.x
        self.origY = rect.y
        
        

def createRandomRect( w_Width, w_Height , rectWidth , rectHeight , playerRect, sinkRect):
    goodCoords = False
    x = 0
    y = 0

    while not goodCoords:
        x = random.randint(0,(w_Width - rectWidth))
        y = random.randint(0,(w_Height - rectHeight))
        newRect = pygame.Rect(x,y,41,36)
        if(not playerRect.colliderect(newRect) and (not sinkRect.colliderect(newRect))):
            goodCoords = True

    itemRect=pygame.Rect(x,y,41,36)
    crystal = Crystal(itemRect)

    return crystal
