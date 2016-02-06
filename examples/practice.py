import pygame
import sys
import random
from pygame.locals import *

#-----------initializers-----------------
pygame.init()

screen = pygame.display.set_mode((450, 450))
clock = pygame.time.Clock()
isBlue = True
x = 30
y = 30
size = 60

sound_lib = {}
image_lib = {}

pygame.display.set_caption('Hello World!')

#-----------image/background stuff -------

def get_image(path):
    global image_lib
    image = image_lib.get(path)
    if image is None:
        image = pygame.image.load(path).convert()
        image_lib[path] = image
    return image


#-------------sound stuff--------------------

songs = ['Raining.mp3','punk.mp3']
currentSong = 'assets/' + songs[0]
pygame.mixer.music.load(currentSong)
SONG_END = pygame.USEREVENT + 1 # USEREVENT has the highest value of the enum
pygame.mixer.music.set_endevent(SONG_END)
#pygame.mixer.music.play()
#pygame.mixer.music.queue('assets/crash.mp3')

def play_a_different_song():
    global currentSong,songs
    next_song =  'assets/'+random.choice(songs)
    while next_song == currentSong:
        next_song =  'assets/' + random.choice(songs)
    currentSong = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()

def playSound(path):
    global sound_lib
    sound = sound_lib.get(path)
    if sound is None:
        sound = pygame.mixer.Sound(path)
        sound_lib[path] = sound
    sound.play()


#---------- functions ------------------- 
def deduct(coord):
    coord -= 6
    if coord < 0:
        return 0
    return coord

def increase(coord):
    coord += 6
    if coord > (450-size):
        return (450-size)
    return coord

# -----------Game Loop ---------------
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isBlue = not isBlue
                playSound('assets/ahem.wav')
            elif event.key == pygame.K_RETURN:
                play_a_different_song()
                #pygame.mixer.music.stop()
        if event.type == SONG_END:
            print "happy days"
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y = deduct(y)
    if pressed[pygame.K_DOWN]: y = increase(y)
    if pressed[pygame.K_LEFT]: x = deduct(x)
    if pressed[pygame.K_RIGHT]: x = increase(x)

    if isBlue:
        color = (0,128,255)
    else:
        color = (255,100,0)

    # up_pressed = pygame.get_pressed()[pygame.K_UP]
   
   # screen.fill((255, 255, 255))
    screen.blit(get_image('assets/Revived_forest.png'), (-50,0))

    #screen = surface    Colour          (x,y,width,height)
    pygame.draw.rect(screen, color, pygame.Rect(x,y,size,size))
    pygame.draw.circle(screen,(120,40,100), (150,150), 50)

    #does the same thing
    #pygame.display.update()
    pygame.display.flip()
    
    #60 FPS
    clock.tick(60)


