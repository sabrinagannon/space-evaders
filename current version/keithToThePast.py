import pygame, sys , items
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2, wolfPath, bearPath, itemPath, prototype_text
import player,enemy

def drawEnemies(screen,enemies):
    for enemy in enemies:
        pygame.draw.rect(screen,colors['blue'],enemy.detection,3)
        screen.blit(enemy.image, enemy.rectangle)

def drawText(screen):
    font = gameFont
    text = font.render('You are carrying '+str(keith.itemsHeld)+' crystals', 1,colors['blue'])
    textpos = pygame.Rect(10,10,w_width/2,w_height/2)
    screen.blit(text, textpos)

def drawItems(screen,itemList,sink):
    sink.draw(screen)
    for itemRect in itemRectList:
        itemImg = pygame.image.load(itemPath[0] + itemPath[1])
        pygame.draw.rect(screen,colors['green'],itemRect,3)
        screen.blit(itemImg, itemRect)

def playLvlMusic(lvlNumber):
    pygame.mixer.music.load("assets/music/keithDenial.mp3")
    pygame.mixer.music.play(-1)

def playSoundEffect(effectCode):
    if effectCode == 0: # BAD SOUND
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/music/GETBONKED.mp3")
        pygame.mixer.music.play()
    elif effectCode == 1: # Pickup sound
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/music/PICKUP.mp3")
        pygame.mixer.music.play()



if __name__ == '__main__':
    pygame.init()
    #pygame.mixer.init(44100)
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    gameFont = pygame.font.SysFont("monospace", 15)

    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    pygame.display.set_caption('Use WASD to move, collect crystals by pressing SPACE, drop crystals into the red box by pressing K, avoid the bears and wolves!! (oh my!) Press ESCAPE to QUIT')
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #info = pygame.display.Info()
    #w_width, w_height = info.current_w, info.current_h

    # display text (just for prototype)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    for i in range(0, len(prototype_text)):
        text = gameFont.render(prototype_text[i], 1, (250, 250, 250))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, (10, 10 + (20 * i)))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1500)
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                loop = False

    x,y = 100,100
    keith = player.Player((x,y), playerPath2, playerSpeed)
    # Uncomment to see the modern version!
    #keith = player.Player((x,y), playerPath1, playerSpeed)
    keith.score = 0
    musicPointer = 0

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
    font=gameFont
    frameCount = 0
    while True:
        if pygame.mixer.music.get_busy() == False:
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
            if(e.rectangle.colliderect(keith.rectangle)):
                playSoundEffect(0)
                if(keith.itemsHeld > 0):
                    keith.itemsHeld -= 1
                    keith.updateSpeed()
                    droppedItem = pygame.Rect(keith.rectangle.x, keith.rectangle.y, 50,50)
                    itemRectList.append(droppedItem)
                e.caughtHim = 1

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
                    playSoundEffect(1)
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
        drawText(screen)
        screen.blit(keith.image, keith.rectangle)

        pygame.display.update()
        gameClock.tick(20)
