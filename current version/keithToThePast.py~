import pygame, sys,items,sounds,cutscenes, random
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2, wolfPath, bearPath
import player,enemy,backgrounds

def drawEnemies(screen,enemies):
    for enemy in enemies:
        pygame.draw.rect(screen,colors['blue'],enemy.detection,3)
        screen.blit(enemy.image, enemy.rectangle)

def drawText(screen):
    text = gameFont.render('You are carrying '+str(keith.itemsHeld)+' crystals', 1,colors['blue'])
    textpos = pygame.Rect(10,10,w_width/2,w_height/2)
    screen.blit(text, textpos)

def drawItems(screen,crystalList,sink,bg):
    sink.draw(screen,bg.x,bg.y,bg.offset)

    for crystal in crystalList:
        crystal.rect.x = crystal.origX + (bg.x + bg.offset)
        crystal.rect.y = crystal.origY + (bg.y + bg.offset)
        pygame.draw.rect(screen,colors['green'],crystal.rect,3)
        screen.blit(crystal.sheet, crystal.rect)#(itemRect.x + (b.x + b.offset), itemRect.y + (b.y + b.offset)))

def playLvlMusic(lvlNumber):
    pygame.mixer.music.load("assets/music/keithDenial.mp3")
    pygame.mixer.music.play(-1)


if __name__ == '__main__':
    pygame.init()

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    gameFont = pygame.font.SysFont("monospace", 15)

    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption('Use WASD to move, collect crystals by pressing SPACE, drop crystals into the red box by pressing K, avoid the bears and wolves!! (oh my!) Press ESCAPE to QUIT')

    # cutscenes.playCutscene1(screen,gameFont)

    x,y = 600,350 # start player at center
    enemyStartX, enemyStartY = random.randrange(w_width),random.randrange(w_height) # give enemies random start points
    keith = player.Player((x,y), playerPath2, playerSpeed)
    # Uncomment to see the modern version!
    #keith = player.Player((x,y), playerPath1, playerSpeed)

    enemies = []
    wolf = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,7)
    bear = enemy.Enemy((enemyStartX, enemyStartY),bearPath,9)
    wolf2 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,10)
    bear2 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,11)
    wolf3 = enemy.Enemy((enemyStartX, enemyStartY),wolfPath,3)
    bear3 = enemy.Enemy((enemyStartX, enemyStartY),bearPath,12)
    enemies.extend([wolf,bear,wolf2,bear2,bear3,wolf3])

    sink = items.Sink(150,gameFont,10)
    soundEffects = sounds.SoundFX()
    initRect = pygame.Rect(-4000,-4000,25,25)
    initCrystal = items.Crystal(initRect)
    crystalList= [initCrystal]

    screen.fill(colors['black'])
    pygame.draw.rect(screen,colors['green'],initRect,3)
    #sink.draw(screen)
    pygame.display.update()

    font=gameFont
    frameCount = 0
    background = backgrounds.Background(1)


    while True:
        if pygame.mixer.music.get_busy() == False:
            playLvlMusic(0)

        frameCount+=1
        soundEffects.coolDown()
        if sink.itemsHeld == 10:
              print "player score is : " + str(keith.score)
              sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "player score is : " + str(keith.score)
                sys.exit()

        keys = pygame.key.get_pressed()

        background.handle(keys,keith)
        update = keith.handle(keys)

        for e in enemies:
            e.update(keith,background,keys)
            if(e.rectangle.colliderect(keith.rectangle)):
                #soundEffects.playBloop()
                e.caughtHim = 1
                if(keith.itemsHeld > 0):
                    keith.itemsHeld -= 1
                    keith.updateSpeed()
                    droppedBox = pygame.Rect(keith.rectangle.x, keith.rectangle.y, 41,36)
                    droppedItem = items.Crystal(droppedBox)
                    crystalList.append(droppedItem)

        # generate new crystal that does not collide with player or sink
        if(frameCount == 90):
            frameCount = 0
            if(len(crystalList) < 10): # quick way of limiting us to 10 items (or however many crystals, can be changed depending on level.)
                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))
            elif(len(crystalList) > 0):
                del crystalList[1]
                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))

        # Check for collisions, update speed and score
        index = 0
        while index < len(crystalList):
            if(crystalList[index].rect.colliderect(keith.rectangle)):
                if(keys[pygame.K_SPACE]):
                    soundEffects.playChime()
                    del crystalList[index]
                    index = index-1
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
                crystalList.append(update)

        screen.fill(colors['black'])
        background.draw(screen)
        drawItems(screen,crystalList,sink,background)
        drawEnemies(screen,enemies)
        drawText(screen)
        screen.blit(keith.image, keith.rectangle)

        pygame.display.update()
        gameClock.tick(30)
