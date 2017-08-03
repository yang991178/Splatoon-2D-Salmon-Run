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
        self.controller = input.Input()

    def fireTimer(self, data):
        action = self.controller.getAction()
        if "A" in action:
            data.scene = preparation.Preparation(data)
        elif "B" in action:
            pass

    def updateDisplay(self, screen, data):
        screen.fill((0,0,0))
        screen.blit(self.logo, self.logoRect)
        screen.blit(self.caption, self.captionRect)