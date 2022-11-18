import pygame as pg


# TODO document
# TODO refactor

class GUIElement:

    def __init__(self, player, disx, disy, image, display, scale:tuple):
        self.player = player
        self.disx = disx
        self.disy = disy
        self.image = image
        self.display = display
        self.scale = scale
    
    def draw(self):
        self.display.blit(pg.transform.scale((self.image), self.scale), (self.disx, self.disy))

class GUIHealthBar(GUIElement):

    def draw(self):
        super().draw()


