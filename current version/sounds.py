import pygame

class Sounds():
    def __init__(self):
        self.sound_lib = {}

    def addSound(self,path):
        if (self.sound_lib.get(path) is None): # new sound
            sound = pygame.mixer.Sound(path)
            self.sound_lib[path] = sound

    def playSound(self,path):
        sound = self.sound_lib.get(path)
        if sound is None:
            # needs to be added!
            # may be dangerous if path doesn't exist...should throw error
            self.addSong(path)
            self.playSoundEffect(path)
        else:
            sound.play()
