import pygame, sys , items
from constants import w_width, w_height, colors, playerSpeed, playerPath1, playerPath2, enemyPath
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
    e = enemy.Enemy((x+100,y+200),enemyPath,7)
    enemies.append(e)

    # Uncomment to see the modern version!
    #keith = player.Player((x,y), playerPath1, playerSpeed)
    playerScore = 0
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
                print "player score is : " + str(playerScore)
                sys.exit()

        keith.handle(event)
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
        length = len(itemRectList)
        index = 0
        while index < length:
            #print("index: " + str(index))
            if(itemRectList[index].colliderect(keith.rectangle)):
                #print "the two items collided!"
                keys = pygame.key.get_pressed()
                if(keys[pygame.K_SPACE]):

                    del itemRectList[index]
                    #print str(itemRectList)
                    index = index -1
                    length = length - 1
                    playerScore = playerScore + 1
                if keith.speed > 0 :
                    keith.speed = keith.speed - (0.01 * playerScore)
                else:
                    keith.speed = 0.01
            index+=1
        for itemRect in itemRectList:
            pygame.draw.rect(screen,colors['green'],itemRect,3)

        pygame.draw.rect(screen,colors['green'],itemRect,3)
        screen.blit(keith.image, keith.rectangle)
        drawEnemies(screen,enemies)
        pygame.display.update()

        gameClock.tick(20)
