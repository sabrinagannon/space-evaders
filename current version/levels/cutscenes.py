import pygame
from constants import w_width,w_height,prototype_text

    
def playCutscene1(screen,gameFont):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    for i in range(len(prototype_text)):
        text = gameFont.render(prototype_text[i], 1, (250, 250, 250))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, (10, 10 + (20 * i)))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1500)

    cutscene = True
    while cutscene:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                cutscene = False
