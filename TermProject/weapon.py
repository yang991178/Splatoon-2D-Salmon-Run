import pygame, input, random, os

class Blot(object):
    def __init__(self, pos, dir, r, distance, damage, color, speed):
        self.x = pos[0]
        self.y = pos[1]
        self.r = r
        self.dir = dir
        self.t = distance
        self.d = damage
        self.c = color
        self.s = speed

    def move(self, game):
        self.x += self.dir[0] * self.s
        self.y -= self.dir[1] * self.s
        self.t -= (self.dir[0]**2 + self.dir[1]**2)**0.5 * self.s
        if self.t <= 0 or game.hit(self.x, self.y, self.dir):
            return self.explode(game)

    def explode(self, game, r=(0,0,0,0)):
        pointList = []
        for p in range(self.r*3):
            x = random.randint(self.x-self.r-r[0],self.x+self.r-r[1])
            y = random.randint(self.y-self.r-r[2],self.y+self.r-r[3])
            pointList.append((x, y))
        pygame.draw.polygon(game.map, self.c, pointList)
        return "exploded"

    def draw(self, screen):
        pygame.draw.circle(screen, self.c, (self.x, self.y), 4)
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), 4, 1)

class Weapon(object):
    def __init__(self, color, range, blotRadius, damage, speed, cost):
        self.c = color
        self.r = range
        self.br = blotRadius
        self.d = damage
        self.s = speed
        self.cost = cost
        self.cooldown = 0
        self.ink = 100
        self.drain = pygame.mixer.Sound(os.path.join('audio', 'no_ink_sound.wav'))

    def cool(self):
        self.cooldown = max(0, self.cooldown - 1)

    def fire(self, pos, dir):
        pass

    def name(self):
        return type(self).__name__

class SplatShot(Weapon):
    def __init__(self, color):
        super().__init__(color, 90, 18, 35, 6, 4)
        self.sound = pygame.mixer.Sound(os.path.join('audio', 'shot_short.wav'))
        self.aim = pygame.image.load(os.path.join('assets', 'shot_aim.bmp'))
        self.aim.set_colorkey((255, 255, 255))
    
    def fire(self, pos, dir):
        if self.cooldown == 0:
            if self.ink == 0:
                self.drain.play()
                self.cooldown = 30
                return []
            else:
                self.cooldown = 10
                self.ink = max(0, self.ink - self.cost)
                self.sound.play()
                return [Blot(pos, dir, self.br, self.r, self.d, self.c, self.s),
                       Blot(pos, dir, self.br, random.randint(1,self.r), 0, self.c, self.s)]
        else: return []

class InkBrush(Weapon):
    pass

WEAPONS = [SplatShot, SplatShot]