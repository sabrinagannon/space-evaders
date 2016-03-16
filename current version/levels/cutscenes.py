import pygame
from constants import w_width,w_height

# plays any cutscene text stored in cutsceneText.py
def playCutscene(screen, cutscene):

    # initialize cutscene background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # initialize font
    font = pygame.font.SysFont("monospace", 15)

    # set flag, timer, ticks, and initialize index
    cutscenePlaying = True
    timer = 0;
    ticks = pygame.time.get_ticks();
    textIndex = 0;

    # loop as long as the cutscene is playing
    while cutscenePlaying:

        # check keypresses to end cutscene
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                cutscenePlaying = False

        # get latest ticks
        ticks = pygame.time.get_ticks();

        # loop through each line of text in cutscene
        if (textIndex != len(cutscene)) and (ticks - timer >= cutscene[textIndex][1]):

            # render that line of text and properly position it
            text = font.render(cutscene[textIndex][0], 1, (250, 250, 250))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            background.blit(text, (10, 10 + (20 * textIndex)))
            screen.blit(background, (0, 0))
            pygame.display.flip()

            # reset timer
            timer = pygame.time.get_ticks();

            # increment text index
            textIndex += 1
