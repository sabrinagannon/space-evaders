import pygame, sys,items,random
sys.path.insert(0,'levels/')
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2
import player, level1, level2, level3, level4, level5, sounds
import cutscenes, cutsceneText, menu

def reset(sink,soundEffects,initRect,initCrystal,crystalList):
    sink.itemsHeld = 0
    soundEffects = sounds.SoundFX()
    initRect = pygame.Rect(-4000,-4000,25,25)
    initCrystal = items.Crystal(initRect)
    crystalList= [initCrystal]

if __name__ == '__main__':
    pygame.init()

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    font = pygame.font.SysFont("monospace", 15)
    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    screen.fill(colors['black'])
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    level = level1.level(screen)
    levelNum = 1

    pygame.display.set_caption('*~*~*KEITH TO THE PAST*~*~*')

    keith = player.Player((level.startingPosX,level.startingPosY), playerPath2, playerSpeed)

    sink = items.Sink(150,font,10)
    soundEffects = sounds.SoundFX()
    initRect = pygame.Rect(-4000,-4000,25,25)
    initCrystal = items.Crystal(initRect)
    crystalList= [initCrystal]

    pygame.display.update()

    frameCount = 0
    gameLoop = menu.display()
    if gameLoop:
        cutscenes.playCutscene(screen, cutsceneText.text["intro_cutscene"])
        # play level cutscene
        level.playCutscene(1)
        
        # CUTSCENE TESTING
        # cutscenes.playCutscene(screen, cutsceneText.text["intro_cutscene"])
        # level.playCutscene(1)
        # level.playCutscene(2)
        # level.playCutscene(3)
        # level.playCutscene(4)
        # level.playCutscene(5)

    while gameLoop:

        if pygame.mixer.music.get_busy() == False:
            level.playLvlMusic(levelNum)

        frameCount+=1
        if sink.itemsHeld == 10 and levelNum != 4:
              # print "player score is : " + str(keith.score)
              # sys.exit()
            pygame.mixer.music.stop()
            reset(sink,soundEffects,initRect,initCrystal,crystalList)
            if levelNum == 1:
                level = level2.level(screen)
                levelNum = 2
                level.playCutscene(levelNum)
                keith.itemsHeld = 0
                keith.updateSpeed()
                crystalList= [initCrystal]
            elif levelNum == 2:
                level = level3.level(screen)
                levelNum = 3
                level.playCutscene(levelNum)
                keith.itemsHeld = 0
                keith.updateSpeed()
                crystalList= [initCrystal]
            elif levelNum == 3:
                level = level4.level(screen)
                levelNum = 4
                # play level cutscene
                level.playCutscene(levelNum)
                keith.itemsHeld = 0
                keith.updateSpeed()
                crystalList= [initCrystal]

                initRect1 = pygame.Rect(-580,-560,36,36)
                initRect2 = pygame.Rect(-580,1000,36,36)
                initRect3 = pygame.Rect(990,830,36,36)
                initRect4 = pygame.Rect(1000,-560,36,36)

                initCoin1 = items.Coin(initRect1)
                initCoin2 = items.Coin(initRect2)
                initCoin3 = items.Coin(initRect3)
                initCoin4 = items.Coin(initRect4)

                crystalList= [initCoin1,initCoin2,initCoin3,initCoin4]

        elif sink.itemsHeld == 4 and levelNum == 4:
            # Need to make window static and constrain movement still for level 5
            reset(sink,soundEffects,initRect,initCrystal,crystalList)
            level = level5.level(screen)
            levelNum = 5

            sink.itemsHeld =0
            level.playLvlMusic(levelNum)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "player score is : " + str(keith.score)
                sys.exit()

        keys = pygame.key.get_pressed()

        # React to key press
        disabled = level.background.handle(keys,keith,level)
        update = keith.handle(keys,level.background)
        level.updateEnemies(keith,keys,crystalList,disabled,level.obstacles)

        # generate new crystal that does not collide with player or sink
        if(frameCount == 90) and (levelNum != 4):
            frameCount = 0
            if(len(crystalList) < 10): # quick way of limiting us to 10 items (or however many crystals, can be changed depending on level.)
                #make sure the crystal is not inside of an obstacle
                goodCrystal = True
                crystalToAppend = items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect)
                while 1:
                    for obstacle in level.obstacles:
                        if (crystalToAppend.rect.colliderect((obstacle.rect.x ,obstacle.rect.y,obstacle.rect.width,obstacle.rect.height))):
                            goodCrystal = False
                            break
                    if(goodCrystal == False):
                        crystalToAppend = items.createRandomRect(w_width, w_height,41,36,keith.rectangle,sink.rect)
                        goodCrystal = True
                    else:
                        break

                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))
            elif(len(crystalList) > 0):
                del crystalList[1]
                crystalList.append(items.createRandomRect(w_width,w_height,41,36,keith.rectangle,sink.rect))

        # Check for collisions, update speed and score
        index = 0
        while index < len(crystalList):
            if(crystalList[index].rect.colliderect(keith.rectangle)):

                if(keys[pygame.K_SPACE] and keith.isInvincible==False):
                    soundEffects.playChime()
                    crystal = crystalList[index]
                    del crystalList[index]
                    index = index-1

                    if crystal.isCoin():
                        keith.coinsHeld += 1
                    else:
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

        if levelNum == 4:
            if level.timer == 0:
                 print "you weren't fast enough"
                 sys.exit()

        level.draw(crystalList,sink,keith)
        pygame.display.update()
        if keith.lives <= 0 :
            print "you lost all your lives!"
            sys.exit()

        gameClock.tick(30)
