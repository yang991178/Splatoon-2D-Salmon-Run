import pygame, scene, os, input, pause
from player import Player

class Game(scene.Scene):
    def __init__(self, data, controllers):
        self.map = pygame.image.load(os.path.join('assets', 'map.bmp'))
        self.obstacles = pygame.image.load(os.path.join('assets', 'layer.bmp'))
        self.obstacles.set_colorkey((255,255,255))
        self.mapRect = self.map.get_rect()
        self.birthPoint = (data.width//2,data.height//2)
        self.playerColor = pygame.color.Color(255,127,39)
        self.enemyColor = pygame.color.Color(16,124,93)
        self.players = Player.fromControllerList(self, controllers)
        self.submergeSound = pygame.mixer.Sound(os.path.join('audio', 'submerge_sound.wav'))
        self.emergeSound = pygame.mixer.Sound(os.path.join('audio', 'emerge_sound.wav'))

        #self.map.fill(self.playerColor)

    def fireTimer(self, data):
        for player in self.players:
            actions = player.controller.getAction()
            if "pause" in actions:
                data.scene = pause.Pause(data, self)
            elif "squid" in actions:
                if player.state == "kid":
                    self.submergeSound.play()
                player.state = "squid"
            else:
                if player.state == "squid":
                    self.emergeSound.play()
                player.state = "kid"
            player.move(self)

    def updateDisplay(self, screen, data):
        screen.blit(self.map, self.mapRect)
        screen.blit(self.obstacles, self.mapRect)
        for player in self.players:
            player.draw(screen)