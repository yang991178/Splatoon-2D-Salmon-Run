import pygame, menu, os

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
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Splatoon 2D")
    clock = pygame.time.Clock()
    data = GameData(width, height)
    while data.active:
        processEvent(data)
        fireTimer(data)
        screen.fill((255, 255, 255))
        updateDisplay(screen, data)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

run()