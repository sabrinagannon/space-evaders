import pygame

chime = "assets/music/chime.wav"
bloop = "assets/music/bloop.wav"

soundFx = [chime,bloop]

class SoundFX():

    def __init__(self):
        self.sound_lib = {}
        self.cooldown = 0
        for path in soundFx:
            sound = pygame.mixer.Sound(path)
            self.sound_lib[path] = sound

    def coolDown(self):
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0

    def playBloop(self):
        if not self.cooldown:
            sound = self.sound_lib.get(bloop)
            sound.play()
            self.cooldown = 10

    def playChime(self):
        if not self.cooldown:
            sound = self.sound_lib.get(chime)
            sound.play()
            self.cooldown = 10
