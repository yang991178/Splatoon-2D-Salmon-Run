import pygame

class Barrier(object):
    def __init__(self, pos, dir, passage, move, length):
        self.x, self.y = pos
        self.dir = dir
        self.passage = passage
        self.move = move
        self.l = length
        self.rect = pygame.Rect(pos, (10 if dir[0] == 0 else length, 10 if dir[1] == 0 else length))

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)