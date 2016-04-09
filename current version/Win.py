import pygame
# This code taken from user nebelhom's tutorial
# at https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/
# on April 8th 2016

class MenuItem(pygame.font.Font):
    def __init__(self, text, font='nanumgothic', font_size=60,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):

        style = pygame.font.match_font(font)
        pygame.font.Font.__init__(self, style, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False


class GameMenu():
    def __init__(self, screen, items, font=None, font_size=60,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bgImage = pygame.image.load('assets/sprites/menuImages/cloudNice.jpg').convert()
        self.clock = pygame.time.Clock()

        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section for an explanation
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def show(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                   for item in self.items:
                       if item.is_mouse_selection(pygame.mouse.get_pos()):
                           mainloop = False

            # Redraw the background
            #self.screen.fill(self.bg_color)
            self.screen.blit(self.bgImage,(0,0))

            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((0, 255, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

def display():
    # Creating the screen
    screen = pygame.display.set_mode((1200, 700), 0, 32)
    menu_items = ('Exit',)
    gm = GameMenu(screen, menu_items)
    gm.show()
