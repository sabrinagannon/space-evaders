import random, pygame

def createRandomRect( w_Width, w_Height , rectWidth , rectHeight , playerRect):

    goodCoords = False
    x = 0 
    y = 0 

    while not goodCoords:
        x = random.randint(0,(w_Width - rectWidth))
        y = random.randint(0,(w_Height - rectHeight))
        if(not playerRect.collidepoint(x,y)):
            goodCoords = True
    
    itemRect = pygame.Rect(x,y,50,50)
    
    return itemRect
