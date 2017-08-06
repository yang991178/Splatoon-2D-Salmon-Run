import pygame, scene, os, input, pause, random
from player import Player
from barrier import Barrier
from enemy import *

WHITE = pygame.color.Color(255,255,255)

class Game(scene.Scene):
    def __init__(self, data, controllers):
        self.map = pygame.image.load(os.path.join('assets', 'map.bmp'))
        self.obstacles = pygame.image.load(os.path.join('assets', 'layer.bmp'))
        self.obstacles.set_colorkey(WHITE)
        self.mapRect = self.map.get_rect()
        self.birthPoint = (data.width//2,data.height//2)
        self.playerColor = pygame.color.Color(255,127,39)
        self.enemyColor = pygame.color.Color(16,124,93)
        self.players = Player.fromControllerList(self, controllers)
        self.submergeSound = pygame.mixer.Sound(os.path.join('audio', 'submerge_sound.wav'))
        self.emergeSound = pygame.mixer.Sound(os.path.join('audio', 'emerge_sound.wav'))
        self.blots = []
        self.house = pygame.Rect((170,170),(310,150))
        self.barriers = [Barrier((170, 160), (1,0), (0,1), (1,0), 280),
                         Barrier((360, 110), (1,0), (0,1), (-1,0), 120),
                         Barrier((160, 160), (0,1), (-1,0), (0,-1), 120),
                         Barrier((160, 270), (1,0), (0,-1), (1,0), 100),
                         Barrier((480, 110), (0,1), (1,0), (0,1), 120),
                         Barrier((480, 230), (0,1), (1,0), (0,-1), 140),
                         Barrier((160, 320), (1,0), (0,-1), (-1,0), 170),
                         Barrier((330, 320), (1,0), (0,-1), (1,0), 90),
                         Barrier((420, 320), (0,1), (-1,0), (0,-1), 50)]
        self.entrances = [(440,175),(165,250),(440,310)]
        self.enemySpawnPoints = [(0,0), (320,0), (620,0),(0,230),(620,230),(0,450), (320,450), (620,450)]
        self.enemySpawn = {"time":150, "count":5}
        self.enemies = []
        self.wave = 1
        self.captionCount = 150
        self.bossCount = 1

    def hit(self, x, y, dir, damage, color):
        if color == self.playerColor:
            for enemy in self.enemies:
                if enemy.rect().collidepoint(x, y):
                    enemy.hp -= damage
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)
                    return True
            for player in self.players:
                if player.state == "lifesaver" and player.rect().collidepoint(x, y):
                    player.state = "kid"
                    return True
        else:
            for player in self.players:
                if player.rect().collidepoint(x, y):
                    player.hp -= damage
                    player.recoverCount = 90
                    if player.hp <= 0:
                        player.state = "lifesaver"
                    return True
        for barrier in self.barriers:
            if barrier.rect.collidepoint(x, y):
                if not ((barrier.passage[0] == dir[0] and dir[0] != 0) or (barrier.passage[1] == dir[1] and dir[1] != 0)):
                    return True
        return False

    def isOnHouse(self, pos):
        return self.house.collidepoint(pos)
    def isOffHouse(self, pos):
        return not self.isOnHouse(pos)

    def fireTimer(self, data):
        for blot in self.blots:
            if blot.move(self) == "exploded":
                self.blots.remove(blot)
        for player in self.players:
            actions = player.controller.getAction()
            if "pause" in actions:
                data.scene = pause.Pause(data, self)
            elif player.state == "lifesaver":
                pass
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
        if self.enemySpawn["time"] == 0:
            species = random.choice(ENEMIES)
            self.enemies.append(species(random.choice([(random.randint(0, 630),random.choice([0,450])),(random.choice([0,630]),random.randint(0,450))]),self.enemyColor))
            self.enemySpawn["count"] -= species.cost
            self.enemySpawn["time"] = 40
            if self.enemySpawn["count"] <= 0:
                self.bossCount += 1
                if self.bossCount % 3 == 0:
                    self.enemies.append(random.choice(BOSSES)(random.choice([(random.randint(0, 630),random.choice([0,450])),(random.choice([0,630]),random.randint(0,450))]),self.enemyColor))
                    self.enemySpawn = {"time":400, "count":5}
                else:
                    self.enemySpawn = {"time":200, "count":5}
        else:
            self.enemySpawn["time"] -= 1
        for enemy in self.enemies:
            enemy.move(self)

    def updateDisplay(self, screen, data):
        screen.blit(self.map, self.mapRect)
        screen.blit(self.obstacles, self.mapRect)
        for barrier in self.barriers:
            barrier.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for player in self.players:
            player.draw(screen)
        for player in self.players:
            player.drawOverlay(screen)
        for blot in self.blots:
            blot.draw(screen)

        if self.captionCount > 0:
            l1 = data.font.render("Wave %d starts in %d" % (self.wave, self.captionCount // 30), True, WHITE)
            l1Rect = l1.get_rect()
            l1Rect.bottomright = data.width - 10, data.height
            l2 = data.font.render("1P: %s, 2P: %s" % (self.players[0].weapon.name(), self.players[1].weapon.name()), True, WHITE)
            l2Rect = l2.get_rect()
            l2Rect.bottomleft = 10, data.height
            screen.blit(l1, l1Rect)
            screen.blit(l2, l2Rect)
            self.captionCount -= 1