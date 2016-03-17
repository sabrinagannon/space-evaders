import pygame
from constants import w_width,w_height

# plays any cutscene text stored in cutsceneText.py
def playCutscene(screen, cutscene):

    # initialize cutscene background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # initialize fonts
    narratorFont = pygame.font.SysFont("sans-serif", 30, True)
    protagonistFont = pygame.font.SysFont("monospace", 20, False)

    # set flag, timer, ticks, index, and offset
    cutscenePlaying = True
    timer = 0;
    ticks = pygame.time.get_ticks();
    textIndex = 0;
    offset = 0;

    # loop as long as the cutscene is playing
    while cutscenePlaying:

        # check keypresses to end cutscene
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                cutscenePlaying = False

        # get latest ticks
        ticks = pygame.time.get_ticks();

        # loop through each line of text in cutscene
        if (textIndex != len(cutscene)) and (ticks - timer >= cutscene[textIndex][2]):

            # which font style should we use?
            if cutscene[textIndex][1]:
                font = narratorFont
            else:
                font = protagonistFont

            # render that line of text and properly position it
            text = font.render(cutscene[textIndex][0], 1, (250, 250, 250))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            background.blit(text, (10, 15 + (32 * offset)))
            screen.blit(background, (0, 0))
            pygame.display.flip()

            # reset timer
            timer = pygame.time.get_ticks();

            # increment text index
            textIndex += 1

            # reset/increment offset
            offset += 1
            if offset > 20:
                offset = 0
                background = pygame.Surface(screen.get_size())
                background = background.convert()
                background.fill((0, 0, 0))
