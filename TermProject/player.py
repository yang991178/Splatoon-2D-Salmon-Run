import pygame, os, input, weapon, random, math

WHITE = pygame.color.Color(255,255,255)
ROTATE_MAP = {(0,1):0,(-1,1):45,(-1,0):90,(-1,-1):135,(0,-1):180,(1,-1):225,(1,0):270,(1,1):315}

class Player(object):
    def __init__(self, game, controller, weapon):
        self.controller = controller
        self.x, self.y = game.birthPoint
        self.side = 19
        self.color = game.playerColor
        self.dir = (0,-1)
        self.weapon = weapon
        self.state = "kid"
        self.kid = pygame.image.load(os.path.join('assets', 'kid.bmp'))
        self.kid.set_colorkey(WHITE)
        self.kid_back = pygame.image.load(os.path.join('assets', 'kid_back.bmp'))
        self.kid_back.set_colorkey(WHITE)
        self.squid = pygame.image.load(os.path.join('assets', 'squid.bmp'))
        self.squid.set_colorkey(WHITE)
        self.squid_swim = pygame.image.load(os.path.join('assets', 'squid_swim.bmp'))
        self.squid_swim.set_colorkey(WHITE)
        self.ground = "neutral"
        self.moved = False

    def pos(self):
        return int(self.x), int(self.y)

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
        threshold = self.side * math.pi * 0.7
        if count[p] > threshold: return "friendly"
        elif count[e] > threshold: return "hostile"
        else: return "neutral"

    def speed(self, game):
        self.ground = ground = self.checkGround(game)
        if ground == "hostile":
            return 0.5
        elif ground == "friendly":
            return 2.25 if self.state == "squid" else 1
        else:
            return 1

    def blocked(self, game, m):
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

    def draw(self, screen):
        if self.state == "kid":
            kid = self.kid if self.dir[1] != 1 else self.kid_back
            if self.dir[0] == -1: kid = pygame.transform.flip(kid, True, False)
            screen.blit(kid, self.pos())
        else:
            if self.ground == "friendly":
                if self.moved:
                    screen.blit(pygame.transform.rotate(self.squid_swim, ROTATE_MAP.get(self.dir)), self.pos())
            else:
                screen.blit(pygame.transform.rotate(self.squid, ROTATE_MAP.get(self.dir)), self.pos())

    @staticmethod
    def fromControllerList(game, controllers):
        weapons = weapon.WEAPONS.copy()
        random.shuffle(weapons)
        return [Player(game, controller, weapons.pop()) for controller in controllers]