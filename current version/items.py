import random, pygame

from constants import w_width,w_height,colors

class Sink():
    def __init__(self,size,font,capacity):
        self.dims = size
        self.rect = pygame.Rect((w_width/2)-100,(w_height/2)-50,size,size)
        self.itemsHeld = 0
        self.capacity = capacity
        self.font = font

    def draw(self,screen):
        pygame.draw.rect(screen,colors['red'],self.rect,3)
        dispString = 'Collect: '+str(self.itemsHeld)+'/'+str(self.capacity)
        label = self.font.render(dispString , 1, colors['blue'])
        if self.itemsHeld > 9:  # not digit
            screen.blit(label,(self.rect.x+12,self.rect.y+5))
        else:
            screen.blit(label,(self.rect.x+14,self.rect.y+5))

    def take(self):
        self.itemsHeld += 1

def createRandomRect( w_Width, w_Height , rectWidth , rectHeight , playerRect, sinkRect):
    goodCoords = False
    x = 0
    y = 0

    while not goodCoords:
        x = random.randint(0,(w_Width - rectWidth))
        y = random.randint(0,(w_Height - rectHeight))
        if(not playerRect.collidepoint(x,y)) and (not sinkRect.collidepoint(x,y)):
            goodCoords = True

    itemRect = pygame.Rect(x,y,50,50)

    return itemRect
