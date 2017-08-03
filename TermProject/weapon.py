import pygame, input

class Weapon(object):
    def __init__(self):
        pass

    def name(self):
        return type(self).__name__

class SplatShot(Weapon):
    pass

class InkBrush(Weapon):
    pass

WEAPONS = [SplatShot(), InkBrush()]