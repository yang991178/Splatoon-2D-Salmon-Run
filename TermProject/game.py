import pygame, scene, os, input, pause
from player import Player
from barrier import Barrier

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
        self.blots = []
        self.barriers = [Barrier((160, 160), (1,0), (0,1), (1,0), 280),
                         Barrier((360, 110), (1,0), (0,1), (-1,9), 130),
                         Barrier((160, 160), (0,1), (-1,0), (0,1), 120),
                         Barrier((160, 270), (1,0), (0,-1), (1,0), 100),
                         Barrier((480, 110), (0,1), (1,0), (0,1), 120),
                         Barrier((480, 230), (0,1), (1,0), (0,-1), 140),
                         Barrier((160, 320), (1,0), (0,-1), (-1,0), 170),
                         Barrier((330, 320), (1,0), (0,-1), (1,0), 100),
                         Barrier((420, 320), (0,1), (-1,0), (0,-1), 50)]

    def hit(self, x, y, dir):
        for barrier in self.barriers:
            if barrier.rect.collidepoint(x, y):
                if not ((barrier.passage[0] == dir[0] and dir[0] != 0) or (barrier.passage[1] == dir[1] and dir[1] != 0)):
                    return True
        return False

    def fireTimer(self, data):
        for blot in self.blots:
            if blot.move(self) == "exploded":
                self.blots.remove(blot)
        for player in self.players:
            actions = player.controller.getAction()
            if "pause" in actions:
                data.scene = pause.Pause(data, self)
            elif "squid" in actions:
                if player.state == "kid":
                    self.submergeSound.play()
                player.state = "squid"
            elif "shoot" in actions and player.state != "squid":
                self.blots += player.weapon.fire(player.center(), player.dir)
            else:
                if player.state == "squid":
                    self.emergeSound.play()
                player.state = "kid"
            player.move(self)

    def updateDisplay(self, screen, data):
        screen.blit(self.map, self.mapRect)
        screen.blit(self.obstacles, self.mapRect)
        for barrier in self.barriers:
            barrier.draw(screen)
        for player in self.players:
            player.draw(screen)
        for player in self.players:
            player.drawOverlay(screen)
        for blot in self.blots:
            blot.draw(screen)