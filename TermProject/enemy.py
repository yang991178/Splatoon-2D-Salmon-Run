import pygame, os, weapon

class Enemy(object):
    cost = 1
    def __init__(self, pos, size, hp, image, speed, color):
        self.x, self.y = pos
        self.last = pos
        self.lastCount = 0
        self.size = size
        self.hp = hp
        self.speed = speed
        self.image = pygame.image.load(os.path.join('assets', image + '.bmp'))
        self.image.set_colorkey((255,255,255))
        self.dir = (0,-1)
        self.c = color
        self.attackCounter = 15

    def pos(self):
        return int(self.x), int(self.y)

    def center(self):
        return int(self.x + self.size / 2), int(self.y + self.size / 2)

    def rect(self):
        return pygame.Rect(self.pos(), (self.size, self.size))

    def track(self, game, findEntrance=False):
        dis = lambda p1, p2: ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5
        target = min(game.players, key=lambda p:dis(self.pos(), p.pos())+int(p.state=="lifesaver")*1000)
        dir = [0,0,dis(self.pos(),target.pos())]
        x, y = target.pos()
        if findEntrance and game.isOnHouse((x, y)) and game.isOffHouse(self.pos()):
            x, y = min(game.entrances, key=lambda p:dis(self.pos(), p))
        if self.x < x: dir[0] = 1
        else: dir[0] = -1
        if self.y < y: dir[1] = -1
        else: dir[1] = 1
        
        return tuple(dir)

    def avoidBarrier(self, game, m):
        to = self.rect()
        to.move(m)
        for barrier in game.barriers:
            if barrier.rect.colliderect(to) and (self.x, self.y) != self.last:
                if m[0] != 0:
                    if m[0] == -barrier.passage[0]:
                        self.dir = barrier.move
                        return barrier.move

                elif m[1] != 0:
                    if m[1] == -barrier.passage[1]:
                        self.dir = barrier.move
                        return barrier.move

        return m

    def move(self, game):
        self.lastCount += self.speed
        self.dir = self.track(game, True)[:2]
        self.avoidBarrier(game, (self.dir[0], 0))
        self.avoidBarrier(game, (0, self.dir[1]))
        self.last = self.x, self.y
        if self.lastCount >= 1: self.lastCount = 0
        self.x += self.dir[0]*self.speed
        self.y -= self.dir[1]*self.speed
        if self.attackCounter == 0:
            game.blots.append(weapon.Blot(self.center(),self.dir,self.size,3,20,self.c,2))
            self.attackCounter = 15
        self.attackCounter -= 1

    def draw(self, screen):
        screen.blit(self.image, self.pos())

class Chum(Enemy):
    def __init__(self, pos, color):
        super().__init__(pos, 22, 60, "chum", 0.75, color)

class SmallFly(Enemy):
    def __init__(self, pos, color):
        super().__init__(pos, 14, 30, "smallfly", 1.5, color)

class Cohock(Enemy):
    cost = 3
    def __init__(self, pos, color):
        super().__init__(pos, 14, 120, "cohock", 0.4, color)

    def rect(self):
        return pygame.Rect(self.pos(), (22, 27))

class TankMan(Enemy):
    def __init__(self, pos, color):
        super().__init__(pos, 30, 320, "tankman", 0.55, color)

    def rect(self):
        return pygame.Rect(self.pos(), (30, 30))

    def move(self, game):
        super().move(game)
        tar = self.track(game)
        if self.attackCounter == 14:
            game.blots.append(weapon.Blot(self.center(),tar[:2],self.size,tar[2],20,self.c,4))

ENEMIES = [Chum, Chum, Chum, Cohock, SmallFly, SmallFly]
BOSSES = [TankMan]