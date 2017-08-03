import pygame, scene, menu, input

WHITE = (255,255,255)

class Pause(scene.Scene):
    def __init__(self, data, game):
        self.game = game
        self.controller = input.Input()
        self.exitCount = 0
        self.overlay = pygame.Surface((data.width, data.height))
        self.overlay.set_alpha(150)

        self.paused = data.font.render("GAME PAUSED",True,WHITE)
        self.pausedRect = self.paused.get_rect()
        self.pausedRect.center = data.width // 2, data.height // 3

        self.prompt = data.font.render("Press ENTER to Continue or Hold ESC to Exit",True,WHITE)
        self.promptRect = self.prompt.get_rect()
        self.promptRect.center = data.width // 2, data.height // 2

    def fireTimer(self, data):
        actions = self.controller.getAction()
        if "A" in actions:
            data.scene = self.game
        elif "B" in actions:
            self.exitCount += 1
            if self.exitCount >= 60:
                data.scene = menu.Menu(data)
        else:
            self.exitCount = 0

    def updateDisplay(self, screen, data):
        self.game.updateDisplay(screen, data)
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.paused, self.pausedRect)
        screen.blit(self.prompt, self.promptRect)