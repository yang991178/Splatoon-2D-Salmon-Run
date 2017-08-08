import pygame, os, weapon, math, random

RED = pygame.color.Color("red")

class Enemy(object):
    cost = 1
    score = 10
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
        super().__init__(pos, 22, 90, "chum", 0.75, color)

class SmallFly(Enemy):
    def __init__(self, pos, color):
        super().__init__(pos, 14, 30, "smallfly", 1.5, color)

class Cohock(Enemy):
    cost = 3
    score = 20
    def __init__(self, pos, color):
        super().__init__(pos, 14, 150, "cohock", 0.4, color)

    def rect(self):
        return pygame.Rect(self.pos(), (22, 27))

class TankMan(Enemy):
    score = 80
    def __init__(self, pos, color):
        super().__init__(pos, 30, 320, "tankman", 0.55, color)

    def rect(self):
        return pygame.Rect(self.pos(), (30, 30))

    def move(self, game):
        super().move(game)
        tar = self.track(game)
        if self.attackCounter == 14:
            game.blots.append(weapon.Blot(self.center(),tar[:2],self.size,tar[2],20,self.c,4))

class Maws(Enemy):
    score = 80
    def __init__(self, pos, color):
        super().__init__(pos, 30, 240, "maws", 1.5, color)
        self.state = "swimming"
        self.count = 0

    dirList = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]

    def rect(self):
        if self.state != "attacking":
            return pygame.Rect((-1,-1), (0, 0))
        else:
            return super().rect()

    def move(self, game):
        if self.state == "swimming":
            self.dir = dir = self.track(game)
            if dir[2] <= 15:
                self.state = "preparing"
                self.count = 60
            else:
                self.x += dir[0]*self.speed
                self.y -= dir[1]*self.speed
        elif self.state == "preparing":
            if self.count == 0:
                for dir in self.dirList:
                    game.blots.append(weapon.Blot(self.pos(),dir,30,28,150,self.c,10))
                self.state = "attacking"
                self.count = 90
            else: self.count -= 1
        else:
            if self.count == 0:
               self.state = "swimming"
            else: self.count -= 1

    def draw(self, screen):
        if self.state == "attacking":
            super().draw(screen)
        else:
            pygame.draw.circle(screen, RED, self.center(), 5)
            if self.state == "preparing":
                color = (21,198,148) if self.count % 30 > 15 else (16,124,93)
                pygame.draw.circle(screen, color, self.center(), 30, 2)

class Griller(Enemy):
    score = 100
    def __init__(self, pos, color):
        super().__init__(pos, 40, 200, "griller", 0.9, color)
        self.target = None
        self.spawnCount = 120
        self.rotation = 0
        self.rotateCount = 45
        self.lastHP = self.hp
        self.stuntCount = 0
        self.tentacle = pygame.image.load(os.path.join('assets', 'griller_tentacle.bmp'))
        self.tentacle.set_colorkey((255,255,255))

    def rect(self):
        if self.stuntCount > 60: return super().rect()
        x, y = self.center()
        x += math.cos(math.pi * self.rotation / 180) * 27
        y -= math.sin(math.pi * self.rotation / 180) * 27
        return pygame.Rect((x-8,y-8),(20, 20))

    def track(self, target):
        dir = [0,0]
        x, y = target.pos()
        if self.x < x: dir[0] = 1
        else: dir[0] = -1
        if self.y < y: dir[1] = -1
        else: dir[1] = 1
        return tuple(dir)

    def move(self, game):
        if self.hp != self.lastHP: 
            self.stuntCount += 60
        else: self.stuntCount = max(0, self.stuntCount - 1)
        if self.target == None: self.target = random.choice(game.players)
        while self.target.state == "lifesaver" and not game.isOver(): 
            self.target = random.choice(game.players)
        self.dir = self.track(self.target)
        self.x += self.dir[0]*self.speed
        self.y -= self.dir[1]*self.speed
        if self.spawnCount == 0:
            game.enemies.append(SmallFly(self.center(), self.c))
            self.spawnCount = 120
        else: self.spawnCount -= 1
        if self.rotateCount == 0:
            self.rotation = (self.rotation + 45) % 360
            self.rotateCount = 45
        else: self.rotateCount -= 1
        if self.attackCounter == 0:
            game.blots.append(weapon.Blot(self.center(),self.dir,self.size,3,40,self.c,2))
            self.attackCounter = 15
        self.attackCounter -= 1
        self.lastHP = self.hp

    def draw(self, screen):
        pygame.draw.line(screen, RED, self.center(), self.target.center())
        if self.stuntCount <= 40:
            tentacles = [pygame.transform.rotate(self.tentacle, self.rotation)]
        else:
            tentacles = [pygame.transform.rotate(self.tentacle, r) for r in range(0,360,45)]
        for tentacle in tentacles:
            rect = tentacle.get_rect()
            rect.center = self.center()
            screen.blit(tentacle, rect)
        super().draw(screen)

ENEMIES = [Chum, Chum, Chum, Cohock, SmallFly, SmallFly]
BOSSES = [TankMan, Maws, Griller]