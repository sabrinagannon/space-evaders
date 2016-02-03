import pygame, sys , items
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2, wolfPath, bearPath
import player,enemy

def drawEnemies(screen,enemies):
    for enemy in enemies:
        pygame.draw.rect(screen,colors['blue'],enemy.detection,3)
        screen.blit(enemy.image, enemy.rectangle)
    

if __name__ == '__main__':
    pygame.init()


    gameClock = pygame.time.Clock()
    screen = pygame.display.set_mode([w_width,w_height])
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #info = pygame.display.Info()
    #w_width, w_height = info.current_w, info.current_h


    x,y = 100,100
    keith = player.Player((x,y), playerPath2, playerSpeed)
    enemies = []
    wolf = enemy.Enemy((x+100,y+200),wolfPath,7)
    bear = enemy.Enemy((x+300,y+100),bearPath,9)
    enemies.extend([wolf,bear])

    # Uncomment to see the modern version!
    #keith = player.Player((x,y), playerPath1, playerSpeed)
    keith.score = 0
    itemRect = pygame.Rect(w_width+10,w_height+10,25,25)

    itemRectList= [itemRect]

    screen.fill(colors['black'])
    # screen.blit(keith.image, keith.rectangle)
    # screen.blit(enemy.image, enemy.rectangle)
    pygame.draw.rect(screen,colors['green'],itemRect,3)
    pygame.display.update()

    frameCount = 0
    while True:
        frameCount+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "player score is : " + str(keith.score)
                sys.exit()

        update = keith.handle(event)

        for e in enemies:
            e.update(keith.rectangle)
        screen.fill(colors['black'])

        # generate new item--(fragment?) that does not collide with player
        if(frameCount == 80):
            frameCount = 0
            if(len(itemRectList) < 10): # quick way of limiting us to 10 items (or however many fragments/items, can be changed depending on level.)
                itemRectList.append(items.createRandomRect(w_width,w_height,50,50,keith.rectangle))
            elif(len(itemRectList) > 0):
                del itemRectList[1]
                itemRectList.append(items.createRandomRect(w_width,w_height,50,50,keith.rectangle))

        # Check for collisions, update speed and score
        index = 0
        while index < len(itemRectList):
            #print("index: " + str(index))
            if(itemRectList[index].colliderect(keith.rectangle)):
                #print "the two items collided!"
                keys = pygame.key.get_pressed()
                if(keys[pygame.K_SPACE]):

                    del itemRectList[index]
                    #print str(itemRectList)
                    index = index -1
                    keith.score = keith.score + 1
                    keith.itemsHeld = keith.itemsHeld + 1
                    if keith.speed > 5 :
                        keith.updateSpeed()
                    else:
                        keith.speed = 5
            index+=1

        if update is None:
            pass
        else:
            # player dropped an item and we need to re-draw it
            itemRectList.append(update)
        
        for itemRect in itemRectList:
            pygame.draw.rect(screen,colors['green'],itemRect,3)

        # print 'speed= ', keith.speed
        # print 'items=', keith.itemsHeld
        pygame.draw.rect(screen,colors['green'],itemRect,3)
        screen.blit(keith.image, keith.rectangle)
        drawEnemies(screen,enemies)
        pygame.display.update()

        gameClock.tick(20)
