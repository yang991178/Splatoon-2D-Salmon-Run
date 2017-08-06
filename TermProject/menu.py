import pygame, scene, preparation, os, input

class Menu(scene.Scene):
    def __init__(self, data):
        super().__init__()
        self.logo = pygame.image.load(os.path.join('assets', 'logo.png'))
        self.logoRect = self.logo.get_rect()
        self.logoRect.center = (data.width / 2, data.height / 3)
        self.caption = data.font.render("Press Enter to Start !",True,(255,255,255))
        self.captionRect = self.caption.get_rect()
        self.captionRect.center = (data.width / 2, data.height * 2 / 3)
        self.help = data.font.render("Press H for instructions",True,(255,255,255))
        self.helpRect = self.help.get_rect()
        self.helpRect.bottomright = (data.width - 10, data.height - 5)
        self.controller = input.Input()
        self.exitCount = 0

    def fireTimer(self, data):
        action = self.controller.getAction()
        if "A" in action:
            data.scene = preparation.Preparation(data)
        elif "B" in action:
            self.exitCount += 1
            if self.exitCount >= 30:
                data.active = False
        elif "help" in action:
            data.scene = Help()
        else:
            self.exitCount = 0

    def updateDisplay(self, screen, data):
        screen.fill((0,0,0))
        screen.blit(self.logo, self.logoRect)
        screen.blit(self.caption, self.captionRect)
        screen.blit(self.help, self.helpRect)

class Help(scene.Scene):
    def __init__(self):
        super().__init__()
        self.help = pygame.image.load(os.path.join('assets', 'help.jpg'))
        self.y = 0
        self.controller = input.Input()

    def fireTimer(self, data):
        move = self.controller.getMove()[1]*3
        if data.height - self.help.get_height() <= self.y + move <= 0:
            self.y += move
        if "B" in self.controller.getAction():
            data.scene = Menu(data)

    def updateDisplay(self, screen, data):
        screen.blit(self.help, (0, self.y))