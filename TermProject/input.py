import pygame

pg = pygame

WASD = {pg.K_w:(0,-1),pg.K_a:(-1,0),pg.K_s:(0,1),pg.K_d:(1,0)}
ARROWS = {pg.K_UP:(0,-1),pg.K_LEFT:(-1,0),pg.K_DOWN:(0,1),pg.K_RIGHT:(1,0)}
GENERAL_MAP = {"move":{**WASD,**ARROWS},"action":{pg.K_RETURN:"A",pg.K_ESCAPE:"B",pg.K_h:"help"}}
JOYSTICK_ACTIONS = {0:"sub", 4: "squid", 5: "shoot", 8: "pause", 9: "pause", 10: "special"}
KEYBOARD_P1 = {"move":WASD, "action":{pg.K_SPACE: "shoot", pg.K_LALT: "squid", pg.K_LCTRL: "special", pg.K_LSHIFT: "sub", pg.K_ESCAPE:"pause"}}
KEYBOARD_P2 = {"move":ARROWS, "action":{pg.K_SLASH: "shoot", pg.K_PERIOD: "squid", pg.K_RETURN: "special", pg.K_RSHIFT: "sub", pg.K_ESCAPE:"pause"}}

class Input(object):
    def __init__(self,keymap=GENERAL_MAP,joystick=None):
        if joystick != None: 
            joystick.init()
        self.joystick = joystick
        self.keymap = keymap

    def getMove(self):
        if self.joystick != None:
            return self.joystick.get_hat(0)
        else:
            keys = pygame.key.get_pressed()
            result = [0, 0]
            for key in self.keymap["move"]:
                if keys[key]:
                    result[0] += self.keymap["move"][key][0]
                    result[1] -= self.keymap["move"][key][1]
            return tuple(result)

    def getAction(self):
        result = set()
        if self.joystick != None:
            for key in JOYSTICK_ACTIONS:
                if self.joystick.get_button(key):
                    result.add(JOYSTICK_ACTIONS[key])
        else:
            keys = pygame.key.get_pressed()
            for key in self.keymap["action"]:
                if keys[key]:
                    result.add(self.keymap["action"][key])
        return result