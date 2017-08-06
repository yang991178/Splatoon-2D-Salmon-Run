import pygame, os, input, weapon, random, math

WHITE = pygame.color.Color(255,255,255)
BLACK = pygame.color.Color(0,0,0)
ROTATE_MAP = {(0,1):90,(-1,1):135,(-1,0):180,(-1,-1):225,(0,-1):270,(1,-1):315,(1,0):0,(1,1):45}

class Player(object):
    def __init__(self, game, controller, weapon):
        self.controller = controller
        self.x, self.y = game.birthPoint
        self.side = 19
        self.color = game.playerColor
        self.dir = (0,-1)
        self.weapon = weapon
        self.state = "kid"
        self.hp = 100
        self.recoverCount = 0
        self.kid = pygame.image.load(os.path.join('assets', 'kid.bmp'))
        self.kid.set_colorkey(WHITE)
        self.kid_back = pygame.image.load(os.path.join('assets', 'kid_back.bmp'))
        self.kid_back.set_colorkey(WHITE)
        self.squid = pygame.image.load(os.path.join('assets', 'squid.bmp'))
        self.squid.set_colorkey(WHITE)
        self.squid_swim = pygame.image.load(os.path.join('assets', 'squid_swim.bmp'))
        self.squid_swim.set_colorkey(WHITE)
        self.lifesaver = pygame.image.load(os.path.join('assets', 'lifesaver.bmp'))
        self.lifesaver.set_colorkey(BLACK)
        self.ground = "neutral"
        self.moved = False
        self.swimSound = pygame.mixer.Sound(os.path.join('audio', 'swim_sound.wav'))
        self.swimChannel = pygame.mixer.find_channel()
        self.swimChannel.play(self.swimSound, -1)
        self.swimChannel.pause()
        self.inkTank = pygame.image.load(os.path.join('assets', 'ink_tank.bmp'))
        self.inkTank.set_colorkey(WHITE)
        self.bgTank = pygame.Surface((10, 20))
        self.bgTank.set_alpha(150)

    def pos(self):
        return int(self.x), int(self.y)

    def center(self):
        return int(self.x+self.side/2), int(self.y+self.side/2)

    def rect(self):
        return pygame.Rect(int(self.x),int(self.y),self.side,self.side)

    def checkGround(self, game):
        ground = game.map.subsurface(self.rect())
        p = game.playerColor.normalize()
        e = game.enemyColor.normalize()
        count = {p:0, e:0}
        for x in range(ground.get_width()):
            for y in range(ground.get_height()):
                c = ground.get_at((x,y)).normalize()
                if c in count: count[c] += 1
        threshold = (self.side/2)**2 * math.pi * 0.7
        if count[p] > threshold: return "friendly"
        elif count[e] > threshold: return "hostile"
        else: return "neutral"

    def speed(self, game):
        if self.state == "lifesaver": return 1.5
        self.ground = ground = self.checkGround(game)
        if ground == "hostile":
            return 0.5
        elif ground == "friendly":
            return 2.25 if self.state == "squid" else 1
        else:
            return 1

    def blocked(self, game, m):
        x, y = self.pos()
        to = pygame.Rect((x,y+self.side-10),(self.side,self.side-10))
        to.move(m)
        for barrier in game.barriers:
            if barrier.rect.colliderect(to):
                if m[0] != 0 and m[0] == -barrier.passage[0]:
                    return True
                elif m[1] != 0 and m[1] == -barrier.passage[1]:
                    return True
        to = self.rect()
        to.move(m)
        if m[0] != 0:
            x = to.right if m[0] == 1 else to.left
            for y in range(to.top, to.bottom + 1):
                if game.obstacles.get_at((x,y)) != WHITE:
                    return True
        if m[1] != 0:
            y = to.top if m[1] == 1 else to.bottom
            for x in range(to.left, to.right + 1):
                if game.obstacles.get_at((x,y)) != WHITE:
                    return True
        return False

    def move(self, game):
        self.weapon.cool()
        m = self.controller.getMove()
        if m == (0,0): 
            self.moved = False
        else:
            self.dir = m
            s = self.speed(game)
            if 0 not in m: s *= 0.65
            if not self.blocked(game, (m[0],0)):
                self.x += m[0] * s
            if not self.blocked(game, (0,m[1])):
                self.y -= m[1] * s
            self.moved = True
        if self.state == "squid" and self.ground == "friendly":
            self.weapon.ink = min(100, self.weapon.ink + 1)
        self.recoverCount = max(0, self.recoverCount - 1)
        if self.recoverCount == 0: self.hp = 100

    def draw(self, screen):
        if self.state == "lifesaver":
            screen.blit(self.lifesaver, self.pos())
        elif self.state == "kid":
            kid = self.kid if self.dir[1] != 1 else self.kid_back
            if self.dir[0] == -1: kid = pygame.transform.flip(kid, True, False)
            x, y = self.pos()
            screen.blit(kid, (x, y-10))
        else:
            if self.ground == "friendly":
                if self.moved:
                    screen.blit(pygame.transform.rotate(self.squid_swim, ROTATE_MAP.get(self.dir)-90), self.pos())
                    self.swimChannel.unpause()
                    return
            else:
                screen.blit(pygame.transform.rotate(self.squid, ROTATE_MAP.get(self.dir)-90), self.pos())
        self.swimChannel.pause()

    def drawOverlay(self, screen):
        angle = math.pi * ROTATE_MAP[self.dir] / 180
        x, y = self.center()
        screen.blit(self.weapon.aim, (round(x+self.weapon.r*math.cos(angle)), round(y-self.weapon.r*math.sin(angle))))
        if self.state == "squid":
            screen.blit(self.inkTank, (x, y-34))
            inkRect = pygame.Rect((0, 0), (10, self.weapon.ink // 5))
            inkRect.bottomleft = (x+16, y-11)
            screen.blit(self.bgTank, (x+16, y-31))
            pygame.draw.rect(screen, self.color, inkRect)

    @staticmethod
    def fromControllerList(game, controllers):
        weapons = weapon.WEAPONS.copy()
        random.shuffle(weapons)
        return [Player(game, controller, weapons.pop()(game.playerColor)) for controller in controllers]