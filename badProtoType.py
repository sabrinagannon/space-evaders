import pygame, sys , random

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


pygame.init()

w_width = 700
w_height = 700
windowSize  = [w_width,w_height]

gameClock = pygame.time.Clock()

screen = pygame.display.set_mode(windowSize)

colors = {'black': (0,0,0) , 'blue':(0,0,255),'green':(0,255,0),'red':(255,0,0)}

x,y = 10,500
rectWidth,rectHeight = 100, 100
playerRect = pygame.Rect(x,y,100,100)
speed = 5.5
playerScore = 0 

itemRect = pygame.Rect(300,400,50,50)

itemRectList= [itemRect]


screen.fill(colors['black'])
pygame.draw.rect(screen,colors['blue'],playerRect,3)
pygame.draw.rect(screen,colors['green'],itemRect,3)
pygame.display.update()

count = 0
while True:
    count+=1
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            print "player score is : " + str(playerScore)
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if(keys[pygame.K_w]):
       # print "why don't i move"
        if(y > 0 + speed ):
            y = y - speed
    if(keys[pygame.K_s]):
        if(y < w_height - rectHeight):
            y = y + speed
    if(keys[pygame.K_a]):
        if(x > 0 + speed):
            x = x - speed
    if(keys[pygame.K_d]):
        if(x < w_width - rectWidth):
            x = x + speed
    playerRect = pygame.Rect(x,y,100,100)

    screen.fill(colors['black'])
    
    #how to check if two rects are colliding
    if(count == 250):
        count = 0 
        itemRectList.append(createRandomRect(w_width,w_height,50,50,playerRect))
    length = len(itemRectList)
    index = 0
    while index < length:
        
    #for index in range(0,length):
        print("index: " + str(index))
        if(itemRectList[index].colliderect(playerRect)):
            print "the two items collided!"
            del itemRectList[index]
            print str(itemRectList)
            index = index -1
            length = length - 1
            playerScore = playerScore + 1
            speed = speed - (0.05 * playerScore)
        index+=1
    for itemRect in itemRectList:
        pygame.draw.rect(screen,colors['green'],itemRect,3)

    pygame.draw.rect(screen,colors['green'],itemRect,3)
    pygame.draw.rect(screen,colors['blue'],playerRect,3)
    pygame.display.update()

    gameClock.tick(60)


