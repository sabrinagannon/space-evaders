import pygame, sys , items
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2, wolfPath, bearPath, itemPath
import player,enemy

def drawEnemies(screen,enemies):
    for enemy in enemies:
        pygame.draw.rect(screen,colors['blue'],enemy.detection,3)
        screen.blit(enemy.image, enemy.rectangle)

def drawItems(screen,itemList,sink):
    sink.draw(screen)

    for itemRect in itemRectList:
        itemImg = pygame.image.load(itemPath[0] + itemPath[1])
        pygame.draw.rect(screen,colors['green'],itemRect,3)
        screen.blit(itemImg, itemRect)
    
def playLvlMusic(lvlNumber):
	lvl1Song = pygame.mixer.Sound("assets/music/keithDenial.mp3")
	pygame.mixer.Sound.play(lvl1Song,-1)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(44100)
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    gameFont = pygame.font.SysFont("monospace", 15)

    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #info = pygame.display.Info()
    #w_width, w_height = info.current_w, info.current_h

    x,y = 100,100
    keith = player.Player((x,y), playerPath2, playerSpeed)
    # Uncomment to see the modern version!
    #keith = player.Player((x,y), playerPath1, playerSpeed)
    keith.score = 0

    enemies = []
    wolf = enemy.Enemy((x+100,y+200),wolfPath,7)
    bear = enemy.Enemy((x+300,y+100),bearPath,9)
    wolf2 = enemy.Enemy((x+400,y+200),wolfPath,10)
    bear2 = enemy.Enemy((x+100,y+400),bearPath,11)
    enemies.extend([wolf,bear,wolf2,bear2])

    sink = items.Sink(150,gameFont,10)

    initRect = pygame.Rect(w_width+10,w_height+10,25,25)
    itemRectList= [initRect]

    screen.fill(colors['black'])
    # screen.blit(keith.image, keith.rectangle)
    # screen.blit(enemy.image, enemy.rectangle)
    pygame.draw.rect(screen,colors['green'],initRect,3)
    sink.draw(screen)
    pygame.display.update()

    frameCount = 0
    while True:

        if not (pygame.mixer.music.get_busy()):
            print "am i ever here???"
            playLvlMusic(0)

        frameCount+=1
        if sink.itemsHeld == 10:
              print "player score is : " + str(keith.score)
              sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "player score is : " + str(keith.score)
                sys.exit()

        keys = pygame.key.get_pressed()

        update = keith.handle(keys)

        for e in enemies:
            e.update(keith.rectangle)
        screen.fill(colors['black'])

        # generate new crystal that does not collide with player or sink
        if(frameCount == 80):
            frameCount = 0
            if(len(itemRectList) < 10): # quick way of limiting us to 10 items (or however many fragments/items, can be changed depending on level.)
                itemRectList.append(items.createRandomRect(w_width,w_height,50,50,keith.rectangle,sink.rect))
            elif(len(itemRectList) > 0):
                del itemRectList[1]
                itemRectList.append(items.createRandomRect(w_width,w_height,50,50,keith.rectangle,sink.rect))

        # Check for collisions, update speed and score
        index = 0
        while index < len(itemRectList):
            #print("index: " + str(index))
            if(itemRectList[index].colliderect(keith.rectangle)):
                #print "the two items collided!"
                if(keys[pygame.K_SPACE]):

                    del itemRectList[index]
                    #print str(itemRectList)
                    index = index -1
                    keith.itemsHeld = keith.itemsHeld + 1
                    if keith.speed > 5 :
                        keith.updateSpeed()
                    else:
                        keith.speed = 5
            index+=1

        if update is not None:
            if sink.rect.colliderect(keith.rectangle): # dropping in the sink
                sink.take()
                keith.score += 1
            else:
                # player dropped an item and we need to re-draw it
                itemRectList.append(update)

        #pygame.draw.rect(screen,colors['green'],itemRect,3)
        drawItems(screen,itemRectList,sink)
        drawEnemies(screen,enemies)
        screen.blit(keith.image, keith.rectangle)

        pygame.display.update()
        gameClock.tick(20)
