import pygame, menu, game, scene, os, input

class Preparation(scene.Scene):
    def __init__(self, data):
        super().__init__()
        self.controller = input.Input()
        self.controllers = []
        self.mode = "controller"
        self.joyInstruct = pygame.image.load(os.path.join('assets', 'controller.png'))
        self.keyInstruct = pygame.image.load(os.path.join('assets', 'keyboard.png'))
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()

    def processEvent(self, data, event):
        if event.type == pygame.JOYBUTTONUP:
            if len(self.controllers) < 2 and event.button == 1 and event.joy not in self.controllers:
                self.controllers.append(event.joy)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.mode = "keyboard"
            elif event.key == pygame.K_j:
                self.mode = "controller"
            elif event.key == pygame.K_RETURN:
                if self.mode == "controller" and len(self.controllers) == 2:
                    data.scene = game.Game(data, [input.Input(joystick=pygame.joystick.Joystick(j)) for j in self.controllers])
                elif self.mode == "keyboard":
                    data.scene = game.Game(data, [input.Input(input.KEYBOARD_P1), input.Input(input.KEYBOARD_P2)])

    def fireTimer(self, data):
        action = self.controller.getAction()
        if "A" in action:
            pass
        elif "B" in action:
            data.scene = menu.Menu(data)

    def updateDisplay(self, screen, data):
        if self.mode == "controller":
            screen.blit(self.joyInstruct,(0,0,data.width,data.height))
            controller = data.font.render("Player 1: " + ("Ready!" if len(self.controllers) > 0 else "waiting") + \
               "    Player 2: " + ("Ready!" if len(self.controllers) > 1 else "waiting"),True,(0,0,0))
            controllerRect = controller.get_rect()
            controllerRect.center = (data.width / 2, data.height * 3 / 4)
            screen.blit(controller, controllerRect)
            if len(self.controllers) == 2:
                ready = data.font.render("ENTER: START!", True, (0,0,0))
                readyRect = ready.get_rect()
                readyRect.bottomright = (data.width - 5, data.height - 5)
                screen.blit(ready, readyRect)
        else:
            screen.blit(self.keyInstruct,(0,0,data.width,data.height))