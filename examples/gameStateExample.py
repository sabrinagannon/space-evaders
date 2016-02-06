
'''
In this pygame file I (try) to explain how I do basic managment
of (Game?)States. Each State could load a totally different "window"
like a Introscreen, a Logo, a Menu, an Optionscreen, the Game itself etc

This system is far from perfect but it works in a relatively clean way I suppose
Press 1,2,3 to change your state

Src: http://blog.atoav.com/2013/08/statemanagment-in-pygame/
Other good reference: http://stackoverflow.com/questions/14700889/pygame-level-menu-states
'''
try:
    import sys, os, random
    import pygame
    from pygame.locals import *

except ImportError, err:
    print "Yikes! %s Failed to load Module in Game.py: %s" % (__file__, err)
    sys.exit(1)

# Our main Function, this is were everything gets called etc
def main():
    pygame.init()
    screen = pygame.display.set_mode((640,320))
    pygame.display.set_caption("Statemanagment in Pygame")

    # create a timer/clock
    timer = pygame.time.Clock()

    # running is true
    running = True

    # Initializes the Statemanager
    # manager.scene is the active State
    # until there is a change(state) event
    # also we pass the screen-Rect for drawing
    # (you could also pass resolution data etc)
    manager = StateMananger(screen)

    while running:
        #Limit the Framerate just for the heck of it
        timer.tick(50)

        # running is False if handle_events is False (Quit etc)
        running = manager.state.handle_events(pygame.event.get())

        #update and render the managers active state
        manager.update()
        manager.render(screen)

        pygame.display.flip()

    # Say goodbye before you quit
    print 'Quit: See you in Space, Cowboy!'
    pygame.quit()

class StateMananger(object):
    # Statemanager manages States, loads the first state in the
    # constructor and has a option to print things out
    def __init__(self, screen):
        # on constructions change to our first state
        self.change(IntroState(screen))

    def change(self, state):
        # the new self.state is our passed state
        self.state = state
        self.state.manager = self
        # be nice and print what you did
        print ('changed to '+self.get_name())
        print ('('+self.get_descr()+')\n')

    def update(self):
        self.state.update()

    def render(self, screen):
        self.state.render(screen)

    def get_name(self):
        return self.state.name

    def get_descr(self):
        return self.state.description

class State(object):
    # a superclass for our States so we dont have to write things
    # over and over if we want to do sth. in every state we construct.
    def __init__(self, screen):
        self.screen = screen
        self.name = None
        self.description = None

    def __str__(self):
        return str(self.name) + str(self.description)

# After this point there are 3 Scenes defined
# you could do totally different things in each
# I recommend loading those classes from another
# file/module so you don't die a painful death..
class IntroState(State):
    # Our first state
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "IntroState"
        self.description = "Playback of the Logos and stuff"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        self.text3 = self.font2.render("Press 1, 2, 3 to change States", True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()
        self.text3Rect = self.text3.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

        self.text3Rect.centerx = self.screen.get_rect().centerx
        self.text3Rect.centery = self.screen.get_rect().centery+100

    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)
        self.screen.blit(self.text3, self.text3Rect)

    def update(self):
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "2"
                if e.key == K_2:
                    # This is the changecommand. You could also change via
                    # timer or other stuff.
                    self.manager.change(MenuState(self.screen))
                if e.key == K_3:
                    self.manager.change(Gametate(self.screen))
        return True

class MenuState(State):
    # Your Menu could be here
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "MenuState"
        self.description = "Gamemenu"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)

    def update(self):
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "1"
                if e.key == K_1:
                    self.manager.change(IntroState(self.screen))
                # change State if user presses "3"
                if e.key == K_3:
                    self.manager.change(GameState(self.screen))
        return True

class GameState(State):
    # Gamestate - run your stuff inside here (maybe another manager?
    # for your levelmanagment?)
    def __init__(self, screen):
        State.__init__(self, screen)

        self.name = "GameState"
        self.description = "Draw your game inside here"

        # A whole Block just to display the Text ...
        self.font1 = pygame.font.SysFont("Monospaced", 50)
        self.font2 = pygame.font.SysFont("Monospaced", 32)
        # Render the text
        self.text1 = self.font1.render(self.name, True, (255,255, 255), (159, 182, 205))
        self.text2 = self.font2.render(self.description, True, (255,255, 255), (159, 182, 205))
        # Create Text-rectangles
        self.text1Rect = self.text1.get_rect()
        self.text2Rect = self.text2.get_rect()

        # Center the Text-rectangles
        self.text1Rect.centerx = self.screen.get_rect().centerx
        self.text1Rect.centery = self.screen.get_rect().centery

        self.text2Rect.centerx = self.screen.get_rect().centerx
        self.text2Rect.centery = self.screen.get_rect().centery+50

    def render(self, screen):
        # Rendering the State
        pygame.display.set_caption(self.name +"  "+self.description)
        screen.fill((20, 20, 20))

        self.screen.blit(self.text1, self.text1Rect)
        self.screen.blit(self.text2, self.text2Rect)

    def update(self):
        pass

    def handle_events(self,events):
        # every State has its own eventmanagment
        for e in events:
            if e.type == QUIT:
                print ("Pressed Quit (Window)")
                return False

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    print ("Pressed Quit (Esc)")
                    return False
                # change State if user presses "2"
                if e.key == K_2:
                    self.manager.change(MenuState(self.screen))
                # change State if user presses "1"
                if e.key == K_1:
                    self.manager.change(IntroState(self.screen))
        return True

# Run the main function
if __name__ == "__main__":
    main()
