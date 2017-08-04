import pygame, menu, os

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

class GameData(object):
    def __init__(self, width, height):
        self.active = True
        self.width = width
        self.height = height
        self.font = pygame.font.Font(os.path.join('assets', 'font.ttf'),20)
        self.scene = menu.Menu(self)
        

def processEvent(data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.active = False
        else:
            data.scene.processEvent(data, event)

def fireTimer(data):
    data.scene.fireTimer(data)

def updateDisplay(screen, data):
    data.scene.updateDisplay(screen, data)

def run():
    width=640
    height=480
    pygame.init()
    pygame.mixer.init()
    trueScreen = pygame.display.set_mode((1280,960))
    #trueScreen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.Surface((width, height))
    scale = trueScreen.get_height()/screen.get_height()
    scaleRect = pygame.transform.scale(screen, (int(width*scale), int(height*scale))).get_rect()
    scaleRect.center = trueScreen.get_rect().center
    pygame.display.set_caption("Splatoon 2D")
    clock = pygame.time.Clock()
    data = GameData(width, height)
    while data.active:
        processEvent(data)
        fireTimer(data)
        screen.fill((255, 255, 255))
        updateDisplay(screen, data)
        trueScreen.blit(pygame.transform.scale(screen, (int(width*scale), int(height*scale))), scaleRect)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

run()